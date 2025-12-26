#!/usr/bin/env python3
"""Analyze Dr. Mario NES ROM to find pause screen blackout code"""

from capstone import Cs, CS_ARCH_M68K, CS_MODE_16
import struct

# Load the ROM
with open('drmario.nes', 'rb') as f:
    rom_data = bytearray(f.read())

# NES header is 16 bytes
header = rom_data[:16]
prg_rom_size = header[4] * 16384  # PRG ROM in 16KB units
chr_rom_size = header[5] * 8192   # CHR ROM in 8KB units

print(f"PRG ROM: {prg_rom_size} bytes ({header[4]} x 16KB)")
print(f"CHR ROM: {chr_rom_size} bytes ({header[5]} x 8KB)")

# PRG ROM starts at offset 16 (after header)
prg_start = 16
prg_data = rom_data[prg_start:prg_start + prg_rom_size]

# For NES (6502), we need to manually search for patterns
# PPU Mask register is $2001
# A blackout typically involves writing $00 to $2001 (disable rendering)
# Or writing to palette RAM ($3F00-$3F1F via $2006/$2007)

# Search for patterns that write to $2001
# Common sequences:
# LDA #$00; STA $2001 = A9 00 8D 01 20
# LDA #$xx; STA $2001 = A9 xx 8D 01 20

print("\n=== Searching for PPU Mask ($2001) writes ===")
for i in range(len(prg_data) - 4):
    # STA $2001 = 8D 01 20
    if prg_data[i:i+3] == bytes([0x8D, 0x01, 0x20]):
        # Check what's loaded before
        context_start = max(0, i-10)
        context = prg_data[context_start:i+3]
        rom_addr = 0x8000 + i if prg_rom_size <= 0x8000 else 0x8000 + (i % 0x8000)
        if prg_rom_size > 0x8000:
            bank = i // 0x8000
            print(f"  Bank {bank}, ROM offset 0x{prg_start + i:04X}, CPU ~${rom_addr:04X}: STA $2001")
        else:
            print(f"  ROM offset 0x{prg_start + i:04X}, CPU ~${rom_addr:04X}: STA $2001")
        print(f"    Context (hex): {context.hex()}")
        # Look for LDA #immediate before
        for j in range(i-1, max(0, i-10), -1):
            if prg_data[j] == 0xA9:  # LDA #immediate
                val = prg_data[j+1]
                print(f"    LDA #${val:02X} at offset -{i-j}")
                break

# Search for controller reading and Start button checks
# Start button is bit 4 (0x10) when reading from $4016
print("\n=== Searching for Start button checks (pause trigger) ===")
for i in range(len(prg_data) - 2):
    # AND #$10 (check Start) = 29 10
    if prg_data[i:i+2] == bytes([0x29, 0x10]):
        rom_addr = 0x8000 + (i % 0x8000)
        print(f"  ROM offset 0x{prg_start + i:04X}: AND #$10 (Start button check?)")
    # CMP #$10 = C9 10
    if prg_data[i:i+2] == bytes([0xC9, 0x10]):
        rom_addr = 0x8000 + (i % 0x8000)
        print(f"  ROM offset 0x{prg_start + i:04X}: CMP #$10")

# Look for palette manipulation (blackout via palette)
# Writing to $2006 twice then $2007 to set palette
# $3F00 = background palette start
print("\n=== Searching for palette address setup ($3F) ===")
for i in range(len(prg_data) - 4):
    # LDA #$3F; STA $2006 = A9 3F 8D 06 20
    if prg_data[i:i+2] == bytes([0xA9, 0x3F]) and prg_data[i+2:i+5] == bytes([0x8D, 0x06, 0x20]):
        rom_addr = 0x8000 + (i % 0x8000)
        print(f"  ROM offset 0x{prg_start + i:04X}: LDA #$3F; STA $2006 (palette setup)")

# Search for common pause-related patterns
# Many games use a "game state" or "pause flag" variable
print("\n=== Looking for potential pause state handling ===")
# Search for sequences that might be pause loops (waiting for unpause)
# Typically: check button, branch back to wait
for i in range(len(prg_data) - 10):
    # JSR to NMI wait or frame wait is common during pause
    # Look for tight loops with button checks
    pass

print("\n=== ROM Statistics ===")
print(f"Total ROM size: {len(rom_data)} bytes")
print(f"PRG ROM offset: 0x{prg_start:04X}")
print(f"CHR ROM offset: 0x{prg_start + prg_rom_size:04X}")

# Let's also look at known Dr. Mario addresses from community research
# Dr. Mario (USA) known info:
# - Game uses mapper 1 (MMC1)
# - Pause handling involves screen fade

print("\n=== Searching for screen fade/blank patterns ===")
# Look for sequences that write $0F (black) repeatedly to palette
for i in range(len(prg_data) - 5):
    # LDA #$0F = A9 0F (black color in NES palette)
    if prg_data[i:i+2] == bytes([0xA9, 0x0F]):
        # Check if followed by STA $2007
        for j in range(i+2, min(i+10, len(prg_data)-3)):
            if prg_data[j:j+3] == bytes([0x8D, 0x07, 0x20]):
                print(f"  ROM offset 0x{prg_start + i:04X}: LDA #$0F ... STA $2007 (write black to PPU?)")
                break
