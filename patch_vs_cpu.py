#!/usr/bin/env python3
"""
Dr. Mario VS CPU Edition v17 - Weighted Heuristic AI
=====================================================
Features:
1. VS CPU Mode: New 3rd menu option with AI-controlled Player 2
   - Menu cycles: 1 PLAYER -> 2 PLAYER -> VS CPU -> 1 PLAYER
   - Level select: P2 cursor mirrors P1's choices (level & speed)
   - AI controls P2 during gameplay in VS CPU mode
2. Study Mode: Pause shows "STUDY" with visible playfield

v17 Algorithm Changes (vs v16):
- ROM REORG: Toggle/mirror moved to 0x7F40 padding -> AI gets 124-byte window
- v16 micro-optimizations: -8 bytes (EOR, removed TAX/TXA, compact loop, etc.)
- NEW: Fat top check (rows 0+1 of target column must both be empty - height-1)
- NEW: Weighted scoring via $02 zero-page (allows multi-factor combine)
- NEW: Adjacency bonus (-1 score if virus has matching-color tile above OR right)

Technical details:
- $F5/$F7: Player 1 controller input
- $F6/$F8: Player 2 controller input
- $0727: Player mode (1=1P, 2=2P - game sees VS CPU as 2P)
- $04: VS CPU flag (0=normal, 1=VS CPU mode) - using $04 to avoid game conflicts
- Hook points:
  - 0x18E5: Menu toggle -> JSR (cycle 1->2->VS->1)
  - 0x10AE: Level select P2 input -> JSR (mirror P1 in VS mode)
  - 0x37CF: Controller read -> JMP (AI routine in VS mode)
- ROM layout v17 (all before JMPs at 0x7FE0):
  - 0x7F40: Toggle routine (was 0x7F50 in v16)
  - 0x7F5B: Level mirror routine (was 0x7F6B)
  - 0x7F64: AI routine (was 0x7F74) - 124-byte budget
  - 0x7FE0: JMP table (DO NOT MODIFY!)
- AI zero-page memory:
  - $00 = target column (0-7)
  - $01 = best score so far (255 = unset)
  - $02 = candidate score temp (new in v17, used during eval)
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
    # VS CPU MODE: Compact routines (must fit before 0x7FE0)
    # =========================================

    # Toggle routine: Cycles 1P -> 2P -> VS CPU -> 1P
    # Uses $04 for VS CPU flag (avoid $05 which game might use)
    # Logic:
    #   1P (0727=1, 04=0) -> 2P (0727=2, 04=0)
    #   2P (0727=2, 04=0) -> VS CPU (0727=2, 04=1)
    #   VS CPU (0727=2, 04=1) -> 1P (0727=1, 04=0)
    toggle_code = []
    toggle_code += [0xAD, 0x27, 0x07]  # LDA $0727
    toggle_code += [0xC9, 0x01]        # CMP #$01
    # BEQ go_2p (offset calculated later)
    go_2p_branch = len(toggle_code)
    toggle_code += [0xF0, 0x00]
    toggle_code += [0xA5, 0x04]        # LDA $04 (VS CPU flag)
    # BNE go_1p (offset calculated later)
    go_1p_branch = len(toggle_code)
    toggle_code += [0xD0, 0x00]
    toggle_code += [0xE6, 0x04]        # INC $04 (2P -> VS CPU)
    toggle_code += [0x60]              # RTS

    # go_2p: increment player count
    go_2p_pos = len(toggle_code)
    toggle_code += [0xEE, 0x27, 0x07]  # INC $0727
    # go_clear: clear VS CPU flag
    go_clear_pos = len(toggle_code)
    toggle_code += [0xA9, 0x00]        # LDA #$00
    toggle_code += [0x85, 0x04]        # STA $04
    toggle_code += [0x60]              # RTS

    # go_1p: decrement to 1P, then clear flag
    go_1p_pos = len(toggle_code)
    toggle_code += [0xCE, 0x27, 0x07]  # DEC $0727
    # BNE go_clear (2-1=1, always branches)
    toggle_code += [0xD0, (go_clear_pos - (len(toggle_code) + 2)) & 0xFF]

    # Fix branch offsets
    toggle_code[go_2p_branch + 1] = (go_2p_pos - (go_2p_branch + 2)) & 0xFF
    toggle_code[go_1p_branch + 1] = (go_1p_pos - (go_1p_branch + 2)) & 0xFF

    toggle_routine = bytes(toggle_code)

    # =========================================
    # Level Select Mirror - DISABLED
    # =========================================
    # We now handle everything in the controller hook at 0x37CF
    # This routine just does what the original code did: load P2 input
    mirror_code = []
    mirror_code += [0xA5, 0xF6]        # LDA $F6
    mirror_code += [0x85, 0x5B]        # STA $5B
    mirror_code += [0xA5, 0xF8]        # LDA $F8
    mirror_code += [0x85, 0x5C]        # STA $5C
    mirror_code += [0x60]              # RTS

    level_mirror_routine = bytes(mirror_code)

    # =========================================
    # AI Routine v17 - Weighted Heuristic AI
    # =======================================
    # Strategy (v17):
    # 1. Scan ALL P2 playfield tiles for viruses ($0500-$057F)
    # 2. For each color-matching virus, derive target column
    # 3. Compute weighted score (stored in $02 zero-page):
    #    a. Fat top check: skip candidate if row 0 OR row 1 of target col occupied
    #       (combined top-row + height-1 partition penalty)
    #    b. Base score = row number (0-15, lower row = better)
    #    c. Adjacency bonus: -1 if tile above OR right of virus has same color
    #       (sets up 3-in-a-row clears - "consecutive color" / virus adjacency)
    # 4. Select candidate with lowest score
    #
    # Memory:
    #   $00 = target column (0-7)
    #   $01 = best score so far (255 = unset)
    #   $02 = current candidate score (temp, used during eval)
    #
    # Byte budget: 124 bytes (AI window 0x7F64-0x7FDF after ROM reorg)
    ai_code = []

    ai_code += [0x85, 0xF6]        # STA $F6 (complete original store)

    # Check VS CPU mode (v17 opt: BEQ directly on $04 - saves 2 bytes)
    ai_code += [0xA5, 0x04]        # LDA $04
    ai_exit_branch = len(ai_code)
    ai_code += [0xF0, 0x00]        # BEQ exit (if $04 == 0, not VS CPU)

    # Mirror P1 input for level select
    ai_code += [0xA5, 0xF5]        # LDA $F5
    ai_code += [0x85, 0xF6]        # STA $F6

    # Check gameplay mode (>= 4)
    ai_code += [0xA5, 0x46]        # LDA $46
    ai_code += [0xC9, 0x04]        # CMP #$04
    ai_exit_branch2 = len(ai_code)
    ai_code += [0x90, 0x00]        # BCC exit

    # === SETUP ===
    ai_code += [0xA9, 0x03]        # LDA #$03
    ai_code += [0x85, 0x00]        # STA $00 (target = center, default)
    ai_code += [0xA9, 0xFF]        # LDA #$FF
    ai_code += [0x85, 0x01]        # STA $01 (best score = 255, unset)

    # Scan ALL viruses
    ai_code += [0xA0, 0x00]        # LDY #$00

    ai_scan_loop = len(ai_code)
    ai_code += [0xB9, 0x00, 0x05]  # LDA $0500,Y (P2 playfield)

    # Check if virus (0xD0-0xD2) and get color
    # v17 opt: EOR #$D0 instead of SEC ; SBC #$D0 (saves 1 byte)
    ai_code += [0x49, 0xD0]        # EOR #$D0 (virus tiles -> 0/1/2)
    ai_code += [0xC9, 0x03]        # CMP #$03
    ai_not_virus_branch = len(ai_code)
    ai_code += [0xB0, 0x00]        # BCS not_virus (if >= 3, not a virus)
    # A now contains virus color (0=yellow, 1=red, 2=blue)
    # v17 opt: no TAX (color stays in A — saves 1 byte)

    # Check left capsule match
    ai_code += [0xCD, 0x81, 0x03]  # CMP $0381 (compare color)
    ai_left_match_branch = len(ai_code)
    ai_code += [0xF0, 0x00]        # BEQ left_match

    # Check right capsule match (v17 opt: no TXA needed, A still = color)
    ai_code += [0xCD, 0x82, 0x03]  # CMP $0382 (compare color)
    ai_not_match_branch = len(ai_code)
    ai_code += [0xD0, 0x00]        # BNE not_match

    # Right match: target column = virus_col - 1
    ai_code += [0x98]              # TYA (position)
    ai_code += [0x29, 0x07]        # AND #$07 (get column)
    ai_code += [0xF0, 0x00]        # BEQ not_match (col 0 can't use col-1)
    ai_right_col0_branch = len(ai_code) - 1
    ai_code += [0xAA]              # TAX
    ai_code += [0xCA]              # DEX (column - 1)
    ai_right_eval_branch = len(ai_code)
    ai_code += [0xD0, 0x00]        # BNE eval_candidate (always taken when col-1 >= 1)
    # Note: when col was 1, DEX gives X=0, BNE doesn't take. Behavior is
    # equivalent to "use col=1 (left position) as target" because the left
    # path will recompute X from Y. Acceptable degeneracy.

    # Left match: target column = virus_col
    ai_left_match_pos = len(ai_code)
    ai_code += [0x98]              # TYA
    ai_code += [0x29, 0x07]        # AND #$07 (column in A)
    ai_code += [0xAA]              # TAX (column in X)

    # === EVALUATE CANDIDATE ===
    # X = target column, Y = virus position
    ai_eval_pos = len(ai_code)

    # v17 H1: Fat top check - rows 0 AND 1 of target col must both be empty
    # (Combined top-row partition + height-1 penalty in one AND operation)
    ai_code += [0xBD, 0x00, 0x05]  # LDA $0500,X (row 0 of target col)
    ai_code += [0x3D, 0x08, 0x05]  # AND $0508,X (AND with row 1)
    ai_code += [0xC9, 0xFF]        # CMP #$FF (both empty?)
    ai_top_occupied_branch = len(ai_code)
    ai_code += [0xD0, 0x00]        # BNE not_match (skip if either occupied)

    # v17 H2: Weighted scoring via $02 - base score = row number
    ai_code += [0x98]              # TYA
    ai_code += [0x4A]              # LSR
    ai_code += [0x4A]              # LSR
    ai_code += [0x4A]              # LSR (A = row, 0-15)
    ai_code += [0x85, 0x02]        # STA $02 (base score -> temp)

    # v17 H3: Adjacency bonus - if tile above OR right of virus shares color
    # with the virus, subtract 1 from score (sets up 3-in-a-row clears).
    # Tile above virus = $04F8 + Y (i.e. $0500 + Y - 8)
    # Tile right of virus = $0501 + Y (column wrap accepted for byte savings)
    ai_code += [0xB9, 0xF8, 0x04]  # LDA $04F8,Y (tile above virus)
    ai_code += [0xD9, 0x00, 0x05]  # CMP $0500,Y (virus tile)
    ai_adj_above_branch = len(ai_code)
    ai_code += [0xF0, 0x00]        # BEQ adj_apply (above matches)
    ai_code += [0xB9, 0x01, 0x05]  # LDA $0501,Y (tile right of virus)
    ai_code += [0xD9, 0x00, 0x05]  # CMP $0500,Y (virus tile)
    ai_adj_right_branch = len(ai_code)
    ai_code += [0xD0, 0x00]        # BNE skip_adj
    ai_adj_apply_pos = len(ai_code)
    ai_code += [0xC6, 0x02]        # DEC $02 (apply -1 bonus)
    ai_skip_adj_pos = len(ai_code)

    # Compare final score with best
    ai_code += [0xA5, 0x02]        # LDA $02 (final candidate score)
    ai_code += [0xC5, 0x01]        # CMP $01 (compare with best)
    ai_not_better_branch = len(ai_code)
    ai_code += [0xB0, 0x00]        # BCS not_better (if A >= best, skip)

    # This is better! Update best score and target
    ai_code += [0x85, 0x01]        # STA $01 (update best score)
    ai_code += [0x86, 0x00]        # STX $00 (update target column)

    # Continue scanning - v17 opt: INY + BPL replaces INY + CPY + BCC (saves 2)
    # Y goes 0..127. After INY, Y=128 (bit 7 set) -> N=1 -> BPL exits.
    ai_not_virus_pos = len(ai_code)
    ai_code += [0xC8]              # INY
    ai_scan_loop_branch = len(ai_code)
    ai_code += [0x10, 0x00]        # BPL scan_loop (continue if Y < 128)

    # === MOVEMENT LOGIC ===
    # v17 opt: shared STY $F6 tail via BNE store (saves 1 byte)
    ai_move_pos = len(ai_code)
    ai_code += [0xAD, 0x85, 0x03]  # LDA $0385 (P2 X)
    ai_code += [0xC5, 0x00]        # CMP $00 (target)
    ai_at_target_branch = len(ai_code)
    ai_code += [0xF0, 0x00]        # BEQ at_target

    # Move toward target
    ai_code += [0xA0, 0x01]        # LDY #$01 (assume right)
    ai_move_left_branch = len(ai_code)
    ai_code += [0x90, 0x00]        # BCC store_move (capsule_x < target, go right)
    ai_code += [0xC8]              # INY (Y=2 = left)
    ai_to_store_branch = len(ai_code)
    ai_code += [0xD0, 0x00]        # BNE store_move (always taken, Y=2 nonzero)

    # at_target: drop
    ai_at_target_pos = len(ai_code)
    ai_code += [0xA0, 0x04]        # LDY #$04 (Down)

    ai_store_move_pos = len(ai_code)
    ai_code += [0x84, 0xF6]        # STY $F6

    ai_exit_pos = len(ai_code)
    ai_code += [0x60]              # RTS

    # Fix branch offsets
    ai_code[ai_exit_branch + 1] = (ai_exit_pos - (ai_exit_branch + 2)) & 0xFF
    ai_code[ai_exit_branch2 + 1] = (ai_exit_pos - (ai_exit_branch2 + 2)) & 0xFF
    ai_code[ai_not_virus_branch + 1] = (ai_not_virus_pos - (ai_not_virus_branch + 2)) & 0xFF
    ai_code[ai_left_match_branch + 1] = (ai_left_match_pos - (ai_left_match_branch + 2)) & 0xFF
    ai_code[ai_not_match_branch + 1] = (ai_not_virus_pos - (ai_not_match_branch + 2)) & 0xFF
    ai_code[ai_right_col0_branch] = (ai_not_virus_pos - (ai_right_col0_branch + 1)) & 0xFF
    ai_code[ai_right_eval_branch + 1] = (ai_eval_pos - (ai_right_eval_branch + 2)) & 0xFF
    ai_code[ai_top_occupied_branch + 1] = (ai_not_virus_pos - (ai_top_occupied_branch + 2)) & 0xFF
    ai_code[ai_adj_above_branch + 1] = (ai_adj_apply_pos - (ai_adj_above_branch + 2)) & 0xFF
    ai_code[ai_adj_right_branch + 1] = (ai_skip_adj_pos - (ai_adj_right_branch + 2)) & 0xFF
    ai_code[ai_not_better_branch + 1] = (ai_not_virus_pos - (ai_not_better_branch + 2)) & 0xFF
    ai_code[ai_scan_loop_branch + 1] = (ai_scan_loop - (ai_scan_loop_branch + 2)) & 0xFF
    ai_code[ai_at_target_branch + 1] = (ai_at_target_pos - (ai_at_target_branch + 2)) & 0xFF
    ai_code[ai_move_left_branch + 1] = (ai_store_move_pos - (ai_move_left_branch + 2)) & 0xFF
    ai_code[ai_to_store_branch + 1] = (ai_store_move_pos - (ai_to_store_branch + 2)) & 0xFF

    ai_routine = bytes(ai_code)

    # =========================================
    # Calculate offsets and install everything
    # =========================================
    # v17 Layout: Toggle/Mirror moved into former 0x7F40 padding to expand AI
    # window from 108 to 124 bytes (needed for new heuristic logic).
    # Originally 0x7F40-0x7FDF was 160 bytes of unused padding (0x00/0xFF).
    toggle_offset = 0x7F40
    mirror_offset = toggle_offset + len(toggle_routine)
    ai_offset = mirror_offset + len(level_mirror_routine)
    end_offset = ai_offset + len(ai_routine)

    # Check we fit before the JMP table at 0x7FE0
    if end_offset > 0x7FE0:
        print(f"ERROR: Routines overflow into JMP table at 0x7FE0! End: 0x{end_offset:04X}")
        print(f"  Toggle: {len(toggle_routine)} bytes")
        print(f"  Mirror: {len(level_mirror_routine)} bytes")
        print(f"  AI: {len(ai_routine)} bytes")
        print(f"  Total: {len(toggle_routine) + len(level_mirror_routine) + len(ai_routine)} bytes")
        return False

    # Calculate CPU addresses (ROM offset - 0x10 + 0x8000)
    toggle_cpu = 0x8000 + (toggle_offset - 0x10)
    mirror_cpu = 0x8000 + (mirror_offset - 0x10)
    ai_cpu = 0x8000 + (ai_offset - 0x10)

    # Install routines
    print(f"✓ Installing toggle routine at 0x{toggle_offset:04X} ({len(toggle_routine)} bytes) -> CPU ${toggle_cpu:04X}")
    rom_data[toggle_offset:toggle_offset + len(toggle_routine)] = toggle_routine

    print(f"✓ Installing level mirror routine at 0x{mirror_offset:04X} ({len(level_mirror_routine)} bytes) -> CPU ${mirror_cpu:04X}")
    rom_data[mirror_offset:mirror_offset + len(level_mirror_routine)] = level_mirror_routine

    print(f"✓ Installing AI routine at 0x{ai_offset:04X} ({len(ai_routine)} bytes) -> CPU ${ai_cpu:04X}")
    rom_data[ai_offset:ai_offset + len(ai_routine)] = ai_routine

    # Install hooks
    print(f"✓ Patching menu toggle (0x18E5): JSR ${toggle_cpu:04X}")
    rom_data[0x18E5] = 0x20  # JSR
    rom_data[0x18E6] = toggle_cpu & 0xFF
    rom_data[0x18E7] = (toggle_cpu >> 8) & 0xFF
    rom_data[0x18E8:0x18ED] = bytes([0xEA] * 5)  # NOPs

    print(f"✓ Hooking level select P2 input (0x10AE): JSR ${mirror_cpu:04X}")
    rom_data[0x10AE] = 0x20  # JSR
    rom_data[0x10AF] = mirror_cpu & 0xFF
    rom_data[0x10B0] = (mirror_cpu >> 8) & 0xFF
    rom_data[0x10B1:0x10B6] = bytes([0xEA] * 5)  # NOPs

    print(f"✓ Hooking controller (0x37CF): JMP ${ai_cpu:04X}")
    rom_data[0x37CF] = 0x4C  # JMP
    rom_data[0x37D0] = ai_cpu & 0xFF
    rom_data[0x37D1] = (ai_cpu >> 8) & 0xFF

    print(f"  Total: {len(toggle_routine) + len(level_mirror_routine) + len(ai_routine)} bytes, ends at 0x{end_offset:04X}")

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
    print("Dr. Mario VS CPU Edition v17 (Weighted Heuristic AI) applied successfully!")
    print("Features:")
    print("- VS CPU Mode: New 3rd menu option with AI-controlled Player 2")
    print("  - Menu cycles: 1 PLAYER -> 2 PLAYER -> VS CPU")
    print("  - Level select: P2 cursor mirrors P1 (level & speed)")
    print("  - AI only activates during VS CPU gameplay")
    print("- v17 AI heuristics:")
    print("  - Fat top check (rows 0+1 of target column must be empty)")
    print("  - Weighted scoring (combines row + adjacency in $02)")
    print("  - Adjacency bonus (virus with same-color neighbor scores better)")
    print("- Study Mode: Pause shows 'STUDY' with visible playfield")

    return True

if __name__ == "__main__":
    apply_patches(INPUT_ROM, OUTPUT_ROM)
