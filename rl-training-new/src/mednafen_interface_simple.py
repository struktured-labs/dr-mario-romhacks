"""
Simplified Mednafen interface using low-level memory functions.

This directly uses the memory read/write primitives from mednafen-mcp
without creating MednafenMCP objects, avoiding singleton issues.
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Any

# Import from mednafen-mcp directory
MCP_DIR = Path(__file__).parent.parent.parent / "mednafen-mcp"
sys.path.insert(0, str(MCP_DIR))

try:
    from mcp_server import (
        find_mednafen_pid,
        read_process_memory,
        write_process_memory,
        get_all_memory_regions
    )
except ImportError as e:
    print(f"Error importing from mednafen-mcp: {e}")
    print(f"MCP_DIR: {MCP_DIR}")
    raise

# RAM offsets
P2_CONTROLLER = 0x00F6
P2_PLAYFIELD_START = 0x0500
P2_CAPSULE_LEFT_COLOR = 0x0381
P2_CAPSULE_RIGHT_COLOR = 0x0382
P2_CAPSULE_X = 0x0385
P2_CAPSULE_Y = 0x0386
P2_VIRUS_COUNT = 0x03A4
GAME_MODE = 0x0046

# Global state
_pid = None
_nes_ram_base = None


def discover_nes_ram(pid: int) -> int:
    """
    Discover NES RAM location by searching for Dr. Mario patterns.

    Args:
        pid: Mednafen process ID

    Returns:
        NES RAM base address, or None if not found
    """
    regions = get_all_memory_regions(pid)

    for start, end, perms, name in regions:
        size = end - start
        if size < 0x800 or size > 0x10000000:
            continue

        data = read_process_memory(pid, start, min(size, 0x1000000))
        if data is None or len(data) < 0x800:
            continue

        # Search for NES RAM pattern
        for offset in range(0, len(data) - 0x800, 16):
            # Check playfield at offset 0x500 (P2)
            p2_playfield = data[offset + 0x500:offset + 0x580]

            if len(p2_playfield) < 128:
                continue

            # Count characteristics
            p2_empty = sum(1 for b in p2_playfield if b == 0xFF)
            p2_virus = sum(1 for b in p2_playfield if b in (0xD0, 0xD1, 0xD2))

            # Has viruses OR mostly empty
            if p2_virus >= 3 or p2_empty > 100:
                # Validate with additional checks
                num_players = data[offset + 0x727] if offset + 0x727 < len(data) else 255
                game_mode = data[offset + 0x46] if offset + 0x46 < len(data) else 255

                if num_players <= 2 and game_mode < 20:
                    return start + offset

    return None


class MednafenInterface:
    """Simplified interface using direct memory access."""

    def __init__(self):
        """Initialize interface."""
        self.connected = False

    def connect(self, timeout: int = 10) -> bool:
        """
        Connect to running Mednafen process.

        Args:
            timeout: Connection timeout in seconds

        Returns:
            True if connected successfully
        """
        global _pid, _nes_ram_base

        start_time = time.time()
        while time.time() - start_time < timeout:
            _pid = find_mednafen_pid()
            if _pid:
                # Try to discover or reuse RAM base
                if _nes_ram_base is None:
                    print(f"Discovering NES RAM for PID {_pid}...")
                    _nes_ram_base = discover_nes_ram(_pid)

                if _nes_ram_base:
                    self.connected = True
                    print(f"Connected to Mednafen (PID {_pid}), RAM at {hex(_nes_ram_base)}")
                    return True
                else:
                    print(f"PID found but RAM not discovered, retrying...")

            time.sleep(0.5)

        return False

    def disconnect(self):
        """Disconnect from Mednafen."""
        self.connected = False

    def read_memory(self, address: int, size: int) -> List[int]:
        """
        Read bytes from NES RAM.

        Args:
            address: NES RAM address (0x0000-0x07FF)
            size: Number of bytes to read

        Returns:
            List of byte values
        """
        if not self.connected or _nes_ram_base is None:
            raise RuntimeError("Not connected to Mednafen")

        real_address = _nes_ram_base + address
        data = read_process_memory(_pid, real_address, size)
        if data is None:
            raise RuntimeError(f"Failed to read memory at {hex(address)}")

        return list(data)

    def write_memory(self, address: int, data: List[int]):
        """
        Write bytes to NES RAM.

        Args:
            address: NES RAM address (0x0000-0x07FF)
            data: List of byte values to write
        """
        if not self.connected or _nes_ram_base is None:
            raise RuntimeError("Not connected to Mednafen")

        real_address = _nes_ram_base + address
        success = write_process_memory(_pid, real_address, bytes(data))
        if not success:
            raise RuntimeError(f"Failed to write memory at {hex(address)}")

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get comprehensive Dr. Mario game state.

        Returns:
            Dictionary with game state including:
            - mode: Game mode
            - virus_count: P2 virus count
            - capsule_x, capsule_y: P2 capsule position
            - left_color, right_color: P2 capsule colors
            - playfield: P2 playfield bytes (128 bytes)
        """
        if not self.connected:
            raise RuntimeError("Not connected to Mednafen")

        # Read all relevant memory
        game_mode = self.read_memory(GAME_MODE, 1)[0]
        virus_count = self.read_memory(P2_VIRUS_COUNT, 1)[0]
        capsule_x = self.read_memory(P2_CAPSULE_X, 1)[0]
        capsule_y = self.read_memory(P2_CAPSULE_Y, 1)[0]
        left_color = self.read_memory(P2_CAPSULE_LEFT_COLOR, 1)[0]
        right_color = self.read_memory(P2_CAPSULE_RIGHT_COLOR, 1)[0]
        playfield = self.read_memory(P2_PLAYFIELD_START, 128)

        return {
            "mode": game_mode,
            "virus_count": virus_count,
            "capsule_x": capsule_x,
            "capsule_y": capsule_y,
            "left_color": left_color,
            "right_color": right_color,
            "playfield": playfield,
        }

    def step_frame(self):
        """
        Advance emulator by 1 frame.

        Note: Mednafen runs continuously, so we just wait ~1 frame.
        """
        time.sleep(0.016)  # ~60 FPS

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


def set_ram_base(ram_base: int):
    """
    Manually set the NES RAM base address.

    Useful when the RAM base is known from external source (e.g., MCP launch).

    Args:
        ram_base: NES RAM base address
    """
    global _nes_ram_base
    _nes_ram_base = ram_base
    print(f"Set NES RAM base to {hex(ram_base)}")
