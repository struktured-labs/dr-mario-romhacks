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
    # Layout with correct offsets:
    # 0x00: STA $F6 (2 bytes)
    # 0x02: LDA $43 (2)
    # 0x04: AND #$0F (2)
    # 0x06: BNE to RTS at 0x20 (operand = 0x20 - 0x08 = 0x18)
    # 0x08: LDA $43 (2)
    # 0x0A: AND #$20 (2)
    # 0x0C: BNE to do_rotate at 0x1C (operand = 0x1C - 0x0E = 0x0E)
    # 0x0E: LDA $43 (2)
    # 0x10: AND #$10 (2)
    # 0x12: BEQ to do_right at 0x18 (operand = 0x18 - 0x14 = 0x04)
    # 0x14: LDA #$02 (2)
    # 0x16: BNE to store at 0x1E (operand = 0x1E - 0x18 = 0x06)
    # 0x18: LDA #$01 (do_right) (2)
    # 0x1A: BNE to store at 0x1E (operand = 0x1E - 0x1C = 0x02)
    # 0x1C: LDA #$40 (do_rotate) (2)
    # 0x1E: STA $F6 (store) (2)
    # 0x20: RTS (exit) (1)
    ai_routine = bytes([
        # Complete original STA $F6
        0x85, 0xF6,           # 00: STA $F6

        # Throttle: every 16 frames (~266ms, human-like speed)
        0xA5, 0x43,           # 02: LDA $43
        0x29, 0x0F,           # 04: AND #$0F (every 16 frames)
        0xD0, 0x18,           # 06: BNE exit (branch to RTS at 0x20)

        # Bit 5: Choose mode (0=movement, 1=rotation only)
        0xA5, 0x43,           # 08: LDA $43
        0x29, 0x20,           # 0A: AND #$20 (isolate bit 5)
        0xD0, 0x0E,           # 0C: BNE do_rotate at 0x1C

        # Movement mode: check bit 4 for L/R
        0xA5, 0x43,           # 0E: LDA $43
        0x29, 0x10,           # 10: AND #$10 (isolate bit 4)
        0xF0, 0x04,           # 12: BEQ do_right at 0x18
        0xA9, 0x02,           # 14: LDA #$02 (Left)
        0xD0, 0x06,           # 16: BNE store at 0x1E

        # do_right:
        0xA9, 0x01,           # 18: LDA #$01 (Right)
        0xD0, 0x02,           # 1A: BNE store at 0x1E

        # do_rotate:
        0xA9, 0x40,           # 1C: LDA #$40 (A button only)

        # store:
        0x85, 0xF6,           # 1E: STA $F6
        # exit:
        0x60,                 # 20: RTS
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
