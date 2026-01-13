"""
Direct Mednafen interface using subprocess to call MCP tools.

This is the simplest approach: just shell out to Python scripts that use
the MCP tools directly, avoiding all the import/singleton issues.
"""

import subprocess
import json
import time
from typing import Dict, List, Any


class MednafenInterface:
    """Interface that shells out to MCP scripts."""

    def __init__(self):
        """Initialize interface."""
        self.connected = False
        self.mcp_script = "/home/struktured/projects/dr-mario-mods/mednafen-mcp/mcp_client.py"

    def connect(self, timeout: int = 10) -> bool:
        """
        Check if Mednafen is running.

        Args:
            timeout: Not used (for compatibility)

        Returns:
            True if connected
        """
        result = subprocess.run(["pgrep", "mednafen"], capture_output=True, text=True)
        if result.returncode == 0:
            self.connected = True
            print(f"Connected to Mednafen (PID {result.stdout.strip()})")
            return True
        return False

    def disconnect(self):
        """Disconnect (no-op)."""
        self.connected = False

    def read_memory(self, address: int, size: int) -> List[int]:
        """
        Read bytes from NES RAM using MCP read command.

        Args:
            address: NES RAM address
            size: Number of bytes

        Returns:
            List of byte values
        """
        # Use mcp__mednafen__read_memory via subprocess
        cmd = ["python3", "-c", f"""
import sys
sys.path.insert(0, '/home/struktured/projects/dr-mario-mods/mednafen-mcp')
from mcp_server import MednafenMCP
mcp = MednafenMCP()
mcp.connect()
result = mcp.read_nes_ram({address}, {size})
if 'values' in result:
    print(','.join(str(v) for v in result['values']))
else:
    sys.exit(1)
"""]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return [int(v) for v in result.stdout.strip().split(',')]
        raise RuntimeError(f"Failed to read memory: {result.stderr}")

    def write_memory(self, address: int, data: List[int]):
        """
        Write bytes to NES RAM using MCP write command.

        Args:
            address: NES RAM address
            data: List of bytes to write
        """
        data_str = ','.join(str(b) for b in data)
        cmd = ["python3", "-c", f"""
import sys
sys.path.insert(0, '/home/struktured/projects/dr-mario-mods/mednafen-mcp')
from mcp_server import MednafenMCP
mcp = MednafenMCP()
mcp.connect()
result = mcp.write_nes_ram({address}, [{data_str}])
if 'error' in result:
    sys.exit(1)
"""]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to write memory: {result.stderr}")

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get game state using MCP game_state command.

        Returns:
            Dictionary with game state
        """
        cmd = ["python3", "-c", """
import sys, json
sys.path.insert(0, '/home/struktured/projects/dr-mario-mods/mednafen-mcp')
from mcp_server import MednafenMCP
mcp = MednafenMCP()
mcp.connect()
result = mcp.get_game_state()
print(json.dumps(result))
"""]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            full_state = json.loads(result.stdout)
            if 'error' in full_state:
                raise RuntimeError(full_state['error'])

            # Extract P2 state
            p2 = full_state.get('player2', {})

            # Get raw playfield bytes
            playfield_raw = p2.get('playfield', {}).get('raw', '')
            playfield_bytes = bytes.fromhex(playfield_raw) if playfield_raw else bytes([0xFF] * 128)

            return {
                'mode': full_state.get('game_mode', 0),
                'virus_count': p2.get('virus_count', 0),
                'capsule_x': p2.get('x_pos', 0),
                'capsule_y': p2.get('y_pos', 0),
                'left_color': p2.get('left_color', 0),
                'right_color': p2.get('right_color', 0),
                'playfield': list(playfield_bytes),
            }

        raise RuntimeError(f"Failed to get game state: {result.stderr}")

    def step_frame(self):
        """Advance emulator by 1 frame."""
        time.sleep(0.016)  # ~60 FPS

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
