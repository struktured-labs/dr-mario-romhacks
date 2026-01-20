#!/usr/bin/env python3
"""
Debug playfield state and max_height calculation
"""

import sys
sys.path.insert(0, 'src')

import numpy as np
from mednafen_interface_http import MednafenInterface

print("="*60)
print("Playfield State Debug")
print("="*60)
print()

# Connect to MCP
mcp = MednafenInterface(host="localhost", port=8000)
if not mcp.connect(timeout=5):
    print("Failed to connect!")
    sys.exit(1)

print("Connected to MCP server")
print()

# Get game state
state = mcp.get_game_state()

print(f"Game mode: {state['mode']}")
print(f"Virus count: {state['virus_count']}")
print(f"Capsule position: ({state['capsule_x']}, {state['capsule_y']})")
print()

# Get playfield
playfield = np.array(state['playfield'], dtype=np.uint8).reshape(16, 8)

print("P2 Playfield (top 8 rows):")
print("   ", "  ".join(f"{i}" for i in range(8)))
for row in range(8):
    tiles = []
    for col in range(8):
        tile = playfield[row, col]
        if tile == 0xFF:
            tiles.append("  .")
        elif tile == 0xD0:
            tiles.append(" YV")  # Yellow virus
        elif tile == 0xD1:
            tiles.append(" RV")  # Red virus
        elif tile == 0xD2:
            tiles.append(" BV")  # Blue virus
        elif 0x40 <= tile <= 0x72:
            tiles.append(" P" + hex(tile)[2:])  # Pill
        else:
            tiles.append(f" {tile:02x}")
    print(f"{row:2d}:", "".join(tiles))

print()
print("Finding occupied rows...")
for row in range(16):
    occupied = np.any(playfield[row, :] != 0xFF)
    nonzero_count = np.count_nonzero(playfield[row, :] != 0xFF)
    if occupied:
        print(f"   Row {row:2d}: {nonzero_count} occupied tiles")

print()
print("Calculating max_height (lowest occupied row)...")
max_height = 16
for row in range(16):
    if np.any(playfield[row, :] != 0xFF):
        max_height = row
        break

print(f"   max_height = {max_height}")

if max_height == 0:
    print()
    print("❌ CRITICAL BUG FOUND!")
    print("   Row 0 is occupied on reset!")
    print("   Game over condition triggers immediately!")
    print()
    print("   Row 0 contents:")
    for col in range(8):
        tile = playfield[0, col]
        print(f"      Col {col}: 0x{tile:02X} ({tile})")

print()
print("Checking P1 playfield...")
if 'p1_playfield' in state:
    p1_playfield = np.array(state['p1_playfield'], dtype=np.uint8).reshape(16, 8)
    p1_max_height = 16
    for row in range(16):
        if np.any(p1_playfield[row, :] != 0xFF):
            p1_max_height = row
            break
    print(f"   P1 max_height: {p1_max_height}")
else:
    print("   P1 playfield not available")

mcp.disconnect()
