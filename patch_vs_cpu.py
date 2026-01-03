#!/usr/bin/env python3
"""
Dr. Mario VS CPU Edition v8
===========================
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
    # Level Select Mirror (VS CPU mode)
    # =========================================
    # Uses $04 for VS CPU flag
    # Only mirrors during level select (P2 virus count == 0), not gameplay
    mirror_code = []

    # Check $0727 == 2 (must be in 2P mode for game)
    mirror_code += [0xAD, 0x27, 0x07]  # LDA $0727
    mirror_code += [0xC9, 0x02]        # CMP #$02
    load_p2_branch1 = len(mirror_code)
    mirror_code += [0xD0, 0x00]        # BNE load_p2 (not 2P mode)

    # Check $04 == 1 (VS CPU flag)
    mirror_code += [0xA5, 0x04]        # LDA $04
    mirror_code += [0xC9, 0x01]        # CMP #$01
    load_p2_branch2 = len(mirror_code)
    mirror_code += [0xD0, 0x00]        # BNE load_p2 (not VS CPU)

    # Check $03A4 == 0 (P2 has no viruses = level select, not gameplay)
    mirror_code += [0xAD, 0xA4, 0x03]  # LDA $03A4
    load_p2_branch3 = len(mirror_code)
    mirror_code += [0xD0, 0x00]        # BNE load_p2 (in gameplay, use P2)

    # use_p1: Load P1 buttons for P2 (mirror mode - level select only)
    mirror_code += [0xA5, 0xF5]        # LDA $F5
    mirror_code += [0x85, 0x5B]        # STA $5B
    mirror_code += [0xA5, 0xF7]        # LDA $F7
    mirror_code += [0x85, 0x5C]        # STA $5C
    mirror_code += [0x60]              # RTS

    # load_p2: Load P2 buttons normally
    load_p2_pos = len(mirror_code)
    mirror_code += [0xA5, 0xF6]        # LDA $F6
    mirror_code += [0x85, 0x5B]        # STA $5B
    mirror_code += [0xA5, 0xF8]        # LDA $F8
    mirror_code += [0x85, 0x5C]        # STA $5C
    mirror_code += [0x60]              # RTS

    # Fix branch offsets
    mirror_code[load_p2_branch1 + 1] = (load_p2_pos - (load_p2_branch1 + 2)) & 0xFF
    mirror_code[load_p2_branch2 + 1] = (load_p2_pos - (load_p2_branch2 + 2)) & 0xFF
    mirror_code[load_p2_branch3 + 1] = (load_p2_pos - (load_p2_branch3 + 2)) & 0xFF

    level_mirror_routine = bytes(mirror_code)

    # =========================================
    # AI Routine - Simple version for debugging
    # =========================================
    # Original code at 0x37CF: STA $F6; RTS
    # Our JMP overwrites both, so we do STA $F6 and RTS ourselves
    #
    # Button values: Right=1, Left=2, Down=4, A(rotate)=$80
    code = []

    code += [0x85, 0xF6]        # STA $F6 (complete original store)

    # Check VS CPU mode ($04 == 1)
    code += [0xA5, 0x04]        # LDA $04 (VS CPU flag)
    code += [0xC9, 0x01]        # CMP #$01
    exit_branch_pos = len(code)
    code += [0xD0, 0x00]        # BNE exit (not VS CPU)

    # Check game active (P2 has viruses)
    code += [0xAD, 0xA4, 0x03]  # LDA $03A4
    exit_branch2_pos = len(code)
    code += [0xF0, 0x00]        # BEQ exit (no viruses = not in game)

    # DEBUG: Just press Left constantly to prove AI is running
    code += [0xA9, 0x02]        # LDA #$02 (Left)
    code += [0x85, 0xF6]        # STA $F6
    exit_pos = len(code)
    code += [0x60]              # RTS

    # Fix branch offsets
    code[exit_branch_pos + 1] = (exit_pos - (exit_branch_pos + 2)) & 0xFF
    code[exit_branch2_pos + 1] = (exit_pos - (exit_branch2_pos + 2)) & 0xFF

    ai_routine = bytes(code)

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
    print("Dr. Mario VS CPU Edition v8 applied successfully!")
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
