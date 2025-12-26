#!/usr/bin/env python3
"""Analyze text rendering in Dr. Mario"""

import sys
sys.path.insert(0, '.')
from disasm_6502 import disasm

with open('drmario.nes', 'rb') as f:
    rom = bytearray(f.read())

prg_data = rom[16:16+32768]

# Disassemble the text drawing routine at $88F6
# $88F6 - $8000 = $08F6 in PRG
print("=== Text drawing routine at $88F6 ===\n")
offset = 0x08F6
chunk = prg_data[offset:offset+0x80]
lines = disasm(chunk, 0x88F6, 0x08F6 + 16)
for line in lines:
    print(line)

# The pause setup stores $70, $77 in $44, $45
# Let's look at what data is at those addresses as pointers
# If $44/$45 is a pointer, it points to $7770 (little endian)
# But that's RAM... Let's see if these are table indices

print("\n\n=== Looking for text/tile data tables ===")
# In NES games, text is often stored as:
# - Length byte + tile indices
# - Null-terminated tile indices
# - PPU address + tile data

# Let's look for patterns with PPU write sequences
# Common: LDA #$xx, STA $2006 (high), LDA #$xx, STA $2006 (low), then data to $2007

# Search for 5-byte sequences that could spell PAUSE
# Dr. Mario uses custom tiles - let's find the font in CHR ROM
chr_start = 16 + 32768

print("\n=== Searching PRG ROM for tile index patterns ===")
# Try many possible offsets for the letter tiles
for base in range(0, 0x60, 1):
    p = base + ord('P') - ord('A')
    a = base
    u = base + ord('U') - ord('A')
    s = base + ord('S') - ord('A')
    e = base + ord('E') - ord('A')
    pattern = bytes([p, a, u, s, e])

    for i in range(16, 16+32768):
        if rom[i:i+5] == pattern:
            print(f"Found with base={base} (0x{base:02X}) at ROM offset 0x{i:04X}")
            print(f"  Pattern: {list(pattern)}")
            ctx_start = max(16, i-4)
            ctx_end = min(len(rom), i+10)
            print(f"  Context: {list(rom[ctx_start:ctx_end])}")

# Also try reversed
print("\n=== Trying different letter orderings ===")
# Maybe tiles are numbered differently
# Let's look for any 5 distinct bytes that appear multiple times in text-like contexts

# Check the area referenced by the pause display
print("\n=== Examining pause display setup ===")
# Before JSR $88F6, the code does:
# LDA #$70, STA $44
# LDA #$77, STA $45
# LDA #$00, STA $53

# $44/$45 might be a 16-bit pointer to $7770 - but that's RAM
# OR they could be separate parameters: X pos = $70 (112), Y offset table = $77 (119)

# Let's look at what $88F6 does with $44/$45
# From the disassembly we need to trace the logic

print("\n=== Looking for PAUSE text with length prefix ===")
# Try: length(5) + PAUSE tiles
for base in range(0, 0x60):
    p = base + ord('P') - ord('A')
    a = base
    u = base + ord('U') - ord('A')
    s = base + ord('S') - ord('A')
    e = base + ord('E') - ord('A')
    pattern = bytes([5, p, a, u, s, e])

    for i in range(16, 16+32768):
        if rom[i:i+6] == pattern:
            print(f"Found length-prefixed with base={base} at ROM offset 0x{i:04X}")

# Let's look at tile $77 area reference - this might be an index into a table
print("\n=== Looking at potential text table pointers ===")
# If $77 is an index into a table of text strings...
# Common NES pattern: table at fixed address, index * 2 for 16-bit pointers

# Let's examine ROM around common text table locations
print("\n=== Hex dump of areas that might contain text data ===")
# Look at offset $7700 region and similar
for region_start in [0x1770, 0x2770, 0x3770, 0x7700]:
    if region_start < len(rom) - 32:
        print(f"\nOffset 0x{region_start:04X}:")
        print(f"  {rom[region_start:region_start+32].hex()}")
        print(f"  {list(rom[region_start:region_start+16])}")

# The values 112 ($70) and 119 ($77) stored in $44/$45
# Let's check if there's a table at $A800 area (common for data)
print("\n=== Checking $A8xx area (data tables) ===")
# $A8xx in CPU = $28xx in PRG (second 16KB bank)
offset = 0x2800
print(f"PRG offset 0x{offset:04X} (CPU $A800):")
print(f"  {rom[16+offset:16+offset+64].hex()}")
