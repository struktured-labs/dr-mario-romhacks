#!/usr/bin/env python3
"""
Debug raw memory reading from MCP
"""

import sys
sys.path.insert(0, 'src')

import numpy as np
from mednafen_interface_http import MednafenInterface

print("="*60)
print("Memory Read Debug")
print("="*60)
print()

# Connect to MCP
mcp = MednafenInterface(host="localhost", port=8000)
if not mcp.connect(timeout=5):
    print("Failed to connect!")
    sys.exit(1)

print("Connected!")
print()

# Try reading virus count (should be 5)
print("Testing known addresses:")
print(f"  P2 virus count ($03A4): Expected 5")
virus_count_raw = mcp.read_memory(0x03A4, 1)
print(f"    Raw response: {virus_count_raw}")

if 'data' in virus_count_raw:
    virus_count = virus_count_raw['data'][0]
    print(f"    Value: {virus_count}")
    if virus_count == 5:
        print(f"    ✓ Correct!")
    else:
        print(f"    ✗ Wrong! (expected 5)")
print()

# Read game mode
print(f"  Game mode ($0046): Expected 4")
mode_raw = mcp.read_memory(0x0046, 1)
print(f"    Raw response: {mode_raw}")
if 'data' in mode_raw:
    mode = mode_raw['data'][0]
    print(f"    Value: {mode}")
    if mode == 4:
        print(f"    ✓ Correct!")
    else:
        print(f"    ✗ Wrong!")
print()

# Read P2 playfield start
print(f"  P2 playfield start ($0500):")
playfield_raw = mcp.read_memory(0x0500, 16)
print(f"    Raw response: {playfield_raw}")
if 'data' in playfield_raw:
    data = playfield_raw['data']
    print(f"    First 16 bytes: {' '.join(f'{b:02X}' for b in data)}")

    empty_count = sum(1 for b in data if b == 0xFF)
    virus_count = sum(1 for b in data if 0xD0 <= b <= 0xD2)
    print(f"    Empty tiles (0xFF): {empty_count}")
    print(f"    Viruses (0xD0-0xD2): {virus_count}")

    if empty_count > 0 or virus_count > 0:
        print(f"    ✓ Looks like valid playfield data!")
    else:
        print(f"    ✗ Doesn't look like playfield data!")
print()

# Check if read_memory and get_game_state return different data
print("Comparing read_memory vs get_game_state:")
state = mcp.get_game_state()
playfield_from_state = bytes.fromhex(state['playfield']['raw']) if 'playfield' in state and 'raw' in state['playfield'] else None

if playfield_from_state:
    print(f"  get_game_state playfield (first 16 bytes):")
    print(f"    {' '.join(f'{b:02X}' for b in playfield_from_state[:16])}")

    if 'data' in playfield_raw:
        direct_read = bytes(playfield_raw['data'])
        print(f"  read_memory(0x0500) (first 16 bytes):")
        print(f"    {' '.join(f'{b:02X}' for b in direct_read[:16])}")

        if playfield_from_state[:16] == direct_read[:16]:
            print(f"  ✓ Data matches!")
        else:
            print(f"  ✗ Data DIFFERS!")
            print(f"     This indicates MCP parsing issue")

mcp.disconnect()
