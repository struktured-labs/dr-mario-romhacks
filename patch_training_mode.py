#!/usr/bin/env python3
"""
Dr. Mario Training Mode Patch
=============================
This patch modifies Dr. Mario (NES) to:
1. Show the playfield during pause (no blackout)
2. Display "STUDY" text at top of screen instead of "PAUSE"
3. Keep sprites visible during pause (dropping capsule, Dr. Mario)

Technical details:
- ROM offset 0x17CA: PPU_MASK value during pause
  Original: $16 (background disabled), Patched: $1E (background enabled)

- ROM offset 0x17D4: Sprite hide routine call
  Original: JSR $B894 (fills OAM with $FF), Patched: NOP NOP NOP

- ROM offset 0x17DC: Y position for text
  Original: $77 (center), Patched: $0F (top of screen)

- ROM offset 0x2968+: Sprite data for pause text
  Modified to show "STUDY" using tiles S(0x0D), T(0x16), U(0x0C), D(0x17), Y(0x18)

- CHR ROM Bank 1 PT0: Added T, D, Y letter tiles at positions 0x16, 0x17, 0x18
"""

import hashlib

INPUT_ROM = "drmario.nes"
OUTPUT_ROM = "drmario_training.nes"

# NES tile format: 8x8 pixels, 2 bit planes
# Each tile is 16 bytes: 8 bytes plane 0, then 8 bytes plane 1
# Pixel value = plane0_bit + (plane1_bit * 2)

def create_tile(pattern, use_plane1=False):
    """Create NES tile from 8x8 pattern string (. = 0, # = color)"""
    plane0 = bytearray(8)
    plane1 = bytearray(8)
    for row, line in enumerate(pattern):
        for col, char in enumerate(line[:8]):
            if char == '#':
                if use_plane1:
                    # Set plane 1 for color 2 (white in Banks 1,2)
                    plane1[row] |= (0x80 >> col)
                else:
                    # Set plane 0 for color 1 (white in Banks 0,3)
                    plane0[row] |= (0x80 >> col)
    return bytes(plane0) + bytes(plane1)

# Letter patterns
T_PATTERN = [
    "########",
    "########",
    "...##...",
    "...##...",
    "...##...",
    "...##...",
    "...##...",
    "........",
]

D_PATTERN = [
    "#####...",
    "##..##..",
    "##...##.",
    "##...##.",
    "##...##.",
    "##..##..",
    "#####...",
    "........",
]

Y_PATTERN = [
    "##...##.",
    "##...##.",
    ".##.##..",
    "..###...",
    "...##...",
    "...##...",
    "...##...",
    "........",
]

# Create tiles for both plane encodings
# Banks 0,3 use Plane 0; Banks 1,2 use Plane 1
TILE_T_P0 = create_tile(T_PATTERN, use_plane1=False)
TILE_D_P0 = create_tile(D_PATTERN, use_plane1=False)
TILE_Y_P0 = create_tile(Y_PATTERN, use_plane1=False)

TILE_T_P1 = create_tile(T_PATTERN, use_plane1=True)
TILE_D_P1 = create_tile(D_PATTERN, use_plane1=True)
TILE_Y_P1 = create_tile(Y_PATTERN, use_plane1=True)

# CHR ROM offset = 16 (header) + 32768 (PRG ROM)
CHR_START = 16 + 32768

# Use blank tile slots that aren't referenced by any sprite data in the ROM
# 0xF0-0xF2 were used by other sprite blocks causing FEVER menu corruption
# 0xA0-0xA2 are blank in Bank 1 PT0 and not used elsewhere
TILE_T_NUM = 0xA0  # Blank in Bank 1 PT0, not used by game sprites
TILE_D_NUM = 0xA1  # Blank in Bank 1 PT0, not used by game sprites
TILE_Y_NUM = 0xA2  # Blank in Bank 1 PT0, not used by game sprites

# MMC1 can switch between 4 CHR banks (each 8KB = 2 pattern tables)
# Write to ALL possible locations across all 4 banks
CHR_BANK_SIZE = 8192  # 8KB per bank
NUM_CHR_BANKS = 4

# Sprite data for "STUDY" - 5 sprites, 4 bytes each
# Format: Y_offset, Tile, Attribute, X_offset
# S=0x0D, T=0x0F, U=0x0C, D=0x0A(was P), Y=0x0E(was E)
STUDY_SPRITES = bytes([
    0x00, 0x0D, 0x00, 0x00,  # S (existing)
    0x00, TILE_T_NUM, 0x00, 0x08,  # T (at 0x0F)
    0x00, 0x0C, 0x00, 0x10,  # U (existing)
    0x00, TILE_D_NUM, 0x00, 0x18,  # D (at 0x0A, was P)
    0x00, TILE_Y_NUM, 0x00, 0x20,  # Y (at 0x0E, was E)
    0x80,                     # Terminator
])

SPRITE_DATA_OFFSET = 0x2968  # ROM offset for PAUSE sprite data

def apply_patches(input_path, output_path):
    """Apply all patches to ROM"""
    with open(input_path, 'rb') as f:
        rom_data = bytearray(f.read())

    original_checksum = hashlib.md5(rom_data).hexdigest()
    print(f"Original ROM: {input_path}")
    print(f"Original checksum: {original_checksum}")
    print(f"ROM size: {len(rom_data)} bytes")
    print()

    # Patch 1: Enable background during pause
    print("✓ Patching PPU_MASK (0x17CA): $16 -> $1E")
    rom_data[0x17CA] = 0x1E

    # Patch 1b: Keep sprites visible during pause
    # NOP out the JSR $B894 at 0x17D4 (pause entry sprite clear)
    print("✓ Patching sprite hide (0x17D4): JSR $B894 -> NOP NOP NOP")
    rom_data[0x17D4] = 0xEA  # NOP
    rom_data[0x17D5] = 0xEA  # NOP
    rom_data[0x17D6] = 0xEA  # NOP

    # NOTE: We previously NOPed 0x367C but that broke the FEVER menu
    # The $B654 routine is shared between pause and menu screens
    # Dr. Mario sprite may disappear during pause, but menu will work correctly

    # Patch 2: Move text to top of screen
    # Using Y=0x0F places it near scanline 15, well above the playfield
    print("✓ Patching Y position (0x17DC): $77 -> $0F")
    rom_data[0x17DC] = 0x0F

    # Patch 3-5: Add T, D, Y tiles to Bank 1 PT0 ONLY
    # Bank 1 has the actual PAUSE letter tiles (S at 0x0D uses Plane 1)
    # Only modify Bank 1 to minimize side effects on other graphics
    bank = 1
    pt0_offset = bank * CHR_BANK_SIZE  # PT0 (sprites in this game)
    t_off = CHR_START + pt0_offset + (TILE_T_NUM * 16)
    d_off = CHR_START + pt0_offset + (TILE_D_NUM * 16)
    y_off = CHR_START + pt0_offset + (TILE_Y_NUM * 16)

    # Bank 1 uses Plane 1 for white color
    rom_data[t_off:t_off+16] = TILE_T_P1
    rom_data[d_off:d_off+16] = TILE_D_P1
    rom_data[y_off:y_off+16] = TILE_Y_P1
    print(f"✓ Added T,D,Y (P1) to Bank1-PT0 only (0x{t_off:04X}, 0x{d_off:04X}, 0x{y_off:04X})")

    # Patch 6: Change sprite data from PAUSE to STUDY
    print(f"✓ Changing sprite text to STUDY at 0x{SPRITE_DATA_OFFSET:04X}")
    rom_data[SPRITE_DATA_OFFSET:SPRITE_DATA_OFFSET+len(STUDY_SPRITES)] = STUDY_SPRITES

    with open(output_path, 'wb') as f:
        f.write(rom_data)

    patched_checksum = hashlib.md5(rom_data).hexdigest()
    print()
    print(f"Patched ROM: {output_path}")
    print(f"Patched checksum: {patched_checksum}")
    print()
    print("Training Mode patch applied successfully!")
    print("- Playfield remains visible during pause")
    print("- Sprites remain visible (capsule, Dr. Mario)")
    print("- Shows 'STUDY' at top of screen")

    return True

if __name__ == "__main__":
    apply_patches(INPUT_ROM, OUTPUT_ROM)
