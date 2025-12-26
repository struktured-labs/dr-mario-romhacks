#!/usr/bin/env python3
"""
Create IPS patch file for Dr. Mario Training Mode
IPS format: https://zerosoft.zophar.net/ips.php
"""

def create_ips_patch(patches, output_path):
    """
    Create an IPS patch file.

    IPS format:
    - Header: "PATCH" (5 bytes)
    - Records: offset (3 bytes) + size (2 bytes) + data (size bytes)
    - Footer: "EOF" (3 bytes)
    """
    ips_data = bytearray()

    # Header
    ips_data.extend(b'PATCH')

    # Records
    for offset, original, patched, description in patches:
        # Offset: 3 bytes, big-endian
        ips_data.append((offset >> 16) & 0xFF)
        ips_data.append((offset >> 8) & 0xFF)
        ips_data.append(offset & 0xFF)

        # Size: 2 bytes, big-endian (just 1 byte for our patch)
        ips_data.append(0x00)
        ips_data.append(0x01)

        # Data
        ips_data.append(patched)

    # Footer
    ips_data.extend(b'EOF')

    with open(output_path, 'wb') as f:
        f.write(ips_data)

    print(f"Created IPS patch: {output_path}")
    print(f"Size: {len(ips_data)} bytes")

# Same patches as the main script
PATCHES = [
    (0x17CA, 0x16, 0x1E, "PPU_MASK during pause: enable background rendering"),
    (0x17E3, 0x20, 0xEA, "NOP out PAUSE text draw (byte 1/3)"),
    (0x17E4, 0xF6, 0xEA, "NOP out PAUSE text draw (byte 2/3)"),
    (0x17E5, 0x88, 0xEA, "NOP out PAUSE text draw (byte 3/3)"),
]

if __name__ == "__main__":
    create_ips_patch(PATCHES, "drmario_training.ips")
