#!/usr/bin/env python3
"""Atomic 6502 depth-2 search, validated cell-exact in py65 against a 4-STATE-orient
golden built on the agent's validated nes_d2_golden primitives.

The cart must place all 4 rotational states (color swaps mandatory: no-swap craters
L11 67%->40%). orient4 encoding (this file's + the 6502's convention):
  0 = V, A-top   (offa=top=colorA, offb=bottom=colorB)
  1 = V, B-top   (swap: offa=top=colorB, offb=bottom=colorA)
  2 = H, A-left  (offa=left=colorA, offb=right=colorB)
  3 = H, B-left  (swap: offa=left=colorB, offb=right=colorA)
Maps to NES $03A5 via the skill table {0:3(V a-top), 1:1(V b-top), 2:0(H a,b), 3:2(H b,a)}.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nes_d2_golden import (_legal_placements, _place, _cap1, leaf_shape_score,
                           _virus_count, decide_d2, WIN)

EMPTY = 0xFF
ROWS, COLS = 16, 8


def _orient4(orient2, ta, tb, cA, cB):
    if orient2 == 0:                      # vertical
        return 0 if (ta, tb) == (cA, cB) else 1
    return 2 if (ta, tb) == (cA, cB) else 3   # horizontal


def decide_d2_4(board, cA, cB, nA, nB):
    """Full depth-2, returns (best_col, best_orient4). Mirrors decide_d2 exactly
    (same search + tie-break) but tracks the 4-state orientation incl. swap."""
    best_val = None
    best_key = None
    for (orient, col, offa, offb, ta, tb) in _legal_placements(board, cA, cB):
        b1 = _place(board, offa, offb, ta, tb)
        cells1, vir1 = _cap1(b1)
        imm1 = 180 * vir1 + 10 * cells1
        if _virus_count(b1) == 0:
            val = imm1 + WIN
        else:
            best2 = None
            for (_o2, _c2, oa2, ob2, ta2, tb2) in _legal_placements(b1, nA, nB):
                b2 = _place(b1, oa2, ob2, ta2, tb2)
                cells2, vir2 = _cap1(b2)
                leaf = 180 * vir2 + 10 * cells2 + leaf_shape_score(b2)
                if best2 is None or leaf > best2:
                    best2 = leaf
            val = imm1 + (best2 if best2 is not None else leaf_shape_score(b1))
        if best_val is None or val > best_val:
            best_val = val
            best_key = (col, _orient4(orient, ta, tb, cA, cB))
    return best_key


def _rand_board(rng):
    b = [EMPTY] * 128
    for c in range(COLS):
        h = rng.randint(0, ROWS)
        for r in range(ROWS - h, ROWS):
            roll = rng.random(); col = rng.randint(0, 2)
            b[r * COLS + c] = (0xD0 | col) if roll < 0.4 else (0x40 | col)
    for _ in range(rng.randint(0, 8)):
        b[rng.randint(0, 127)] = EMPTY
    return b


def _selfcheck():
    """Confirm decide_d2_4 collapses to the validated decide_d2 (col + V/H)."""
    import random
    rng = random.Random(5)
    agree = 0; n = 150
    for _ in range(n):
        b = _rand_board(rng)
        cA, cB = rng.randint(0, 2), rng.randint(0, 2)
        nA, nB = rng.randint(0, 2), rng.randint(0, 2)
        c4, o4 = decide_d2_4(b, cA, cB, nA, nB)
        c2, o2 = decide_d2(b, cA, cB, nA, nB)
        o4_as_o2 = 0 if o4 in (0, 1) else 1
        if (c4, o4_as_o2) == (c2, o2):
            agree += 1
    print(f"selfcheck decide_d2_4 vs decide_d2: {agree}/{n} (col+V/H must match)")
    return agree == n


if __name__ == "__main__":
    ok = _selfcheck()
    sys.exit(0 if ok else 1)
