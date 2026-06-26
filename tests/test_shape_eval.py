#!/usr/bin/env python3
"""Build a 6502 `score_board_shape` routine, validate it cell-for-cell against a
Python golden model over random boards, and report its cycle cost vs the
vblank-NMI budget (~2273 usable cycles/frame).

Shape terms (match planner.score_board): max_height, holes, top_risk.
Outputs to zero page: $E0=max_height, $E1=holes, $E2=top_risk.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from py65_harness import Cpu
from patch_vs_cpu import Asm6502

EMPTY = 0xFF
ROWS, COLS = 16, 8
O_MAXH, O_HOLES, O_TOPRISK = 0xE0, 0xE1, 0xE2
Z_COL, Z_OFF, Z_SEEN, Z_TMP = 0xE3, 0xE4, 0xE5, 0xE6
BASE = 0x4000


def golden_shape(board):
    occ = [b != EMPTY for b in board]
    max_h = 0
    holes = 0
    for c in range(COLS):
        seen = False
        for r in range(ROWS):
            if occ[r * COLS + c]:
                if not seen:
                    seen = True
                    h = ROWS - r
                    if h > max_h:
                        max_h = h
            elif seen:
                holes += 1
    top_risk = sum(1 for i in range(3 * COLS) if board[i] != EMPTY)
    return max_h, holes, top_risk


def build_shape_routine():
    a = Asm6502(BASE)
    a.ins("LDA_imm", 0); a.ins("STA_zp", O_MAXH); a.ins("STA_zp", O_HOLES)
    a.ins("STA_zp", O_TOPRISK)
    # ---- top_risk: count occupied in offsets 0..23 ----
    a.ins("LDX_imm", 23)
    a.label("tr_loop")
    a.ins16("LDA_absX", 0x0500); a.ins("CMP_imm", EMPTY)
    a.br("BEQ", "tr_skip")
    a.ins("INC_zp", O_TOPRISK)
    a.label("tr_skip")
    a.ins("DEX"); a.br("BPL", "tr_loop")
    # ---- per-column walk: height + holes ----
    a.ins("LDA_imm", 0); a.ins("STA_zp", Z_COL)
    a.label("col_loop")
    a.ins("LDA_zp", Z_COL); a.ins("STA_zp", Z_OFF)   # offset = col (row 0)
    a.ins("LDA_imm", 0); a.ins("STA_zp", Z_SEEN)
    a.ins("LDY_imm", 0)                              # Y = row 0..15
    a.label("row_loop")
    a.ins("LDX_zp", Z_OFF)
    a.ins16("LDA_absX", 0x0500); a.ins("CMP_imm", EMPTY)
    a.br("BEQ", "cell_empty")
    # --- occupied ---
    a.ins("LDA_zp", Z_SEEN); a.br("BNE", "after_cell")     # already seen
    a.ins("LDA_imm", 1); a.ins("STA_zp", Z_SEEN)
    # height = 16 - row(Y)
    a.ins("TYA"); a.ins("STA_zp", Z_TMP)
    a.ins("LDA_imm", ROWS); a.ins("SEC"); a.ins("SBC_zp", Z_TMP)   # A = height
    a.ins("CMP_zp", O_MAXH); a.br("BCC", "after_cell")     # height < maxh -> skip
    a.ins("STA_zp", O_MAXH)
    a.jmp("after_cell")
    a.label("cell_empty")
    a.ins("LDA_zp", Z_SEEN); a.br("BEQ", "after_cell")     # not seen -> not a hole
    a.ins("INC_zp", O_HOLES)
    a.label("after_cell")
    a.ins("LDA_zp", Z_OFF); a.ins("CLC"); a.ins("ADC_imm", 8); a.ins("STA_zp", Z_OFF)
    a.ins("INY"); a.ins("CPY_imm", ROWS); a.br("BNE", "row_loop")
    a.ins("INC_zp", Z_COL); a.ins("LDA_zp", Z_COL); a.ins("CMP_imm", COLS)
    a.br("BNE", "col_loop")
    a.ins("RTS")
    return a.assemble()


def rand_board(rng, mode):
    if mode == "uniform":          # stress holes logic (floating cells)
        return [EMPTY if rng.random() < 0.5 else rng.choice(
            [0xD0, 0xD1, 0xD2, 0x40, 0x51, 0x62, 0x73]) for _ in range(128)]
    # settled: each column filled contiguously from some row to bottom
    b = [EMPTY] * 128
    for c in range(COLS):
        h = rng.randint(0, ROWS)
        for r in range(ROWS - h, ROWS):
            b[r * COLS + c] = rng.choice([0xD0, 0xD1, 0xD2, 0x40, 0x51, 0x62])
    # punch a few holes
    for _ in range(rng.randint(0, 6)):
        b[rng.randint(0, 127)] = EMPTY
    return b


def main():
    code = build_shape_routine()
    rng = random.Random(1234)
    cpu = Cpu(); cpu.load(BASE, code)
    fails = 0; cyc_max = 0; cyc_tot = 0; n = 600
    for t in range(n):
        mode = "uniform" if t % 2 == 0 else "settled"
        board = rand_board(rng, mode)
        cpu.set_board(board)
        cyc = cpu.call(BASE)
        cyc_tot += cyc; cyc_max = max(cyc_max, cyc)
        got = (cpu.zp(O_MAXH), cpu.zp(O_HOLES), cpu.zp(O_TOPRISK))
        exp = golden_shape(board)
        if got != exp:
            fails += 1
            if fails <= 5:
                print(f"  MISMATCH t={t} {mode}: got={got} exp={exp}")
    print(f"routine size = {len(code)} bytes")
    print(f"validation: {n - fails}/{n} boards match  (fails={fails})")
    print(f"cycles: max={cyc_max} avg={cyc_tot // n}  "
          f"(vblank budget ~2273/frame -> {cyc_max/2273:.1f} frames/eval)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
