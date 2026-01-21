#!/usr/bin/env python3
"""
Launch Mesen for RL training with automated health checks
"""

import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from mesen_interface import MesenInterface

print("="*60)
print("Launching Mesen for Dr. Mario RL Training")
print("="*60)

# 1. Launch Mesen
print("\n1. Starting Mesen...")
mesen_exe = Path(__file__).parent.parent / "mesen2/bin/linux-x64/Release/Mesen"
rom_path = Path(__file__).parent.parent / "drmario_vs_cpu.nes"

proc = subprocess.Popen(
    ["pixi", "run", str(mesen_exe), str(rom_path)],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

print(f"  ✓ Mesen started (PID {proc.pid})")
print("\n2. Waiting for window to appear...")
time.sleep(3)

# 2. Check if Lua bridge is running
print("\n3. Checking for Lua bridge on port 8766...")
mesen = MesenInterface()

for attempt in range(10):
    if mesen.connect(timeout=2):
        print("  ✓ Lua bridge connected!")

        # Test game state
        try:
            state = mesen.get_game_state()
            print(f"\n4. Game state check:")
            print(f"  ✓ Mode: {state.get('mode')}")
            print(f"  ✓ Virus count: {state.get('virus_count')}")
            print(f"\n✓ ALL SYSTEMS GO - Ready for RL training!")
            mesen.disconnect()
            sys.exit(0)
        except Exception as e:
            print(f"  ✗ Game state error: {e}")
            mesen.disconnect()

    if attempt == 0:
        print("\n⚠️  Lua bridge not detected!")
        print("\nMANUAL STEP REQUIRED:")
        print("  1. In the Mesen window, press F11 or go to: Tools → Script Window")
        print("  2. Click 'Load Script' (folder icon)")
        print(f"  3. Select: {Path(__file__).parent}/lua/mesen_bridge.lua")
        print("  4. You should see 'Mesen Bridge Server started on port 8766'")
        print("\nWaiting for Lua bridge to start...")

    time.sleep(2)

print("\n✗ Lua bridge did not start after 20 seconds")
print("Please check the script window in Mesen for errors")
sys.exit(1)
