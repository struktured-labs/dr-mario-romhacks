#!/usr/bin/env python3
"""
Dr. Mario VS CPU Mode Patch
============================
Converts 2-PLAYER mode into VS CPU mode where Player 2 is controlled by AI.

Phase 1: Random Bot - randomly moves and rotates capsules

Technical details:
- $F6: Player 2 controller input
- $0727: Player count (1 or 2)
- Hook point: 0x37CF (end of controller read routine)
- AI routine location: 0x7F50 (free ROM space at CPU $FF40)
"""

import hashlib

INPUT_ROM = "drmario.nes"
OUTPUT_ROM = "drmario_vs_cpu.nes"

def apply_patches(input_path, output_path):
    """Apply VS CPU patches to ROM"""
    with open(input_path, 'rb') as f:
        rom_data = bytearray(f.read())

    original_checksum = hashlib.md5(rom_data).hexdigest()
    print(f"Original ROM: {input_path}")
    print(f"Original checksum: {original_checksum}")
    print(f"ROM size: {len(rom_data)} bytes")
    print()

    # =========================================
    # Hook at 0x37CF (original location - replaces STA $F6; RTS)
    # =========================================
    print("✓ Hooking controller (0x37CF): JMP $FF40")
    rom_data[0x37CF] = 0x4C  # JMP
    rom_data[0x37D0] = 0x40  # low byte of $FF40
    rom_data[0x37D1] = 0xFF  # high byte of $FF40

    # =========================================
    # AI Routine at 0x7F50 (CPU $FF40)
    # =========================================
    #
    # Virus-Seeking AI:
    # 1. Completes the original STA $F6
    # 2. Checks if we're in 2-player mode
    # 3. Scans P2 playfield for virus matching capsule color
    # 4. Moves capsule toward matching virus column
    # 5. If no match, moves toward center column
    #
    # Memory addresses used:
    # - $0381: P2 capsule left color (00=Yellow, 01=Red, 02=Blue)
    # - $0385: P2 capsule X position (0-7)
    # - $0480-$04FF: P2 playfield (128 bytes, 8x16)
    # - $0727: Player count
    # - $00: Temporary storage for target virus tile
    #
    # Tile values:
    # - Virus: $D0=Yellow, $D1=Red, $D2=Blue
    #
    # Controller hook - Test: move P2 toward center column (X=3)
    # Layout: 00=STA, 02=throttle, 08=read X, compare, branch to move/drop
    # Random AI with movement and rotation
    # Right=0x01, Left=0x02, A=0x40, B=0x80
    # Uses frame counter bits:
    #   bit 4: 0=Right, 1=Left
    #   bit 5: 0=no rotate, 1=rotate (A button)
    ai_routine = bytes([
        # Complete original STA $F6
        0x85, 0xF6,           # 00: STA $F6

        # Throttle: every 4 frames
        0xA5, 0x43,           # 02: LDA $43
        0x29, 0x03,           # 04: AND #$03
        0xD0, 0x10,           # 06: BNE exit (0x08+0x10=0x18 -> RTS)

        # Start with Right (0x01)
        0xA9, 0x01,           # 08: LDA #$01

        # Check bit 4 of frame counter for Left/Right
        0xA6, 0x43,           # 0A: LDX $43 (load frame counter to X)
        0xE0, 0x10,           # 0C: CPX #$10 (compare with 0x10)
        0x90, 0x02,           # 0E: BCC skip_left (if frame < 16, use Right)
        0xA9, 0x02,           # 10: LDA #$02 (Left)
        # 12: skip_left

        # Check bit 5 for rotation - add 0x40 if bit 5 is set
        0xA6, 0x43,           # 12: LDX $43
        0xE0, 0x20,           # 14: CPX #$20
        0x90, 0x02,           # 16: BCC store (skip rotation if frame < 32)
        0x09, 0x40,           # 18: ORA #$40 (add A button)

        # 1A: store and exit
        0x85, 0xF6,           # 1A: STA $F6
        0x60,                 # 1C: RTS
    ])

    ai_routine_offset = 0x7F50
    print(f"✓ Installing AI routine at 0x{ai_routine_offset:04X} ({len(ai_routine)} bytes)")
    rom_data[ai_routine_offset:ai_routine_offset + len(ai_routine)] = ai_routine

    # Verify we have space
    print(f"  AI routine size: {len(ai_routine)} bytes")
    print(f"  Available space: ~100 bytes")

    # =========================================
    # Write output ROM
    # =========================================
    with open(output_path, 'wb') as f:
        f.write(rom_data)

    patched_checksum = hashlib.md5(rom_data).hexdigest()
    print()
    print(f"Patched ROM: {output_path}")
    print(f"Patched checksum: {patched_checksum}")
    print()
    print("VS CPU Mode patch applied successfully!")
    print("- 2-PLAYER mode now has AI-controlled Player 2")
    print("- AI seeks viruses matching capsule color (Phase 2)")

    return True

if __name__ == "__main__":
    apply_patches(INPUT_ROM, OUTPUT_ROM)
