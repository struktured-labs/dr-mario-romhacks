#!/usr/bin/env python3
"""NES-board depth-2 decision GOLDEN — the validation ORACLE the 6502 cartridge
search is checked against.

`decide_d2(board128, pillA, pillB, nextA, nextB) -> (best_col, best_orient)`

implements FULL depth-2 (NO first-ply pruning) over a flat 128-byte NES tile board
($0500 layout: offset = row*8 + col; EMPTY=0xFF; virus=0xD0|color; pill=0x40|color;
color = low nibble). orient: 0 = vertical (colorA on top), 1 = horizontal
(colorA left, colorB right) — the cartridge's encoding (test_slicer.py SE_ORIENT,
publish $DA: 0=horiz, 3=vert). Tie-break: strict ">" keep-first (lowest enumeration
index), matching the cart's keep-best.

It REUSES the already-validated NES-board primitives rather than reinventing them:
  - py_find_clears / py_gravity   (tests/test_resolve.py)  -- cap-1 resolve
  - golden_shape                  (tests/test_shape_eval.py) -- maxh/holes/toprisk
  - g_buried / g_readiness / g_setup (tests/test_eval_terms.py) -- progress terms
all of which cross-check 400/400 vs the faithful sim.

Score recipe (validated in tests/test_score_combine.py), integer weights = planner
floats x10 (so this is exactly 10x the faithful 'rich' eval -> identical argmax):
  leaf_shape_score(B) = 5000 - 12*maxh - 25*holes - 45*toprisk
                        + 40*setup - 30*buried + 4*readiness
  (B virus-free -> WIN sentinel).
  immediate per ply = 180*viruses_cleared + 10*cells_cleared.

Run `.venv/bin/python tests/nes_d2_golden.py` to cross-validate against the
faithful-sim CartDepth2 (eval='rich', full depth-2). Prints "AGREE: N/150".
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# --- validated NES-board building blocks (do NOT reinvent) ---
from test_resolve import py_find_clears, py_gravity
from test_shape_eval import golden_shape
from test_eval_terms import g_buried, g_readiness, g_setup

EMPTY = 0xFF
ROWS, COLS = 16, 8
WIN = 10 ** 9


# ----------------------------------------------------------------- primitives
def _first_occ(b, c):
    """Topmost occupied row in column c on the LIVE board, or ROWS if empty.
    Matches test_search.first_occ and faithful top_occupied_row."""
    for r in range(ROWS):
        if b[r * COLS + c] != EMPTY:
            return r
    return ROWS


def _virus_count(b):
    return sum(1 for t in b if t != EMPTY and (t & 0xF0) == 0xD0)


def _cap1(b):
    """One cap-1 resolve pass IN PLACE: find_clears -> if cells>0 apply gravity.
    py_find_clears mutates b (clears matched cells) and returns (cells, viruses)."""
    cells, vir = py_find_clears(b)
    if cells:
        py_gravity(b)
    return cells, vir


def _landing(b, orient, col):
    """Resting offsets (offa, offb) for (orient, col) on the LIVE board, or None
    if illegal. Mirrors test_slicer.landing_current exactly.
      vertical  (orient 0): fo=first_occ(col);            legal iff fo>=2;
                            offb=(fo-1)*8+col (bottom), offa=offb-8 (top).
      horizontal(orient 1): fo=min(fo(col),fo(col+1));    legal iff fo>=1;
                            offa=(fo-1)*8+col (left), offb=offa+1 (right)."""
    if orient == 0:
        fo = _first_occ(b, col)
        if fo < 2:
            return None
        offb = (fo - 1) * COLS + col
        return offb - COLS, offb
    else:
        if col + 1 >= COLS:
            return None
        fo = min(_first_occ(b, col), _first_occ(b, col + 1))
        if fo < 1:
            return None
        offa = (fo - 1) * COLS + col
        return offa, offa + 1


def _legal_placements(b, cA, cB):
    """All legal first/second-ply placements of a pill (low-nibble colors cA,cB),
    INCLUDING both color-swaps, enumerated in cart order: vertical cols 0..7 then
    horizontal cols 0..6. Each entry = (orient, col, offa, offb, tcolA, tcolB)
    where tcolA goes to offa (top/left) and tcolB to offb (bottom/right)."""
    out = []
    for col in range(COLS):                     # vertical, orient 0
        land = _landing(b, 0, col)
        if land is None:
            continue
        offa, offb = land
        out.append((0, col, offa, offb, cA, cB))        # colorA on top
        if cA != cB:
            out.append((0, col, offa, offb, cB, cA))     # swap: colorB on top
    for col in range(COLS - 1):                 # horizontal, orient 1
        land = _landing(b, 1, col)
        if land is None:
            continue
        offa, offb = land
        out.append((1, col, offa, offb, cA, cB))        # colorA left
        if cA != cB:
            out.append((1, col, offa, offb, cB, cA))     # swap: colorB left
    return out


def _place(b, offa, offb, ta, tb):
    nb = list(b)
    nb[offa] = 0x40 | ta
    nb[offb] = 0x40 | tb
    return nb


def leaf_shape_score(b):
    """Leaf eval of a fully-resolved board (no clear terms; those are the
    accumulated immediate rewards). WIN sentinel when virus-free."""
    if _virus_count(b) == 0:
        return WIN
    mh, ho, tr = golden_shape(b)
    setup = g_setup(b)
    buried = g_buried(b)
    ready = g_readiness(b)
    return (5000 - 12 * mh - 25 * ho - 45 * tr
            + 40 * setup - 30 * buried + 4 * ready)


# ------------------------------------------------------------------- decision
def decide_d2(board128, pillA, pillB, nextA, nextB):
    """FULL depth-2 decision. Returns (best_col, best_orient) of the argmax-value
    first-ply placement of the current pill (colors pillA,pillB), looking ahead one
    ply over the NEXT pill (nextA,nextB). orient 0=vertical, 1=horizontal."""
    best_val = None
    best_key = None
    for (orient, col, offa, offb, ta, tb) in _legal_placements(board128, pillA, pillB):
        b1 = _place(board128, offa, offb, ta, tb)
        cells1, vir1 = _cap1(b1)                     # mutates b1 -> resolved B1
        imm1 = 180 * vir1 + 10 * cells1
        if _virus_count(b1) == 0:
            val = imm1 + WIN                         # already won after ply 1
        else:
            best2 = None
            for (_o2, _c2, oa2, ob2, ta2, tb2) in _legal_placements(b1, nextA, nextB):
                b2 = _place(b1, oa2, ob2, ta2, tb2)
                cells2, vir2 = _cap1(b2)
                leaf = 180 * vir2 + 10 * cells2 + leaf_shape_score(b2)
                if best2 is None or leaf > best2:
                    best2 = leaf
            val = imm1 + (best2 if best2 is not None else leaf_shape_score(b1))
        if best_val is None or val > best_val:       # strict ">" keep-first
            best_val = val
            best_key = (col, orient)
    return best_key


# =========================== cross-validation ===============================
def _action_to_key(a):
    """Faithful CartDepth2 action int -> (col, cart_orient). Faithful actions
    0..15 are ORIENT_H (cart orient 1), 16..31 ORIENT_V (cart orient 0)."""
    return (a % 8, 1 if a < 16 else 0)


def _make_board(rng, FaithfulBoard):
    """Settled faithful board: contiguous columns of viruses + UNLINKED pill cells
    (singletons), with a few punched holes. Unlinked debris keeps the faithful
    body-gravity == NES column-compact on the resting board, so the only modelled
    divergence is the just-placed pill (a linked pair in faithful)."""
    import numpy as np
    b = FaithfulBoard(ROWS, COLS)
    b.color[:] = 0          # EMPTY
    b.is_virus[:] = False
    for c in range(COLS):
        h = rng.randint(0, ROWS)
        for r in range(ROWS - h, ROWS):
            col = rng.randint(1, 3)
            b.color[r, c] = col
            if rng.random() < 0.40:
                b.is_virus[r, c] = True
    for _ in range(rng.randint(0, 8)):
        r = rng.randint(0, ROWS - 1)
        c = rng.randint(0, COLS - 1)
        b.color[r, c] = 0
        b.is_virus[r, c] = False
    return b


def main():
    import random
    sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/src")
    sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/tmp")
    from drmario.faithful_game import FaithfulBoard, Pill
    import cart_d2_golden
    from cart_d2_golden import CartDepth2
    from xcheck_terms import faithful_to_nes

    cart_d2_golden.EVAL_MODE = "rich"           # full 'rich' progress eval
    dec = CartDepth2(topk=0)                     # topk=0 -> FULL depth-2 (no prune)

    N = 150
    rng = random.Random(20260628)
    agree = 0
    disagree = []
    for t in range(N):
        b = _make_board(rng, FaithfulBoard)
        ca, cb = rng.randint(1, 3), rng.randint(1, 3)   # faithful colors 1..3
        na, nb_ = rng.randint(1, 3), rng.randint(1, 3)
        cur, nxt = Pill(ca, cb), Pill(na, nb_)

        nes = faithful_to_nes(b)
        nes_key = decide_d2(nes, ca - 1, cb - 1, na - 1, nb_ - 1)

        a = CartDepth2(topk=0).choose(b.clone(), cur, nxt)
        if a is None:
            f_key = None
        else:
            f_key = _action_to_key(int(a))

        if nes_key == f_key:
            agree += 1
        else:
            disagree.append((t, nes_key, f_key))

    print(f"AGREE: {agree}/{N}")
    if disagree:
        print(f"disagreements: {len(disagree)}")
        for t, nk, fk in disagree[:20]:
            print(f"  t={t}: nes(col,orient)={nk}  faithful(col,orient)={fk}")
    return agree, N, disagree


if __name__ == "__main__":
    main()
