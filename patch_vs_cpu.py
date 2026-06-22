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


# =====================================================================
# v18 - Depth-1 Simulation AI (real line-of-4 clear detection)
# =====================================================================
# v18 is the first version that ACTUALLY simulates each placement and
# detects immediate row/column-of-4 clears at the resting position,
# instead of guessing via color-adjacency like v17.
#
# Algorithm (depth-1, no gravity cascade):
#   best = -inf ; best_col = 3 (center default)
#   for orient in {vertical, horizontal}:
#     for col in valid columns:
#       find landing row(s) for this column/orient   (real drop)
#       write the 2 capsule cells into the P2 board   (in-place)
#       count cells + viruses in any row/col run >= 4 through them
#       restore the 2 cells                           (undo)
#       score = viruses*BIG + cells*CELL - height_penalty
#       if score > best: best = score, best_col = col
#   move toward best_col (reuse v17-style movement)
#
# Tile/color model (from rl-training-new/src/heuristics.py, validated vs ROM):
#   empty           = 0xFF
#   virus  color k  = 0xD0 + k          (k = 0 yellow, 1 red, 2 blue)
#   capsule color k = 0x4C + k          (settled half)
#   color(tile)     = tile & 0x03       (empty 0xFF -> 3, never a real color)
# Two occupied cells share a color iff (a&3)==(b&3) with both occupied; since
# empty maps to 3 and colors map to 0/1/2, equal low-2-bits already excludes
# empties. This is what makes clear detection cheap on the 6502.
#
# Placement colors: A (left/top) = $0381, B (right/bottom) = $0382. We write
# them as 0x4C|color settled-capsule tiles into the SCRATCH (the live $0500
# board, with undo) so the run scan treats them like any other colored cell.
#
# ROM layout (v18): the routine lives in the large free padding block at
#   ROM 0x7B10..0x7D10  ->  CPU $FB00..$FD00   (512 bytes, was 0x00/0xFF fill)
# v17's toggle/mirror/AI at 0x7F40-0x7FE0 are kept INTACT; only the 0x37CF
# controller hook is repointed from the v17 AI ($FF54) to the v18 AI ($FB00).
#
# RAM: simulation is done IN-PLACE on the real P2 board $0500-$057F with undo,
# so no separate scratch page is needed (zero RAM-conflict risk). The unused
# RAM windows $0480-$04FF and $0580-$05FF are documented as where a
# copy-the-board variant could live. Zero-page temps use only bytes the game
# never touches (verified by static scan): $6B-$6F and $CA-$D4. v18 keeps the
# v17 convention $00 = target column, $01 = best score.

# --- Opcode table (subset used by v18) ---
OPS = {
    "BRK": 0x00,
    "ORA_imm": 0x09, "ORA_zp": 0x05,
    "ASL_A": 0x0A,
    "CLC": 0x18, "SEC": 0x38,
    "AND_imm": 0x29, "AND_zp": 0x25,
    "JMP": 0x4C, "JSR": 0x20, "RTS": 0x60,
    "EOR_imm": 0x49,
    "LSR_A": 0x4A,
    "ADC_imm": 0x69, "ADC_zp": 0x65,
    "SBC_imm": 0xE9, "SBC_zp": 0xE5,
    "STA_zp": 0x85, "STA_abs": 0x8D, "STA_absX": 0x9D, "STA_absY": 0x99,
    "STX_zp": 0x86, "STY_zp": 0x84,
    "LDY_imm": 0xA0, "LDX_imm": 0xA2, "LDA_imm": 0xA9,
    "LDA_zp": 0xA5, "LDX_zp": 0xA6, "LDY_zp": 0xA4,
    "LDA_abs": 0xAD, "LDA_absX": 0xBD, "LDA_absY": 0xB9,
    "LDX_abs": 0xAE, "LDY_abs": 0xAC,
    "TAY": 0xA8, "TYA": 0x98, "TAX": 0xAA, "TXA": 0x8A,
    "TXY": 0x9B,  # not standard; unused
    "CMP_imm": 0xC9, "CMP_zp": 0xC5, "CMP_abs": 0xCD,
    "CMP_absX": 0xDD, "CMP_absY": 0xD9,
    "CPX_imm": 0xE0, "CPY_imm": 0xC0, "CPX_zp": 0xE4, "CPY_zp": 0xC4,
    "INC_zp": 0xE6, "DEC_zp": 0xC6, "INC_abs": 0xEE, "DEC_abs": 0xCE,
    "INX": 0xE8, "DEX": 0xCA, "INY": 0xC8, "DEY": 0x88,
    "PHA": 0x48, "PLA": 0x68,
    "NOP": 0xEA,
}
BRANCHES = {"BPL": 0x10, "BMI": 0x30, "BCC": 0x90, "BCS": 0xB0,
            "BNE": 0xD0, "BEQ": 0xF0, "BVC": 0x50, "BVS": 0x70}


class Asm6502:
    """Tiny two-pass label assembler for the v18 routine.

    Usage: a.label('foo'); a.ins('LDA_imm', 0x03); a.br('BNE','foo'); ...
    Branch targets are resolved in a second pass so forward references work.
    Absolute JMP/JSR may target either internal labels (resolved to base+addr)
    or raw CPU addresses (ints)."""

    def __init__(self, base_cpu):
        self.base = base_cpu
        self.code = bytearray()
        self.labels = {}
        self.fixups = []  # (pos, kind, target) kind in {'rel','abs'}

    def label(self, name):
        assert name not in self.labels, f"dup label {name}"
        self.labels[name] = len(self.code)

    def ins(self, mnem, *operands):
        self.code.append(OPS[mnem])
        for op in operands:
            self.code.append(op & 0xFF)

    def ins16(self, mnem, value):
        """Emit an instruction with a 16-bit little-endian operand (lo,hi)."""
        self.code.append(OPS[mnem])
        self.code.append(value & 0xFF)
        self.code.append((value >> 8) & 0xFF)

    def br(self, mnem, target):
        self.code.append(BRANCHES[mnem])
        self.fixups.append((len(self.code), "rel", target))
        self.code.append(0x00)

    def jmp(self, target, mnem="JMP"):
        self.code.append(OPS[mnem])
        self.fixups.append((len(self.code), "abs", target))
        self.code.append(0x00)
        self.code.append(0x00)

    def jsr(self, target):
        """JSR to an internal label (or raw CPU address), resolved in pass 2."""
        self.code.append(OPS["JSR"])
        self.fixups.append((len(self.code), "abs", target))
        self.code.append(0x00)
        self.code.append(0x00)

    def raw(self, *bytes_):
        for b in bytes_:
            self.code.append(b & 0xFF)

    def assemble(self):
        for pos, kind, target in self.fixups:
            if kind == "rel":
                dest = self.labels[target]
                rel = dest - (pos + 1)
                assert -128 <= rel <= 127, f"branch out of range to {target} ({rel})"
                self.code[pos] = rel & 0xFF
            else:  # abs
                if isinstance(target, str):
                    dest_cpu = self.base + self.labels[target]
                else:
                    dest_cpu = target
                self.code[pos] = dest_cpu & 0xFF
                self.code[pos + 1] = (dest_cpu >> 8) & 0xFF
        return bytes(self.code)


# v18 zero-page temp map (only bytes the game never touches)
Z_TARGET = 0x00   # best target column (v17-compatible)
Z_BEST = 0x01     # best score (signed; init 0x80 = -128 sentinel)
Z_COL = 0x6B      # current column under evaluation
Z_OFFA = 0x6D     # board offset (0-127) of placed cell A
Z_OFFB = 0x6E     # board offset of placed cell B
Z_HIROW = 0x6F    # row of the higher placed cell (for height penalty)
Z_CELLS = 0xCA    # cells cleared (this placement)
Z_VIR = 0xCB      # viruses cleared (this placement)
Z_SCORE = 0xCC    # candidate score
Z_RUNLEN = 0xCD   # run length during a scan
Z_MCOLOR = 0xCE   # color (low 2 bits) being matched in a scan
Z_SOFF = 0xCF     # working offset during a scan
Z_TILEA = 0xD2    # tile byte to place for cell A
Z_TILEB = 0xD3    # tile byte to place for cell B
Z_CELLOFF = 0xD4  # offset of the cell whose row/col we are scanning
Z_STEP = 0xD6     # scan step (1 = row, 8 = column)
Z_MIN = 0xD7      # lowest valid offset for the current axis scan
Z_MAX = 0xD8      # highest valid offset for the current axis scan
Z_ORIENT = 0xD9   # current placement orientation (0 = horizontal, 1 = vertical)
Z_RUNVIR = 0xDB   # scan_run's virus-count temp (must NOT alias Z_OFFA!)

# Compact score weights (see score_update): score = min(vir,3)*VIR_W + cells*CELL_W
# + height. Kept small so a single virus (>= VIR_W) dominates any non-clear
# (height <= 15) and the byte never overflows (max 3*32 + 8*2 + 15 = 127).
VIR_W = 32
CELL_W = 2


def build_v18_ai(ai_cpu):
    """Emit the v18 depth-1 simulation AI. Returns bytes. ai_cpu = CPU load addr.

    Subroutines (internal, called via JSR):
      land_col   : input Z_COL = column. Sets carry=0 and Z_OFFB=bottom offset,
                   Z_HIROW=row, A=top-occupied row; carry=1 if column unusable.
      clear_cell : input Z_CELLOFF = board offset of a placed cell. Adds the
                   cells/viruses cleared via its row-run and col-run (>=4) into
                   Z_CELLS / Z_VIR. (Counts the through-cell once per axis that
                   clears; double counting across axes is acceptable and rare.)
    """
    a = Asm6502(ai_cpu)

    # ---- plumbing (identical contract to v17) ----
    a.ins("STA_zp", 0xF6)            # STA $F6 (finish original store)
    a.ins("LDA_zp", 0x04)           # LDA $04 (VS CPU flag)
    a.br("BNE", "vs_active")
    a.jmp("exit")                    # not VS CPU -> just return
    a.label("vs_active")
    a.ins("LDA_zp", 0xF5)           # mirror P1 input for level select
    a.ins("STA_zp", 0xF6)
    a.ins("LDA_zp", 0x46)           # LDA $46 (game mode)
    a.ins("CMP_imm", 0x04)
    a.br("BCS", "gameplay")
    a.jmp("exit")                    # menu/level select -> done (already mirrored)
    a.label("gameplay")

    # ---- setup search ----
    a.ins("LDA_imm", 0x03)
    a.ins("STA_zp", Z_TARGET)        # default target = center col 3
    a.ins("LDA_imm", 0x00)
    a.ins("STA_zp", Z_BEST)          # best score = 0 (all scores are >= 0)
    # build placement tiles 0x4C|color from $0381/$0382
    a.ins("LDA_abs", 0x81, 0x03)     # LDA $0381 (color A)
    a.ins("ORA_imm", 0x4C)
    a.ins("STA_zp", Z_TILEA)
    a.ins("LDA_abs", 0x82, 0x03)     # LDA $0382 (color B)
    a.ins("ORA_imm", 0x4C)
    a.ins("STA_zp", Z_TILEB)

    # ==================== VERTICAL pass: col 0..7 ====================
    a.ins("LDA_imm", 0x00)
    a.ins("STA_zp", Z_COL)
    a.label("v_loop")
    a.ins("LDX_zp", Z_COL)
    a.jsr("land_col")
    a.br("BCS", "v_next")            # column unusable -> skip
    # vertical needs a cell ABOVE the bottom: top = bottom-8, require row>=1.
    # land_col returns A = top-occupied row (>=1 guaranteed when carry clear and
    # there is room for one). For vertical we need two empty rows: ensure the
    # landing row (Z_HIROW) >= 1 so top = bottom-8 is on the board.
    a.ins("LDA_zp", Z_HIROW)         # landing row (bottom cell row)
    a.br("BNE", "v_haveroom")        # row 0 means only 1 empty row -> no vertical
    a.jmp("v_next")
    a.label("v_haveroom")
    # offsets: bottom = Z_OFFB (set by land_col), top = bottom - 8
    a.ins("LDA_zp", Z_OFFB)
    a.ins("SEC")
    a.ins("SBC_imm", 0x08)
    a.ins("STA_zp", Z_OFFA)          # top cell offset
    # higher cell row = Z_HIROW - 1 (top is one row above bottom)
    a.ins("DEC_zp", Z_HIROW)
    # place A/B, detect clears, undo, and update best (shared)
    a.ins("LDA_imm", 0x01); a.ins("STA_zp", Z_ORIENT)   # vertical
    a.jsr("eval_pair")
    a.label("v_next")
    a.ins("INC_zp", Z_COL)
    a.ins("LDA_zp", Z_COL)
    a.ins("CMP_imm", 0x08)
    a.br("BCS", "h_start")
    a.jmp("v_loop")

    # ==================== HORIZONTAL pass: col 0..6 ====================
    a.label("h_start")
    a.ins("LDA_imm", 0x00)
    a.ins("STA_zp", Z_COL)
    a.label("h_loop")
    # landing row = min(top_occ(col), top_occ(col+1)) - 1 ; both >=1 not required
    a.ins("LDX_zp", Z_COL)
    a.jsr("land_col")
    a.br("BCS", "h_next")
    a.ins("LDA_zp", Z_OFFB)          # offset for landing in left col
    a.ins("STA_zp", Z_OFFA)          # cell A (left)
    a.ins("LDA_zp", Z_HIROW)         # remember left landing row
    a.ins("PHA")
    # right column
    a.ins("INC_zp", Z_COL)
    a.ins("LDX_zp", Z_COL)
    a.jsr("land_col")
    a.ins("DEC_zp", Z_COL)           # restore col to left (carry preserved? no)
    a.br("BCS", "h_next_pull")       # right col unusable -> skip (pull stack first)
    # choose the higher landing row (smaller row index) of the two columns
    a.ins("PLA")                     # A = left landing row
    a.ins("CMP_zp", Z_HIROW)         # compare with right landing row
    a.br("BCC", "h_use_left")        # left row < right row -> left is higher
    # right row is higher (smaller) or equal: use right landing (Z_OFFB/Z_HIROW)
    # recompute both offsets at the right (higher) row:
    a.ins("LDA_zp", Z_HIROW)         # right row = higher row
    a.jmp("h_setrow")
    a.label("h_use_left")
    # left row is higher; A already = left row from PLA
    a.label("h_setrow")
    a.ins("STA_zp", Z_HIROW)         # Z_HIROW = chosen (higher) row
    # offsetA = row*8 + col ; offsetB = offsetA + 1
    a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A")  # A = row*8
    a.ins("CLC")
    a.ins("ADC_zp", Z_COL)
    a.ins("STA_zp", Z_OFFA)
    a.ins("CLC")
    a.ins("ADC_imm", 0x01)
    a.ins("STA_zp", Z_OFFB)
    # place A/B, detect clears, undo, and update best (shared)
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", Z_ORIENT)   # horizontal
    a.jsr("eval_pair")
    a.jmp("h_next")
    a.label("h_next_pull")
    a.ins("PLA")                     # discard saved left row, then fall through
    a.label("h_next")
    a.ins("INC_zp", Z_COL)
    a.ins("LDA_zp", Z_COL)
    a.ins("CMP_imm", 0x07)
    a.br("BCS", "move")
    a.jmp("h_loop")

    # ==================== MOVEMENT (toward best col) ====================
    a.label("move")
    a.ins("LDA_abs", 0x85, 0x03)     # LDA $0385 (P2 capsule X)
    a.ins("CMP_zp", Z_TARGET)
    a.br("BEQ", "at_target")
    a.ins("LDY_imm", 0x01)           # assume Right
    a.br("BCC", "store_move")        # capX < target -> move right
    a.ins("LDY_imm", 0x02)           # else Left
    a.jmp("store_move")
    a.label("at_target")
    a.ins("LDY_imm", 0x04)           # Down (drop)
    a.label("store_move")
    a.ins("STY_zp", 0xF6)
    a.label("exit")
    a.ins("RTS")

    # ==================== SUBROUTINE: eval_pair ====================
    # input Z_OFFA, Z_OFFB = the two cell offsets to place; Z_HIROW = row of the
    # higher cell (for height penalty); Z_TILEA/Z_TILEB = tiles to write;
    # Z_ORIENT = 0 horizontal (cells share a ROW), 1 vertical (share a COLUMN).
    # Places both cells, counts clears, restores both to empty, then scores.
    #
    # Orientation-aware scanning avoids double-counting the SHARED axis:
    #   vertical   -> column run once (through A; spans A and B) + row run of A
    #                 + row run of B.
    #   horizontal -> row run once (through A; spans A and B) + col run of A
    #                 + col run of B.
    # (A residual cross-axis double count of a single cell that sits in BOTH a
    # row-of-4 and a column-of-4 is possible and accepted; see V18_AI_NOTES.)
    a.label("eval_pair")
    a.ins("LDX_zp", Z_OFFA)
    a.ins("LDA_zp", Z_TILEA)
    a.ins16("STA_absX", 0x0500)
    a.ins("LDX_zp", Z_OFFB)
    a.ins("LDA_zp", Z_TILEB)
    a.ins16("STA_absX", 0x0500)
    a.ins("LDA_imm", 0x00)
    a.ins("STA_zp", Z_CELLS)
    a.ins("STA_zp", Z_VIR)
    # decide shared vs perpendicular axes from orientation
    a.ins("LDA_zp", Z_ORIENT)
    a.br("BNE", "ep_vert")
    # ---- horizontal: shared = row(A); perpendicular = col(A), col(B) ----
    a.ins("LDA_zp", Z_OFFA); a.ins("STA_zp", Z_CELLOFF)
    a.jsr("scan_cell_row")               # shared row (spans A & B) once
    a.ins("LDA_zp", Z_OFFA); a.ins("STA_zp", Z_CELLOFF)
    a.jsr("scan_cell_col")               # A's column
    a.ins("LDA_zp", Z_OFFB); a.ins("STA_zp", Z_CELLOFF)
    a.jsr("scan_cell_col")               # B's column
    a.jmp("ep_undo")
    a.label("ep_vert")
    # ---- vertical: shared = col(A); perpendicular = row(A), row(B) ----
    a.ins("LDA_zp", Z_OFFA); a.ins("STA_zp", Z_CELLOFF)
    a.jsr("scan_cell_col")               # shared column (spans A & B) once
    a.ins("LDA_zp", Z_OFFA); a.ins("STA_zp", Z_CELLOFF)
    a.jsr("scan_cell_row")               # A's row
    a.ins("LDA_zp", Z_OFFB); a.ins("STA_zp", Z_CELLOFF)
    a.jsr("scan_cell_row")               # B's row
    a.label("ep_undo")
    a.ins("LDA_imm", 0xFF)            # A=$FF preserved across LDX/STA below
    a.ins("LDX_zp", Z_OFFA)
    a.ins16("STA_absX", 0x0500)
    a.ins("LDX_zp", Z_OFFB)
    a.ins16("STA_absX", 0x0500)
    a.jsr("score_update")
    a.ins("RTS")

    # ==================== SUBROUTINE: land_col ====================
    # input  X = column (0-7)
    # output carry CLEAR + Z_OFFB = bottom (landing) offset, Z_HIROW = landing
    #        row, A = landing row ; carry SET if column has no empty cell.
    # scans rows 0..15 of column X for first occupied; landing is the row above.
    a.label("land_col")
    a.ins("STX_zp", Z_SOFF)          # save column in Z_SOFF (reuse as col)
    a.ins("TXA")                     # A = column = offset of row 0
    a.ins("TAY")                     # Y walks down the column by +8
    a.label("lc_scan")
    a.ins16("LDA_absY", 0x0500)      # LDA $0500,Y
    a.ins("CMP_imm", 0xFF)
    a.br("BNE", "lc_hit")            # occupied -> landing is one row up
    # still empty: advance Y by 8; if Y >= 128 we've fallen off the bottom and
    # treat Y=col+128 as a virtual "hit" at the floor -> lands at row 15.
    a.ins("TYA")
    a.ins("CLC")
    a.ins("ADC_imm", 0x08)
    a.ins("TAY")
    a.ins("CPY_imm", 0x80)           # past bottom?
    a.br("BCC", "lc_scan")
    # fall through to lc_hit with Y = col+128 (a fully empty column): landing
    # offset = Y-8 = col+120 (row 15), which is exactly what lc_hit computes.
    a.label("lc_hit")
    # Y points at first occupied cell (or col+128 = virtual floor). landing
    # offset = Y - 8 ; if Y < 8 the very top row is occupied -> unusable.
    a.ins("TYA")
    a.ins("CMP_imm", 0x08)
    a.br("BCS", "lc_ok")
    a.ins("SEC")                     # top row occupied -> fail
    a.ins("RTS")
    a.label("lc_ok")
    a.ins("SEC")
    a.ins("SBC_imm", 0x08)           # offset of empty cell above
    a.ins("STA_zp", Z_OFFB)
    # landing row = offset / 8
    a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A")
    a.ins("STA_zp", Z_HIROW)
    a.ins("CLC")                     # success
    a.ins("RTS")

    # ==================== SUBROUTINE: clear_cell ====================
    # input Z_CELLOFF = offset of a placed cell. Scans the run THROUGH that cell
    # along its ROW and its COLUMN; if a run length is >= 4 it adds the run's
    # cells to Z_CELLS and its virus cells to Z_VIR. (Tested primitive; eval_pair
    # calls scan_cell_row/scan_cell_col directly for orientation-aware accounting,
    # but clear_cell remains a clean 'both axes through this cell' entry point.)
    a.label("clear_cell")
    a.jsr("scan_cell_row")
    a.jsr("scan_cell_col")
    a.ins("RTS")

    # scan_cell_row: set up ROW axis (step 1, bounds [rowstart, rowstart+7]) then
    # run the shared color-setup + scan tail at sr_setcolor.
    a.label("scan_cell_row")
    a.ins("LDA_imm", 0x01)
    a.ins("STA_zp", Z_STEP)
    a.ins("LDA_zp", Z_CELLOFF)
    a.ins("AND_imm", 0xF8)
    a.ins("STA_zp", Z_MIN)
    a.ins("CLC"); a.ins("ADC_imm", 0x07); a.ins("STA_zp", Z_MAX)
    a.jmp("sr_setcolor")

    # scan_cell_col: set up COLUMN axis (step 8, bounds [col, col+120]) then fall
    # through to the shared sr_setcolor tail.
    a.label("scan_cell_col")
    a.ins("LDA_imm", 0x08)
    a.ins("STA_zp", Z_STEP)
    a.ins("LDA_zp", Z_CELLOFF)
    a.ins("AND_imm", 0x07)
    a.ins("STA_zp", Z_MIN)
    a.ins("CLC"); a.ins("ADC_imm", 120); a.ins("STA_zp", Z_MAX)
    a.label("sr_setcolor")            # shared tail: read color, scan, return
    a.ins("LDX_zp", Z_CELLOFF)
    a.ins16("LDA_absX", 0x0500)
    a.ins("AND_imm", 0x03)
    a.ins("STA_zp", Z_MCOLOR)
    a.jsr("scan_run")
    a.ins("RTS")

    # ==================== SUBROUTINE: scan_run ====================
    # Finds the contiguous same-color (Z_MCOLOR) run THROUGH cell Z_CELLOFF,
    # walking by +/- Z_STEP within [Z_MIN, Z_MAX]. If length >= 4, adds length
    # to Z_CELLS and the run's virus count to Z_VIR.
    #   Z_SOFF   = walking offset
    #   Z_RUNLEN = run length
    #   Z_RUNVIR = run virus count (separate temp; must NOT alias Z_OFFA, which
    #              callers rely on across consecutive scans of the same cell)
    a.label("scan_run")
    # walk backward to the run start
    a.ins("LDA_zp", Z_CELLOFF)
    a.ins("STA_zp", Z_SOFF)
    a.label("sr_back")
    a.ins("LDA_zp", Z_SOFF)
    a.ins("SEC"); a.ins("SBC_zp", Z_STEP)   # candidate previous offset
    a.ins("CMP_zp", Z_MIN)
    a.br("BCC", "sr_backdone")               # below min -> stop
    a.ins("TAX")                             # X = candidate offset
    a.ins16("LDA_absX", 0x0500)
    a.ins("CMP_imm", 0xFF)
    a.br("BEQ", "sr_backdone")               # empty -> stop
    a.ins("AND_imm", 0x03)
    a.ins("CMP_zp", Z_MCOLOR)
    a.br("BNE", "sr_backdone")               # different color -> stop
    a.ins("STX_zp", Z_SOFF)                  # accept; keep walking back
    a.jmp("sr_back")
    a.label("sr_backdone")
    # Z_SOFF = run start. walk forward counting length + viruses.
    a.ins("LDA_imm", 0x00)
    a.ins("STA_zp", Z_RUNLEN)
    a.ins("STA_zp", Z_RUNVIR)
    a.label("sr_fwd")
    a.ins("LDX_zp", Z_SOFF)
    a.ins16("LDA_absX", 0x0500)
    a.ins("CMP_imm", 0xFF)
    a.br("BEQ", "sr_commit")                 # empty -> run ends
    a.ins("AND_imm", 0x03)
    a.ins("CMP_zp", Z_MCOLOR)
    a.br("BNE", "sr_commit")                 # color change -> run ends
    a.ins("INC_zp", Z_RUNLEN)
    a.ins16("LDA_absX", 0x0500)
    a.ins("CMP_imm", 0xD0)                   # virus tile? (>= 0xD0)
    a.br("BCC", "sr_novir")
    a.ins("INC_zp", Z_RUNVIR)
    a.label("sr_novir")
    # advance offset by step; stop if it would exceed max
    a.ins("LDA_zp", Z_SOFF)
    a.ins("CLC"); a.ins("ADC_zp", Z_STEP)
    a.ins("STA_zp", Z_SOFF)
    a.ins("CMP_zp", Z_MAX)
    a.br("BCC", "sr_fwd")                     # < max -> continue
    a.br("BEQ", "sr_fwd")                     # == max -> include last cell
    a.label("sr_commit")
    a.ins("LDA_zp", Z_RUNLEN)
    a.ins("CMP_imm", 0x04)
    a.br("BCC", "sr_done")                    # run < 4 -> nothing cleared
    a.ins("CLC"); a.ins("LDA_zp", Z_CELLS); a.ins("ADC_zp", Z_RUNLEN); a.ins("STA_zp", Z_CELLS)
    a.ins("CLC"); a.ins("LDA_zp", Z_VIR); a.ins("ADC_zp", Z_RUNVIR); a.ins("STA_zp", Z_VIR)
    a.label("sr_done")
    a.ins("RTS")

    # ==================== SUBROUTINE: score_update ====================
    # Compact, overflow-free, all-positive scoring (so a plain unsigned compare
    # works and best can start at 0):
    #   vir' = min(VIR, 3)              (cap so vir*32 stays small)
    #   score = vir'*32 + CELLS*2 + hirow      (max 96+16+15 = 127, no overflow)
    # A virus clear scores >= 32 (dominates); a non-clearing drop scores just
    # hirow (0..15), so any real clear always beats any non-clear. Among clears,
    # more viruses > more cells > lower placement (larger hirow).
    a.label("score_update")
    a.ins("LDA_zp", Z_VIR)
    a.ins("CMP_imm", 0x04)               # cap VIR at 3
    a.br("BCC", "su_capped")
    a.ins("LDA_imm", 0x03)
    a.label("su_capped")
    a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A")
    a.ins("ASL_A"); a.ins("ASL_A")                  # VIR(<=3) * 32
    a.ins("STA_zp", Z_SCORE)
    a.ins("LDA_zp", Z_CELLS)
    a.ins("ASL_A")                                  # CELLS * 2
    a.ins("CLC"); a.ins("ADC_zp", Z_SCORE); a.ins("STA_zp", Z_SCORE)
    a.ins("CLC"); a.ins("LDA_zp", Z_SCORE); a.ins("ADC_zp", Z_HIROW); a.ins("STA_zp", Z_SCORE)
    # update best if strictly greater (plain unsigned: all scores >= 0)
    a.ins("LDA_zp", Z_BEST)
    a.ins("CMP_zp", Z_SCORE)             # best - score
    a.br("BCS", "su_done")               # best >= score -> keep
    a.ins("LDA_zp", Z_SCORE)
    a.ins("STA_zp", Z_BEST)
    a.ins("LDA_zp", Z_COL)
    a.ins("STA_zp", Z_TARGET)
    a.label("su_done")
    a.ins("RTS")

    return a.assemble()


def apply_patches_v18(input_path, output_path):
    """Build the v18 ROM: v17 toggle/mirror/AI stay in place; a new depth-1
    simulation AI is installed at CPU $FB00 and the 0x37CF hook points to it."""
    # Start from a fresh v17 build so toggle/mirror/study mode are all present.
    import tempfile, os
    tmp_v17 = output_path + ".v17tmp"
    if not apply_patches(input_path, tmp_v17):
        return False
    with open(tmp_v17, "rb") as f:
        rom_data = bytearray(f.read())
    os.remove(tmp_v17)

    print()
    print("=== v18: installing depth-1 simulation AI ===")

    V18_ROM_OFF = 0x7B10
    V18_CPU = 0x8000 + (V18_ROM_OFF - 0x10)   # -> $FB00
    assert V18_CPU == 0xFB00, f"unexpected v18 cpu addr {V18_CPU:#06x}"

    v18 = build_v18_ai(V18_CPU)
    end = V18_ROM_OFF + len(v18)
    region_end = 0x7D10
    if end > region_end:
        print(f"ERROR: v18 routine ({len(v18)} bytes) overflows free region "
              f"0x{V18_ROM_OFF:04X}-0x{region_end:04X}")
        return False

    rom_data[V18_ROM_OFF:V18_ROM_OFF + len(v18)] = v18
    print(f"✓ v18 AI at 0x{V18_ROM_OFF:04X} ({len(v18)} bytes) -> CPU ${V18_CPU:04X}"
          f"  (region 0x{V18_ROM_OFF:04X}-0x{region_end:04X}, "
          f"{region_end - end} bytes spare)")

    # Re-point the controller hook 0x37CF from v17 AI to v18 AI.
    rom_data[0x37CF] = 0x4C  # JMP
    rom_data[0x37D0] = V18_CPU & 0xFF
    rom_data[0x37D1] = (V18_CPU >> 8) & 0xFF
    print(f"✓ Re-hooked controller (0x37CF): JMP ${V18_CPU:04X} (was v17 AI)")

    with open(output_path, "wb") as f:
        f.write(rom_data)

    patched_checksum = hashlib.md5(rom_data).hexdigest()
    print(f"✓ Wrote {output_path} ({len(rom_data)} bytes, md5 {patched_checksum})")
    print("Dr. Mario VS CPU Edition v18 (depth-1 simulation AI) built.")
    return True


if __name__ == "__main__":
    apply_patches(INPUT_ROM, OUTPUT_ROM)
    apply_patches_v18(INPUT_ROM, "drmario_v18.nes")
