#!/usr/bin/env python3
"""Find PAUSE sprite data in Dr. Mario"""

with open('drmario.nes', 'rb') as f:
    rom = bytearray(f.read())

# The text routine at $88F6:
# - Uses $53 as index (pause uses $53 = 0)
# - Reads 16-bit pointer from $A8C2 + ($53 * 2)
# - $A8C2 = PRG offset $28C2, ROM offset $28D2

# First, find the pointer table
ptr_table_rom = 0x28C2 + 16  # $A8C2 in ROM
print(f"=== Pointer table at $A8C2 (ROM 0x{ptr_table_rom:04X}) ===")
print(f"First 32 bytes: {rom[ptr_table_rom:ptr_table_rom+32].hex()}")

# Read the first pointer (for $53 = 0, which is PAUSE)
ptr_lo = rom[ptr_table_rom]
ptr_hi = rom[ptr_table_rom + 1]
pause_data_cpu = ptr_lo | (ptr_hi << 8)
print(f"\nPAUSE data pointer (entry 0): ${pause_data_cpu:04X}")

# Convert CPU address to ROM offset
# CPU $8000-$FFFF = PRG ROM
pause_data_prg = pause_data_cpu - 0x8000
pause_data_rom = pause_data_prg + 16
print(f"PAUSE data ROM offset: 0x{pause_data_rom:04X}")

print(f"\n=== PAUSE sprite data ===")
# The routine reads 4 bytes per sprite: Y, tile, attr, X (relative)
# Until it hits $80 as terminator
data = rom[pause_data_rom:pause_data_rom+64]
print(f"Raw: {data[:32].hex()}")

i = 0
sprites = []
while i < len(data) - 3:
    y_off = data[i]
    if y_off == 0x80:
        print(f"Terminator at offset {i}")
        break
    tile = data[i+1]
    attr = data[i+2]
    x_off = data[i+3]
    sprites.append((y_off, tile, attr, x_off))
    print(f"Sprite {len(sprites)}: Y_off=0x{y_off:02X}, Tile=0x{tile:02X}, Attr=0x{attr:02X}, X_off=0x{x_off:02X}")
    i += 4

print(f"\nTotal sprites: {len(sprites)}")
print(f"Tile numbers used: {[hex(s[1]) for s in sprites]}")

# The tiles are the letter graphics
# We need to either:
# 1. Change the tile numbers to spell STUDY
# 2. Or NOP out the JSR to the text drawing routine

print("\n=== To disable PAUSE text, we can NOP the JSR $88F6 call ===")
# The call is at ROM offset 0x17E3 (JSR $88F6 = 20 F6 88)
print("JSR $88F6 at ROM offset 0x17E3: change '20 F6 88' to 'EA EA EA' (3 NOPs)")

print("\n=== Or to change text to STUDY ===")
print("Need to find tiles for S, T, U, D, Y and update the sprite data")

# Let's check what tiles exist by looking at nearby text data
print("\n=== Checking other text entries in pointer table ===")
for entry in range(0, 16, 2):
    ptr_lo = rom[ptr_table_rom + entry]
    ptr_hi = rom[ptr_table_rom + entry + 1]
    ptr = ptr_lo | (ptr_hi << 8)
    if ptr >= 0x8000 and ptr < 0x10000:
        rom_off = ptr - 0x8000 + 16
        print(f"Entry {entry//2}: ${ptr:04X} -> ROM 0x{rom_off:04X}: {rom[rom_off:rom_off+20].hex()}")
