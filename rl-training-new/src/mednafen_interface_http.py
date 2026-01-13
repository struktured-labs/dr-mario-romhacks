"""
Mednafen interface via HTTP MCP server.

This interface makes HTTP requests to the mednafen_mcp_server.py Flask app,
which maintains a persistent MednafenMCP instance.

This solves the RAM base discovery issue by using a single persistent
MCP instance instead of creating new instances per Python process.
"""

import requests
import time
from typing import Dict, List, Any


class MednafenInterface:
    """Interface to Mednafen via HTTP MCP server."""

    def __init__(self, host: str = "localhost", port: int = 8000):
        """
        Initialize interface.

        Args:
            host: MCP server host
            port: MCP server port
        """
        self.base_url = f"http://{host}:{port}"
        self.connected = False
        self.session = requests.Session()  # Reuse connections

    def connect(self, timeout: int = 10) -> bool:
        """
        Check if MCP server is running and connected to Mednafen.

        Args:
            timeout: Connection timeout in seconds

        Returns:
            True if connected
        """
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=timeout
            )
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'ok' and data.get('pid'):
                self.connected = True
                print(f"Connected to Mednafen (PID {data['pid']}, RAM base {data.get('nes_ram_base')})")
                return True
            else:
                print("MCP server running but not connected to Mednafen")
                # Try to connect
                response = self.session.post(
                    f"{self.base_url}/connect",
                    timeout=timeout
                )
                response.raise_for_status()
                data = response.json()

                if data.get('status') == 'connected':
                    self.connected = True
                    print(f"Connected to Mednafen (PID {data['pid']}, RAM base {data.get('nes_ram_base')})")
                    return True

                return False

        except requests.exceptions.ConnectionError:
            print(f"ERROR: MCP server not running at {self.base_url}")
            print("Start it with: python3 mednafen_mcp_server.py")
            return False
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def disconnect(self):
        """Disconnect (cleanup)."""
        self.connected = False
        self.session.close()

    def read_memory(self, address: int, size: int) -> List[int]:
        """
        Read bytes from NES RAM.

        Args:
            address: NES RAM address
            size: Number of bytes

        Returns:
            List of byte values
        """
        try:
            response = self.session.post(
                f"{self.base_url}/read_memory",
                json={'address': address, 'size': size},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            if 'error' in data:
                raise RuntimeError(f"MCP read failed: {data['error']}")

            return data.get('values', [])

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"HTTP request failed: {e}")

    def write_memory(self, address: int, data: List[int]):
        """
        Write bytes to NES RAM.

        Args:
            address: NES RAM address
            data: List of bytes to write
        """
        try:
            response = self.session.post(
                f"{self.base_url}/write_memory",
                json={'address': address, 'data': data},
                timeout=5
            )
            response.raise_for_status()
            result = response.json()

            if 'error' in result:
                raise RuntimeError(f"MCP write failed: {result['error']}")

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"HTTP request failed: {e}")

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get game state using MCP game_state command.

        Returns:
            Dictionary with game state for both players
        """
        try:
            response = self.session.get(
                f"{self.base_url}/game_state",
                timeout=5
            )
            response.raise_for_status()
            full_state = response.json()

            if 'error' in full_state:
                raise RuntimeError(f"MCP game_state failed: {full_state['error']}")

            # Extract P2 state (for compatibility with existing code)
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

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"HTTP request failed: {e}")

    def step_frame(self):
        """Advance emulator by 1 frame."""
        # Mednafen runs continuously, no explicit frame stepping needed
        time.sleep(0.016)  # ~60 FPS

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


if __name__ == "__main__":
    # Test interface
    print("Testing Mednafen HTTP Interface...")
    print()
    print("Prerequisites:")
    print("  1. Mednafen running (via MCP launch or xvfb-run mednafen ROM)")
    print("  2. MCP server running (python3 mednafen_mcp_server.py)")
    print()

    interface = MednafenInterface()

    if not interface.connect(timeout=10):
        print("Failed to connect. Exiting.")
        exit(1)

    try:
        # Get game state
        state = interface.get_game_state()
        print(f"Game mode: {state['mode']}")
        print(f"P2 viruses: {state['virus_count']}")
        print(f"P2 capsule: ({state['capsule_x']}, {state['capsule_y']})")
        print(f"P2 colors: L={state['left_color']}, R={state['right_color']}")

        # Test memory read
        mode_byte = interface.read_memory(0x0046, 1)
        print(f"\nDirect read of game mode ($0046): {mode_byte[0]}")

        # Test memory write (write to unused RAM location)
        test_addr = 0x0000
        interface.write_memory(test_addr, [0x42])
        verify = interface.read_memory(test_addr, 1)
        print(f"Write test: wrote 0x42, read back {hex(verify[0])}")

        if verify[0] == 0x42:
            print("\n✓ Interface test complete!")
        else:
            print("\n✗ Write/read mismatch!")

    finally:
        interface.disconnect()
