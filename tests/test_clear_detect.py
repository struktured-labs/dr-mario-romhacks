#!/usr/bin/env python3
"""6502 `find_clears` (one resolve pass): mark every cell in a horizontal OR
vertical run of >=4 same-color cells, clear them to EMPTY, and return cells/
viruses cleared. Validated cell-for-cell against a Python golden model.

NES tile encoding: empty=$FF; occupied color = tile & $0F (viruses $D0-$D2,
capsules $4x-$7x with low-nibble color 0/1/2). A run clears if 4+ consecutive
same-color cells in a row or column. All runs detected on the PRE-clear board,
then cleared simultaneously (standard Dr. Mario semantics).

Mark buffer: $0300-$037F (scratch). Outputs: $E0=cells_cleared, $E1=viruses_cleared.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from py65_harness import Cpu
from patch_vs_cpu import Asm6502

EMPTY = 0xFF
ROWS, COLS = 16, 8
BOARD = 0x0500
MARK = 0x0300
O_CELLS, O_VIR = 0xE0, 0xE1
Z_ROW, Z_COL, Z_OFF, Z_RUN, Z_MCOL, Z_RSTART = 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7
BASE = 0x4000


def golden_find_clears(board):
    b = list(board)
    mark = [False] * 128
    def color(t): return None if t == EMPTY else (t & 0x0F)
    # horizontal
    for r in range(ROWS):
        run = []
        last = None
        for c in range(COLS):
            t = b[r * COLS + c]; col = color(t)
            if col is not None and col == last:
                run.append(r * COLS + c)
            else:
                if last is not None and len(run) >= 4:
                    for o in run: mark[o] = True
                run = [r * COLS + c] if col is not None else []
                last = col
        if last is not None and len(run) >= 4:
            for o in run: mark[o] = True
    # vertical
    for c in range(COLS):
        run = []; last = None
        for r in range(ROWS):
            t = b[r * COLS + c]; col = color(t)
            if col is not None and col == last:
                run.append(r * COLS + c)
            else:
                if last is not None and len(run) >= 4:
                    for o in run: mark[o] = True
                run = [r * COLS + c] if col is not None else []
                last = col
        if last is not None and len(run) >= 4:
            for o in run: mark[o] = True
    cells = viruses = 0
    for o in range(128):
        if mark[o]:
            if (b[o] & 0xF0) == 0xD0: viruses += 1
            cells += 1
            b[o] = EMPTY
    return b, cells, viruses


def build_find_clears():
    a = Asm6502(BASE)
    # ---- clear mark buffer ($0300-$037F) ----
    a.ins("LDA_imm", 0); a.ins("LDX_imm", 127)
    a.label("mk_clr"); a.ins16("STA_absX", MARK); a.ins("DEX"); a.br("BPL", "mk_clr")
    a.ins("STA_zp", O_CELLS); a.ins("STA_zp", O_VIR)   # A is still 0

    # =========================================================
    # A run-scan helper is inlined twice (H and V) via a subroutine `scan_line`
    # that walks `len` cells starting at `Z_OFF`, stepping by `Z_RUN` (reused as
    # step), marking runs >=4. To keep it simple we instead write two explicit
    # nested loops sharing a `mark_run` subroutine.
    # =========================================================
    # ---- HORIZONTAL: for row r in 0..15, scan 8 cols step 1 ----
    a.ins("LDA_imm", 0); a.ins("STA_zp", Z_ROW)
    a.label("h_row")
    a.ins("LDA_zp", Z_ROW)
    # offset = row*8 : ASL x3
    a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("STA_zp", Z_OFF)
    a.ins("LDA_imm", 1); a.ins("STA_zp", 0xE8)   # step=1 in $E8
    a.ins("LDA_imm", COLS); a.ins("STA_zp", 0xE9)  # count=8 in $E9
    a.jsr("scan_line")
    a.ins("INC_zp", Z_ROW); a.ins("LDA_zp", Z_ROW); a.ins("CMP_imm", ROWS)
    a.br("BNE", "h_row")
    # ---- VERTICAL: for col c in 0..7, scan 16 rows step 8 ----
    a.ins("LDA_imm", 0); a.ins("STA_zp", Z_COL)
    a.label("v_col")
    a.ins("LDA_zp", Z_COL); a.ins("STA_zp", Z_OFF)
    a.ins("LDA_imm", 8); a.ins("STA_zp", 0xE8)    # step=8
    a.ins("LDA_imm", ROWS); a.ins("STA_zp", 0xE9) # count=16
    a.jsr("scan_line")
    a.ins("INC_zp", Z_COL); a.ins("LDA_zp", Z_COL); a.ins("CMP_imm", COLS)
    a.br("BNE", "v_col")

    # ---- apply marks: clear marked cells, count cells/viruses ----
    a.ins("LDX_imm", 127)
    a.label("ap_loop")
    a.ins16("LDA_absX", MARK); a.br("BEQ", "ap_next")
    # marked: check virus (board high nibble == $D0)
    a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0)
    a.br("BNE", "ap_notvir"); a.ins("INC_zp", O_VIR)
    a.label("ap_notvir")
    a.ins("INC_zp", O_CELLS)
    a.ins("LDA_imm", EMPTY); a.ins16("STA_absX", BOARD)  # clear
    a.label("ap_next")
    a.ins("DEX"); a.br("BPL", "ap_loop")
    a.ins("RTS")

    # ================= scan_line subroutine =================
    # Walk count($E9) cells from Z_OFF stepping step($E8). Track current run of
    # same color; when a run of >=4 ends, mark its cells. Z_RUN=run length,
    # Z_MCOL=current match color, Z_RSTART=offset of run start. Y = cells done.
    a.label("scan_line")
    a.ins("LDY_imm", 0)
    a.ins("LDA_imm", 0); a.ins("STA_zp", Z_RUN)
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", Z_MCOL)   # no current color
    a.label("sl_cell")
    a.ins("LDX_zp", Z_OFF)
    a.ins16("LDA_absX", BOARD)
    a.ins("CMP_imm", EMPTY); a.br("BEQ", "sl_break")  # empty -> run ends
    a.ins("AND_imm", 0x0F)                            # color
    a.ins("CMP_zp", Z_MCOL); a.br("BNE", "sl_newcol") # color changed -> new run
    # same color: extend run
    a.ins("INC_zp", Z_RUN)
    a.jmp("sl_adv")
    a.label("sl_break")
    a.jsr("sl_flush")                                 # flush a completed run
    a.ins("LDA_imm", 0); a.ins("STA_zp", Z_RUN)
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", Z_MCOL)
    a.jmp("sl_adv")
    a.label("sl_newcol")
    a.jsr("sl_flush")                                 # flush previous run
    a.ins("LDX_zp", Z_OFF); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0x0F)
    a.ins("STA_zp", Z_MCOL)
    a.ins("LDA_zp", Z_OFF); a.ins("STA_zp", Z_RSTART)
    a.ins("LDA_imm", 1); a.ins("STA_zp", Z_RUN)
    a.label("sl_adv")
    # if run just became 1 (start), record start offset
    a.ins("LDA_zp", Z_RUN); a.ins("CMP_imm", 1); a.br("BNE", "sl_noset")
    a.ins("LDA_zp", Z_OFF); a.ins("STA_zp", Z_RSTART)
    a.label("sl_noset")
    a.ins("LDA_zp", Z_OFF); a.ins("CLC"); a.ins("ADC_zp", 0xE8); a.ins("STA_zp", Z_OFF)
    a.ins("INY"); a.ins("CPY_zp", 0xE9); a.br("BNE", "sl_cell")
    a.jsr("sl_flush")                                 # flush run at line end
    a.ins("RTS")

    # ---- sl_flush: if Z_RUN>=4, mark the run's cells (from Z_RSTART, step E8) ----
    a.label("sl_flush")
    a.ins("LDA_zp", Z_RUN); a.ins("CMP_imm", 4); a.br("BCC", "fl_done")  # <4 -> nothing
    a.ins("LDX_zp", Z_RSTART)
    a.ins("LDA_zp", Z_RUN); a.ins("STA_zp", 0xEA)    # counter
    a.label("fl_mark")
    a.ins("LDA_imm", 1); a.ins16("STA_absX", MARK)
    a.ins("TXA"); a.ins("CLC"); a.ins("ADC_zp", 0xE8); a.ins("TAX")
    a.ins("DEC_zp", 0xEA); a.br("BNE", "fl_mark")
    a.label("fl_done")
    a.ins("RTS")
    return a.assemble()


def rand_board(rng, mode):
    cap = [0x40, 0x41, 0x42, 0x51, 0x52, 0x60, 0x61, 0x62, 0x71, 0x72]
    vir = [0xD0, 0xD1, 0xD2]
    if mode == "uniform":
        return [EMPTY if rng.random() < 0.45 else rng.choice(cap + vir)
                for _ in range(128)]
    # settled + deliberately seed some 4-runs
    b = [EMPTY] * 128
    for c in range(COLS):
        h = rng.randint(0, ROWS)
        for r in range(ROWS - h, ROWS):
            b[r * COLS + c] = rng.choice(cap + vir)
    # force a few horizontal runs of one color
    for _ in range(rng.randint(0, 3)):
        r = rng.randint(0, ROWS - 1); c0 = rng.randint(0, COLS - 4)
        col = rng.randint(0, 2)
        for c in range(c0, c0 + rng.randint(4, COLS - c0)):
            b[r * COLS + c] = rng.choice(vir + cap) & 0xF0 | col
    return b


def main():
    code = build_find_clears()
    rng = random.Random(99)
    cpu = Cpu(); cpu.load(BASE, code)
    fails = 0; cyc_max = cyc_tot = 0; n = 800
    for t in range(n):
        mode = "uniform" if t % 2 == 0 else "settled"
        board = rand_board(rng, mode)
        cpu.set_board(board)
        cyc = cpu.call(BASE); cyc_tot += cyc; cyc_max = max(cyc_max, cyc)
        gb, gc, gv = golden_find_clears(board)
        rb = cpu.get_board(); rc = cpu.zp(O_CELLS); rv = cpu.zp(O_VIR)
        if rb != gb or rc != gc or rv != gv:
            fails += 1
            if fails <= 6:
                print(f"  MISMATCH t={t} {mode}: cells {rc}/{gc} vir {rv}/{gv} "
                      f"board_eq={rb == gb}")
    print(f"routine size = {len(code)} bytes")
    print(f"validation: {n - fails}/{n} match  (fails={fails})")
    print(f"cycles: max={cyc_max} avg={cyc_tot // n}  "
          f"({cyc_max/2273:.1f} vblank frames/pass)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
