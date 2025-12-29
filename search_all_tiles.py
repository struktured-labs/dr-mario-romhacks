#!/usr/bin/env python3
"""Search all CHR ROM tiles for potential letters T, D, Y"""

with open('drmario.nes', 'rb') as f:
    rom = bytearray(f.read())

chr_start = 16 + 32768
chr_data = rom[chr_start:]
total_tiles = len(chr_data) // 16

print(f"Total tiles in CHR ROM: {total_tiles}")
print("\n=== Searching for letter-like tiles ===\n")

# Store tiles that look like they could be letters
candidates = []

for tile_num in range(total_tiles):
    offset = tile_num * 16
    tile_bytes = chr_data[offset:offset+16]

    # Skip empty or nearly empty tiles
    if sum(tile_bytes) < 10:
        continue

    # Render tile to string for pattern matching
    rows = []
    for row in range(8):
        plane0 = tile_bytes[row]
        plane1 = tile_bytes[row + 8]
        line = ""
        for bit in range(7, -1, -1):
            p0 = (plane0 >> bit) & 1
            p1 = (plane1 >> bit) & 1
            pixel = p0 | (p1 << 1)
            line += "X" if pixel else "."
        rows.append(line)

    # Look for T-like pattern (horizontal bar on top, vertical bar in middle)
    # Look for D-like pattern (vertical bar on left, curve on right)
    # Look for Y-like pattern (diagonal lines meeting in middle, then vertical)

    tile_str = "\n".join(rows)

    # Check for T: top row mostly filled, column 3-4 filled
    top_filled = rows[0].count('X') >= 5
    center_col = sum(1 for r in rows if r[3:5].count('X') >= 1) >= 5

    # Check for any interesting patterns
    has_content = sum(tile_bytes) > 30

    if has_content:
        candidates.append((tile_num, rows, sum(tile_bytes)))

# Print all non-trivial tiles grouped by CHR bank
print("=== Non-trivial tiles (potential letters) ===\n")
for bank in range(4):
    print(f"\n--- CHR Bank {bank} ---")
    bank_start = bank * 512  # 512 tiles per 8KB bank
    bank_end = bank_start + 512

    for tile_num, rows, weight in candidates:
        if bank_start <= tile_num < bank_end:
            local_tile = tile_num - bank_start
            print(f"\nTile 0x{tile_num:03X} (bank {bank}, local 0x{local_tile:02X}):")
            for r in rows:
                print(f"  {r}")

# Let's specifically look at the PAUSE letters and nearby tiles again
print("\n\n=== PAUSE tiles (0x0A-0x0E) and neighbors ===")
for tile_num in range(0x08, 0x20):
    offset = tile_num * 16
    tile_bytes = chr_data[offset:offset+16]
    print(f"\nTile 0x{tile_num:02X}:")
    for row in range(8):
        plane0 = tile_bytes[row]
        plane1 = tile_bytes[row + 8]
        line = ""
        for bit in range(7, -1, -1):
            p0 = (plane0 >> bit) & 1
            p1 = (plane1 >> bit) & 1
            pixel = p0 | (p1 << 1)
            line += [".", "█", "▓", "░"][pixel]
        print(f"  {line}")
