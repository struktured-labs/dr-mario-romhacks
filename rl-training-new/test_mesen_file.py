#!/usr/bin/env python3
"""Test file-based Mesen connection"""
import sys
sys.path.insert(0, 'src')
from mesen_interface_file import MesenInterface
import numpy as np

print('Testing file-based Mesen connection...')
mesen = MesenInterface()

if mesen.connect(timeout=5):
    print('\n✓ Connected!')

    # Test game state
    state = mesen.get_game_state()
    print(f'\nGame State:')
    print(f'  Mode: {state["mode"]}')
    print(f'  Virus count: {state["virus_count"]}')
    print(f'  Capsule: ({state["capsule_x"]}, {state["capsule_y"]})')

    # Check playfield
    playfield = np.array(state['playfield'], dtype=np.uint8).reshape(16, 8)
    empty = np.sum(playfield == 0xFF)
    viruses = np.sum((playfield == 0xD0) | (playfield == 0xD1) | (playfield == 0xD2))
    row0_occ = np.sum(playfield[0, :] != 0xFF)

    print(f'\nPlayfield:')
    print(f'  Empty tiles: {empty}/128')
    print(f'  Virus tiles: {viruses}')
    print(f'  Row 0 occupancy: {row0_occ}')

    # Show first few rows
    print('\nFirst 3 rows:')
    for i in range(3):
        row_tiles = playfield[i, :]
        row_str = ' '.join(f'{t:02X}' for t in row_tiles)
        print(f'  Row {i}: {row_str}')

    if empty > 100:
        print('\n✓✓✓ CLEAN PLAYFIELD - Mesen properly initialized!')
        print('Ready to start RL training!')
    else:
        print(f'\n⚠ Garbage detected - only {empty} empty')

    mesen.disconnect()
else:
    print('✗ Connection failed')
    sys.exit(1)
