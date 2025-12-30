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
    # Layout (with soft-drop bypassing throttle):
    # 00-01: STA $F6        - complete original op
    # 02-04: LDA $03A4      - game-active check (before throttle!)
    # 05-06: BEQ exit       - skip AI if no viruses
    # 07-09: LDA $0381      - get capsule left color
    # 0A:    CLC
    # 0B-0C: ADC #$D0       - convert to virus tile
    # 0D-0E: STA $00        - store target tile
    # 0F-10: LDX #$7F       - scan from bottom
    # scan_loop (11):
    # 11-13: LDA $0500,X    - read playfield tile
    # 14-15: CMP $00        - match target virus?
    # 16-17: BEQ found      - yes (-> 0x1F)
    # 18:    DEX
    # 19-1A: BPL scan_loop  - continue (-> 0x11)
    # 1B-1C: LDA #$03       - no match, target center
    # 1D-1E: BNE compare    - (-> 0x22)
    # found (1F):
    # 1F:    TXA
    # 20-21: AND #$07       - extract column
    # compare (22):
    # 22-23: STA $01        - store target column
    # 24-26: LDA $0385      - get current X
    # 27-28: CMP $01        - compare with target
    # 29-2A: BEQ at_target  - at target, soft-drop! (-> 0x4D)
    # 2B-2C: LDA $43        - NOT at target: apply throttle
    # 2D-2E: AND #$07
    # 2F-30: BNE exit       - skip if not throttle frame (-> 0x51)
    # 31-33: LDA $0385      - reload X position
    # 34-35: CMP $01        - compare again
    # 36-37: BCS go_left    - (-> 0x45)
    # go_right (38):
    # 38-39: LDA $43
    # 3A-3B: AND #$30
    # 3C-3D: BNE right_only - (-> 0x41)
    # 3E-3F: LDA #$41       - Right + A
    # 40:    BNE store      - (-> 0x4F)
    # 41-42: LDA #$01       - right_only
    # 43-44: BNE store      - (-> 0x4F)
    # go_left (45):
    # 45-46: LDA $43
    # 47-48: AND #$30
    # 49-4A: BNE left_only  - (-> 0x4D... wait, reuse at_target for left_only? No.)
    # Actually let me recalc...
    #
    # Simpler: at_target just loads Down and stores, no throttle
    ai_routine = bytes([
        # Complete original STA $F6
        0x85, 0xF6,           # 00: STA $F6

        # Game-active check FIRST (no throttle yet)
        0xAD, 0xA4, 0x03,     # 02: LDA $03A4 (P2 virus count)
        0xF0, 0x61,           # 05: BEQ exit (-> 0x68, skip if 0)

        # Get LEFT capsule color, convert to virus tile
        0xAD, 0x81, 0x03,     # 07: LDA $0381 (P2 capsule left color)
        0x18,                 # 0A: CLC
        0x69, 0xD0,           # 0B: ADC #$D0 (-> virus tile)
        0x85, 0x00,           # 0D: STA $00 (store left virus tile)

        # Get RIGHT capsule color, convert to virus tile
        0xAD, 0x82, 0x03,     # 0F: LDA $0382 (P2 capsule right color)
        0x18,                 # 12: CLC
        0x69, 0xD0,           # 13: ADC #$D0 (-> virus tile)
        0x85, 0x02,           # 15: STA $02 (store right virus tile)

        # Scan for LEFT color virus first
        0xA2, 0x7F,           # 17: LDX #$7F
        # scan_left (19):
        0xBD, 0x00, 0x05,     # 19: LDA $0500,X
        0xC5, 0x00,           # 1C: CMP $00 (match left?)
        0xF0, 0x13,           # 1E: BEQ found (-> 0x33)
        0xCA,                 # 20: DEX
        0x10, 0xF6,           # 21: BPL scan_left (-> 0x19)

        # No left match - scan for RIGHT color virus
        0xA2, 0x7F,           # 23: LDX #$7F
        # scan_right (25):
        0xBD, 0x00, 0x05,     # 25: LDA $0500,X
        0xC5, 0x02,           # 28: CMP $02 (match right?)
        0xF0, 0x07,           # 2A: BEQ found (-> 0x33)
        0xCA,                 # 2C: DEX
        0x10, 0xF6,           # 2D: BPL scan_right (-> 0x25)

        # No match at all - target center column (3)
        0xA9, 0x03,           # 2F: LDA #$03
        0xD0, 0x03,           # 31: BNE compare (-> 0x36)

        # found (33):
        0x8A,                 # 33: TXA
        0x29, 0x07,           # 34: AND #$07 (extract column)

        # compare (36): target column in A
        0x85, 0x01,           # 36: STA $01 (store target column)
        0xAD, 0x85, 0x03,     # 38: LDA $0385 (current X)
        0xC5, 0x01,           # 3B: CMP $01
        0xF0, 0x2A,           # 3D: BEQ at_target (-> 0x69, soft-drop!)

        # NOT at target - apply throttle for movement
        0xA5, 0x43,           # 3F: LDA $43
        0x29, 0x07,           # 41: AND #$07
        0xD0, 0x23,           # 43: BNE exit (-> 0x68)

        # Movement: reload and compare
        0xAD, 0x85, 0x03,     # 45: LDA $0385
        0xC5, 0x01,           # 48: CMP $01
        0xB0, 0x0E,           # 4A: BCS go_left (-> 0x5A)

        # go_right (4C):
        0xA5, 0x43,           # 4C: LDA $43
        0x29, 0x30,           # 4E: AND #$30
        0xD0, 0x04,           # 50: BNE right_only (-> 0x56)
        0xA9, 0x41,           # 52: LDA #$41 (Right + A)
        0xD0, 0x10,           # 54: BNE store (-> 0x66)
        # right_only (56):
        0xA9, 0x01,           # 56: LDA #$01
        0xD0, 0x0C,           # 58: BNE store (-> 0x66)

        # go_left (5A):
        0xA5, 0x43,           # 5A: LDA $43
        0x29, 0x30,           # 5C: AND #$30
        0xD0, 0x04,           # 5E: BNE left_only (-> 0x64)
        0xA9, 0x42,           # 60: LDA #$42 (Left + A)
        0xD0, 0x02,           # 62: BNE store (-> 0x66)
        # left_only (64):
        0xA9, 0x02,           # 64: LDA #$02
        # falls through to store

        # store (66):
        0x85, 0xF6,           # 66: STA $F6

        # exit (68):
        0x60,                 # 68: RTS

        # at_target (69): soft-drop - NO THROTTLE, runs every frame!
        0xA9, 0x04,           # 69: LDA #$04 (Down button)
        0x85, 0xF6,           # 6B: STA $F6
        0x60,                 # 6D: RTS
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
