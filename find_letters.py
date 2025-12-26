#!/usr/bin/env python3
"""Find letter tiles in Dr. Mario CHR ROM"""

with open('drmario.nes', 'rb') as f:
    rom = bytearray(f.read())

# CHR ROM starts after PRG ROM (16 header + 32768 PRG)
chr_start = 16 + 32768
chr_data = rom[chr_start:]

print(f"CHR ROM size: {len(chr_data)} bytes ({len(chr_data)//16} tiles)")

# Each 8x8 tile is 16 bytes (2 bit planes)
# The PAUSE tiles are 0x0A-0x0E
# Let's see if there are more letter tiles nearby

# PAUSE uses tiles 0x0A, 0x0B, 0x0C, 0x0D, 0x0E
# For STUDY we need: S, T, U, D, Y
# We already have from PAUSE:
#   S = tile 0x0D
#   U = tile 0x0C
# We need: T, D, Y

print("\n=== Examining tiles around PAUSE letters ===")
for tile_num in range(0x00, 0x20):
    offset = tile_num * 16
    tile_bytes = chr_data[offset:offset+16]
    # Print a visual representation
    print(f"\nTile 0x{tile_num:02X}:")
    for row in range(8):
        plane0 = tile_bytes[row]
        plane1 = tile_bytes[row + 8]
        line = ""
        for bit in range(7, -1, -1):
            p0 = (plane0 >> bit) & 1
            p1 = (plane1 >> bit) & 1
            pixel = p0 | (p1 << 1)
            line += [".", "#", "+", "@"][pixel]
        print(f"  {line}")

# Let's also check if there are letter tiles elsewhere
print("\n\n=== Searching for other text tiles (checking all CHR banks) ===")
# Dr. Mario has 4 CHR banks of 8KB each
for bank in range(4):
    bank_start = bank * 8192
    print(f"\n--- CHR Bank {bank} (offset 0x{chr_start + bank_start:04X}) ---")
    # Check first 32 tiles of each bank
    for tile_num in range(0x10):
        offset = bank_start + tile_num * 16
        if offset + 16 <= len(chr_data):
            tile_bytes = chr_data[offset:offset+16]
            # Check if tile has significant content
            if sum(tile_bytes) > 20:  # Non-empty tile
                print(f"Tile 0x{tile_num:02X} (bank {bank}):")
                for row in range(8):
                    plane0 = tile_bytes[row]
                    plane1 = tile_bytes[row + 8]
                    line = ""
                    for bit in range(7, -1, -1):
                        p0 = (plane0 >> bit) & 1
                        p1 = (plane1 >> bit) & 1
                        pixel = p0 | (p1 << 1)
                        line += [" ", "█", "▓", "░"][pixel]
                    print(f"  {line}")
