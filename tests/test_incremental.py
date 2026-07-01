#!/usr/bin/env python3
"""Incremental delta-eval: for a NON-CLEARING placement of 2 cells on a settled board,
compute the eval-term deltas in closed form from per-column info (surface + virus count),
instead of rescanning the whole board. Validates the deltas are cell-exact vs full recompute.
This is the ~10x cart speed lever (the inner second-ply loop places 2 cells on a fixed board
~28 times; recomputing the whole eval each time is the bottleneck).

Easy terms (this file): toprisk, maxh, holes, buried -- clean closed forms (color-independent).
Hard terms (setup, readiness) recompute local windows/runs -- separate file, or drop readiness.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
from test_shape_eval import golden_shape
from test_eval_terms import g_buried
from nes_d2_golden import _landing, _first_occ

EMPTY = 0xFF
ROWS, COLS = 16, 8


def base_info(b):
    """Per-column surface (first_occ) and virus count -- precomputed once per board."""
    surf = [_first_occ(b, c) for c in range(COLS)]
    vc = [sum(1 for r in range(ROWS)
              if b[r*COLS+c] != EMPTY and (b[r*COLS+c] & 0xF0) == 0xD0) for c in range(COLS)]
    return surf, vc


def delta_easy(b, orient2, col, base):
    """(maxh,holes,toprisk,buried) after placing (orient2,col) -- color-independent.
    base = (surf, vc, mh0, ho0, tr0, bur0). Assumes NON-CLEARING. Returns None if illegal."""
    land = _landing(b, orient2, col)
    if land is None:
        return None
    offa, offb = land
    surf, vc, mh0, ho0, tr0, bur0 = base
    d_tr = (offa < 24) + (offb < 24)
    new_maxh = max(mh0, ROWS - (offa >> 3), ROWS - (offb >> 3))
    if orient2 == 0:                       # vertical, both cells in col
        d_ho = 0
        d_bur = 2 * vc[col]
    else:                                  # horizontal cols col, col+1
        d_ho = abs(surf[col] - surf[col+1])
        d_bur = vc[col] + vc[col+1]
    return new_maxh, ho0 + d_ho, tr0 + d_tr, bur0 + d_bur


def _place(b, orient2, col, ta, tb):
    land = _landing(b, orient2, col)
    if land is None:
        return None
    offa, offb = land
    nb = list(b); nb[offa] = 0x40 | ta; nb[offb] = 0x40 | tb
    return nb


def _clears(nb, offa, offb):
    for o in (offa, offb):
        r, c, col = o >> 3, o & 7, nb[o] & 0x0F
        run = 1; cc = c-1
        while cc >= 0 and nb[r*COLS+cc] != EMPTY and (nb[r*COLS+cc] & 0x0F) == col: run += 1; cc -= 1
        cc = c+1
        while cc < COLS and nb[r*COLS+cc] != EMPTY and (nb[r*COLS+cc] & 0x0F) == col: run += 1; cc += 1
        if run >= 4: return True
        run = 1; rr = r-1
        while rr >= 0 and nb[rr*COLS+c] != EMPTY and (nb[rr*COLS+c] & 0x0F) == col: run += 1; rr -= 1
        rr = r+1
        while rr < ROWS and nb[rr*COLS+c] != EMPTY and (nb[rr*COLS+c] & 0x0F) == col: run += 1; rr += 1
        if run >= 4: return True
    return False


def _rand_settled(rng):
    b = [EMPTY] * 128
    for c in range(COLS):
        h = rng.randint(0, 14)
        for r in range(ROWS - h, ROWS):
            b[r*COLS+c] = (0xD0 | rng.randint(0, 2)) if rng.random() < 0.4 else (0x40 | rng.randint(0, 2))
    return b


def main():
    rng = random.Random(2026); fails = 0; tested = 0
    for t in range(3000):
        b = _rand_settled(rng)
        surf, vc = base_info(b)
        mh0, ho0, tr0 = golden_shape(b)
        bur0 = g_buried(b)
        base = (surf, vc, mh0, ho0, tr0, bur0)
        ta, tb = rng.randint(0, 2), rng.randint(0, 2)
        for orient2 in (0, 1):
            for col in range(COLS):
                land = _landing(b, orient2, col)
                if land is None:
                    continue
                offa, offb = land
                nb = _place(b, orient2, col, ta, tb)
                if _clears(nb, offa, offb):
                    continue                                   # clearing -> full path (rare)
                d = delta_easy(b, orient2, col, base)
                nmh, nho, ntr, nbur = d
                emh, eho, etr = golden_shape(nb); ebur = g_buried(nb)
                tested += 1
                if (nmh, nho, ntr, nbur) != (emh, eho, etr, ebur):
                    fails += 1
                    if fails <= 6:
                        print(f"  MISMATCH o{orient2} c{col}: got ({nmh},{nho},{ntr},{nbur}) "
                              f"exp ({emh},{eho},{etr},{ebur})")
    print(f"incremental easy deltas (maxh/holes/toprisk/buried): {tested-fails}/{tested} match")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
