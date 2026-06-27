#!/usr/bin/env python3
"""eval_placement_deep — the depth-2 search's per-placement kernel:
backup board -> place the pill's 2 cells -> resolve (cascades) -> score shape ->
restore board. Outputs the score COMPONENTS (viruses/cells cleared + max_height/
holes/top_risk). Validated cell-for-cell against Python, including that the live
board is byte-identical after the call (non-destructive to $0500).

Uses the v18 zero-page contract (Z_OFFA=$6D, Z_OFFB=$6E, Z_TILEA=$D2, Z_TILEB=$D3)
so it drops into the existing search loop in place of eval_pair.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from py65_harness import Cpu
from patch_vs_cpu import Asm6502
from primitives import emit_all, RV_CELLS, RV_VIR, SH_MAXH, SH_HOLES, SH_TOPRISK
from test_resolve import py_resolve
from test_shape_eval import golden_shape

EMPTY = 0xFF
BOARD = 0x0500
SCRATCH = 0x0600
Z_OFFA, Z_OFFB, Z_TILEA, Z_TILEB = 0x6D, 0x6E, 0xD2, 0xD3
BASE = 0x4000


def build_kernel(targeted=False):
    a = Asm6502(BASE)
    a.label("kernel")
    # backup $0500 -> $0600
    a.ins("LDX_imm", 127)
    a.label("k_bk"); a.ins16("LDA_absX", BOARD); a.ins16("STA_absX", SCRATCH)
    a.ins("DEX"); a.br("BPL", "k_bk")
    # place the two cells
    a.ins("LDX_zp", Z_OFFA); a.ins("LDA_zp", Z_TILEA); a.ins16("STA_absX", BOARD)
    a.ins("LDX_zp", Z_OFFB); a.ins("LDA_zp", Z_TILEB); a.ins16("STA_absX", BOARD)
    # resolve + shape (operate on live board)
    a.jsr("resolve_targeted" if targeted else "resolve")
    a.jsr("shape")
    # restore $0500 from $0600
    a.ins("LDX_imm", 127)
    a.label("k_rs"); a.ins16("LDA_absX", SCRATCH); a.ins16("STA_absX", BOARD)
    a.ins("DEX"); a.br("BPL", "k_rs")
    a.ins("RTS")
    emit_all(a)
    return a.assemble()


def golden_kernel(board, offa, offb, tilea, tileb):
    b = list(board)
    b[offa] = tilea; b[offb] = tileb
    rb, cells, vir = py_resolve(b)
    maxh, holes, toprisk = golden_shape(rb)
    return vir, cells, maxh, holes, toprisk


def landing(board, orient, col):
    """Compute the two landed offsets for a placement, matching v18 land_col:
    drop in column `col`; vertical = stacked (col), horizontal = (col,col+1)."""
    def first_occ(c):
        for r in range(16):
            if board[r * 8 + c] != EMPTY:
                return r
        return 16
    if orient == 1:  # vertical: two cells stacked in `col`
        fo = first_occ(col)
        if fo < 2:
            return None
        b_off = (fo - 1) * 8 + col      # lower cell
        a_off = (fo - 2) * 8 + col      # upper cell
        return a_off, b_off
    else:            # horizontal: cells in col and col+1, share landing row
        if col >= 7:
            return None
        fo = min(first_occ(col), first_occ(col + 1))
        if fo < 1:
            return None
        r = fo - 1
        return r * 8 + col, r * 8 + col + 1


def rand_board(rng):
    # Pre-RESOLVED board (no >=4 runs), as in real play: the game resolves after
    # every pill, so the board the AI evaluates from is always run-free. This is
    # the precondition the targeted first pass relies on.
    cap = [0x40, 0x41, 0x42, 0x51, 0x52, 0x60, 0x61, 0x62]
    vir = [0xD0, 0xD1, 0xD2]
    b = [EMPTY] * 128
    for c in range(8):
        h = rng.randint(0, 13)
        for r in range(16 - h, 16):
            x = rng.random()
            b[r * 8 + c] = rng.choice(cap) if x < 0.8 else rng.choice(vir)
    b, _, _ = py_resolve(b)      # settle: removes any pre-existing runs
    return b


def run_variant(targeted):
    code = build_kernel(targeted=targeted)
    rng = random.Random(424242)
    cpu = Cpu(); cpu.load(BASE, code)
    fails = restore_fails = cyc_max = cyc_tot = n_eval = n_clear = 0
    for t in range(300):
        board = rand_board(rng)
        for orient in (0, 1):
            for col in range(8):
                land = landing(board, orient, col)
                if land is None:
                    continue
                offa, offb = land
                ca, cb = rng.randint(0, 2), rng.randint(0, 2)
                tilea, tileb = 0x40 | ca, 0x40 | cb
                cpu.set_board(board)
                cpu.set_zp(Z_OFFA, offa); cpu.set_zp(Z_OFFB, offb)
                cpu.set_zp(Z_TILEA, tilea); cpu.set_zp(Z_TILEB, tileb)
                cyc = cpu.call(BASE); cyc_tot += cyc; cyc_max = max(cyc_max, cyc); n_eval += 1
                got = (cpu.zp(RV_VIR), cpu.zp(RV_CELLS), cpu.zp(SH_MAXH),
                       cpu.zp(SH_HOLES), cpu.zp(SH_TOPRISK))
                exp = golden_kernel(board, offa, offb, tilea, tileb)
                if exp[1] > 0:
                    n_clear += 1
                if got != exp:
                    fails += 1
                    if fails <= 6:
                        print(f"  MISMATCH t={t} o={orient} col={col} targeted={targeted}: got={got} exp={exp}")
                if cpu.get_board() != board:
                    restore_fails += 1
    label = "targeted" if targeted else "full"
    print(f"[{label}] size={len(code)}B  match {n_eval-fails}/{n_eval}  "
          f"restored {n_eval-restore_fails}/{n_eval}  "
          f"cyc avg={cyc_tot//max(1,n_eval)} max={cyc_max}  "
          f"(clearing placements: {n_clear}/{n_eval})")
    return fails + restore_fails


def main():
    bad = run_variant(False) + run_variant(True)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
