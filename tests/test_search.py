#!/usr/bin/env python3
"""search_firstply — the depth-1-with-full-resolve search driver: enumerate every
placement (vertical cols 0-7, horizontal cols 0-6), evaluate each via the
validated kernel (place->resolve->shape), score with a multi-term byte eval, and
pick the best (col, orient). Validated against a Python golden that does the
identical enumeration + scoring + argmax.

This is the search skeleton the depth-2 second ply plugs into. Score (16-bit,
biased non-negative):  500 + 18*vir + cells - maxh - 3*holes - 5*toprisk.
Output: SE_BCOL($64), SE_BORIENT($65), SE_BESTLO/HI($62/$63).
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from py65_harness import Cpu
from patch_vs_cpu import Asm6502
from primitives import (emit_all, emit_kernel, emit_first_occ, BOARD, EMPTY,
                        Z_OFFA, Z_OFFB, Z_TILEA, Z_TILEB,
                        ROWS, COLS, RV_CELLS, RV_VIR, SH_MAXH, SH_HOLES, SH_TOPRISK)
from test_resolve import py_resolve
from test_shape_eval import golden_shape

BASE = 0x4000
# search zero page (clear of the primitives' $E0-$F8 and kernel inputs)
SE_ORIENT, SE_COL = 0x60, 0x61
SE_BESTLO, SE_BESTHI = 0x62, 0x63
SE_BCOL, SE_BORIENT = 0x64, 0x65
SE_SLO, SE_SHI = 0xCA, 0xCB     # pool (PhaseD score; disjoint from fc/kernel)
SE_PCA, SE_PCB = 0x68, 0x69
SE_T = 0xCC                      # pool
SE_FOL = 0xCB                    # pool (PhaseA landing; disjoint from SE_SHI)
T_LO, T_HI = 0xCD, 0xCE         # pool
# Z_OFFA/Z_OFFB/Z_TILEA/Z_TILEB imported from primitives (verified zp map)
BIAS = 500


# ---------------- Python golden ----------------
WV, WC, WH, WHO, WT = 18, 1, 1, 3, 5


def first_occ(b, c):
    for r in range(ROWS):
        if b[r * COLS + c] != EMPTY:
            return r
    return ROWS


def score_components(vir, cells, maxh, holes, toprisk):
    return BIAS + WV * vir + WC * cells - WH * maxh - WHO * holes - WT * toprisk


def golden_search(board, pca, pcb):
    best = -1
    best_key = None
    # vertical first (orient 0), then horizontal (orient 1)
    cands = []
    for c in range(COLS):
        fo = first_occ(board, c)
        if fo >= 2:
            offa = (fo - 2) * COLS + c
            offb = (fo - 1) * COLS + c
            cands.append((0, c, offa, offb))
    for c in range(COLS - 1):
        fo = min(first_occ(board, c), first_occ(board, c + 1))
        if fo >= 1:
            offa = (fo - 1) * COLS + c
            offb = (fo - 1) * COLS + c + 1
            cands.append((1, c, offa, offb))
    for orient, c, offa, offb in cands:
        b = list(board)
        b[offa] = 0x40 | pca
        b[offb] = 0x40 | pcb
        rb, cells, vir = py_resolve(b)
        maxh, holes, toprisk = golden_shape(rb)
        s = score_components(vir, cells, maxh, holes, toprisk)
        if s > best:                       # strict: keep first on tie
            best = s
            best_key = (orient, c)
    return best_key, best


# ---------------- 6502 builder ----------------
def build_search():
    a = Asm6502(BASE)
    a.label("search")
    a.ins("LDA_imm", 0); a.ins("STA_zp", SE_BESTLO); a.ins("STA_zp", SE_BESTHI)
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", SE_BCOL); a.ins("STA_zp", SE_BORIENT)
    # ---------- VERTICAL pass: orient 0, col 0..7 ----------
    a.ins("LDA_imm", 0); a.ins("STA_zp", SE_ORIENT); a.ins("STA_zp", SE_COL)
    a.label("v_loop")
    a.ins("LDX_zp", SE_COL); a.jsr("first_occ")        # A = fo
    a.ins("CMP_imm", 2); a.br("BCC", "v_skip")          # fo < 2 -> skip
    a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("STA_zp", SE_T)  # fo*8
    a.ins("LDA_zp", SE_T); a.ins("SEC"); a.ins("SBC_imm", 8)
    a.ins("CLC"); a.ins("ADC_zp", SE_COL); a.ins("STA_zp", Z_OFFB)         # (fo-1)*8+col
    a.ins("LDA_zp", Z_OFFB); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", Z_OFFA)
    a.jsr("eval_and_score")
    a.label("v_skip")
    a.ins("INC_zp", SE_COL); a.ins("LDA_zp", SE_COL); a.ins("CMP_imm", COLS); a.br("BNE", "v_loop")
    # ---------- HORIZONTAL pass: orient 1, col 0..6 ----------
    a.ins("LDA_imm", 1); a.ins("STA_zp", SE_ORIENT)
    a.ins("LDA_imm", 0); a.ins("STA_zp", SE_COL)
    a.label("h_loop")
    a.ins("LDX_zp", SE_COL); a.jsr("first_occ"); a.ins("STA_zp", SE_FOL)    # foL
    a.ins("LDX_zp", SE_COL); a.ins("INX"); a.jsr("first_occ")               # A=foR (X=col+1)
    a.ins("CMP_zp", SE_FOL); a.br("BCC", "h_useA")      # foR < foL -> use foR(A)
    a.ins("LDA_zp", SE_FOL)                              # else use foL
    a.label("h_useA")                                   # A = min(foL,foR)
    a.ins("CMP_imm", 1); a.br("BCC", "h_skip")          # fo < 1 -> skip
    a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A")      # fo*8
    a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("CLC"); a.ins("ADC_zp", SE_COL); a.ins("STA_zp", Z_OFFA)
    a.ins("LDA_zp", Z_OFFA); a.ins("CLC"); a.ins("ADC_imm", 1); a.ins("STA_zp", Z_OFFB)
    a.jsr("eval_and_score")
    a.label("h_skip")
    a.ins("INC_zp", SE_COL); a.ins("LDA_zp", SE_COL); a.ins("CMP_imm", COLS - 1); a.br("BNE", "h_loop")
    a.ins("RTS")

    # ----- eval_and_score: set tiles, JSR kernel, compute score, update best -----
    a.label("eval_and_score")
    a.ins("LDA_imm", 0x40); a.ins("ORA_zp", SE_PCA); a.ins("STA_zp", Z_TILEA)
    a.ins("LDA_imm", 0x40); a.ins("ORA_zp", SE_PCB); a.ins("STA_zp", Z_TILEB)
    a.jsr("kernel")
    # score = 500 + 18*vir + cells - maxh - 3*holes - 5*toprisk  (16-bit in SE_SLO/HI)
    a.ins("LDA_imm", BIAS & 0xFF); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_imm", (BIAS >> 8) & 0xFF); a.ins("STA_zp", SE_SHI)
    # + 18*vir  (= vir*16 + vir*2, <=144)
    a.ins("LDA_zp", RV_VIR); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("STA_zp", SE_T)
    a.ins("LDA_zp", RV_VIR); a.ins("ASL_A"); a.ins("CLC"); a.ins("ADC_zp", SE_T); a.ins("STA_zp", SE_T)
    a.ins("LDA_zp", SE_SLO); a.ins("CLC"); a.ins("ADC_zp", SE_T); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_zp", SE_SHI); a.ins("ADC_imm", 0); a.ins("STA_zp", SE_SHI)
    # + cells
    a.ins("LDA_zp", SE_SLO); a.ins("CLC"); a.ins("ADC_zp", RV_CELLS); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_zp", SE_SHI); a.ins("ADC_imm", 0); a.ins("STA_zp", SE_SHI)
    # - maxh
    a.ins("LDA_zp", SE_SLO); a.ins("SEC"); a.ins("SBC_zp", SH_MAXH); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_zp", SE_SHI); a.ins("SBC_imm", 0); a.ins("STA_zp", SE_SHI)
    # - 3*holes  (term16 = holes*2 + holes)
    a.ins("LDA_zp", SH_HOLES); a.ins("ASL_A"); a.ins("STA_zp", T_LO)   # holes*2 (<=240, no carry)
    a.ins("LDA_imm", 0); a.ins("STA_zp", T_HI)
    a.ins("LDA_zp", T_LO); a.ins("CLC"); a.ins("ADC_zp", SH_HOLES); a.ins("STA_zp", T_LO)
    a.ins("LDA_zp", T_HI); a.ins("ADC_imm", 0); a.ins("STA_zp", T_HI)
    a.ins("LDA_zp", SE_SLO); a.ins("SEC"); a.ins("SBC_zp", T_LO); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_zp", SE_SHI); a.ins("SBC_zp", T_HI); a.ins("STA_zp", SE_SHI)
    # - 5*toprisk  (= tr*4 + tr, <=120)
    a.ins("LDA_zp", SH_TOPRISK); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("STA_zp", SE_T)
    a.ins("LDA_zp", SH_TOPRISK); a.ins("CLC"); a.ins("ADC_zp", SE_T); a.ins("STA_zp", SE_T)
    a.ins("LDA_zp", SE_SLO); a.ins("SEC"); a.ins("SBC_zp", SE_T); a.ins("STA_zp", SE_SLO)
    a.ins("LDA_zp", SE_SHI); a.ins("SBC_imm", 0); a.ins("STA_zp", SE_SHI)
    # compare score(SE_S) > best(SE_BEST) unsigned 16-bit ; strict -> keep first
    a.ins("LDA_zp", SE_SHI); a.ins("CMP_zp", SE_BESTHI); a.br("BCC", "es_no"); a.br("BNE", "es_yes")
    a.ins("LDA_zp", SE_SLO); a.ins("CMP_zp", SE_BESTLO); a.br("BCC", "es_no"); a.br("BEQ", "es_no")
    a.label("es_yes")
    a.ins("LDA_zp", SE_SLO); a.ins("STA_zp", SE_BESTLO)
    a.ins("LDA_zp", SE_SHI); a.ins("STA_zp", SE_BESTHI)
    a.ins("LDA_zp", SE_COL); a.ins("STA_zp", SE_BCOL)
    a.ins("LDA_zp", SE_ORIENT); a.ins("STA_zp", SE_BORIENT)
    a.label("es_no")
    a.ins("RTS")

    emit_all(a); emit_kernel(a); emit_first_occ(a)
    return a.assemble()


def rand_board(rng):
    cap = [0x40, 0x41, 0x42, 0x51, 0x52, 0x60, 0x61, 0x62]
    vir = [0xD0, 0xD1, 0xD2]
    b = [EMPTY] * 128
    for c in range(COLS):
        h = rng.randint(0, 12)
        for r in range(ROWS - h, ROWS):
            b[r * COLS + c] = rng.choice(cap) if rng.random() < 0.8 else rng.choice(vir)
    b, _, _ = py_resolve(b)
    return b


def main():
    code = build_search()
    rng = random.Random(31337)
    cpu = Cpu(); cpu.load(BASE, code)
    fails = cyc_max = cyc_tot = 0
    n = 400
    for t in range(n):
        board = rand_board(rng)
        pca, pcb = rng.randint(0, 2), rng.randint(0, 2)
        cpu.set_board(board)
        cpu.set_zp(SE_PCA, pca); cpu.set_zp(SE_PCB, pcb)
        cyc = cpu.call(BASE, max_steps=4_000_000)
        cyc_tot += cyc; cyc_max = max(cyc_max, cyc)
        gkey, gbest = golden_search(board, pca, pcb)
        got = (cpu.zp(SE_BORIENT), cpu.zp(SE_BCOL))
        gotscore = cpu.zp(SE_BESTLO) | (cpu.zp(SE_BESTHI) << 8)
        if got != gkey or gotscore != gbest:
            fails += 1
            if fails <= 8:
                print(f"  MISMATCH t={t} pca={pca} pcb={pcb}: "
                      f"got=(o{got[0]},c{got[1]},s{gotscore}) exp=(o{gkey[0]},c{gkey[1]},s{gbest})")
    print(f"routine size = {len(code)} bytes")
    print(f"validation: {n - fails}/{n} boards pick the same placement+score (fails={fails})")
    print(f"cycles/search: max={cyc_max} avg={cyc_tot // n}  "
          f"({cyc_tot // n / 25000:.1f} frames at 25k/frame main-loop budget)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
