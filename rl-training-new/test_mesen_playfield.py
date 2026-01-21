#!/usr/bin/env python3
"""Test if Mesen has clean playfield (vs garbage in Mednafen)"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mesen_interface import MesenInterface
import numpy as np

print("Testing Mesen playfield...")
mesen = MesenInterface()

if not mesen.connect(timeout=5):
    print("✗ Could not connect to Mesen")
    sys.exit(1)

state = mesen.get_game_state()

print(f"\nGame State:")
print(f"  Mode: {state.get('mode')}")
print(f"  Virus count: {state.get('virus_count')}")

# Check playfield
playfield = np.array(state['playfield'], dtype=np.uint8).reshape(16, 8)
empty_count = np.sum(playfield == 0xFF)
virus_tiles = np.sum((playfield == 0xD0) | (playfield == 0xD1) | (playfield == 0xD2))
row0_occupied = np.sum(playfield[0, :] != 0xFF)

print(f"\nPlayfield Analysis:")
print(f"  Empty tiles (0xFF): {empty_count}/128")
print(f"  Virus tiles (0xD0-0xD2): {virus_tiles}")
print(f"  Row 0 occupancy: {row0_occupied} tiles")

# Show first few rows
print(f"\nFirst 3 rows:")
for row in range(3):
    print(f"  Row {row}: {playfield[row, :]}")

if empty_count > 100:
    print("\n✓ CLEAN PLAYFIELD - Mesen initialized properly!")
else:
    print(f"\n⚠ GARBAGE - Only {empty_count} empty tiles")

mesen.disconnect()
