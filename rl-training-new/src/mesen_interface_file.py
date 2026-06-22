"""Mesen Interface: file-based IPC (no socket dependency).

Companion to ``lua/mesen_bridge_file.lua``. The protocol is:

* Python writes a command as ``<seq> <COMMAND ...>`` to ``mesen_cmd.txt.new``
  and atomically renames it to ``mesen_cmd.txt``.
* The Lua bridge consumes the file at the end of each emulated frame,
  executes the command, and writes ``<seq> <response>`` to
  ``mesen_response.txt.new`` (renamed atomically to ``mesen_response.txt``).
* Python polls for a response file whose sequence id matches its outstanding
  request, then deletes it.

Why atomic rename: ``os.rename`` is atomic on POSIX (and on Windows when the
target does not exist), so the reader never sees a half-written file. The
sequence id protects against the reader seeing a stale response from a
previous command if the rename happens to be slow on a particular FS.

Usage:

    from mesen_interface_file import MesenInterface
    iface = MesenInterface(work_dir=Path("../mesen2/bin/linux-x64/Release"))
    if iface.connect():
        state = iface.get_game_state()
        iface.write_memory(0x00F6, [0x01])  # press RIGHT
        iface.disconnect()
"""

from __future__ import annotations

import itertools
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


_CMD_NAME = "mesen_cmd.txt"
_CMD_TMP = "mesen_cmd.txt.new"
_RESPONSE_NAME = "mesen_response.txt"
_RESPONSE_TMP = "mesen_response.txt.new"
_READY_NAME = "mesen_ready.txt"


class MesenInterface:
    """Interface to Mesen emulator via file-based IPC."""

    def __init__(self, work_dir: Optional[Path] = None, poll_interval: float = 0.001):
        """
        Args:
            work_dir: Directory for IPC files. Must match the directory
                Mesen is launched from (because the Lua bridge writes to
                paths relative to that CWD). Defaults to the current
                working directory.
            poll_interval: Seconds to sleep between polls when waiting
                for a response. 1 ms is plenty for sub-frame latency.
        """
        self.work_dir = Path(work_dir) if work_dir is not None else Path.cwd()
        self.cmd_file = self.work_dir / _CMD_NAME
        self.cmd_tmp = self.work_dir / _CMD_TMP
        self.response_file = self.work_dir / _RESPONSE_NAME
        self.response_tmp = self.work_dir / _RESPONSE_TMP
        self.ready_file = self.work_dir / _READY_NAME
        self.poll_interval = poll_interval
        self.connected = False
        # Sequence id generator. Starts at 1 because "0" might be a stale
        # response on disk from another process.
        self._seq = itertools.count(1)

    # ------------------------------------------------------------------ helpers

    def _clear_stale_files(self) -> None:
        """Remove any leftover IPC files from prior runs."""
        for path in (self.cmd_file, self.cmd_tmp, self.response_file, self.response_tmp):
            try:
                path.unlink()
            except FileNotFoundError:
                pass

    def _atomic_write_command(self, seq: int, command: str) -> None:
        """Write the command via temp + rename so the reader never sees a partial file."""
        payload = f"{seq} {command}"
        # Use binary write so we don't get unexpected newlines from Windows linebreaks.
        with open(self.cmd_tmp, "wb") as f:
            f.write(payload.encode("utf-8"))
            f.flush()
            os.fsync(f.fileno())
        os.replace(self.cmd_tmp, self.cmd_file)

    def _read_response(self, expected_seq: int) -> str:
        """Read and consume the response file if its sequence id matches."""
        try:
            with open(self.response_file, "rb") as f:
                raw = f.read().decode("utf-8", errors="replace").strip()
        except FileNotFoundError:
            return ""

        # Response format: "<seq> <payload>" (payload may contain spaces).
        parts = raw.split(" ", 1)
        if not parts or not parts[0].isdigit():
            # Malformed; leave the file alone so we don't lose data we can't parse.
            return ""

        seq = int(parts[0])
        if seq != expected_seq:
            # Stale response from a previous command. Consume it and keep waiting.
            try:
                self.response_file.unlink()
            except FileNotFoundError:
                pass
            return ""

        payload = parts[1] if len(parts) > 1 else ""
        try:
            self.response_file.unlink()
        except FileNotFoundError:
            pass
        return payload

    # ----------------------------------------------------------------- protocol

    def connect(self, timeout: float = 10.0) -> bool:
        """Wait for the Lua bridge to come online and respond to PING."""
        # Clear stale files BEFORE we look for the ready flag — otherwise we
        # might consume a stale response on the very first command.
        self._clear_stale_files()

        deadline = time.time() + timeout
        print(f"Waiting for Mesen bridge ready file at {self.ready_file} ...")

        while time.time() < deadline:
            if self.ready_file.exists():
                # The bridge is loaded. Probe with PING to be sure it's responsive.
                self.connected = True  # required so _send_command does not refuse
                try:
                    if self._send_command("PING", timeout=2.0) == "PONG":
                        print(f"Connected to Mesen bridge (file-based IPC) at {self.work_dir}")
                        return True
                except Exception as exc:
                    print(f"PING failed: {exc}")
                self.connected = False

            time.sleep(0.1)

        print(f"Failed to connect to Mesen bridge after {timeout}s")
        return False

    def disconnect(self) -> None:
        """Mark disconnected and clear any half-written command files.

        We deliberately do NOT delete the ready file here — the bridge is
        still running inside Mesen, and removing the file would confuse a
        second client that tries to connect.
        """
        self.connected = False
        for path in (self.cmd_file, self.cmd_tmp, self.response_file, self.response_tmp):
            try:
                path.unlink()
            except FileNotFoundError:
                pass

    def _send_command(self, command: str, timeout: float = 5.0) -> str:
        """Send a single command and return the payload (without the 'OK ' prefix)."""
        if not self.connected:
            raise ConnectionError("Not connected to Mesen")

        seq = next(self._seq)
        self._atomic_write_command(seq, command)

        deadline = time.time() + timeout
        while time.time() < deadline:
            response = self._read_response(seq)
            if response:
                if response.startswith("ERROR"):
                    raise RuntimeError(f"Mesen bridge error: {response}")
                if response == "OK":
                    return ""
                if response.startswith("OK "):
                    return response[3:]
                # Bare PONG / arbitrary payload.
                return response
            time.sleep(self.poll_interval)

        raise TimeoutError(f"Command timed out after {timeout}s: {command}")

    # --------------------------------------------------------------- public API

    def read_memory(self, address: int, size: int) -> List[int]:
        """Read ``size`` bytes from NES CPU memory starting at ``address``."""
        response = self._send_command(f"READ {address:04X} {size}")
        return [int(response[i : i + 2], 16) for i in range(0, len(response), 2)]

    def write_memory(self, address: int, data: List[int]) -> None:
        """Write ``data`` bytes to NES CPU memory starting at ``address``."""
        hex_data = "".join(f"{b & 0xFF:02X}" for b in data)
        self._send_command(f"WRITE {address:04X} {hex_data}")

    def step_frame(self, frames: int = 1) -> None:
        """Advance the emulator by ``frames`` frames (cooperative, see Lua)."""
        self._send_command(f"STEP {frames}")

    def get_game_state(self) -> Dict[str, Any]:
        """Return the consolidated Dr. Mario P2 state dictionary."""
        response = self._send_command("GET_STATE")
        parts = response.split(":")
        if len(parts) != 7:
            raise ValueError(f"Invalid GET_STATE response: {response!r}")

        mode, virus_count, capsule_x, capsule_y, left_color, right_color, playfield_hex = parts
        playfield = [int(playfield_hex[i : i + 2], 16) for i in range(0, len(playfield_hex), 2)]

        return {
            "mode": int(mode),
            # game_mode is the historical key used by some downstream code.
            "game_mode": int(mode),
            "virus_count": int(virus_count),
            "capsule_x": int(capsule_x),
            "capsule_y": int(capsule_y),
            "left_color": int(left_color),
            "right_color": int(right_color),
            "playfield": playfield,
        }

    # ---------------------------------------------------------- context manager

    def __enter__(self) -> "MesenInterface":
        if not self.connected:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()


if __name__ == "__main__":
    print("Testing Mesen file-based interface...")

    mesen = MesenInterface()

    if not mesen.connect(timeout=5):
        print("Failed to connect")
        raise SystemExit(1)

    virus_count_bytes = mesen.read_memory(0x03A4, 1)
    print(f"P2 virus count: {virus_count_bytes[0]}")

    state = mesen.get_game_state()
    print(f"Game state: {state}")

    mesen.disconnect()
    print("Test complete")
