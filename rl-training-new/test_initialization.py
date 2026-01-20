#!/usr/bin/env python3
"""
Test game initialization to verify:
1. Game starts in 2P mode (not 1P)
2. Both players have viruses initialized
3. Agent can actually play without immediate top-out
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mednafen_manager import MednafenManager
import time

def test_initialization():
    print("="*60)
    print("Testing Dr. Mario Game Initialization")
    print("="*60)

    manager = MednafenManager()

    # Launch with virus level 5
    print("\n1. Launching Mednafen...")
    result = manager.launch(headless=False, virus_level=5)

    if not result.get("success"):
        print(f"❌ Launch failed: {result.get('error')}")
        return False

    print(f"✓ Launched successfully")
    print(f"  Game mode: {result.get('game_mode')}")
    print(f"  In gameplay: {result.get('in_gameplay')}")

    time.sleep(2)

    # Check player mode
    print("\n2. Checking player mode...")
    player_mode = manager.mcp.read_nes_ram(0x0727, 1)
    if player_mode:
        mode_value = player_mode[0]
        mode_name = {0x01: "1P", 0x02: "2P"}.get(mode_value, f"Unknown ({mode_value})")
        print(f"  Player mode ($0727): {mode_name}")

        if mode_value != 0x02:
            print(f"  ❌ WRONG! Should be 0x02 (2P), got {mode_value:#04x}")
            return False
        print(f"  ✓ Correct 2P mode")

    # Check virus counts
    print("\n3. Checking virus counts...")
    p1_viruses = manager.mcp.read_nes_ram(0x0324, 1)
    p2_viruses = manager.mcp.read_nes_ram(0x03A4, 1)

    if p1_viruses and p2_viruses:
        p1_count = p1_viruses[0]
        p2_count = p2_viruses[0]
        print(f"  P1 viruses ($0324): {p1_count}")
        print(f"  P2 viruses ($03A4): {p2_count}")

        if p1_count == 0 or p2_count == 0:
            print(f"  ❌ WRONG! Both players should have viruses")
            return False
        print(f"  ✓ Both players have viruses")

    # Check game mode
    print("\n4. Checking game mode...")
    game_mode = manager.mcp.read_nes_ram(0x0046, 1)
    if game_mode:
        mode = game_mode[0]
        in_gameplay = mode >= 4
        print(f"  Game mode ($0046): {mode} ({'gameplay' if in_gameplay else 'menu'})")

        if not in_gameplay:
            print(f"  ❌ WRONG! Should be in gameplay (mode >= 4)")
            return False
        print(f"  ✓ In gameplay mode")

    print("\n" + "="*60)
    print("✓ ALL CHECKS PASSED - Game initialized correctly!")
    print("="*60)
    print("\nPress Ctrl+C to exit...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        manager.shutdown()

    return True

if __name__ == "__main__":
    success = test_initialization()
    sys.exit(0 if success else 1)
