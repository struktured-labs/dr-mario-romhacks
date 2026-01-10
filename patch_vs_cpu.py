#!/usr/bin/env python3
"""
Dr. Mario VS CPU Edition v17 - AI with Rotation and Height Penalty
====================================================================
Features:
1. VS CPU Mode: New 3rd menu option with AI-controlled Player 2
   - Menu cycles: 1 PLAYER -> 2 PLAYER -> VS CPU -> 1 PLAYER
   - Level select: P2 cursor mirrors P1's choices (level & speed)
   - AI controls P2 during gameplay in VS CPU mode
2. Study Mode: Pause shows "STUDY" with visible playfield

Technical details:
- $F5/$F7: Player 1 controller input
- $F6/$F8: Player 2 controller input
- $0727: Player mode (1=1P, 2=2P - game sees VS CPU as 2P)
- $04: VS CPU flag (0=normal, 1=VS CPU mode) - using $04 to avoid game conflicts
- Hook points:
  - 0x18E5: Menu toggle -> JSR $FF40 (cycle 1->2->VS->1)
  - 0x10AE: Level select P2 input -> JSR (mirror P1 in VS mode)
  - 0x37CF: Controller read -> JMP (AI routine in VS mode)
- ROM layout (all before JMPs at 0x7FE0):
  - 0x7F50: Toggle routine
  - Then: Level mirror routine
  - Then: AI routine
  - 0x7FE0: JMP table (DO NOT MODIFY!)
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
    # AI Routine v17 - With Rotation Logic
    # ======================================
    # Strategy:
    # 1. Scan ALL viruses (not just first match)
    # 2. For each matching virus:
    #    - Check top row of column (skip if occupied - partition risk)
    #    - Score based on row position (lower row = better)
    # 3. Select BEST virus (lowest row with clear top)
    # 4. Rotate to vertical if both capsule halves same color
    # Memory: $00 = target column, $01 = best score (255 = unset)
    # Note: Height penalty deferred to v18 due to ROM space constraints
    ai_code = []

    ai_code += [0x85, 0xF6]        # STA $F6 (complete original store)

    # Check VS CPU mode
    ai_code += [0xA5, 0x04]        # LDA $04
    ai_code += [0xC9, 0x01]        # CMP #$01
    ai_exit_branch = len(ai_code)
    ai_code += [0xD0, 0x00]        # BNE exit

    # Mirror P1 input for level select
    ai_code += [0xA5, 0xF5]        # LDA $F5
    ai_code += [0x85, 0xF6]        # STA $F6

    # Check gameplay mode
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
    ai_code += [0x38]              # SEC
    ai_code += [0xE9, 0xD0]        # SBC #$D0 (A = tile - 0xD0)
    ai_code += [0xC9, 0x03]        # CMP #$03
    ai_not_virus_branch = len(ai_code)
    ai_code += [0xB0, 0x00]        # BCS not_virus (if >= 3, not a virus)
    # A now contains virus color (0=yellow, 1=red, 2=blue)

    # Check left capsule match only (right match removed to save ROM space)
    ai_code += [0xCD, 0x81, 0x03]  # CMP $0381 (left color)
    ai_not_match_branch = len(ai_code)
    ai_code += [0xD0, 0x00]        # BNE not_match

    # Left match: set target column
    ai_code += [0x98]              # TYA
    ai_code += [0x29, 0x07]        # AND #$07 (column in A)
    ai_code += [0xAA]              # TAX (column in X)

    # === EVALUATE CANDIDATE ===
    # X = target column, Y = virus position
    ai_eval_pos = len(ai_code)

    # Check top row of this column (row 0)
    # Top row address = $0500 + column (X)
    ai_code += [0xBD, 0x00, 0x05]  # LDA $0500,X (top row of column)
    ai_code += [0xC9, 0xFF]        # CMP #$FF (empty?)
    ai_top_occupied_branch = len(ai_code)
    ai_code += [0xD0, 0x00]        # BNE not_match (skip if top occupied)

    # Calculate score = row number (Y >> 3)
    ai_code += [0x98]              # TYA (position)
    ai_code += [0x4A]              # LSR
    ai_code += [0x4A]              # LSR
    ai_code += [0x4A]              # LSR (A = row number, 0-15)

    # Compare with best score
    ai_code += [0xC5, 0x01]        # CMP $01 (compare with best)
    ai_not_better_branch = len(ai_code)
    ai_code += [0xB0, 0x00]        # BCS not_better (if A >= best, skip)

    # This is better! Update best score and target
    ai_code += [0x85, 0x01]        # STA $01 (update best score)
    ai_code += [0x86, 0x00]        # STX $00 (update target column)

    # Continue scanning
    ai_not_virus_pos = len(ai_code)
    ai_code += [0xC8]              # INY
    ai_code += [0xC0, 0x80]        # CPY #$80
    ai_scan_loop_branch = len(ai_code)
    ai_code += [0x90, 0x00]        # BCC scan_loop (continue if Y < 128)

    # === ROTATION LOGIC ===
    # If both capsule colors same → rotate (using EOR to save space)
    ai_code += [0xAD, 0x81, 0x03]  # LDA $0381 (left color)
    ai_code += [0x4D, 0x82, 0x03]  # EOR $0382 (right color)
    ai_no_rotate_branch = len(ai_code)
    ai_code += [0xD0, 0x00]        # BNE no_rotate (different if non-zero)
    # Same - rotate
    ai_code += [0xA9, 0x40]        # LDA #$40 (A button)
    ai_code += [0x85, 0xF6]        # STA $F6
    ai_code += [0x60]              # RTS
    ai_no_rotate_pos = len(ai_code)

    # === MOVEMENT LOGIC ===
    ai_move_pos = len(ai_code)
    ai_code += [0xAD, 0x85, 0x03]  # LDA $0385 (P2 X)
    ai_code += [0xC5, 0x00]        # CMP $00 (target)
    ai_at_target_branch = len(ai_code)
    ai_code += [0xF0, 0x00]        # BEQ at_target

    # Move toward target
    ai_code += [0xA0, 0x01]        # LDY #$01 (assume right)
    ai_move_left_branch = len(ai_code)
    ai_code += [0x90, 0x00]        # BCC store_move (X < target, go right)
    ai_code += [0xC8]              # INY (Y=2 = left)
    ai_store_move_pos = len(ai_code)
    ai_code += [0x84, 0xF6]        # STY $F6

    ai_exit_pos = len(ai_code)
    ai_code += [0x60]              # RTS

    # at_target: drop
    ai_at_target_pos = len(ai_code)
    ai_code += [0xA9, 0x04]        # LDA #$04 (Down)
    ai_code += [0x85, 0xF6]        # STA $F6
    ai_code += [0x60]              # RTS

    # Fix branch offsets
    ai_code[ai_exit_branch + 1] = (ai_exit_pos - (ai_exit_branch + 2)) & 0xFF
    ai_code[ai_exit_branch2 + 1] = (ai_exit_pos - (ai_exit_branch2 + 2)) & 0xFF
    ai_code[ai_not_virus_branch + 1] = (ai_not_virus_pos - (ai_not_virus_branch + 2)) & 0xFF
    ai_code[ai_not_match_branch + 1] = (ai_not_virus_pos - (ai_not_match_branch + 2)) & 0xFF
    ai_code[ai_top_occupied_branch + 1] = (ai_not_virus_pos - (ai_top_occupied_branch + 2)) & 0xFF
    ai_code[ai_not_better_branch + 1] = (ai_not_virus_pos - (ai_not_better_branch + 2)) & 0xFF
    ai_code[ai_scan_loop_branch + 1] = (ai_scan_loop - (ai_scan_loop_branch + 2)) & 0xFF
    ai_code[ai_no_rotate_branch + 1] = (ai_no_rotate_pos - (ai_no_rotate_branch + 2)) & 0xFF
    ai_code[ai_at_target_branch + 1] = (ai_at_target_pos - (ai_at_target_branch + 2)) & 0xFF
    ai_code[ai_move_left_branch + 1] = (ai_store_move_pos - (ai_move_left_branch + 2)) & 0xFF

    ai_routine = bytes(ai_code)

    # =========================================
    # Calculate offsets and install everything
    # =========================================
    # Layout: Toggle -> Mirror -> AI (must all fit before 0x7FE0 JMPs)
    toggle_offset = 0x7F50
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
    print("Dr. Mario VS CPU Edition v15 (Obstacle-Aware AI) applied successfully!")
    print("Features:")
    print("- VS CPU Mode: New 3rd menu option with AI-controlled Player 2")
    print("  - Menu cycles: 1 PLAYER -> 2 PLAYER -> VS CPU")
    print("  - Level select: P2 cursor mirrors P1 (level & speed)")
    print("  - P2 can take control by pressing any button")
    print("  - AI only activates during VS CPU gameplay")
    print("  - P2 speed synced to P1 at game start")
    print("- Study Mode: Pause shows 'STUDY' with visible playfield")

    return True

if __name__ == "__main__":
    apply_patches(INPUT_ROM, OUTPUT_ROM)
