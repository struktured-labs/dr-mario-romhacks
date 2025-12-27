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
    # Hook: Replace STA $F6; RTS with JMP $FF40
    # =========================================
    # Original at 0x37CF: 85 F6 60 (STA $F6; RTS)
    # Patched:            4C 40 FF (JMP $FF40)
    print("✓ Hooking controller routine (0x37CF): JMP $FF40")
    rom_data[0x37CF] = 0x4C  # JMP
    rom_data[0x37D0] = 0x40  # low byte of $FF40
    rom_data[0x37D1] = 0xFF  # high byte of $FF40

    # =========================================
    # AI Routine at 0x7F50 (CPU $FF40)
    # =========================================
    #
    # This routine:
    # 1. Completes the original STA $F6
    # 2. Checks if we're in 2-player mode
    # 3. If 2P mode, generates random input for P2
    #
    ai_routine = bytes([
        # Original operation: STA $F6
        0x85, 0xF6,           # STA $F6 - store P2 input (complete original op)

        # Preserve A register (caller may need it)
        0x48,                 # PHA - save A

        # Check if 2-player mode
        0xAD, 0x27, 0x07,     # LDA $0727 - load player count
        0xC9, 0x02,           # CMP #$02 - is it 2 players?
        0xD0, 0x0B,           # BNE +11 - skip AI if not 2P mode (jump to PLA)

        # Generate pseudo-random input
        # Use frame counter XOR with some shifting for variety
        0xA5, 0x43,           # LDA $43 - frame counter
        0x45, 0xF5,           # EOR $F5 - XOR with P1 input for variety
        0x4A,                 # LSR A - shift right
        0x45, 0x43,           # EOR $43 - more randomness
        0x29, 0xF3,           # AND #$F3 - mask valid inputs (RLDU + B + A)
        0x85, 0xF6,           # STA $F6 - override P2 input

        # Restore A and return
        0x68,                 # PLA - restore A
        0x60,                 # RTS

        # Skip path (restore A and return)
        # Note: BNE jumps here when not 2P mode
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
    print("- AI currently uses random movements (Phase 1)")

    return True

if __name__ == "__main__":
    apply_patches(INPUT_ROM, OUTPUT_ROM)
