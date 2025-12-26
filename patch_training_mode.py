#!/usr/bin/env python3
"""
Dr. Mario Training Mode Patch
=============================
This patch modifies Dr. Mario (NES) to show the playfield during pause,
allowing players to analyze the board state while paused.

The original game sets PPU_MASK to $16 during pause which hides the background.
This patch changes it to $1E to keep the background visible.

Technical details:
- ROM offset 0x17CA: PPU_MASK value during pause
- Original: $16 (00010110) - background disabled, sprites enabled
- Patched:  $1E (00011110) - background enabled, sprites enabled
"""

import shutil
import hashlib

INPUT_ROM = "drmario.nes"
OUTPUT_ROM = "drmario_training.nes"

# Patch definitions: (offset, original_byte, patched_byte, description)
PATCHES = [
    (0x17CA, 0x16, 0x1E, "PPU_MASK during pause: enable background rendering"),
]

def calculate_checksum(data):
    """Calculate MD5 checksum of ROM data"""
    return hashlib.md5(data).hexdigest()

def apply_patches(input_path, output_path, patches):
    """Apply binary patches to ROM"""
    # Read original ROM
    with open(input_path, 'rb') as f:
        rom_data = bytearray(f.read())

    original_checksum = calculate_checksum(rom_data)
    print(f"Original ROM: {input_path}")
    print(f"Original checksum: {original_checksum}")
    print(f"ROM size: {len(rom_data)} bytes")
    print()

    # Apply each patch
    for offset, original, patched, description in patches:
        current = rom_data[offset]

        if current == original:
            print(f"✓ Patching offset 0x{offset:04X}:")
            print(f"  {description}")
            print(f"  ${original:02X} -> ${patched:02X}")
            rom_data[offset] = patched
        elif current == patched:
            print(f"! Offset 0x{offset:04X} already patched (found ${current:02X})")
        else:
            print(f"✗ ERROR at offset 0x{offset:04X}:")
            print(f"  Expected ${original:02X}, found ${current:02X}")
            print(f"  This may be a different ROM version")
            return False

    # Write patched ROM
    with open(output_path, 'wb') as f:
        f.write(rom_data)

    patched_checksum = calculate_checksum(rom_data)
    print()
    print(f"Patched ROM: {output_path}")
    print(f"Patched checksum: {patched_checksum}")
    print()
    print("Training Mode patch applied successfully!")
    print("The playfield will now remain visible during pause.")

    return True

if __name__ == "__main__":
    apply_patches(INPUT_ROM, OUTPUT_ROM, PATCHES)
