#!/usr/bin/env python3
"""128B-board INTEGER depth-3 golden for the copro port (the reference emit_search_d3 must
match cell-exact). depth-3 = topk1 ply1-prune + topk2 ply2-prune + expectimax over a pill
subset, with the ext+pollute leaf eval (x10 firmware weights). Cross-checked vs the faithful
CartDepth3 (the 91.7% config) -- agreement is modulo integer-vs-float mean rounding."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from nes_d2_golden import (_legal_placements, _landing, _place, _cap1, _virus_count,
                           py_gravity)
from test_shape_eval import golden_shape
from test_eval_terms import g_buried, g_setup
from test_incremental import g_readiness_ext

WIN = 30000   # firmware 16-bit-fitting win bonus (dominates max-non-win ~16600, +imm < 32767)
DISC_SHIFT = None   # temporal discount: val = imm1 + leaf1 + ((best2-leaf1) >> DISC_SHIFT).
                    # None = off (classic). 1 = d=0.5 (fixes dual-end park pathology; +14% solo efficiency).
USE_VRDY = True
RESOLVE = "targeted"   # deploy config (isolation 12/12); "full" only for older cross-checks


def _cap1_targeted(b, offa, offb):
    """One TARGETED cap-1 resolve IN PLACE, mirroring the 6502 resolve_capped:
    find_clears_targeted (scan only rowA/colA/rowB/colB of the placed cells, mark
    runs>=4 on low-nibble color) + apply + ONE gravity, no cascade loop."""
    mark = set()
    for off, step, cnt in ((offa & 0xF8, 1, 8), (offa & 0x07, 8, 16),
                           (offb & 0xF8, 1, 8), (offb & 0x07, 8, 16)):
        run = 0; rstart = off; mcol = None; o = off
        for _ in range(cnt):
            x = b[o]
            if x == 0xFF:
                if run >= 4:
                    mark.update(rstart + k * step for k in range(run))
                run = 0; mcol = None
            elif (x & 0x0F) != mcol:
                if run >= 4:
                    mark.update(rstart + k * step for k in range(run))
                mcol = x & 0x0F; rstart = o; run = 1
            else:
                run += 1
            o += step
        if run >= 4:
            mark.update(rstart + k * step for k in range(run))
    cells = len(mark)
    vir = sum(1 for k in mark if (b[k] & 0xF0) == 0xD0)
    for k in mark:
        b[k] = 0xFF
    if cells:
        py_gravity(b)
    return cells, vir


def _resolve(b, offa, offb):
    if RESOLVE == "targeted":
        return _cap1_targeted(b, offa, offb)
    return _cap1(b)


def _pollution(b):
    total = 0
    for idx in range(128):
        if (b[idx] & 0xF0) != 0xD0:
            continue
        v = b[idx] & 0x0F; r = idx >> 3; c = idx & 7
        for cc in range(8):
            if cc == c:
                continue
            x = b[r * 8 + cc]
            if x != 0xFF and (x & 0xF0) != 0xD0 and (x & 0x0F) != v:
                total += 1
        for rr in range(16):
            if rr == r:
                continue
            x = b[rr * 8 + c]
            if x != 0xFF and (x & 0xF0) != 0xD0 and (x & 0x0F) != v:
                total += 1
    return total


def _vrdy(b):
    total = 0
    for idx in range(128):
        if (b[idx] & 0xF0) != 0xD0:
            continue
        v = b[idx] & 0x0F; r = idx >> 3; c = idx & 7
        run = 1; rr = r - 1
        while rr >= 0 and b[rr * 8 + c] != 0xFF and (b[rr * 8 + c] & 0x0F) == v:
            run += 1; rr -= 1
        rr = r + 1
        while rr < 16 and b[rr * 8 + c] != 0xFF and (b[rr * 8 + c] & 0x0F) == v:
            run += 1; rr += 1
        total += run * run
    return total


def leaf_d3(b):
    if _virus_count(b) == 0:
        return WIN
    mh, ho, tr = golden_shape(b)
    spawn = sum(1 for off in (3, 4, 11, 12, 19, 20, 27, 28) if b[off] != 0xFF)
    s = (5000 - 12 * mh - 20 * ho - 90 * tr - 150 * spawn
         + 60 * g_setup(b) - 30 * g_buried(b) + 12 * g_readiness_ext(b) - 6 * _pollution(b))
    if USE_VRDY:
        s += 12 * _vrdy(b)
    return s


def _imm(cells, vir):
    return 180 * vir + 10 * cells


def _placements4(b, cA, cB):
    """6502-faithful enumeration: orient4-major (0=V A-top, 1=V B-top, 2=H A-left,
    3=H B-left), col 0..7 inner, INCLUDING same-color swap duplicates -- the 6502
    evaluates o4=1/3 even when cA==cB, and those dup entries occupy top-k slots."""
    out = []
    for o4 in range(4):
        orient = 0 if o4 < 2 else 1
        swap = (o4 & 1) == 1
        for col in range(8):
            land = _landing(b, orient, col)
            if land is None:
                continue
            offa, offb = land
            ta, tb = (cB, cA) if swap else (cA, cB)
            out.append((o4, col, offa, offb, ta, tb))
    return out


def _jitter(seed, o4, col):
    """Seeded tie-break jitter, bit-exact vs the 6502: t = seed ^ ((o4<<3)|col);
    j = (t ^ (t>>3)) & 3. seed==0 -> no jitter (exact deterministic search)."""
    if seed == 0:
        return 0
    t = (seed ^ ((o4 << 3) | col)) & 0xFF
    return (t ^ (t >> 3)) & 3


def decide_d3(board, pA, pB, nA, nB, topk1=8, topk2=8, third=None, seed=0):
    """Returns (col, orient4) exactly as the 6502 emit_search_d3 does (same enumeration
    order, same tie-breaks: strictly-greater keep-first). seed!=0 adds the per-candidate
    +0..3 val1 jitter (per-copro tie-break divergence; same strategy)."""
    pills3 = third if third is not None else [(x, y) for x in range(3) for y in range(3)]
    first = []
    for (o4, col, offa, offb, ta, tb) in _placements4(board, pA, pB):
        b1 = _place(board, offa, offb, ta, tb); cells1, vir1 = _resolve(b1, offa, offb)
        imm1 = _imm(cells1, vir1)
        first.append((imm1 + leaf_d3(b1), imm1, b1, col, o4))
    if not first:
        return None
    if topk1 > 0:                                 # 6502 does full ply1 (topk1=0): no sort,
        first.sort(key=lambda t: t[0], reverse=True)   # preserve enumeration tie-break order
        shortlist = first[:topk1]
    else:
        shortlist = first
    best_val = None; best_key = None
    for (_k1, imm1, b1, col, o4) in shortlist:
        if _virus_count(b1) == 0:
            val = imm1 + WIN
        else:
            second = []
            for (_o2, _c2, oa2, ob2, ta2, tb2) in _placements4(b1, nA, nB):
                b2 = _place(b1, oa2, ob2, ta2, tb2); cells2, vir2 = _resolve(b2, oa2, ob2)
                imm2 = _imm(cells2, vir2)
                second.append((imm2 + leaf_d3(b2), imm2, b2))
            if not second:
                val = imm1 + leaf_d3(b1)
            else:
                second.sort(key=lambda t: t[0], reverse=True)   # stable == 6502 first-max scan
                keep = second[:topk2] if topk2 > 0 else second
                best2 = None
                for (_k2, imm2, b2) in keep:
                    if _virus_count(b2) == 0:
                        v2 = imm2 + WIN                       # won at ply2 -> skip expectimax
                    else:
                        tot = 0
                        for (x, y) in pills3:
                            best3 = None
                            for (_o3, _c3, oa3, ob3, ta3, tb3) in _placements4(b2, x, y):
                                b3 = _place(b2, oa3, ob3, ta3, tb3); cells3, vir3 = _resolve(b3, oa3, ob3)
                                v3 = _imm(cells3, vir3) + leaf_d3(b3)
                                if best3 is None or v3 > best3:
                                    best3 = v3
                            tot += best3 if best3 is not None else leaf_d3(b2)
                        v2 = imm2 + tot // len(pills3)
                    if best2 is None or v2 > best2:
                        best2 = v2
                if DISC_SHIFT is None:
                    val = imm1 + best2
                else:
                    leaf1_ = _k1 - imm1
                    val = imm1 + leaf1_ + ((best2 - leaf1_) >> DISC_SHIFT)
        val += _jitter(seed, o4, col)
        if best_val is None or val > best_val:
            best_val = val; best_key = (col, o4)
    return best_key


def main():
    import random
    global USE_VRDY
    sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/src")
    sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/tmp")
    from drmario.faithful_game import FaithfulBoard, Pill
    from nes_d2_golden import _make_board, _action_to_key
    from xcheck_terms import faithful_to_nes
    import cart_regime as G

    TOPK1, TOPK2 = 8, 8
    G.EVAL_MODE = "endgame"; G.GRAVITY_MODE = "compact"; G.RESOLVE_MODE = "full"; G.LEVEL = 11
    G.WH = 1.2; G.WTR = 9.0; G.W_SPAWN = 15.0; G.WHO = 2.0
    G.W_SETUP = 6.0; G.W_READY = 1.2; G.W_VRDY = 1.2 if USE_VRDY else 0.0; G.W_BURIED = 3.0
    G.W_POLLUTE = 0.6; G.USE_EXT_RDY = True; G.THIRD_SUBSET = None

    N = 60; rng = random.Random(303); agree = 0; dis = []
    for t in range(N):
        b = _make_board(rng, FaithfulBoard)
        ca, cb = rng.randint(1, 3), rng.randint(1, 3); na, nb_ = rng.randint(1, 3), rng.randint(1, 3)
        nes = faithful_to_nes(b)
        nk = decide_d3(nes, ca - 1, cb - 1, na - 1, nb_ - 1, TOPK1, TOPK2)
        a = G.CartDepth3(topk=TOPK1, topk2=TOPK2).choose(b.clone(), Pill(ca, cb), Pill(na, nb_))
        fk = None if a is None else _action_to_key(int(a))
        if nk == fk:
            agree += 1
        else:
            dis.append((t, nk, fk))
    print(f"decide_d3 vs CartDepth3 (topk1={TOPK1} topk2={TOPK2} 9-pill, ext+pollute): AGREE {agree}/{N}")
    for t, nk, fk in dis[:12]:
        print(f"  t={t}: nes={nk} faithful={fk}")


if __name__ == "__main__":
    main()
