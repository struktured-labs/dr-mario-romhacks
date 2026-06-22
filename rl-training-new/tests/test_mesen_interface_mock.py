"""Mock-bridge smoke test for :mod:`mesen_interface_file`.

This file deliberately runs WITHOUT a real Mesen instance. It spins up a
tiny Python "fake bridge" thread that mimics the Lua side of the
file-based IPC protocol: it watches for ``mesen_cmd.txt`` in the test
work directory, parses ``<seq> <COMMAND>``, and writes back
``<seq> <response>`` to ``mesen_response.txt`` using the same atomic
rename pattern.

The goal is to verify that :class:`MesenInterface` correctly:

* honours the sequence id in responses (no stale-response confusion);
* parses READ/WRITE/STEP/GET_STATE/PING payloads;
* surfaces ERROR responses as ``RuntimeError``;
* times out cleanly when the bridge never answers.

If this file ever fails, the Python interface is broken before we even
launch Mesen — which is the whole point.
"""

from __future__ import annotations

import os
import sys
import threading
import time
from pathlib import Path
from typing import Callable, Optional

import pytest

# Allow `from mesen_interface_file import ...` even when pytest is launched
# from the repo root rather than rl-training-new/.
_SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(_SRC))

from mesen_interface_file import MesenInterface  # noqa: E402


# ---------------------------------------------------------- fake bridge helper


class FakeBridge:
    """Lua-side stand-in that exposes the same file protocol."""

    def __init__(self, work_dir: Path, responder: Callable[[str], str]):
        self.work_dir = work_dir
        self.cmd_file = work_dir / "mesen_cmd.txt"
        self.response_file = work_dir / "mesen_response.txt"
        self.response_tmp = work_dir / "mesen_response.txt.new"
        self.ready_file = work_dir / "mesen_ready.txt"
        self.responder = responder
        self.commands_seen: list[str] = []
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        # Write the ready flag synchronously so the test does not race
        # on connect().
        self.ready_file.write_text("READY\n")
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                raw = self.cmd_file.read_text().strip()
            except FileNotFoundError:
                time.sleep(0.001)
                continue

            # Consume the command file immediately to mirror the Lua side.
            try:
                self.cmd_file.unlink()
            except FileNotFoundError:
                pass

            self.commands_seen.append(raw)

            parts = raw.split(" ", 1)
            if len(parts) < 2 or not parts[0].isdigit():
                continue
            seq, command = parts[0], parts[1]
            response_payload = self.responder(command)
            full = f"{seq} {response_payload}"

            with open(self.response_tmp, "wb") as f:
                f.write(full.encode("utf-8"))
                f.flush()
                os.fsync(f.fileno())
            os.replace(self.response_tmp, self.response_file)


# --------------------------------------------------------------------- fixtures


@pytest.fixture
def bridge_factory(tmp_path):
    """Yield a function that boots a FakeBridge with a custom responder."""

    bridges: list[FakeBridge] = []

    def _factory(responder: Callable[[str], str]) -> tuple[FakeBridge, MesenInterface]:
        bridge = FakeBridge(tmp_path, responder)
        bridge.start()
        bridges.append(bridge)
        iface = MesenInterface(work_dir=tmp_path, poll_interval=0.001)
        assert iface.connect(timeout=2.0), "connect() failed against fake bridge"
        return bridge, iface

    yield _factory

    for bridge in bridges:
        bridge.stop()


# ----------------------------------------------------------------- responders


def _ping_only(command: str) -> str:
    if command == "PING":
        return "PONG"
    return "ERROR unhandled"


def _dr_mario_responder(command: str) -> str:
    """Pretend to be a Dr. Mario game in mid-play, level 5."""
    if command == "PING":
        return "PONG"
    if command.startswith("READ "):
        _, addr_hex, size_str = command.split()
        size = int(size_str)
        addr = int(addr_hex, 16)
        if addr == 0x03A4 and size == 1:
            # Virus count = 18
            return "OK 12"
        if addr == 0x0385 and size == 1:
            # Capsule X = 3
            return "OK 03"
        # Default: zeros
        return "OK " + "00" * size
    if command.startswith("WRITE "):
        return "OK"
    if command.startswith("STEP"):
        return "OK"
    if command == "GET_STATE":
        # mode=4 (gameplay), virus=18, x=3, y=1, left=1 (red), right=2 (blue)
        # Playfield: mostly 0xFF (empty); first two bytes are viruses.
        playfield_bytes = [0xD0, 0xD1] + [0xFF] * 126
        playfield_hex = "".join(f"{b:02X}" for b in playfield_bytes)
        return f"OK 4:18:3:1:1:2:{playfield_hex}"
    return "ERROR unknown command"


# ------------------------------------------------------------------------ tests


def test_connect_and_ping(bridge_factory):
    bridge, iface = bridge_factory(_ping_only)
    try:
        assert iface.connected is True
        # The connect() call itself issues a PING; the bridge should have seen it.
        assert any(cmd.endswith("PING") for cmd in bridge.commands_seen)
    finally:
        iface.disconnect()


def test_read_memory_parses_hex(bridge_factory):
    bridge, iface = bridge_factory(_dr_mario_responder)
    try:
        # Virus count byte
        result = iface.read_memory(0x03A4, 1)
        assert result == [0x12]

        # Capsule X
        assert iface.read_memory(0x0385, 1) == [0x03]

        # Multi-byte read returns the full list
        result = iface.read_memory(0x0000, 4)
        assert result == [0, 0, 0, 0]
    finally:
        iface.disconnect()


def test_write_memory_serialises_hex(bridge_factory):
    bridge, iface = bridge_factory(_dr_mario_responder)
    try:
        iface.write_memory(0x00F6, [0x01])
        iface.write_memory(0x00F6, [0x02, 0xFF])

        # Check the bridge actually received uppercase 4-char address + uppercase hex bytes.
        writes = [c for c in bridge.commands_seen if "WRITE" in c]
        assert any("WRITE 00F6 01" in c for c in writes)
        assert any("WRITE 00F6 02FF" in c for c in writes)
    finally:
        iface.disconnect()


def test_step_frame_acknowledged(bridge_factory):
    bridge, iface = bridge_factory(_dr_mario_responder)
    try:
        iface.step_frame()
        iface.step_frame(5)
        steps = [c for c in bridge.commands_seen if "STEP" in c]
        assert any(c.endswith("STEP 1") for c in steps)
        assert any(c.endswith("STEP 5") for c in steps)
    finally:
        iface.disconnect()


def test_get_game_state_parses_all_fields(bridge_factory):
    bridge, iface = bridge_factory(_dr_mario_responder)
    try:
        state = iface.get_game_state()

        assert state["mode"] == 4
        assert state["game_mode"] == 4  # backward-compat alias
        assert state["virus_count"] == 18
        assert state["capsule_x"] == 3
        assert state["capsule_y"] == 1
        assert state["left_color"] == 1
        assert state["right_color"] == 2
        assert len(state["playfield"]) == 128
        assert state["playfield"][0] == 0xD0
        assert state["playfield"][1] == 0xD1
        assert state["playfield"][2] == 0xFF
        # The remaining 125 bytes should all be empty.
        assert all(b == 0xFF for b in state["playfield"][2:])
    finally:
        iface.disconnect()


def test_error_response_raises(bridge_factory):
    def responder(command: str) -> str:
        if command == "PING":
            return "PONG"
        return "ERROR something is on fire"

    bridge, iface = bridge_factory(responder)
    try:
        with pytest.raises(RuntimeError, match="something is on fire"):
            iface.get_game_state()
    finally:
        iface.disconnect()


def test_timeout_when_bridge_silent(tmp_path):
    """If the bridge never writes a response, _send_command must raise TimeoutError."""
    # Create only the ready file so connect() will probe with PING.
    ready = tmp_path / "mesen_ready.txt"
    ready.write_text("READY\n")

    iface = MesenInterface(work_dir=tmp_path, poll_interval=0.001)
    # No bridge thread -> PING will time out -> connect() returns False.
    assert iface.connect(timeout=0.5) is False

    # Force the interface to think it's connected so we can exercise the
    # timeout path of _send_command directly.
    iface.connected = True
    with pytest.raises(TimeoutError):
        iface._send_command("READ 0000 1", timeout=0.2)


def test_sequence_ids_skip_stale_responses(tmp_path):
    """A leftover response with the wrong sequence id must not be returned."""
    # Write a STALE response file from a hypothetical previous command (seq=999).
    (tmp_path / "mesen_response.txt").write_text("999 OK STALE_DATA")
    (tmp_path / "mesen_ready.txt").write_text("READY\n")

    delivered: list[str] = []

    def responder(command: str) -> str:
        # Echo each command so we can confirm the real one was processed.
        delivered.append(command)
        if command == "PING":
            return "PONG"
        if command.startswith("READ "):
            return "OK AB"
        return "OK"

    bridge = FakeBridge(tmp_path, responder)
    bridge.start()
    try:
        iface = MesenInterface(work_dir=tmp_path, poll_interval=0.001)
        # connect() should clean up stale files first.
        assert iface.connect(timeout=2.0) is True
        result = iface.read_memory(0x1234, 1)
        # If the stale response had bled through we'd see [] or garbage; the
        # correct fresh response is 0xAB.
        assert result == [0xAB]
        # And the real READ command must have been processed by the bridge.
        assert any("READ 1234 1" in cmd for cmd in delivered)
        iface.disconnect()
    finally:
        bridge.stop()
