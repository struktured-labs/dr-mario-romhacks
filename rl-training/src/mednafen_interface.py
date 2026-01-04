"""
Mednafen Headless Emulator Interface

This module provides communication with Mednafen emulator for:
- Reading NES memory
- Writing to memory (controller injection)
- Frame stepping
- Save state management

Two implementation strategies:
1. Network debugger protocol (preferred, if available)
2. Save state file manipulation (fallback)
"""

import subprocess
import socket
import struct
import time
from pathlib import Path
from typing import Optional


class MednafenDebugger:
    """
    Interface to Mednafen via network debugger protocol

    Requires Mednafen to be launched with debugger enabled:
    mednafen -debugger.autostart 1 -debugger.server 1 -debugger.serverport 6502 rom.nes

    TODO: Investigate if Mednafen actually supports network debugger.
    If not, fall back to MednafenSaveState implementation below.
    """

    def __init__(self, rom_path: str, headless: bool = True, debugger_port: int = 6502):
        self.rom_path = rom_path
        self.headless = headless
        self.debugger_port = debugger_port
        self.process: Optional[subprocess.Popen] = None
        self.socket: Optional[socket.socket] = None

    def start(self):
        """Launch Mednafen in debugger mode"""
        cmd = [
            "mednafen",
            "-debugger.autostart", "1",
            "-debugger.server", "1",
            "-debugger.serverport", str(self.debugger_port),
        ]

        if self.headless:
            cmd.extend(["-video.disable", "1"])

        cmd.append(self.rom_path)

        self.process = subprocess.Popen(cmd)

        # Wait for debugger to be ready
        time.sleep(1)

        # Connect to debugger
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("localhost", self.debugger_port))

    def stop(self):
        """Stop Mednafen process"""
        if self.socket:
            self.socket.close()
        if self.process:
            self.process.terminate()
            self.process.wait()

    def send_command(self, command: str) -> str:
        """Send debugger command and receive response"""
        if not self.socket:
            raise RuntimeError("Debugger not connected")

        self.socket.send(f"{command}\n".encode())
        response = self.socket.recv(4096).decode()
        return response

    def read_memory(self, address: int, length: int = 1) -> bytes:
        """
        Read NES CPU memory

        Args:
            address: CPU address (0x0000-0xFFFF)
            length: Number of bytes to read

        Returns:
            Bytes read from memory
        """
        # TODO: Implement actual debugger protocol commands
        # Placeholder for now
        response = self.send_command(f"read {address:04X} {length}")
        # Parse response and extract bytes
        return b'\x00' * length  # Placeholder

    def write_memory(self, address: int, value: int):
        """
        Write to NES CPU memory

        Args:
            address: CPU address
            value: Byte value to write (0-255)
        """
        self.send_command(f"write {address:04X} {value:02X}")

    def step_frame(self):
        """Advance emulation by 1 frame (~16.67ms at 60Hz)"""
        # TODO: Determine correct command for frame stepping
        self.send_command("step_frame")

    def reset(self):
        """Reset emulator"""
        self.send_command("reset")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class MednafenSaveState:
    """
    Fallback implementation using save state file manipulation

    This approach:
    1. Runs Mednafen for N frames
    2. Saves state to file
    3. Reads state file to extract memory
    4. Modifies state file to inject inputs
    5. Loads modified state and continues

    Slower than network debugger but more reliable.
    """

    def __init__(self, rom_path: str, headless: bool = True):
        self.rom_path = rom_path
        self.headless = headless
        self.state_file = Path("mednafen_state.mcs")  # Mednafen save state format

    def start(self):
        """Initialize emulator"""
        # Create initial save state
        self._run_frames(1)
        self._save_state()

    def _run_frames(self, num_frames: int):
        """Run Mednafen for N frames"""
        cmd = ["mednafen"]

        if self.headless:
            cmd.extend(["-video.disable", "1"])

        cmd.extend([
            "-frames", str(num_frames),
            self.rom_path
        ])

        subprocess.run(cmd, check=True)

    def _save_state(self):
        """Save current emulator state to file"""
        # TODO: Trigger save state via Mednafen command
        # May need to use savestate command or hotkey simulation
        pass

    def _load_state(self):
        """Load state from file"""
        # TODO: Trigger load state
        pass

    def read_memory(self, address: int, length: int = 1) -> bytes:
        """
        Read memory by parsing save state file

        Mednafen .mcs format contains full NES RAM dump.
        Need to parse file structure and extract relevant bytes.
        """
        if not self.state_file.exists():
            raise FileNotFoundError("Save state not found")

        # TODO: Parse .mcs file format
        # For now, return dummy data
        return b'\x00' * length

    def write_memory(self, address: int, value: int):
        """
        Write memory by modifying save state file
        """
        # Read state file
        with open(self.state_file, 'rb') as f:
            state_data = bytearray(f.read())

        # TODO: Find offset of NES RAM within .mcs file
        # Modify the byte at that offset
        # Write back to file

        with open(self.state_file, 'wb') as f:
            f.write(state_data)

    def step_frame(self):
        """Step one frame by running Mednafen"""
        self._run_frames(1)
        self._save_state()

    def reset(self):
        """Reset by deleting save state"""
        if self.state_file.exists():
            self.state_file.unlink()
        self.start()


# Factory function to choose implementation
def create_mednafen_interface(
    rom_path: str,
    headless: bool = True,
    use_debugger: bool = True
) -> 'MednafenDebugger | MednafenSaveState':
    """
    Create appropriate Mednafen interface

    Args:
        rom_path: Path to Dr. Mario ROM
        headless: Run without GUI
        use_debugger: Try network debugger first, fall back to save state

    Returns:
        Mednafen interface instance
    """
    if use_debugger:
        try:
            interface = MednafenDebugger(rom_path, headless)
            interface.start()
            return interface
        except Exception as e:
            print(f"Debugger mode failed ({e}), falling back to save state mode")

    return MednafenSaveState(rom_path, headless)
