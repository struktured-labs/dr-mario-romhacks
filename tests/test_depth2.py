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


# ====================== ATOMIC 6502 depth-2 search ======================
# Memory: LIVE=$0500 (input), CUR=$0700 (BOARD, all sims), WORK1=$0600 (board-after
# -first-ply). State in $6120+. Validates (best_col,best_orient4) == decide_d2_4.
import primitives as P
from patch_vs_cpu import Asm6502 as _Asm
from py65_harness import Cpu as _Cpu
from test_landplace import emit_landplace

CUR, WORK1, LIVE = 0x0700, 0x0600, 0x0500
S_O1,S_C1,S_O2,S_C2 = 0x6120,0x6121,0x6122,0x6123
S_CA,S_CB,S_NA,S_NB = 0x6124,0x6125,0x6126,0x6127
S_IMM_LO,S_IMM_HI = 0x6128,0x6129
S_BL_WIN,S_BL_LO,S_BL_HI,S_BL_SET = 0x612C,0x612D,0x612E,0x612F
S_ANY2 = 0x6130
S_BV_WIN,S_BV_LO,S_BV_HI = 0x6131,0x6132,0x6133
S_BEST_C,S_BEST_O = 0x6134,0x6135
CAND_WIN,CAND_LO,CAND_HI = 0x6136,0x6137,0x6138
CI_LO,CI_HI,TMP_LO,TMP_HI = 0x613B,0x613C,0x613D,0x613E
PO,PC,PCA,PCB = 0xE2,0xE3,0xE4,0xE5


def _emit_copy(a, name, src, dst):
    a.label(name); a.ins("LDX_imm",127); a.label(name+"_l")
    a.ins16("LDA_absX",src); a.ins16("STA_absX",dst); a.ins("DEX"); a.br("BPL",name+"_l"); a.ins("RTS")


def _emit_calc_imm(a):
    # CI = 180*RV_VIR + 10*RV_CELLS  (X=count always >0)
    a.label("calc_imm")
    a.ins("LDA_zp",P.RV_VIR); a.ins16("STA_abs",P.EV_MLO); a.ins("LDA_imm",0); a.ins16("STA_abs",P.EV_MHI)
    a.ins("LDX_imm",180); a.jsr("cm_mul")
    a.ins16("LDA_abs",P.EV_PLO); a.ins16("STA_abs",TMP_LO); a.ins16("LDA_abs",P.EV_PHI); a.ins16("STA_abs",TMP_HI)
    a.ins("LDA_zp",P.RV_CELLS); a.ins16("STA_abs",P.EV_MLO); a.ins("LDA_imm",0); a.ins16("STA_abs",P.EV_MHI)
    a.ins("LDX_imm",10); a.jsr("cm_mul")
    a.ins16("LDA_abs",P.EV_PLO); a.ins("CLC"); a.ins16("ADC_abs",TMP_LO); a.ins16("STA_abs",CI_LO)
    a.ins16("LDA_abs",P.EV_PHI); a.ins16("ADC_abs",TMP_HI); a.ins16("STA_abs",CI_HI); a.ins("RTS")


def _emit_cmp_update(a):
    # if CAND (win,lo,hi) strictly > best -> best=cand, S_BEST_C/O = S_C1/S_O1
    a.label("cmp_update")
    a.ins16("LDA_abs",S_BEST_O); a.ins("CMP_imm",0xFF); a.br("BEQ","cu_take")
    a.ins16("LDA_abs",CAND_WIN); a.ins16("CMP_abs",S_BV_WIN); a.br("BCC","cu_no"); a.br("BNE","cu_take")
    # win equal: signed 16-bit CAND - BV ; strict >
    a.ins16("LDA_abs",CAND_LO); a.ins16("CMP_abs",S_BV_LO)
    a.ins16("LDA_abs",CAND_HI); a.ins16("SBC_abs",S_BV_HI)
    a.br("BVC","cu_s1"); a.ins("EOR_imm",0x80); a.label("cu_s1"); a.br("BMI","cu_no")
    # CAND >= BV; exclude equal (keep-first)
    a.ins16("LDA_abs",CAND_LO); a.ins16("CMP_abs",S_BV_LO); a.br("BNE","cu_take")
    a.ins16("LDA_abs",CAND_HI); a.ins16("CMP_abs",S_BV_HI); a.br("BEQ","cu_no")
    a.label("cu_take")
    a.ins16("LDA_abs",CAND_WIN); a.ins16("STA_abs",S_BV_WIN)
    a.ins16("LDA_abs",CAND_LO); a.ins16("STA_abs",S_BV_LO); a.ins16("LDA_abs",CAND_HI); a.ins16("STA_abs",S_BV_HI)
    a.ins16("LDA_abs",S_C1); a.ins16("STA_abs",S_BEST_C); a.ins16("LDA_abs",S_O1); a.ins16("STA_abs",S_BEST_O)
    a.label("cu_no"); a.ins("RTS")


def _emit_search(a):
    a.label("search")
    a.ins("LDA_imm",0xFF); a.ins16("STA_abs",S_BEST_O)
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_O1)
    a.label("o_outer")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_C1)
    a.label("c_outer")
    a.jsr("cp_live_cur")
    a.ins16("LDA_abs",S_O1); a.ins("STA_zp",PO); a.ins16("LDA_abs",S_C1); a.ins("STA_zp",PC)
    a.ins16("LDA_abs",S_CA); a.ins("STA_zp",PCA); a.ins16("LDA_abs",S_CB); a.ins("STA_zp",PCB)
    a.jsr("land_place"); a.ins("CMP_imm",1); a.br("BEQ","o_legal"); a.jmp("o_next")
    a.label("o_legal")
    a.jsr("resolve_capped_full"); a.jsr("calc_imm")
    a.ins16("LDA_abs",CI_LO); a.ins16("STA_abs",S_IMM_LO); a.ins16("LDA_abs",CI_HI); a.ins16("STA_abs",S_IMM_HI)
    a.jsr("has_virus"); a.ins16("LDA_abs",P.EV_VIRFLAG); a.br("BNE","o_notwon")
    # won after ply1: CAND = (1, imm1)
    a.ins("LDA_imm",1); a.ins16("STA_abs",CAND_WIN)
    a.ins16("LDA_abs",S_IMM_LO); a.ins16("STA_abs",CAND_LO); a.ins16("LDA_abs",S_IMM_HI); a.ins16("STA_abs",CAND_HI)
    a.jmp("o_cand")
    a.label("o_notwon")
    a.jsr("cp_cur_work1")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_BL_SET); a.ins16("STA_abs",S_ANY2)
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_O2)
    a.label("i_outer")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_C2)
    a.label("i_inner")
    a.jsr("cp_work1_cur")
    a.ins16("LDA_abs",S_O2); a.ins("STA_zp",PO); a.ins16("LDA_abs",S_C2); a.ins("STA_zp",PC)
    a.ins16("LDA_abs",S_NA); a.ins("STA_zp",PCA); a.ins16("LDA_abs",S_NB); a.ins("STA_zp",PCB)
    a.jsr("land_place"); a.ins("CMP_imm",1); a.br("BEQ","i_legal"); a.jmp("i_next")
    a.label("i_legal")
    a.ins("LDA_imm",1); a.ins16("STA_abs",S_ANY2)
    a.jsr("resolve_capped_full"); a.jsr("calc_imm")   # CI = imm2
    a.jsr("leaf_score")                          # EV_WIN, EV_SCO on CUR
    # leaf = (EV_WIN, imm2 + EV_SCO)
    a.ins16("LDA_abs",CI_LO); a.ins("CLC"); a.ins16("ADC_abs",P.EV_SCO_LO); a.ins16("STA_abs",CAND_LO)
    a.ins16("LDA_abs",CI_HI); a.ins16("ADC_abs",P.EV_SCO_HI); a.ins16("STA_abs",CAND_HI)
    a.ins16("LDA_abs",P.EV_WIN); a.ins16("STA_abs",CAND_WIN)
    # if not S_BL_SET or leaf > best_leaf -> best_leaf = leaf
    a.ins16("LDA_abs",S_BL_SET); a.br("BEQ","i_setbl")
    a.ins16("LDA_abs",CAND_WIN); a.ins16("CMP_abs",S_BL_WIN); a.br("BCC","i_next"); a.br("BNE","i_setbl")
    a.ins16("LDA_abs",CAND_LO); a.ins16("CMP_abs",S_BL_LO)
    a.ins16("LDA_abs",CAND_HI); a.ins16("SBC_abs",S_BL_HI)
    a.br("BVC","i_s1"); a.ins("EOR_imm",0x80); a.label("i_s1"); a.br("BMI","i_next")
    # >= ; keep-first so only strict > : exclude equal
    a.ins16("LDA_abs",CAND_LO); a.ins16("CMP_abs",S_BL_LO); a.br("BNE","i_setbl")
    a.ins16("LDA_abs",CAND_HI); a.ins16("CMP_abs",S_BL_HI); a.br("BEQ","i_next")
    a.label("i_setbl")
    a.ins("LDA_imm",1); a.ins16("STA_abs",S_BL_SET)
    a.ins16("LDA_abs",CAND_WIN); a.ins16("STA_abs",S_BL_WIN)
    a.ins16("LDA_abs",CAND_LO); a.ins16("STA_abs",S_BL_LO); a.ins16("LDA_abs",CAND_HI); a.ins16("STA_abs",S_BL_HI)
    a.label("i_next")
    a.ins16("INC_abs",S_C2); a.ins16("LDA_abs",S_C2); a.ins("CMP_imm",8); a.br("BEQ","i_ocheck"); a.jmp("i_inner")
    a.label("i_ocheck")
    a.ins16("INC_abs",S_O2); a.ins16("LDA_abs",S_O2); a.ins("CMP_imm",4); a.br("BEQ","i_done"); a.jmp("i_outer")
    a.label("i_done")
    # value = imm1 + best_leaf (any2) else imm1 + leaf_score(WORK1)
    a.ins16("LDA_abs",S_ANY2); a.br("BNE","o_have2")
    a.jsr("cp_work1_cur"); a.jsr("leaf_score")
    a.ins16("LDA_abs",P.EV_WIN); a.ins16("STA_abs",S_BL_WIN)
    a.ins16("LDA_abs",P.EV_SCO_LO); a.ins16("STA_abs",S_BL_LO); a.ins16("LDA_abs",P.EV_SCO_HI); a.ins16("STA_abs",S_BL_HI)
    a.label("o_have2")
    # CAND = (S_BL_WIN, imm1 + S_BL_score)
    a.ins16("LDA_abs",S_BL_WIN); a.ins16("STA_abs",CAND_WIN)
    a.ins16("LDA_abs",S_IMM_LO); a.ins("CLC"); a.ins16("ADC_abs",S_BL_LO); a.ins16("STA_abs",CAND_LO)
    a.ins16("LDA_abs",S_IMM_HI); a.ins16("ADC_abs",S_BL_HI); a.ins16("STA_abs",CAND_HI)
    a.label("o_cand")
    a.jsr("cmp_update")
    a.label("o_next")
    a.ins16("INC_abs",S_C1); a.ins16("LDA_abs",S_C1); a.ins("CMP_imm",8); a.br("BEQ","o_ocheck"); a.jmp("c_outer")
    a.label("o_ocheck")
    a.ins16("INC_abs",S_O1); a.ins16("LDA_abs",S_O1); a.ins("CMP_imm",4); a.br("BEQ","o_done"); a.jmp("o_outer")
    a.label("o_done")
    a.ins("RTS")


def build_search():
    P.BOARD = CUR; P.LIVE_BOARD = CUR; P.MARK = 0x0780
    a = _Asm(0x8000)
    _emit_search(a)
    _emit_calc_imm(a); _emit_cmp_update(a)
    _emit_copy(a, "cp_live_cur", LIVE, CUR)
    _emit_copy(a, "cp_cur_work1", CUR, WORK1)
    _emit_copy(a, "cp_work1_cur", WORK1, CUR)
    emit_landplace(a)
    P.emit_first_occ(a); P.emit_find_clears(a); P.emit_gravity(a); P.emit_shape(a)
    P.emit_resolve_capped_full(a); P.emit_eval(a)
    code = a.assemble()
    return code, a.labels


def validate_search(nboards=8, seed=321):
    import random
    code, labels = build_search()
    cpu = _Cpu(); cpu.load(0x8000, code)
    for i in range(17):
        cpu.mem[P.SQ_LO_ADDR+i] = (i*i)&0xFF; cpu.mem[P.SQ_HI_ADDR+i] = (i*i)>>8
    addr = 0x8000 + labels["search"]
    rng = random.Random(seed); fails = 0
    for t in range(nboards):
        b = _rand_board(rng)
        cA,cB,nA,nB = (rng.randint(0,2) for _ in range(4))
        cpu.set_board(b)   # writes $0500 (LIVE)
        cpu.set_zp(0,0)  # noop
        for addr_,val in [(S_CA,cA),(S_CB,cB),(S_NA,nA),(S_NB,nB)]:
            cpu.mem[addr_] = val
        cpu.call(addr, max_steps=60_000_000)
        gc, go = decide_d2_4(b, cA, cB, nA, nB)
        bc, bo = cpu.mem[S_BEST_C], cpu.mem[S_BEST_O]
        if (bc,bo) != (gc,go):
            fails += 1
            print(f"  board {t}: 6502=({bc},{bo}) golden=({gc},{go})")
    print(f"search: {nboards-fails}/{nboards} match best (col,orient4)")
    return fails == 0
