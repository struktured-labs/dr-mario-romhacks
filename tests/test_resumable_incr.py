#!/usr/bin/env python3
"""Incremental resumable depth-2 machine: reuses a BASE eval computed ONCE per first-ply
(on WORK1) + a cheap per-second-ply DELTA phase, instead of a full board rescan per leaf.
~6x fewer cycles per leaf, IDENTICAL picks (delta_eval is cell-exact). Validates
(best_col,best_orient4) == decide_d2_4 over random boards.

PC states ($6140): 0 LAND1  1 CLEAR1(+14 GRAV1)  2 IMM1  3 BASE(BASE_STEP sub-phases)
  4 LAND2  5 CLEAR2(+15 GRAV2)  6 SHAPE 7 BURIED 8 READ 9 SETUP 10 COMB   (6-10 = clearing full path)
  16 DELTA (non-clearing incremental leaf)  11 VALUE 12 CMP 13 DONE.
BASE_STEP ($614D): 0 shape 1 buried 2..7 readiness(6 rgn) 8..11 setup(4 rgn, unless DROP_SETUP)
  12 base_info 13 has_virus+done.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import primitives as P
from patch_vs_cpu import Asm6502
from py65_harness import Cpu
from test_landplace import emit_landplace
import test_depth2 as D2
import test_delta6502 as D
from test_depth2 import (CUR, WORK1, LIVE, S_O1,S_C1,S_O2,S_C2, S_CA,S_CB,S_NA,S_NB,
    S_IMM_LO,S_IMM_HI, S_BL_WIN,S_BL_LO,S_BL_HI,S_BL_SET, S_ANY2, S_BV_WIN,S_BV_LO,S_BV_HI,
    S_BEST_C,S_BEST_O, CAND_WIN,CAND_LO,CAND_HI, CI_LO,CI_HI, PO,PC,PCA,PCB, decide_d2_4, _rand_board)
from test_resumable import (ST2_PC, RD_RGN, SU_RGN, ARMED, ST2_OFFA, ST2_OFFB,
    ST2_MH, ST2_HO, ST2_TR, RD_REGIONS, SU_REGIONS)

BASE_STEP = 0x614D
DROP_SETUP = False        # production cart flips this True (setup hurts L11 + is slower)


def build_resumable_incr(base=0x8000, cur=CUR, work1=WORK1, live=LIVE, mark=0x0780, sq_lo=None, sq_hi=None):
    P.BOARD = cur; P.LIVE_BOARD = cur; P.MARK = mark
    if sq_lo is not None:
        P.SQ_LO_ADDR = sq_lo; P.SQ_HI_ADDR = sq_hi
    # point the delta routines at this machine's board + offa/offb source
    D.BOARD = cur; D.DROP_SETUP = DROP_SETUP
    D.Z_OFFA = P.Z_OFFA; D.Z_OFFB = P.Z_OFFB
    # Remap delta scratch onto the NMI-safe zp pool the existing machine already clobbers
    # ($40-$66 is game-critical during NMI). Only the DROP_SETUP (production) vars matter; they
    # run only in the DELTA phase (alongside combine which owns $D6-D8), so this pool is free.
    # easy-delta vars alias readiness vars (easy completes before readiness_new runs).
    D.CURCELL, D.PCOL, D.VO, D.TVMASK = 0xCA, 0xD4, 0xD5, 0xD9
    D.RCOL, D.HRUN, D.VRUN, D.WOFF, D.RUN = 0xE0, 0xE1, 0xE2, 0xE3, 0xE4
    D.NV, D.RAYOFF, D.NI = 0xE5, 0xE6, 0xE7
    D.COLA, D.COLB, D.DT, D.SA, D.SB = 0xE0, 0xE1, 0xE2, 0xE3, 0xE4   # alias (dead during easy)
    a = Asm6502(base)

    # ---- arm ----
    a.label("arm")
    a.ins("LDA_imm",0)
    for r in (S_O1,S_C1,S_BV_WIN): a.ins16("STA_abs", r)
    a.ins("LDA_imm",0xFF); a.ins16("STA_abs", S_BEST_O)
    a.ins("LDA_imm",0); a.ins16("STA_abs", ST2_PC); a.ins("LDA_imm",1); a.ins16("STA_abs", ARMED)
    a.ins("RTS")

    # ---- step: dispatch ----
    a.label("step")
    a.ins16("LDA_abs", ARMED); a.br("BNE","st_go"); a.ins("RTS")
    a.label("st_go")
    a.ins16("LDA_abs", ST2_PC)
    for pcval,lbl in [(0,"p_land1"),(1,"p_res1"),(2,"p_imm1"),(3,"p_base"),(4,"p_land2"),(5,"p_res2"),
                      (6,"p_shape"),(7,"p_buried"),(8,"p_read"),(9,"p_setup"),(10,"p_comb"),
                      (16,"p_delta"),(17,"p_delta2"),(11,"p_value"),(12,"p_cmp"),(14,"p_grav1"),(15,"p_grav2")]:
        a.ins("CMP_imm", pcval); a.br("BNE", f"n_{pcval}"); a.jmp(lbl); a.label(f"n_{pcval}")
    a.ins("RTS")

    def setpc(v): a.ins("LDA_imm", v); a.ins16("STA_abs", ST2_PC); a.jmp("st_rts")

    # PHASE 0 LAND1
    a.label("p_land1")
    a.jsr("cp_live_cur")
    a.ins16("LDA_abs",S_O1); a.ins("STA_zp",PO); a.ins16("LDA_abs",S_C1); a.ins("STA_zp",PC)
    a.ins16("LDA_abs",S_CA); a.ins("STA_zp",PCA); a.ins16("LDA_abs",S_CB); a.ins("STA_zp",PCB)
    a.jsr("land_place"); a.ins("CMP_imm",1); a.br("BEQ","pl1_ok")
    a.ins16("INC_abs",S_C1); a.ins16("LDA_abs",S_C1); a.ins("CMP_imm",8); a.br("BEQ","lret1"); a.ins("RTS"); a.label("lret1")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_C1); a.ins16("INC_abs",S_O1)
    a.ins16("LDA_abs",S_O1); a.ins("CMP_imm",4); a.br("BEQ","lret2"); a.ins("RTS"); a.label("lret2")
    a.ins("LDA_imm",13); a.ins16("STA_abs",ST2_PC); a.jmp("p_publish")
    a.label("pl1_ok"); a.ins("LDA_zp",P.Z_OFFA); a.ins16("STA_abs",ST2_OFFA); a.ins("LDA_zp",P.Z_OFFB); a.ins16("STA_abs",ST2_OFFB); setpc(1)

    # PHASE 1 CLEAR1 (+ GRAV1 14)
    a.label("p_res1")
    a.ins16("LDA_abs",ST2_OFFA); a.ins("STA_zp",P.Z_OFFA); a.ins16("LDA_abs",ST2_OFFB); a.ins("STA_zp",P.Z_OFFB)
    a.jsr("find_clears_targeted")
    a.ins("LDA_zp",P.PASS_CELLS); a.ins("STA_zp",P.RV_CELLS)
    a.ins("LDA_zp",P.PASS_VIR); a.ins("STA_zp",P.RV_VIR)
    a.jsr("calc_imm")
    a.ins16("LDA_abs",CI_LO); a.ins16("STA_abs",S_IMM_LO); a.ins16("LDA_abs",CI_HI); a.ins16("STA_abs",S_IMM_HI)
    a.jsr("has_virus")
    a.ins("LDA_zp",P.PASS_CELLS); a.br("BEQ","cl1_nograv")
    a.ins("LDA_imm",14); a.ins16("STA_abs",ST2_PC); a.jmp("st_rts")
    a.label("cl1_nograv"); setpc(2)
    a.label("p_grav1")
    a.jsr("gravity"); setpc(2)

    # PHASE 2 IMM1
    a.label("p_imm1")
    a.ins16("LDA_abs",P.EV_VIRFLAG); a.br("BNE","pi1_notwon")
    a.ins("LDA_imm",1); a.ins16("STA_abs",CAND_WIN)
    a.ins16("LDA_abs",S_IMM_LO); a.ins16("STA_abs",CAND_LO); a.ins16("LDA_abs",S_IMM_HI); a.ins16("STA_abs",CAND_HI)
    a.ins("LDA_imm",12); a.ins16("STA_abs",ST2_PC); a.jmp("st_rts")
    a.label("pi1_notwon")
    a.jsr("cp_cur_work1")                                   # WORK1 = board after first ply
    a.ins("LDA_imm",0); a.ins16("STA_abs",BASE_STEP); setpc(3)

    # PHASE 3 BASE: compute base terms on WORK1 once (BASE_STEP sub-phases). CUR already == WORK1
    # (IMM1 did cp_cur_work1 and the base routines are read-only), so no per-step copy needed.
    a.label("p_base")
    # sub-dispatch
    a.ins16("LDA_abs",BASE_STEP); a.ins("CMP_imm",0); a.br("BNE","b_n0")
    a.jsr("shape")
    a.ins("LDA_zp",P.SH_MAXH); a.ins16("STA_abs",D.BASE_MH); a.ins("LDA_zp",P.SH_HOLES); a.ins16("STA_abs",D.BASE_HO); a.ins("LDA_zp",P.SH_TOPRISK); a.ins16("STA_abs",D.BASE_TR)
    a.jmp("b_adv")
    a.label("b_n0"); a.ins("CMP_imm",1); a.br("BNE","b_n1")
    a.jsr("buried")
    a.ins16("LDA_abs",P.EV_BUR_LO); a.ins16("STA_abs",D.BASE_BUR_LO); a.ins16("LDA_abs",P.EV_BUR_HI); a.ins16("STA_abs",D.BASE_BUR_HI)
    a.ins("LDA_imm",0); a.ins16("STA_abs",P.EV_RDY_LO); a.ins16("STA_abs",P.EV_RDY_HI)   # zero rdy accumulator
    a.jmp("b_adv")
    a.label("b_n1"); a.ins("CMP_imm",8); a.br("BCS","b_ge8")
    # steps 2..7: readiness regions 0..5
    a.ins("SEC"); a.ins("SBC_imm",2); a.ins16("STA_abs",RD_RGN)
    a.jsr("set_rd_region"); a.jsr("readiness_rg")
    a.ins16("LDA_abs",BASE_STEP); a.ins("CMP_imm",7); a.br("BNE","b_adv")
    a.ins16("LDA_abs",P.EV_RDY_LO); a.ins16("STA_abs",D.BASE_RDY_LO); a.ins16("LDA_abs",P.EV_RDY_HI); a.ins16("STA_abs",D.BASE_RDY_HI)
    a.jmp("b_adv")
    a.label("b_ge8"); a.ins("CMP_imm",12); a.br("BCS","b_ge12")
    # steps 8..11: setup regions 0..3 (skipped if DROP_SETUP)
    if DROP_SETUP:
        a.ins("LDA_imm",0); a.ins16("STA_abs",D.BASE_SET); a.jmp("b_skip_to_binfo")
    else:
        a.ins16("LDA_abs",BASE_STEP); a.ins("CMP_imm",8); a.br("BNE","b_su")
        a.ins("LDA_imm",0); a.ins16("STA_abs",P.EV_SET)
        a.label("b_su")
        a.ins16("LDA_abs",BASE_STEP); a.ins("SEC"); a.ins("SBC_imm",8); a.ins16("STA_abs",SU_RGN)
        a.jsr("set_su_region"); a.jsr("setup_rg")
        a.ins16("LDA_abs",BASE_STEP); a.ins("CMP_imm",11); a.br("BNE","b_adv")
        a.ins16("LDA_abs",P.EV_SET); a.ins16("STA_abs",D.BASE_SET); a.jmp("b_adv")
    a.label("b_ge12"); a.ins("CMP_imm",12); a.br("BNE","b_n12")
    a.jsr("base_info"); a.jmp("b_adv")
    a.label("b_n12")   # step 13: has_virus + finish
    a.jsr("has_virus")
    a.ins16("LDA_abs",P.EV_VIRFLAG); a.ins16("STA_abs",D.BASE_VIRFLAG)
    # init inner loop
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_BL_SET); a.ins16("STA_abs",S_ANY2)
    a.ins16("STA_abs",S_O2); a.ins16("STA_abs",S_C2)
    setpc(4)
    if DROP_SETUP:
        a.label("b_skip_to_binfo")   # after zeroing BASE_SET on step 8, jump straight to binfo step
        a.ins("LDA_imm",12); a.ins16("STA_abs",BASE_STEP); a.jmp("st_rts")
    a.label("b_adv")
    a.ins16("INC_abs",BASE_STEP); a.jmp("st_rts")

    # PHASE 4 LAND2
    a.label("p_land2")
    a.jsr("cp_work1_cur")
    a.ins16("LDA_abs",S_O2); a.ins("STA_zp",PO); a.ins16("LDA_abs",S_C2); a.ins("STA_zp",PC)
    a.ins16("LDA_abs",S_NA); a.ins("STA_zp",PCA); a.ins16("LDA_abs",S_NB); a.ins("STA_zp",PCB)
    a.jsr("land_place"); a.ins("CMP_imm",1); a.br("BEQ","pl2_ok")
    a.ins16("INC_abs",S_C2); a.ins16("LDA_abs",S_C2); a.ins("CMP_imm",8); a.br("BEQ","lret3"); a.ins("RTS"); a.label("lret3")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_C2); a.ins16("INC_abs",S_O2)
    a.ins16("LDA_abs",S_O2); a.ins("CMP_imm",4); a.br("BEQ","lret4"); a.ins("RTS"); a.label("lret4")
    a.ins("LDA_imm",11); a.ins16("STA_abs",ST2_PC); a.jmp("st_rts")
    a.label("pl2_ok")
    a.ins("LDA_imm",1); a.ins16("STA_abs",S_ANY2); a.ins("LDA_zp",P.Z_OFFA); a.ins16("STA_abs",ST2_OFFA); a.ins("LDA_zp",P.Z_OFFB); a.ins16("STA_abs",ST2_OFFB); setpc(5)

    # PHASE 5 CLEAR2: clearing? -> full path (6). non-clearing -> DELTA (16).
    a.label("p_res2")
    a.ins16("LDA_abs",ST2_OFFA); a.ins("STA_zp",P.Z_OFFA); a.ins16("LDA_abs",ST2_OFFB); a.ins("STA_zp",P.Z_OFFB)
    a.jsr("find_clears_targeted")
    a.ins("LDA_zp",P.PASS_CELLS); a.ins("STA_zp",P.RV_CELLS)
    a.ins("LDA_zp",P.PASS_VIR); a.ins("STA_zp",P.RV_VIR)
    a.jsr("calc_imm")
    a.ins("LDA_zp",P.PASS_CELLS); a.br("BNE","cl2_clearing")
    # non-clearing: incremental delta leaf
    a.ins("LDA_imm",16); a.ins16("STA_abs",ST2_PC); a.jmp("st_rts")
    a.label("cl2_clearing")
    # clearing: full eval on resolved board. init rdy/setup accumulators, gravity, then SHAPE.
    a.ins("LDA_imm",0); a.ins16("STA_abs",P.EV_RDY_LO); a.ins16("STA_abs",P.EV_RDY_HI)
    a.ins16("STA_abs",P.EV_SET); a.ins16("STA_abs",RD_RGN); a.ins16("STA_abs",SU_RGN)
    a.ins("LDA_imm",15); a.ins16("STA_abs",ST2_PC); a.jmp("st_rts")
    a.label("p_grav2")
    a.jsr("gravity"); setpc(6)

    # PHASE 16/17 DELTA: incremental leaf (non-clearing), split across 2 NMI frames (worst-case
    # single-phase delta was ~9.8k > budget). CUR = WORK1 + 2 cells; offa/offb in ST2_OFF*.
    # DELTA1: easy deltas + readiness NEW pass; shadow SH_* (zp dies between frames).
    a.label("p_delta")
    a.ins16("LDA_abs",ST2_OFFA); a.ins("STA_zp",P.Z_OFFA); a.ins16("LDA_abs",ST2_OFFB); a.ins("STA_zp",P.Z_OFFB)
    a.jsr("delta_terms")
    a.ins("LDA_zp",P.SH_MAXH); a.ins16("STA_abs",ST2_MH); a.ins("LDA_zp",P.SH_HOLES); a.ins16("STA_abs",ST2_HO); a.ins("LDA_zp",P.SH_TOPRISK); a.ins16("STA_abs",ST2_TR)
    setpc(17)
    # DELTA2: restore SH_*, readiness OLD pass + combine, then finish the leaf.
    a.label("p_delta2")
    a.ins16("LDA_abs",ST2_MH); a.ins("STA_zp",P.SH_MAXH); a.ins16("LDA_abs",ST2_HO); a.ins("STA_zp",P.SH_HOLES); a.ins16("LDA_abs",ST2_TR); a.ins("STA_zp",P.SH_TOPRISK)
    a.ins16("LDA_abs",ST2_OFFA); a.ins("STA_zp",P.Z_OFFA); a.ins16("LDA_abs",ST2_OFFB); a.ins("STA_zp",P.Z_OFFB)
    a.jsr("delta_finish")                                   # -> EV_SCO / EV_WIN
    a.ins16("LDA_abs",CI_LO); a.ins("CLC"); a.ins16("ADC_abs",P.EV_SCO_LO); a.ins16("STA_abs",CAND_LO)
    a.ins16("LDA_abs",CI_HI); a.ins16("ADC_abs",P.EV_SCO_HI); a.ins16("STA_abs",CAND_HI)
    a.ins16("LDA_abs",P.EV_WIN); a.ins16("STA_abs",CAND_WIN)
    a.jsr("leaf_finish"); a.jmp("st_rts")

    # PHASE 6 SHAPE / 7 BURIED / 8 READ / 9 SETUP / 10 COMB  (clearing full path)
    a.label("p_shape"); a.jsr("shape"); a.ins("LDA_zp",P.SH_MAXH); a.ins16("STA_abs",ST2_MH); a.ins("LDA_zp",P.SH_HOLES); a.ins16("STA_abs",ST2_HO); a.ins("LDA_zp",P.SH_TOPRISK); a.ins16("STA_abs",ST2_TR); setpc(7)
    a.label("p_buried"); a.jsr("buried"); setpc(8)
    a.label("p_read")
    a.ins16("LDA_abs",RD_RGN); a.ins("ASL_A"); a.ins("TAX")
    a.jsr("set_rd_region"); a.jsr("readiness_rg")
    a.ins16("INC_abs",RD_RGN); a.ins16("LDA_abs",RD_RGN); a.ins("CMP_imm",len(RD_REGIONS)); a.br("BEQ","lret5"); a.ins("RTS"); a.label("lret5")
    if DROP_SETUP:
        a.ins("LDA_imm",0); a.ins16("STA_abs",P.EV_SET); setpc(10)
    else:
        setpc(9)
    a.label("p_setup")
    a.jsr("set_su_region"); a.jsr("setup_rg")
    a.ins16("INC_abs",SU_RGN); a.ins16("LDA_abs",SU_RGN); a.ins("CMP_imm",4); a.br("BEQ","lret6"); a.ins("RTS"); a.label("lret6")
    setpc(10)
    a.label("p_comb")
    a.ins16("LDA_abs",ST2_MH); a.ins("STA_zp",P.SH_MAXH); a.ins16("LDA_abs",ST2_HO); a.ins("STA_zp",P.SH_HOLES); a.ins16("LDA_abs",ST2_TR); a.ins("STA_zp",P.SH_TOPRISK)
    a.jsr("has_virus"); a.jsr("combine")
    a.ins16("LDA_abs",CI_LO); a.ins("CLC"); a.ins16("ADC_abs",P.EV_SCO_LO); a.ins16("STA_abs",CAND_LO)
    a.ins16("LDA_abs",CI_HI); a.ins16("ADC_abs",P.EV_SCO_HI); a.ins16("STA_abs",CAND_HI)
    a.ins16("LDA_abs",P.EV_WIN); a.ins16("STA_abs",CAND_WIN)
    a.jsr("leaf_finish"); a.jmp("st_rts")

    # leaf_finish: update best_leaf with CAND, advance inner cursor, set next PC (4 or 11)
    a.label("leaf_finish")
    a.ins16("LDA_abs",S_BL_SET); a.br("BEQ","lf_setbl")
    a.ins16("LDA_abs",CAND_WIN); a.ins16("CMP_abs",S_BL_WIN); a.br("BCC","lf_adv"); a.br("BNE","lf_setbl")
    a.ins16("LDA_abs",CAND_LO); a.ins16("CMP_abs",S_BL_LO)
    a.ins16("LDA_abs",CAND_HI); a.ins16("SBC_abs",S_BL_HI)
    a.br("BVC","lf_s1"); a.ins("EOR_imm",0x80); a.label("lf_s1"); a.br("BMI","lf_adv")
    a.ins16("LDA_abs",CAND_LO); a.ins16("CMP_abs",S_BL_LO); a.br("BNE","lf_setbl")
    a.ins16("LDA_abs",CAND_HI); a.ins16("CMP_abs",S_BL_HI); a.br("BEQ","lf_adv")
    a.label("lf_setbl")
    a.ins("LDA_imm",1); a.ins16("STA_abs",S_BL_SET)
    a.ins16("LDA_abs",CAND_WIN); a.ins16("STA_abs",S_BL_WIN)
    a.ins16("LDA_abs",CAND_LO); a.ins16("STA_abs",S_BL_LO); a.ins16("LDA_abs",CAND_HI); a.ins16("STA_abs",S_BL_HI)
    a.label("lf_adv")
    a.ins16("INC_abs",S_C2); a.ins16("LDA_abs",S_C2); a.ins("CMP_imm",8); a.br("BNE","lf_more")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_C2); a.ins16("INC_abs",S_O2)
    a.ins16("LDA_abs",S_O2); a.ins("CMP_imm",4); a.br("BNE","lf_more")
    a.ins("LDA_imm",11); a.ins16("STA_abs",ST2_PC); a.ins("RTS")
    a.label("lf_more"); a.ins("LDA_imm",4); a.ins16("STA_abs",ST2_PC); a.ins("RTS")

    # PHASE 11 VALUE
    a.label("p_value")
    a.ins16("LDA_abs",S_ANY2); a.br("BNE","pv_have2")
    a.jsr("cp_work1_cur"); a.jsr("leaf_score_base")
    a.ins16("LDA_abs",P.EV_WIN); a.ins16("STA_abs",S_BL_WIN)
    a.ins16("LDA_abs",P.EV_SCO_LO); a.ins16("STA_abs",S_BL_LO); a.ins16("LDA_abs",P.EV_SCO_HI); a.ins16("STA_abs",S_BL_HI)
    a.label("pv_have2")
    a.ins16("LDA_abs",S_BL_WIN); a.ins16("STA_abs",CAND_WIN)
    a.ins16("LDA_abs",S_IMM_LO); a.ins("CLC"); a.ins16("ADC_abs",S_BL_LO); a.ins16("STA_abs",CAND_LO)
    a.ins16("LDA_abs",S_IMM_HI); a.ins16("ADC_abs",S_BL_HI); a.ins16("STA_abs",CAND_HI)
    setpc(12)

    # PHASE 12 CMP
    a.label("p_cmp")
    a.jsr("cmp_update")
    a.ins16("INC_abs", S_C1); a.ins16("LDA_abs", S_C1); a.ins("CMP_imm",8); a.br("BNE","cm_more")
    a.ins("LDA_imm",0); a.ins16("STA_abs", S_C1); a.ins16("INC_abs", S_O1)
    a.ins16("LDA_abs", S_O1); a.ins("CMP_imm",4); a.br("BNE","cm_more")
    a.ins("LDA_imm",13); a.ins16("STA_abs", ST2_PC); a.jmp("p_publish")
    a.label("cm_more"); a.ins("LDA_imm",0); a.ins16("STA_abs", ST2_PC); a.jmp("st_rts")

    # PHASE 13 publish
    a.label("p_publish")
    a.ins16("LDA_abs",S_BEST_O); a.ins("CMP_imm",0xFF); a.br("BNE","pub_ok")
    a.ins("LDA_imm",3); a.ins("STA_zp",0xDD); a.ins("STA_zp",0xDA)
    a.jmp("pub_done")
    a.label("pub_ok")
    a.ins16("LDA_abs",S_BEST_C); a.ins("STA_zp",0xDD)
    a.ins16("LDA_abs",S_BEST_O); a.ins("CMP_imm",0); a.br("BNE","pm1"); a.ins("LDA_imm",3); a.jmp("pmst")
    a.label("pm1"); a.ins("CMP_imm",1); a.br("BNE","pm2"); a.ins("LDA_imm",1); a.jmp("pmst")
    a.label("pm2"); a.ins("CMP_imm",2); a.br("BNE","pm3"); a.ins("LDA_imm",0); a.jmp("pmst")
    a.label("pm3"); a.ins("LDA_imm",2)
    a.label("pmst"); a.ins("STA_zp",0xDA)
    a.label("pub_done")
    a.ins("LDA_imm",0); a.ins16("STA_abs",ARMED)
    a.label("st_rts")
    a.ins("RTS")

    # ---- dispatch (cart entry) ----
    a.label("dispatch")
    a.ins16("LDA_abs",0x0386); a.ins("CMP_zp",0xDF)
    a.br("BCC","d_step"); a.br("BEQ","d_step")
    a.ins16("LDA_abs",0x0381); a.ins("AND_imm",0x0F); a.ins16("STA_abs",S_CA)
    a.ins16("LDA_abs",0x0382); a.ins("AND_imm",0x0F); a.ins16("STA_abs",S_CB)
    a.ins16("LDA_abs",0x039A); a.ins("AND_imm",0x0F); a.ins16("STA_abs",S_NA)
    a.ins16("LDA_abs",0x039B); a.ins("AND_imm",0x0F); a.ins16("STA_abs",S_NB)
    a.jsr("arm")
    a.label("d_step")
    a.jsr("step")
    a.ins("RTS")

    # ---- region helpers ----
    a.label("set_rd_region")
    for i,(st,en) in enumerate(RD_REGIONS):
        a.ins16("LDA_abs",RD_RGN); a.ins("CMP_imm",i); a.br("BNE",f"srr_{i}")
        a.ins("LDA_imm",st); a.ins16("STA_abs",P.RD_START); a.ins("LDA_imm",en); a.ins16("STA_abs",P.RD_END); a.ins("RTS")
        a.label(f"srr_{i}")
    a.ins("RTS")
    a.label("set_su_region")
    for i,(stp,ls,le,na) in enumerate(SU_REGIONS):
        a.ins16("LDA_abs",SU_RGN); a.ins("CMP_imm",i); a.br("BNE",f"ssr_{i}")
        a.ins("LDA_imm",stp); a.ins16("STA_abs",P.SU_STEP); a.ins("LDA_imm",ls); a.ins16("STA_abs",P.SU_LSTART)
        a.ins("LDA_imm",le); a.ins16("STA_abs",P.SU_LEND); a.ins("LDA_imm",na); a.ins16("STA_abs",P.SU_NALONG); a.ins("RTS")
        a.label(f"ssr_{i}")
    a.ins("RTS")

    # leaf_score_base: base eval (no setup unless enabled) on CUR -- rare no-legal-p2 VALUE path
    a.label("leaf_score_base")
    a.jsr("shape"); a.jsr("buried")
    a.ins("LDA_imm",0); a.ins16("STA_abs",P.EV_RDY_LO); a.ins16("STA_abs",P.EV_RDY_HI); a.ins16("STA_abs",P.EV_SET)
    for (st,en) in RD_REGIONS:
        a.ins("LDA_imm",st); a.ins16("STA_abs",P.RD_START); a.ins("LDA_imm",en); a.ins16("STA_abs",P.RD_END); a.jsr("readiness_rg")
    if not DROP_SETUP:
        for (stp,ls,le,na) in SU_REGIONS:
            a.ins("LDA_imm",stp); a.ins16("STA_abs",P.SU_STEP); a.ins("LDA_imm",ls); a.ins16("STA_abs",P.SU_LSTART)
            a.ins("LDA_imm",le); a.ins16("STA_abs",P.SU_LEND); a.ins("LDA_imm",na); a.ins16("STA_abs",P.SU_NALONG); a.jsr("setup_rg")
    a.jsr("has_virus"); a.jsr("combine"); a.ins("RTS")

    # atomic helpers + primitives + delta routines
    D2._emit_calc_imm(a); D2._emit_cmp_update(a)
    D2._emit_copy(a,"cp_live_cur",live,cur); D2._emit_copy(a,"cp_cur_work1",cur,work1); D2._emit_copy(a,"cp_work1_cur",work1,cur)
    emit_landplace(a)
    P.emit_first_occ(a); P.emit_find_clears(a); P.emit_gravity(a); P.emit_shape(a)
    P.emit_resolve_capped(a)
    P.emit_buried(a); P.emit_readiness_resumable(a); P.emit_setup(a); P.emit_setup_resumable(a)
    P.emit_has_virus(a); P.emit_combine(a)
    # delta routines (base_info, wq, row/col wins, setup_delta, vir_run2, collect, readiness_delta, delta_eval)
    D.emit_base_info(a); D.emit_wq(a); D.emit_row_wins(a); D.emit_col_wins(a); D.emit_setup_delta(a)
    D.emit_vir_run2(a); D.emit_collect_virus(a); D.emit_collect_cell(a); D.emit_clear_visit(a)
    D.emit_readiness_new(a); D.emit_readiness_old(a)
    D.emit_delta_terms(a); D.emit_delta_finish(a)
    code = a.assemble()
    return code, a.labels


def validate(nboards=12, seed=321):
    import py65_harness as _ph
    code, labels = build_resumable_incr()
    _ph.HALT = 0x8000 + len(code) + 0x100   # sentinel must sit ABOVE the (now larger) code
    cpu = Cpu(); cpu.load(0x8000, code)
    for i in range(17): cpu.mem[P.SQ_LO_ADDR+i]=(i*i)&0xFF; cpu.mem[P.SQ_HI_ADDR+i]=(i*i)>>8
    arm = 0x8000+labels["arm"]; step = 0x8000+labels["step"]
    rng = random.Random(seed); fails=0; cmax=0
    for t in range(nboards):
        b = _rand_board(rng); cA,cB,nA,nB=(rng.randint(0,2) for _ in range(4))
        cpu.set_board(b)
        for ad,v in [(S_CA,cA),(S_CB,cB),(S_NA,nA),(S_NB,nB)]: cpu.mem[ad]=v
        cpu.call(arm); n=0
        while cpu.mem[ARMED]!=0 and n<400000:
            cmax=max(cmax, cpu.call(step, max_steps=300000)); n+=1
        gc,go = decide_d2_4(b,cA,cB,nA,nB)
        bc,bo = cpu.mem[S_BEST_C], cpu.mem[S_BEST_O]
        if (bc,bo)!=(gc,go):
            fails+=1; print(f"  board {t}: incr=({bc},{bo}) golden=({gc},{go}) steps={n}")
        else:
            print(f"  board {t}: OK ({bc},{bo}) in {n} steps")
    print(f"resumable_incr(DROP_SETUP={DROP_SETUP}): {nboards-fails}/{nboards} match; max step cyc={cmax}")
    return fails==0


if __name__ == "__main__":
    ok = validate()
    sys.exit(0 if ok else 1)
