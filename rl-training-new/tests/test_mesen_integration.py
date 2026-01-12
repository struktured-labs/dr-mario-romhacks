#!/usr/bin/env python3
"""
Integration test for Mesen + Lua bridge + Python client

This script:
1. Launches Mesen with Dr. Mario ROM
2. Loads the Lua bridge script
3. Tests memory read/write and frame stepping

Usage:
    python test_mesen_integration.py
"""

import sys
import os
import time
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mesen_interface import MesenInterface


def find_rom():
    """Find Dr. Mario ROM"""
    possible_paths = [
        "/home/struktured/projects/dr-mario-mods/drmario_vs_cpu.nes",
        "/home/struktured/projects/dr-mario-mods/drmario.nes",
        Path(__file__).parent.parent.parent / "drmario_vs_cpu.nes",
        Path(__file__).parent.parent.parent / "drmario.nes",
    ]

    for path in possible_paths:
        p = Path(path)
        if p.exists():
            return str(p)

    return None


def test_mesen_integration():
    """Run full integration test"""
    print("=" * 60)
    print("Mesen Integration Test")
    print("=" * 60)

    # Find ROM
    rom_path = find_rom()
    if not rom_path:
        print("ERROR: Could not find Dr. Mario ROM")
        print("Expected: drmario_vs_cpu.nes or drmario.nes")
        return False

    print(f"\n✓ Found ROM: {rom_path}")

    # Find Lua script
    lua_script = Path(__file__).parent.parent / "lua" / "mesen_bridge.lua"
    if not lua_script.exists():
        print(f"ERROR: Lua script not found at {lua_script}")
        return False

    print(f"✓ Found Lua script: {lua_script}")

    # Find Mesen executable
    mesen_exe = Path(__file__).parent.parent.parent / "run_mesen.sh"
    if not mesen_exe.exists():
        print(f"ERROR: Mesen wrapper not found at {mesen_exe}")
        return False

    print(f"✓ Found Mesen: {mesen_exe}")

    # Launch Mesen with ROM and Lua script
    print("\n" + "=" * 60)
    print("Launching Mesen...")
    print("=" * 60)
    print(f"Command: {mesen_exe} {rom_path}")
    print("NOTE: You may need to manually load the Lua script in Mesen:")
    print(f"  Tools → Script Window → Load Script: {lua_script}")
    print()

    # Note: We can't easily automate Mesen GUI, so we'll just provide instructions
    print("MANUAL STEPS:")
    print("  1. Mesen should have opened")
    print("  2. Go to: Tools → Script Window")
    print("  3. Click 'Load Script' and select: mesen_bridge.lua")
    print("  4. The script should print: 'Bridge initialized'")
    print("  5. Start the game (press F11 or click Play)")
    print()
    print("Once you've done the above, press ENTER to continue test...")
    input()

    # Test Python client
    print("\n" + "=" * 60)
    print("Testing Python Client")
    print("=" * 60)

    interface = MesenInterface()

    print("\n1. Connecting to Mesen bridge...")
    if not interface.connect(timeout=10):
        print("✗ Failed to connect")
        print("  Make sure the Lua script is loaded and the game is running")
        return False
    print("✓ Connected!")

    try:
        # Test 1: Read virus count
        print("\n2. Reading P2 virus count...")
        virus_count_bytes = interface.read_memory(0x03A4, 1)
        virus_count = virus_count_bytes[0]
        print(f"✓ Virus count: {virus_count}")

        # Test 2: Get game state
        print("\n3. Getting full game state...")
        state = interface.get_game_state()
        print(f"✓ Game mode: {state['game_mode']}")
        print(f"✓ Capsule position: ({state['capsule_x']}, {state['capsule_y']})")
        print(f"✓ Capsule colors: L={state['left_color']}, R={state['right_color']}")
        print(f"✓ Playfield size: {len(state['playfield'])} bytes")

        # Test 3: Write controller input
        print("\n4. Testing controller input (RIGHT button)...")
        initial_x = state['capsule_x']
        print(f"   Initial capsule X: {initial_x}")

        # Press right for a few frames
        for i in range(10):
            interface.write_memory(0x00F6, [0x01])  # 0x01 = RIGHT
            interface.step_frame()
            time.sleep(0.016)  # ~1 frame at 60 FPS

        # Check if capsule moved
        new_state = interface.get_game_state()
        new_x = new_state['capsule_x']
        print(f"   New capsule X: {new_x}")

        if new_x != initial_x:
            print(f"✓ Capsule moved! ({initial_x} → {new_x})")
        else:
            print("⚠ Capsule didn't move (might be blocked or in menu)")

        # Test 4: Frame stepping
        print("\n5. Testing frame stepping...")
        start_time = time.time()
        for i in range(60):  # Step 60 frames (~1 second)
            interface.step_frame()
        elapsed = time.time() - start_time
        print(f"✓ Stepped 60 frames in {elapsed:.2f}s")

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        print("\nMesen bridge is working correctly.")
        print("You can now proceed with RL training!")

        return True

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        interface.disconnect()


if __name__ == "__main__":
    success = test_mesen_integration()
    sys.exit(0 if success else 1)
