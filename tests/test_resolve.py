#!/usr/bin/env python3
"""6502 `resolve` = loop { find_clears; if nothing cleared -> stop; gravity }.
Composes the validated find_clears + column-compact gravity primitives into the
full board-sim the depth-2 search needs. Validated two ways:
  1. cell-for-cell vs the Python column-compact resolve reference;
  2. total viruses_cleared vs the faithful engine (drmario.faithful_game.resolve),
     translating NES tiles <-> faithful color enum.

Outputs: $E0=total cells cleared, $E1=total viruses cleared (summed over passes).
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
O_CELLS, O_VIR = 0xE0, 0xE1          # grand totals across passes
P_CELLS, P_VIR = 0xEB, 0xEC          # per-pass counts (find_clears writes these)
Z_ROW, Z_COL, Z_OFF, Z_RUN, Z_MCOL, Z_RSTART = 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7
GZ_COL, GZ_READ, GZ_DEST, GZ_TILE = 0xED, 0xEE, 0xEF, 0xF0
BASE = 0x4000


def is_virus(t): return t != EMPTY and (t & 0xF0) == 0xD0


# ----- Python references -----
def py_find_clears(b):
    mark = [False] * 128
    def color(t): return None if t == EMPTY else (t & 0x0F)
    for r in range(ROWS):
        run, last = [], None
        for c in range(COLS):
            col = color(b[r * COLS + c])
            if col is not None and col == last:
                run.append(r * COLS + c)
            else:
                if last is not None and len(run) >= 4:
                    for o in run: mark[o] = True
                run = [r * COLS + c] if col is not None else []; last = col
        if last is not None and len(run) >= 4:
            for o in run: mark[o] = True
    for c in range(COLS):
        run, last = [], None
        for r in range(ROWS):
            col = color(b[r * COLS + c])
            if col is not None and col == last:
                run.append(r * COLS + c)
            else:
                if last is not None and len(run) >= 4:
                    for o in run: mark[o] = True
                run = [r * COLS + c] if col is not None else []; last = col
        if last is not None and len(run) >= 4:
            for o in run: mark[o] = True
    cells = vir = 0
    for o in range(128):
        if mark[o]:
            if is_virus(b[o]): vir += 1
            cells += 1; b[o] = EMPTY
    return cells, vir


def py_gravity(b):
    for c in range(COLS):
        dest = 15
        for read in range(15, -1, -1):
            off = read * COLS + c; t = b[off]
            if t == EMPTY: continue
            if is_virus(t): dest = read - 1
            else:
                doff = dest * COLS + c
                if doff != off: b[doff] = t; b[off] = EMPTY
                dest -= 1


def py_resolve(board):
    b = list(board); tc = tv = 0
    while True:
        c, v = py_find_clears(b)
        if c == 0: break
        tc += c; tv += v
        py_gravity(b)
    return b, tc, tv


# ----- 6502 builder: resolve driver + find_clears + gravity in one blob -----
def build_resolve():
    a = Asm6502(BASE)
    # ---- resolve entry ----
    a.ins("LDA_imm", 0); a.ins("STA_zp", O_CELLS); a.ins("STA_zp", O_VIR)
    a.label("rs_loop")
    a.jsr("find_clears")
    a.ins("LDA_zp", P_CELLS); a.br("BNE", "rs_more")
    a.ins("RTS")
    a.label("rs_more")
    a.ins("CLC"); a.ins("ADC_zp", O_CELLS); a.ins("STA_zp", O_CELLS)
    a.ins("LDA_zp", P_VIR); a.ins("CLC"); a.ins("ADC_zp", O_VIR); a.ins("STA_zp", O_VIR)
    a.jsr("gravity")
    a.jmp("rs_loop")

    # ================= find_clears (writes P_CELLS/P_VIR) =================
    a.label("find_clears")
    a.ins("LDA_imm", 0); a.ins("LDX_imm", 127)
    a.label("mk_clr"); a.ins16("STA_absX", MARK); a.ins("DEX"); a.br("BPL", "mk_clr")
    a.ins("STA_zp", P_CELLS); a.ins("STA_zp", P_VIR)
    a.ins("LDA_imm", 0); a.ins("STA_zp", Z_ROW)
    a.label("h_row")
    a.ins("LDA_zp", Z_ROW); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("STA_zp", Z_OFF)
    a.ins("LDA_imm", 1); a.ins("STA_zp", 0xE8); a.ins("LDA_imm", COLS); a.ins("STA_zp", 0xE9)
    a.jsr("scan_line")
    a.ins("INC_zp", Z_ROW); a.ins("LDA_zp", Z_ROW); a.ins("CMP_imm", ROWS); a.br("BNE", "h_row")
    a.ins("LDA_imm", 0); a.ins("STA_zp", Z_COL)
    a.label("v_col")
    a.ins("LDA_zp", Z_COL); a.ins("STA_zp", Z_OFF)
    a.ins("LDA_imm", 8); a.ins("STA_zp", 0xE8); a.ins("LDA_imm", ROWS); a.ins("STA_zp", 0xE9)
    a.jsr("scan_line")
    a.ins("INC_zp", Z_COL); a.ins("LDA_zp", Z_COL); a.ins("CMP_imm", COLS); a.br("BNE", "v_col")
    a.ins("LDX_imm", 127)
    a.label("ap_loop")
    a.ins16("LDA_absX", MARK); a.br("BEQ", "ap_next")
    a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0)
    a.br("BNE", "ap_notvir"); a.ins("INC_zp", P_VIR)
    a.label("ap_notvir")
    a.ins("INC_zp", P_CELLS)
    a.ins("LDA_imm", EMPTY); a.ins16("STA_absX", BOARD)
    a.label("ap_next")
    a.ins("DEX"); a.br("BPL", "ap_loop")
    a.ins("RTS")
    # scan_line
    a.label("scan_line")
    a.ins("LDY_imm", 0); a.ins("LDA_imm", 0); a.ins("STA_zp", Z_RUN)
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", Z_MCOL)
    a.label("sl_cell")
    a.ins("LDX_zp", Z_OFF); a.ins16("LDA_absX", BOARD)
    a.ins("CMP_imm", EMPTY); a.br("BEQ", "sl_break")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", Z_MCOL); a.br("BNE", "sl_newcol")
    a.ins("INC_zp", Z_RUN); a.jmp("sl_adv")
    a.label("sl_break")
    a.jsr("sl_flush"); a.ins("LDA_imm", 0); a.ins("STA_zp", Z_RUN)
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", Z_MCOL); a.jmp("sl_adv")
    a.label("sl_newcol")
    a.jsr("sl_flush")
    a.ins("LDX_zp", Z_OFF); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0x0F); a.ins("STA_zp", Z_MCOL)
    a.ins("LDA_zp", Z_OFF); a.ins("STA_zp", Z_RSTART)
    a.ins("LDA_imm", 1); a.ins("STA_zp", Z_RUN)
    a.label("sl_adv")
    a.ins("LDA_zp", Z_RUN); a.ins("CMP_imm", 1); a.br("BNE", "sl_noset")
    a.ins("LDA_zp", Z_OFF); a.ins("STA_zp", Z_RSTART)
    a.label("sl_noset")
    a.ins("LDA_zp", Z_OFF); a.ins("CLC"); a.ins("ADC_zp", 0xE8); a.ins("STA_zp", Z_OFF)
    a.ins("INY"); a.ins("CPY_zp", 0xE9); a.br("BNE", "sl_cell")
    a.jsr("sl_flush"); a.ins("RTS")
    # sl_flush
    a.label("sl_flush")
    a.ins("LDA_zp", Z_RUN); a.ins("CMP_imm", 4); a.br("BCC", "fl_done")
    a.ins("LDX_zp", Z_RSTART); a.ins("LDA_zp", Z_RUN); a.ins("STA_zp", 0xEA)
    a.label("fl_mark")
    a.ins("LDA_imm", 1); a.ins16("STA_absX", MARK)
    a.ins("TXA"); a.ins("CLC"); a.ins("ADC_zp", 0xE8); a.ins("TAX")
    a.ins("DEC_zp", 0xEA); a.br("BNE", "fl_mark")
    a.label("fl_done"); a.ins("RTS")

    # ================= gravity =================
    a.label("gravity")
    a.ins("LDA_imm", 0); a.ins("STA_zp", GZ_COL)
    a.label("g_col")
    a.ins("LDA_imm", 120); a.ins("CLC"); a.ins("ADC_zp", GZ_COL); a.ins("STA_zp", GZ_DEST)
    a.ins("LDA_imm", 120); a.ins("CLC"); a.ins("ADC_zp", GZ_COL); a.ins("STA_zp", GZ_READ)
    a.ins("LDY_imm", 0)
    a.label("g_row")
    a.ins("LDX_zp", GZ_READ); a.ins16("LDA_absX", BOARD)
    a.ins("CMP_imm", EMPTY); a.br("BEQ", "g_next")
    a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BNE", "g_iscap")
    a.ins("LDA_zp", GZ_READ); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", GZ_DEST)
    a.jmp("g_next")
    a.label("g_iscap")
    a.ins("LDX_zp", GZ_READ); a.ins16("LDA_absX", BOARD); a.ins("STA_zp", GZ_TILE)
    a.ins("LDA_zp", GZ_READ); a.ins("CMP_zp", GZ_DEST); a.br("BEQ", "g_nomove")
    a.ins("LDA_imm", EMPTY); a.ins16("STA_absX", BOARD)
    a.ins("LDX_zp", GZ_DEST); a.ins("LDA_zp", GZ_TILE); a.ins16("STA_absX", BOARD)
    a.label("g_nomove")
    a.ins("LDA_zp", GZ_DEST); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", GZ_DEST)
    a.label("g_next")
    a.ins("LDA_zp", GZ_READ); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", GZ_READ)
    a.ins("INY"); a.ins("CPY_imm", ROWS); a.br("BNE", "g_row")
    a.ins("INC_zp", GZ_COL); a.ins("LDA_zp", GZ_COL); a.ins("CMP_imm", COLS); a.br("BNE", "g_col")
    a.ins("RTS")
    return a.assemble()


# ----- faithful cross-check -----
def faithful_virus_cleared(board):
    """Translate NES tiles -> faithful FaithfulBoard, run resolve, return viruses cleared."""
    from drmario.faithful_game import FaithfulBoard
    fb = FaithfulBoard(ROWS, COLS)
    fb.color[:] = 0  # EMPTY
    # NES low-nibble color 0/1/2 -> faithful RED/YELLOW/BLUE (1/2/3)
    for r in range(ROWS):
        for c in range(COLS):
            t = board[r * COLS + c]
            if t == EMPTY:
                fb.color[r, c] = 0
            else:
                fb.color[r, c] = (t & 0x0F) + 1
                if is_virus(t):
                    fb.is_virus[r, c] = True
    out = fb.resolve()
    # resolve() returns (total_cleared, viruses_cleared, chain)
    try:
        return int(out[1])
    except Exception:
        return None


def rand_board(rng):
    cap = [0x40, 0x41, 0x42, 0x51, 0x52, 0x60, 0x61, 0x62]
    vir = [0xD0, 0xD1, 0xD2]
    b = [EMPTY] * 128
    for c in range(COLS):
        for r in range(ROWS):
            x = rng.random()
            if x < 0.30: b[r * COLS + c] = rng.choice(cap)
            elif x < 0.38: b[r * COLS + c] = rng.choice(vir)
    return b


def main():
    code = build_resolve()
    rng = random.Random(2026)
    cpu = Cpu(); cpu.load(BASE, code)
    have_faithful = True
    try:
        from drmario.faithful_game import FaithfulBoard  # noqa
    except Exception:
        have_faithful = False
    fails = vfails = cyc_max = cyc_tot = 0; n = 500
    for t in range(n):
        board = rand_board(rng)
        cpu.set_board(board)
        cyc = cpu.call(BASE); cyc_tot += cyc; cyc_max = max(cyc_max, cyc)
        gb, gc, gv = py_resolve(board)
        rb = cpu.get_board(); rc = cpu.zp(O_CELLS); rv = cpu.zp(O_VIR)
        if rb != gb or rc != gc or rv != gv:
            fails += 1
            if fails <= 5:
                print(f"  PY MISMATCH t={t}: cells {rc}/{gc} vir {rv}/{gv} board_eq={rb==gb}")
        if have_faithful:
            fv = faithful_virus_cleared(board)
            if rv != fv:
                vfails += 1
                if vfails <= 5:
                    print(f"  FAITHFUL vir mismatch t={t}: 6502={rv} faithful={fv}")
    print(f"routine size = {len(code)} bytes")
    print(f"vs Python column-compact resolve: {n - fails}/{n} match (fails={fails})")
    if have_faithful:
        print(f"vs faithful engine (viruses_cleared): {n - vfails}/{n} match (fails={vfails})")
    else:
        print("(faithful engine not importable here — set PYTHONPATH to faithful-sim/src)")
    print(f"cycles: max={cyc_max} avg={cyc_tot // n}  ({cyc_max/2273:.1f} vblank frames/resolve)")
    sys.exit(1 if (fails or vfails) else 0)


if __name__ == "__main__":
    main()
