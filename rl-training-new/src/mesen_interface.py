"""
Mesen Interface: Python client for Mesen Lua bridge
Provides RL training interface via TCP socket to Mesen emulator

Usage:
    interface = MesenInterface()
    interface.connect()

    # Read memory
    data = interface.read_memory(0x03A4, 1)  # Read virus count

    # Write memory (e.g., controller input)
    interface.write_memory(0x00F6, [0x01])  # Press right

    # Step frames
    interface.step_frame()

    # Get full game state
    state = interface.get_game_state()
"""

import socket
import struct
import time
from typing import List, Optional, Dict, Any


class MesenInterface:
    """Interface to Mesen emulator via Lua bridge"""

    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.connected = False

    def connect(self, timeout: float = 10.0) -> bool:
        """
        Connect to Mesen Lua bridge server

        Args:
            timeout: Maximum time to wait for connection (seconds)

        Returns:
            True if connected, False otherwise
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(2.0)
                self.socket.connect((self.host, self.port))
                self.connected = True
                print(f"Connected to Mesen bridge at {self.host}:{self.port}")
                return True
            except (ConnectionRefusedError, socket.timeout):
                if self.socket:
                    self.socket.close()
                    self.socket = None
                time.sleep(0.5)

        print(f"Failed to connect to Mesen bridge after {timeout}s")
        return False

    def disconnect(self):
        """Close connection to Mesen"""
        if self.socket:
            try:
                self._send_command("QUIT")
            except:
                pass
            self.socket.close()
            self.socket = None
        self.connected = False

    def _send_command(self, command: str) -> str:
        """
        Send command to Lua bridge and get response

        Args:
            command: Command string (e.g., "READ 03A4 1")

        Returns:
            Response string from Lua bridge

        Raises:
            ConnectionError: If not connected or connection lost
        """
        if not self.connected or not self.socket:
            raise ConnectionError("Not connected to Mesen")

        try:
            # Send command
            self.socket.sendall((command + "\n").encode('utf-8'))

            # Receive response
            response = self.socket.recv(4096).decode('utf-8').strip()

            if response.startswith("ERROR"):
                raise RuntimeError(f"Mesen bridge error: {response}")

            return response

        except socket.error as e:
            self.connected = False
            raise ConnectionError(f"Connection lost: {e}")

    def read_memory(self, address: int, size: int) -> List[int]:
        """
        Read bytes from NES memory

        Args:
            address: Memory address (0x0000-0xFFFF)
            size: Number of bytes to read

        Returns:
            List of byte values
        """
        cmd = f"READ {address:04X} {size}"
        response = self._send_command(cmd)

        # Parse "OK <hex_string>"
        if not response.startswith("OK "):
            raise ValueError(f"Unexpected response: {response}")

        hex_data = response[3:].strip()

        # Convert hex string to bytes
        bytes_list = []
        for i in range(0, len(hex_data), 2):
            byte_str = hex_data[i:i+2]
            bytes_list.append(int(byte_str, 16))

        return bytes_list

    def write_memory(self, address: int, data: List[int]):
        """
        Write bytes to NES memory

        Args:
            address: Memory address (0x0000-0xFFFF)
            data: List of byte values to write
        """
        hex_data = ''.join(f'{byte:02X}' for byte in data)
        cmd = f"WRITE {address:04X} {hex_data}"
        response = self._send_command(cmd)

        if not response.startswith("OK"):
            raise RuntimeError(f"Write failed: {response}")

    def step_frame(self, num_frames: int = 1):
        """
        Step forward N frames

        Args:
            num_frames: Number of frames to advance
        """
        cmd = f"STEP {num_frames}"
        response = self._send_command(cmd)

        if not response.startswith("OK"):
            raise RuntimeError(f"Step failed: {response}")

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get full Dr. Mario game state

        Returns:
            Dictionary with:
                - playfield: List[int] (128 bytes, 8x16 grid)
                - capsule_x: int (0-7)
                - capsule_y: int (0-15)
                - left_color: int (0=yellow, 1=red, 2=blue)
                - right_color: int (0=yellow, 1=red, 2=blue)
                - virus_count: int
                - game_mode: int (< 4 = menu, >= 4 = gameplay)
        """
        response = self._send_command("GET_STATE")

        if not response.startswith("OK {"):
            raise ValueError(f"Unexpected response: {response}")

        # Parse JSON-like response
        # Format: OK {playfield:HEXSTRING,capsule_x:INT,...}
        data_str = response[3:].strip()
        state = {}

        # Simple parser for the format
        parts = data_str.strip('{}').split(',')
        for part in parts:
            key, value = part.split(':', 1)

            if key == 'playfield':
                # Convert hex string to byte list
                playfield = []
                for i in range(0, len(value), 2):
                    playfield.append(int(value[i:i+2], 16))
                state['playfield'] = playfield
            else:
                state[key] = int(value)

        return state

    def __enter__(self):
        """Context manager support"""
        if not self.connected:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        self.disconnect()


if __name__ == "__main__":
    # Simple test
    print("Testing Mesen interface...")
    print("Make sure Mesen is running with mesen_bridge.lua loaded")
    print()

    interface = MesenInterface()

    if interface.connect(timeout=5):
        try:
            # Read virus count
            virus_count_bytes = interface.read_memory(0x03A4, 1)
            print(f"P2 Virus count: {virus_count_bytes[0]}")

            # Get full game state
            state = interface.get_game_state()
            print(f"Game mode: {state['game_mode']}")
            print(f"Capsule position: ({state['capsule_x']}, {state['capsule_y']})")
            print(f"Capsule colors: L={state['left_color']}, R={state['right_color']}")
            print(f"Virus count: {state['virus_count']}")
            print(f"Playfield size: {len(state['playfield'])} bytes")

            # Write controller input (press right for 1 frame)
            print("\nWriting controller input (RIGHT)...")
            interface.write_memory(0x00F6, [0x01])  # 0x01 = RIGHT
            interface.step_frame()

            print("\nTest completed successfully!")

        except Exception as e:
            print(f"Error during test: {e}")
            import traceback
            traceback.print_exc()
        finally:
            interface.disconnect()
    else:
        print("Failed to connect to Mesen")
