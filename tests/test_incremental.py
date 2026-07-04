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
from test_eval_terms import g_buried, g_setup, g_readiness
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


def _col(b, o):
    return -1 if b[o] == EMPTY else (b[o] & 0x0F)

def _isvir(b, o):
    return b[o] != EMPTY and (b[o] & 0xF0) == 0xD0

def _window_q(nb, cells, ends):
    """1 if the 3-cell window is a same-color run touching a same-color virus (matches g_setup)."""
    o0, o1, o2 = cells
    c0 = _col(nb, o0)
    if c0 == -1 or _col(nb, o1) != c0 or _col(nb, o2) != c0:
        return 0
    if any(_isvir(nb, o) and (nb[o] & 0x0F) == c0 for o in cells):
        return 1
    for e in ends:
        if e is not None and _isvir(nb, e) and (nb[e] & 0x0F) == c0:
            return 1
    return 0

def _affected_windows(off):
    """Row+col length-3 windows CONTAINING off (with their end-adjacent cells)."""
    r, c = off >> 3, off & 7
    wins = []
    for i in range(max(0, c-2), min(c, COLS-3) + 1):        # row windows
        base = r*COLS + i
        wins.append(((base, base+1, base+2),
                     (base-1 if i > 0 else None, base+3 if i+3 < COLS else None)))
    for j in range(max(0, r-2), min(r, ROWS-3) + 1):        # col windows
        base = j*COLS + c
        wins.append(((base, base+COLS, base+2*COLS),
                     (base-COLS if j > 0 else None, base+3*COLS if j+3 < ROWS else None)))
    return wins

def setup_delta(nb, offa, offb, base_setup):
    """base_setup + (new run-of-3-touching-virus windows through offa/offb). Old contribution
    was 0 (offa/offb were empty). Assumes NON-CLEARING (no >=4 runs form)."""
    seen = set(); d = 0
    for off in (offa, offb):
        for cells, ends in _affected_windows(off):
            if cells in seen:
                continue
            seen.add(cells)
            d += _window_q(nb, cells, ends)
    return base_setup + d


def _vir_run2(b, o):
    """Readiness of one virus: max(horiz run, vert run) squared."""
    color = b[o] & 0x0F; r, c = o >> 3, o & 7
    hr = 1; cc = c-1
    while cc >= 0 and _col(b, r*COLS+cc) == color: hr += 1; cc -= 1
    cc = c+1
    while cc < COLS and _col(b, r*COLS+cc) == color: hr += 1; cc += 1
    vr = 1; rr = r-1
    while rr >= 0 and _col(b, rr*COLS+c) == color: vr += 1; rr -= 1
    rr = r+1
    while rr < ROWS and _col(b, rr*COLS+c) == color: vr += 1; rr += 1
    return max(hr, vr) ** 2

def _vir_run2_ext(b, o):
    """Extendability-aware readiness of one virus: per direction, run^2 only if the
    contiguous span of (same-color OR empty) cells through the virus is >= 4; else 0.
    max over the two directions."""
    color = b[o] & 0x0F; r, c = o >> 3, o & 7
    # horizontal run
    hr = 1; cc = c - 1
    while cc >= 0 and _col(b, r*COLS+cc) == color: hr += 1; cc -= 1
    lo = cc
    while lo >= 0 and (b[r*COLS+lo] == EMPTY or _col(b, r*COLS+lo) == color): lo -= 1
    cc = c + 1
    while cc < COLS and _col(b, r*COLS+cc) == color: hr += 1; cc += 1
    hi = cc
    while hi < COLS and (b[r*COLS+hi] == EMPTY or _col(b, r*COLS+hi) == color): hi += 1
    h_ok = (hi - lo - 1) >= 4
    # vertical run
    vr = 1; rr = r - 1
    while rr >= 0 and _col(b, rr*COLS+c) == color: vr += 1; rr -= 1
    vlo = rr
    while vlo >= 0 and (b[vlo*COLS+c] == EMPTY or _col(b, vlo*COLS+c) == color): vlo -= 1
    rr = r + 1
    while rr < ROWS and _col(b, rr*COLS+c) == color: vr += 1; rr += 1
    vhi = rr
    while vhi < ROWS and (b[vhi*COLS+c] == EMPTY or _col(b, vhi*COLS+c) == color): vhi += 1
    v_ok = (vhi - vlo - 1) >= 4
    return max(hr*hr if h_ok else 0, vr*vr if v_ok else 0)


def g_readiness_ext(b):
    """Board-wide extendability-aware readiness (golden)."""
    return sum(_vir_run2_ext(b, o) for o in range(128)
               if b[o] != EMPTY and (b[o] & 0xF0) == 0xD0)


def readiness_ext_delta(b, nb, offa, offb, base_rdy):
    """Ext readiness delta: a placed cell can change any virus in its ROW or COLUMN
    (runs via contiguity, spans via occupancy). Recompute those viruses old vs new."""
    affected = set()
    for off in (offa, offb):
        r, c = off >> 3, off & 7
        for cc in range(COLS):
            o = r*COLS + cc
            if _isvir(b, o): affected.add(o)
        for rr in range(ROWS):
            o = rr*COLS + c
            if _isvir(b, o): affected.add(o)
    d = 0
    for o in affected:
        d += _vir_run2_ext(nb, o) - _vir_run2_ext(b, o)
    return base_rdy + d


def _vir_vrun2(b, o):
    """Vertical-only readiness of one virus: vertical same-color run squared."""
    color = b[o] & 0x0F; r, c = o >> 3, o & 7
    vr = 1; rr = r - 1
    while rr >= 0 and _col(b, rr*COLS+c) == color: vr += 1; rr -= 1
    rr = r + 1
    while rr < ROWS and _col(b, rr*COLS+c) == color: vr += 1; rr += 1
    return vr * vr


def g_vreadiness(b):
    return sum(_vir_vrun2(b, o) for o in range(128)
               if b[o] != EMPTY and (b[o] & 0xF0) == 0xD0)


def vreadiness_delta(b, nb, offa, offb, base_vrdy):
    """Vertical runs change only for same-color viruses vertically CONTIGUOUS to a placed
    cell (walk up/down through same-color cells from each placed cell)."""
    affected = set()
    for off in (offa, offb):
        c = off & 7; X = nb[off] & 0x0F
        for step in (-COLS, COLS):
            o = off + step
            while 0 <= o < 128 and (o & 7) == c and nb[o] != EMPTY and (nb[o] & 0x0F) == X:
                if _isvir(nb, o): affected.add(o)
                o += step
    d = 0
    for o in affected:
        d += _vir_vrun2(nb, o) - _vir_vrun2(b, o)
    return base_vrdy + d


def readiness_delta(b, nb, offa, offb, base_rdy):
    """Only viruses in the placed cells' row/col with the placed color can change their run.
    Recompute those viruses' run^2 on old vs new; sum the deltas. (Non-contiguous ones delta 0.)"""
    affected = set()
    for off in (offa, offb):
        r, c = off >> 3, off & 7; X = nb[off] & 0x0F
        for cc in range(COLS):
            o = r*COLS + cc
            if _isvir(b, o) and (b[o] & 0x0F) == X: affected.add(o)
        for rr in range(ROWS):
            o = rr*COLS + c
            if _isvir(b, o) and (b[o] & 0x0F) == X: affected.add(o)
    d = 0
    for o in affected:
        d += _vir_run2(nb, o) - _vir_run2(b, o)
    return base_rdy + d


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
        set0 = g_setup(b)
        rdy0 = g_readiness(b)
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
                nmh, nho, ntr, nbur = delta_easy(b, orient2, col, base)
                nset = setup_delta(nb, offa, offb, set0)
                nrdy = readiness_delta(b, nb, offa, offb, rdy0)
                emh, eho, etr = golden_shape(nb); ebur = g_buried(nb); eset = g_setup(nb); erdy = g_readiness(nb)
                tested += 1
                if (nmh, nho, ntr, nbur, nset, nrdy) != (emh, eho, etr, ebur, eset, erdy):
                    fails += 1
                    if fails <= 6:
                        print(f"  MISMATCH o{orient2} c{col}: got (mh{nmh},ho{nho},tr{ntr},bur{nbur},set{nset},rdy{nrdy}) "
                              f"exp (mh{emh},ho{eho},tr{etr},bur{ebur},set{eset},rdy{erdy})")
    print(f"incremental deltas (maxh/holes/toprisk/buried/setup/READINESS -- ALL 6): {tested-fails}/{tested} match")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
