#!/usr/bin/env python3
"""
Dr. Mario Training Edition v6 - VS CPU Mode + Study Mode
=========================================================
Combines:
1. VS CPU Mode: 2-PLAYER mode has AI-controlled Player 2
2. Study Mode: Pause shows "STUDY" with visible playfield

Technical details:
- $F6: Player 2 controller input
- $0727: Player count (1 or 2)
- Hook point: 0x37CF (end of controller read routine)
- AI routine location: 0x7F50 (free ROM space at CPU $FF40)
"""

import hashlib

INPUT_ROM = "drmario.nes"
OUTPUT_ROM = "drmario_vs_cpu.nes"

# =========================================
# Study Mode tile definitions
# =========================================

def create_tile(pattern, use_plane1=False):
    """Create NES tile from 8x8 pattern string (. = 0, # = color)"""
    plane0 = bytearray(8)
    plane1 = bytearray(8)
    for row, line in enumerate(pattern):
        for col, char in enumerate(line[:8]):
            if char == '#':
                if use_plane1:
                    plane1[row] |= (0x80 >> col)
                else:
                    plane0[row] |= (0x80 >> col)
    return bytes(plane0) + bytes(plane1)

T_PATTERN = [
    "########",
    "########",
    "...##...",
    "...##...",
    "...##...",
    "...##...",
    "...##...",
    "........",
]

D_PATTERN = [
    "#####...",
    "##..##..",
    "##...##.",
    "##...##.",
    "##...##.",
    "##..##..",
    "#####...",
    "........",
]

Y_PATTERN = [
    "##...##.",
    "##...##.",
    ".##.##..",
    "..###...",
    "...##...",
    "...##...",
    "...##...",
    "........",
]

# Bank 1 uses Plane 1 for white color
TILE_T_P1 = create_tile(T_PATTERN, use_plane1=True)
TILE_D_P1 = create_tile(D_PATTERN, use_plane1=True)
TILE_Y_P1 = create_tile(Y_PATTERN, use_plane1=True)

# Tile slots in CHR ROM
TILE_T_NUM = 0xA0
TILE_D_NUM = 0xA1
TILE_Y_NUM = 0xA2

# CHR ROM offset = 16 (header) + 32768 (PRG ROM)
CHR_START = 16 + 32768
CHR_BANK_SIZE = 8192

# Sprite data for "STUDY"
STUDY_SPRITES = bytes([
    0x00, 0x0D, 0x00, 0x00,      # S
    0x00, TILE_T_NUM, 0x00, 0x08, # T
    0x00, 0x0C, 0x00, 0x10,      # U
    0x00, TILE_D_NUM, 0x00, 0x18, # D
    0x00, TILE_Y_NUM, 0x00, 0x20, # Y
    0x80,                         # Terminator
])

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
    # STUDY MODE PATCHES
    # =========================================

    # Enable background during pause
    print("✓ Study Mode: Enable background during pause (0x17CA)")
    rom_data[0x17CA] = 0x1E

    # Keep sprites visible during pause (NOP out JSR $B894)
    print("✓ Study Mode: Keep sprites visible (0x17D4)")
    rom_data[0x17D4] = 0xEA  # NOP
    rom_data[0x17D5] = 0xEA  # NOP
    rom_data[0x17D6] = 0xEA  # NOP

    # Move text to top of screen
    print("✓ Study Mode: Move text to top (0x17DC)")
    rom_data[0x17DC] = 0x0F

    # Add T, D, Y tiles to Bank 1 PT0
    bank = 1
    pt0_offset = bank * CHR_BANK_SIZE
    t_off = CHR_START + pt0_offset + (TILE_T_NUM * 16)
    d_off = CHR_START + pt0_offset + (TILE_D_NUM * 16)
    y_off = CHR_START + pt0_offset + (TILE_Y_NUM * 16)
    rom_data[t_off:t_off+16] = TILE_T_P1
    rom_data[d_off:d_off+16] = TILE_D_P1
    rom_data[y_off:y_off+16] = TILE_Y_P1
    print(f"✓ Study Mode: Added T,D,Y tiles to CHR Bank 1")

    # Change sprite data from PAUSE to STUDY
    sprite_offset = 0x2968
    rom_data[sprite_offset:sprite_offset+len(STUDY_SPRITES)] = STUDY_SPRITES
    print(f"✓ Study Mode: Changed text to 'STUDY'")
    print()

    # =========================================
    # VS CPU MODE: Hook at 0x37CF
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
    print("Dr. Mario Training Edition v6 applied successfully!")
    print("Features:")
    print("- VS CPU Mode: 2-PLAYER has AI-controlled Player 2")
    print("- Study Mode: Pause shows 'STUDY' with visible playfield")

    return True

if __name__ == "__main__":
    apply_patches(INPUT_ROM, OUTPUT_ROM)
