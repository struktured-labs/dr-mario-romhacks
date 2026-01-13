"""
Mednafen interface for RL training using MCP server logic.

This directly uses the MednafenMCP from mednafen-mcp with a singleton pattern
to ensure all instances share the same RAM discovery.
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import from mednafen-mcp directory
MCP_DIR = Path(__file__).parent.parent.parent / "mednafen-mcp"
sys.path.insert(0, str(MCP_DIR))

try:
    from mcp_server import MednafenMCP, find_mednafen_pid
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

# Singleton MCP controller shared by all MednafenInterface instances
_mcp_controller: Optional[MednafenMCP] = None


def get_mcp_controller() -> MednafenMCP:
    """Get or create the singleton MCP controller."""
    global _mcp_controller
    if _mcp_controller is None:
        _mcp_controller = MednafenMCP()
    return _mcp_controller


def initialize_mcp_controller(pid: int = None, nes_ram_base: int = None):
    """
    Initialize the singleton MCP controller with known values.

    This is useful when Mednafen was launched externally (e.g., via MCP launch tool)
    and we need to sync the controller state.

    Args:
        pid: Mednafen process ID (will auto-detect if None)
        nes_ram_base: NES RAM base address (will auto-discover if None)
    """
    global _mcp_controller
    controller = get_mcp_controller()

    # Set PID
    if pid is None:
        pid = find_mednafen_pid()
    controller.pid = pid

    # Set or discover RAM base
    if nes_ram_base is not None:
        controller.nes_ram_base = nes_ram_base
    elif controller.nes_ram_base is None:
        # Try to discover RAM
        controller._discover_nes_ram()


class MednafenInterface:
    """Interface to Mednafen emulator via MCP server logic."""

    def __init__(self):
        """Initialize interface using singleton MCP controller."""
        self._controller = get_mcp_controller()
        self.connected = False

    def connect(self, timeout: int = 10) -> bool:
        """
        Connect to running Mednafen process.

        Args:
            timeout: Connection timeout in seconds

        Returns:
            True if connected successfully
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self._controller.connect()
            if result.get("success"):
                # Force RAM discovery after connecting
                if result.get("nes_ram_base") is None:
                    print("Discovering NES RAM...")
                    self._controller._discover_nes_ram()

                self.connected = True
                ram_hex = hex(self._controller.nes_ram_base) if self._controller.nes_ram_base else "not found"
                print(f"Connected to Mednafen (PID {result['pid']}), RAM at {ram_hex}")
                return True
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
        if not self.connected:
            raise RuntimeError("Not connected to Mednafen")

        result = self._controller.read_nes_ram(address, size)
        if "error" in result:
            raise RuntimeError(f"Failed to read memory: {result['error']}")

        return result["values"]

    def write_memory(self, address: int, data: List[int]):
        """
        Write bytes to NES RAM.

        Args:
            address: NES RAM address (0x0000-0x07FF)
            data: List of byte values to write
        """
        if not self.connected:
            raise RuntimeError("Not connected to Mednafen")

        result = self._controller.write_nes_ram(address, data)
        if "error" in result:
            raise RuntimeError(f"Failed to write memory: {result['error']}")

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

        # Get full game state
        result = self._controller.get_game_state()
        if "error" in result:
            raise RuntimeError(f"Failed to get game state: {result['error']}")

        # Extract P2 state for RL training
        p2 = result.get("player2", {})

        return {
            "mode": result.get("game_mode", 0),
            "virus_count": p2.get("virus_count", 0),
            "capsule_x": p2.get("x_pos", 0),
            "capsule_y": p2.get("y_pos", 0),
            "left_color": p2.get("left_color", 0),
            "right_color": p2.get("right_color", 0),
            "playfield": self._extract_playfield_bytes(p2),
        }

    def _extract_playfield_bytes(self, player_state: Dict) -> List[int]:
        """
        Extract playfield bytes from player state.

        Args:
            player_state: Player state dictionary from get_game_state

        Returns:
            List of 128 bytes representing playfield
        """
        # The playfield in game_state is parsed, but we need raw bytes
        # Read directly from memory for now
        try:
            return self.read_memory(P2_PLAYFIELD_START, 128)
        except:
            # Fallback to empty playfield
            return [0xFF] * 128

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
