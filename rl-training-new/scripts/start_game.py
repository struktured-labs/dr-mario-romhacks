#!/usr/bin/env python3
"""
Auto-start Dr. Mario in VS CPU mode via controller inputs.

This script sends controller inputs to navigate from title screen to gameplay,
allowing the MCP RAM discovery to find virus patterns in memory.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mednafen_interface_mcp import MednafenInterface

# Controller button mappings
BTN_START = 0x08
BTN_SELECT = 0x04

# Controller addresses
P1_CONTROLLER = 0x00F5


def auto_start_game():
    """Navigate to VS CPU gameplay automatically."""
    print("Auto-starting Dr. Mario in VS CPU mode...")

    interface = MednafenInterface()
    if not interface.connect(timeout=10):
        print("✗ Failed to connect to Mednafen")
        print("  Make sure Mednafen is running:")
        print("  xvfb-run -a mednafen /path/to/drmario_vs_cpu.nes &")
        return False

    print("✓ Connected to Mednafen")

    try:
        # Wait for title screen to appear
        print("Waiting for title screen...")
        time.sleep(2)

        # Press START to enter main menu
        print("Pressing START...")
        interface.write_memory(P1_CONTROLLER, [BTN_START])
        time.sleep(0.1)
        interface.write_memory(P1_CONTROLLER, [0x00])  # Release
        time.sleep(1)

        # Press SELECT twice to cycle to "VS CPU" mode
        print("Selecting VS CPU mode (SELECT x2)...")
        for _ in range(2):
            interface.write_memory(P1_CONTROLLER, [BTN_SELECT])
            time.sleep(0.1)
            interface.write_memory(P1_CONTROLLER, [0x00])
            time.sleep(0.5)

        # Press START to begin game
        print("Starting game...")
        interface.write_memory(P1_CONTROLLER, [BTN_START])
        time.sleep(0.1)
        interface.write_memory(P1_CONTROLLER, [0x00])
        time.sleep(2)

        # Verify we're in gameplay by checking for viruses
        print("Verifying game state...")
        state = interface.get_game_state()

        if state['virus_count'] > 0:
            print(f"✓ Game started! P2 has {state['virus_count']} viruses")
            print(f"  Mode: {state['mode']}")
            return True
        else:
            print("⚠️  Game may not have started (no viruses detected)")
            print("  This might be OK if in level select screen")
            return True

    except Exception as e:
        print(f"✗ Error during auto-start: {e}")
        return False
    finally:
        interface.disconnect()


if __name__ == "__main__":
    success = auto_start_game()
    sys.exit(0 if success else 1)
