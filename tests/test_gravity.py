#!/usr/bin/env python3
"""6502 `apply_gravity` — column-compact gravity with viruses FIXED: within each
column, capsule cells fall to the lowest free row, never passing through a virus
(which stays put). This is the simplification proven equal to faithful linked-body
gravity for virus counting (0% mismatch / 400 boards). Validated cell-for-cell
against the Python column-compact reference.

NES tiles: empty=$FF; virus = (tile & $F0)==$D0; capsule = occupied, not virus.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from py65_harness import Cpu
from patch_vs_cpu import Asm6502

EMPTY = 0xFF
ROWS, COLS = 16, 8
BOARD = 0x0500
Z_COL, Z_READ, Z_DEST, Z_TILE = 0xE2, 0xE3, 0xE4, 0xE5
BASE = 0x4000


def is_virus(t): return t != EMPTY and (t & 0xF0) == 0xD0


def golden_gravity(board):
    b = list(board)
    for c in range(COLS):
        dest = 15
        for read in range(15, -1, -1):
            off = read * COLS + c
            t = b[off]
            if t == EMPTY:
                continue
            if is_virus(t):
                dest = read - 1
            else:  # capsule falls to dest
                doff = dest * COLS + c
                if doff != off:
                    b[doff] = t
                    b[off] = EMPTY
                dest -= 1
    return b


def build_gravity():
    a = Asm6502(BASE)
    a.ins("LDA_imm", 0); a.ins("STA_zp", Z_COL)
    a.label("col_loop")
    # dest = 15*8 + col  (bottom row offset for this column)
    a.ins("LDA_imm", 120); a.ins("CLC"); a.ins("ADC_zp", Z_COL); a.ins("STA_zp", Z_DEST)
    # read = 15*8 + col, walk upward by -8 for 16 rows
    a.ins("LDA_imm", 120); a.ins("CLC"); a.ins("ADC_zp", Z_COL); a.ins("STA_zp", Z_READ)
    a.ins("LDY_imm", 0)                       # row counter 0..15
    a.label("row_loop")
    a.ins("LDX_zp", Z_READ); a.ins16("LDA_absX", BOARD)
    a.ins("CMP_imm", EMPTY); a.br("BEQ", "next")          # empty -> skip
    a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BNE", "is_cap")
    # --- virus: stays; dest = read - 8 ---
    a.ins("LDA_zp", Z_READ); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", Z_DEST)
    a.jmp("next")
    a.label("is_cap")
    # --- capsule: move tile from READ to DEST (if different), dest -= 8 ---
    a.ins("LDX_zp", Z_READ); a.ins16("LDA_absX", BOARD); a.ins("STA_zp", Z_TILE)
    a.ins("LDA_zp", Z_READ); a.ins("CMP_zp", Z_DEST); a.br("BEQ", "cap_nomove")
    a.ins("LDA_imm", EMPTY); a.ins16("STA_absX", BOARD)   # clear READ (X=READ)
    a.ins("LDX_zp", Z_DEST); a.ins("LDA_zp", Z_TILE); a.ins16("STA_absX", BOARD)
    a.label("cap_nomove")
    a.ins("LDA_zp", Z_DEST); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", Z_DEST)
    a.label("next")
    a.ins("LDA_zp", Z_READ); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", Z_READ)
    a.ins("INY"); a.ins("CPY_imm", ROWS); a.br("BNE", "row_loop")
    a.ins("INC_zp", Z_COL); a.ins("LDA_zp", Z_COL); a.ins("CMP_imm", COLS)
    a.br("BNE", "col_loop")
    a.ins("RTS")
    return a.assemble()


def rand_board(rng, mode):
    cap = [0x40, 0x41, 0x42, 0x51, 0x52, 0x60, 0x61, 0x62]
    vir = [0xD0, 0xD1, 0xD2]
    if mode == "floaty":   # lots of floating capsules to stress falling
        return [EMPTY if rng.random() < 0.6 else rng.choice(cap + vir)
                for _ in range(128)]
    b = [EMPTY] * 128
    for c in range(COLS):
        for r in range(ROWS):
            x = rng.random()
            if x < 0.25:
                b[r * COLS + c] = rng.choice(cap)
            elif x < 0.32:
                b[r * COLS + c] = rng.choice(vir)
    return b


def main():
    code = build_gravity()
    rng = random.Random(7)
    cpu = Cpu(); cpu.load(BASE, code)
    fails = 0; cyc_max = cyc_tot = 0; n = 800
    for t in range(n):
        mode = "floaty" if t % 2 == 0 else "mixed"
        board = rand_board(rng, mode)
        cpu.set_board(board)
        cyc = cpu.call(BASE); cyc_tot += cyc; cyc_max = max(cyc_max, cyc)
        gb = golden_gravity(board); rb = cpu.get_board()
        if rb != gb:
            fails += 1
            if fails <= 6:
                diff = [(i, rb[i], gb[i]) for i in range(128) if rb[i] != gb[i]][:6]
                print(f"  MISMATCH t={t} {mode}: diffs(off,got,exp)={diff}")
    print(f"routine size = {len(code)} bytes")
    print(f"validation: {n - fails}/{n} match  (fails={fails})")
    print(f"cycles: max={cyc_max} avg={cyc_tot // n}  ({cyc_max/2273:.1f} vblank frames)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
