#!/usr/bin/env python3
"""Find PAUSE text in Dr. Mario ROM"""

with open('drmario.nes', 'rb') as f:
    rom = bytearray(f.read())

# NES games often encode text as tile indices
# Common encodings: ASCII-based, or custom tile mappings
# PAUSE = P A U S E

# Let's search for patterns that could be PAUSE
# If tiles are sequential A=0, B=1, etc: P=15, A=0, U=20, S=18, E=4
# If tiles are ASCII-like: P=80, A=65, U=85, S=83, E=69

# Search for "PAUSE" in various encodings
patterns = {
    "ASCII": bytes([0x50, 0x41, 0x55, 0x53, 0x45]),  # PAUSE
    "ASCII lowercase": bytes([0x70, 0x61, 0x75, 0x73, 0x65]),  # pause
    "A=0 sequential": bytes([15, 0, 20, 18, 4]),  # P A U S E
    "A=1 sequential": bytes([16, 1, 21, 19, 5]),  # P A U S E (1-indexed)
    "A=10 (0x0A)": bytes([25, 10, 30, 28, 14]),  # P A U S E
    "A=0x0A offset": bytes([0x19, 0x0A, 0x1E, 0x1C, 0x0E]),
    "A=0x21 offset": bytes([0x30, 0x21, 0x35, 0x33, 0x25]),  # Common NES
    "A=0x41 ASCII caps": bytes([0x50, 0x41, 0x55, 0x53, 0x45]),
}

print("Searching for PAUSE text patterns...\n")

for name, pattern in patterns.items():
    for i in range(len(rom) - len(pattern)):
        if rom[i:i+len(pattern)] == pattern:
            print(f"Found '{name}' at offset 0x{i:04X}")
            # Show context
            start = max(0, i-8)
            end = min(len(rom), i+len(pattern)+8)
            print(f"  Context: {rom[start:end].hex()}")
            print(f"  Bytes: {list(rom[i:i+len(pattern)])}")
            print()

# Also search for the subroutine that draws text
# From disassembly: JSR $88F6 draws the pause text
# Let's look at what's near the text drawing routine

print("\n=== Looking at text drawing routine area (around $88F6 = ROM 0x08F6+0x10) ===")
# $88F6 in CPU space, PRG starts at $8000, so offset = $88F6 - $8000 + 16 = 0x0906
offset = 0x08F6 + 0x10
print(f"Offset 0x{offset:04X}:")
print(f"  Hex: {rom[offset:offset+32].hex()}")

# Let's also check the PPU nametable update buffer setup
# Values $70, $77 stored before calling the text routine
# These might be PPU addresses - $2070 and $2077 would be in nametable 0
print("\n=== Searching for screen position values ===")
# The pause text position setup was:
# LDA #$70; STA $44; LDA #$77; STA $45
# $70 and $77 might be PPU address bytes or tile coordinates

# Let's search for data tables with text
print("\n=== Searching for potential text tables ===")
# Look for sequences that could be tile data for text
for i in range(16, len(rom) - 20):
    # Look for 5 bytes that increment roughly like alphabet tiles
    chunk = rom[i:i+5]
    # Check if it could be "PAUSE" with some base offset
    # P-A = 15, A-U = -20, U-S = 2, S-E = 14
    if len(chunk) == 5:
        diffs = [chunk[j+1] - chunk[j] for j in range(4)]
        # PAUSE diffs with A=0: [15-0, 0-20, 20-18, 18-4] = [15, -20, 2, 14] -- doesn't work simply
        pass

# Let's look for the actual tile data in CHR ROM
chr_start = 16 + 32768  # After PRG ROM
print(f"\n=== CHR ROM starts at offset 0x{chr_start:04X} ===")

# Let's search more specifically around the pause display code
print("\n=== Examining pause display code context ===")
# The pause loop at ROM 0x17D7 loads $70 into $44, $77 into $45
# These are likely pointers to text data or PPU addresses
# Let's look at memory around $70-$77 area or search for what $88F6 references

# Search for data that looks like "PAUSE" screen layout
# PPU nametable addresses: high byte first, then low byte
# Screen row ~10-12 would be around $2140-$2180 range
