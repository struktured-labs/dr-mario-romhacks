#!/usr/bin/env python3
"""
Dr. Mario Training Mode Patch
=============================
This patch modifies Dr. Mario (NES) to:
1. Show the playfield during pause (no blackout)
2. Remove the PAUSE text completely (clean study view)

Technical details:
- ROM offset 0x17CA: PPU_MASK value during pause
  Original: $16 (background disabled), Patched: $1E (background enabled)

- ROM offset 0x17E3-0x17E5: JSR $88F6 (draw PAUSE text)
  Original: 20 F6 88 (JSR $88F6), Patched: EA EA EA (NOP NOP NOP)
  This disables the PAUSE text rendering entirely for a clean study view.
"""

import hashlib

INPUT_ROM = "drmario.nes"
OUTPUT_ROM = "drmario_training.nes"

# Patch definitions: (offset, original_byte, patched_byte, description)
PATCHES = [
    # Enable background during pause
    (0x17CA, 0x16, 0x1E, "PPU_MASK during pause: enable background rendering"),

    # NOP out the JSR $88F6 call that draws PAUSE text
    # JSR $88F6 = 20 F6 88 at offset 0x17E3
    (0x17E3, 0x20, 0xEA, "NOP out PAUSE text draw (byte 1/3)"),
    (0x17E4, 0xF6, 0xEA, "NOP out PAUSE text draw (byte 2/3)"),
    (0x17E5, 0x88, 0xEA, "NOP out PAUSE text draw (byte 3/3)"),
]

def calculate_checksum(data):
    """Calculate MD5 checksum of ROM data"""
    return hashlib.md5(data).hexdigest()

def apply_patches(input_path, output_path, patches):
    """Apply binary patches to ROM"""
    with open(input_path, 'rb') as f:
        rom_data = bytearray(f.read())

    original_checksum = calculate_checksum(rom_data)
    print(f"Original ROM: {input_path}")
    print(f"Original checksum: {original_checksum}")
    print(f"ROM size: {len(rom_data)} bytes")
    print()

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

    with open(output_path, 'wb') as f:
        f.write(rom_data)

    patched_checksum = calculate_checksum(rom_data)
    print()
    print(f"Patched ROM: {output_path}")
    print(f"Patched checksum: {patched_checksum}")
    print()
    print("Training Mode patch applied successfully!")
    print("- Playfield remains visible during pause")
    print("- PAUSE text removed for clean study view")

    return True

if __name__ == "__main__":
    apply_patches(INPUT_ROM, OUTPUT_ROM, PATCHES)
