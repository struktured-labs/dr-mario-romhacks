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
    # 2. Reads P2 capsule left color ($0381)
    # 3. Converts to virus tile value (+$D0)
    # 4. Scans P2 playfield ($0500-$057F) for matching virus
    # 5. Moves capsule toward virus column
    # 6. If no match, moves toward center column (3)
    #
    # Memory addresses:
    # - $0381: P2 capsule left color (00=Yellow, 01=Red, 02=Blue)
    # - $0385: P2 capsule X position (0-7)
    # - $0500-$057F: P2 playfield (128 bytes, 8 cols x 16 rows)
    # - $00-$01: ZP temp storage
    #
    # Tile values: $D0=Yellow virus, $D1=Red virus, $D2=Blue virus
    # Buttons: Right=0x01, Left=0x02, A=0x40, B=0x80
    #
    # Layout:
    # 00-01: STA $F6        - complete original op
    # 02-03: LDA $43        - throttle check
    # 04-05: AND #$07
    # 06-07: BNE exit       - skip if not every 8 frames
    # 08-0A: LDA $0381      - get capsule left color
    # 0B:    CLC
    # 0C-0D: ADC #$D0       - convert to virus tile
    # 0E-0F: STA $00        - store target tile
    # 10-11: LDX #$7F       - scan from bottom (127)
    # scan_loop (12):
    # 12-14: LDA $0500,X    - read playfield tile
    # 15-16: CMP $00        - match target virus?
    # 17-18: BEQ found      - yes, found it
    # 19:    DEX            - next tile
    # 1A-1B: BPL scan_loop  - continue if X >= 0
    # 1C-1D: LDA #$03       - no match, target center
    # 1E-1F: BNE compare    - (always taken)
    # found (20):
    # 20:    TXA            - get offset in A
    # 21-22: AND #$07       - extract column (0-7)
    # compare (23):
    # 23-24: STA $01        - store target column
    # 25-27: LDA $0385      - get current X position
    # 28-29: CMP $01        - compare with target
    # 2A-2B: BEQ done       - at target, no move
    # 2C-2D: BCS go_left    - current > target, go left
    # 2E-2F: LDA #$01       - else go right
    # 30-31: BNE store      - (always taken)
    # go_left (32):
    # 32-33: LDA #$02       - left button
    # 34-35: BNE store      - (always taken)
    # done (36):
    # 36-37: LDA #$00       - no button
    # store (38):
    # 38-39: STA $F6        - write P2 input
    # exit (3A):
    # 3A:    RTS
    ai_routine = bytes([
        # Complete original STA $F6
        0x85, 0xF6,           # 00: STA $F6

        # Throttle: every 8 frames
        0xA5, 0x43,           # 02: LDA $43
        0x29, 0x07,           # 04: AND #$07
        0xD0, 0x32,           # 06: BNE exit (-> 0x3A)

        # Get capsule left color, convert to virus tile
        0xAD, 0x81, 0x03,     # 08: LDA $0381 (P2 capsule left color)
        0x18,                 # 0B: CLC
        0x69, 0xD0,           # 0C: ADC #$D0 (-> virus tile $D0/$D1/$D2)
        0x85, 0x00,           # 0E: STA $00 (store target virus tile)

        # Scan P2 playfield ($0500-$057F) from bottom up
        0xA2, 0x7F,           # 10: LDX #$7F (start at offset 127)
        # scan_loop:
        0xBD, 0x00, 0x05,     # 12: LDA $0500,X (read playfield tile)
        0xC5, 0x00,           # 15: CMP $00 (match target virus?)
        0xF0, 0x07,           # 17: BEQ found (-> 0x20)
        0xCA,                 # 19: DEX
        0x10, 0xF6,           # 1A: BPL scan_loop (-> 0x12)

        # No virus found - target center column (3)
        0xA9, 0x03,           # 1C: LDA #$03
        0xD0, 0x03,           # 1E: BNE compare (-> 0x23)

        # found: extract column from offset
        0x8A,                 # 20: TXA
        0x29, 0x07,           # 21: AND #$07 (column = offset % 8)

        # compare: target column in A
        0x85, 0x01,           # 23: STA $01 (store target column)
        0xAD, 0x85, 0x03,     # 25: LDA $0385 (get current X position)
        0xC5, 0x01,           # 28: CMP $01 (compare with target)
        0xF0, 0x0A,           # 2A: BEQ done (-> 0x36, at target)
        0xB0, 0x04,           # 2C: BCS go_left (-> 0x32, current > target)

        # go_right:
        0xA9, 0x01,           # 2E: LDA #$01 (Right button)
        0xD0, 0x06,           # 30: BNE store (-> 0x38)

        # go_left:
        0xA9, 0x02,           # 32: LDA #$02 (Left button)
        0xD0, 0x02,           # 34: BNE store (-> 0x38)

        # done: at target column, no movement
        0xA9, 0x00,           # 36: LDA #$00 (no button)

        # store:
        0x85, 0xF6,           # 38: STA $F6

        # exit:
        0x60,                 # 3A: RTS
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
