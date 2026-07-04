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

# ---- frame-packing (LEVER: run multiple phases per 'step' call, staying <=budget) ----
# BUDGET is a per-'step'-call cycle allowance in units of 64 cycles. Before running each
# phase, we look up its (static, per-PC / per-BASE_STEP) MAX cost and only run it if the
# remaining budget still covers it (the FIRST phase of a call always runs). Because each
# cost >= ceil((measured_max+MARGIN)/64), a packed group of N>=2 phases costs at most
# 64*PACK_LIMIT - MARGIN*N actual cycles <= 64*125 - 512 = 7488 cyc << 8086. Single
# phases whose own cost exceeds the budget (PC1/PC5 ~8.2k) simply run solo, exactly as
# before, so MAX_STEP_CYC is unchanged. Purely control-flow: same phases, same order,
# same data -> identical picks.
PK_BUDGET = 0x614E        # remaining budget this step call (units of 64 cyc)
PK_FIRST  = 0x614F        # 0 until the first phase of this call has run
PK_COST   = 0x6144        # scratch: cost (units) of the phase about to run
PACK_LIMIT = 125          # 125*64 = 8000 cyc ceiling for a packed group
_PK_MARGIN = 256          # per-phase cycle head-room folded into each static cost


def _pack_cost_tables(drop_setup):
    """Static per-PC and per-BASE_STEP cost tables (units of 64 cyc), padded with
    _PK_MARGIN so a phase never overruns its budgeted cost. Measured maxima below come
    from the DROP_SETUP-specific frame sweeps (True: seed7 x40; False: seed321 x12)."""
    HUGE = 200            # unused/solo-only entries (> PACK_LIMIT => never packed)
    def u(cyc):
        return min(HUGE, (cyc + _PK_MARGIN + 63) // 64)
    if drop_setup:
        pc_max = {0:2936,1:8204,2:1861,3:0,4:2962,5:8164,6:5323,7:6019,8:4719,9:8192,
                  10:5757,11:139,12:242,13:8192,14:6775,15:6884,16:3193,17:7321}
        base_max = {0:5353,1:6057,2:2448,3:2705,4:3339,5:4095,6:4717,7:4352,8:80,
                    9:8192,10:8192,11:8192,12:7239,13:417}
    else:
        pc_max = {0:2936,1:8368,2:1861,3:0,4:2962,5:6601,6:5491,7:5349,8:3624,9:5331,
                  10:5727,11:139,12:222,13:8192,14:6307,15:6314,16:4429,17:7033}
        base_max = {0:5515,1:5408,2:1332,3:2040,4:3138,5:2978,6:3225,7:3629,8:3105,
                    9:5340,10:4197,11:4861,12:6966,13:261}
    cost_pc = [u(pc_max[i]) for i in range(18)]
    cost_pc[3] = HUGE     # PC3 cost comes from cost_base[BASE_STEP], never this entry
    cost_base = [u(base_max[i]) for i in range(14)]
    return cost_pc, cost_base


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

    cost_pc, cost_base = _pack_cost_tables(DROP_SETUP)
    def costload(table):   # LDA table,X  (X = index)  -- fixup-resolved absolute operand
        a.code.append(0xBD); a.fixups.append((len(a.code), "abs", table)); a.code.append(0); a.code.append(0)

    # ---- step: frame-packing dispatch loop ----
    # Each 'step' call runs phases back-to-back until the next phase would blow the budget
    # (or ARMED clears at publish). Phases end with 'jmp st_rts' which loops back here.
    a.label("step")
    a.ins16("LDA_abs", ARMED); a.br("BNE","st_enter"); a.ins("RTS")
    a.label("st_enter")
    a.ins("LDA_imm", PACK_LIMIT); a.ins16("STA_abs", PK_BUDGET)   # untouched budget also flags "first phase"
    a.label("st_go")
    a.ins16("LDA_abs", ARMED); a.br("BNE","st_bck"); a.jmp("ph_ret")   # publish cleared ARMED -> return
    a.label("st_bck")
    a.ins16("LDA_abs", PK_BUDGET); a.br("BNE","st_cost"); a.jmp("ph_ret")  # budget spent (solo big phase) -> fast return
    a.label("st_cost")
    # cost of the phase about to run: cost_base[BASE_STEP] if PC==3 else cost_pc[PC]
    a.ins16("LDA_abs", ST2_PC); a.ins("CMP_imm",3); a.br("BNE","st_cpc")
    a.ins16("LDA_abs", BASE_STEP); a.ins("TAX"); costload("cost_base"); a.jmp("st_hav")
    a.label("st_cpc")
    a.ins16("LDA_abs", ST2_PC); a.ins("TAX"); costload("cost_pc")
    a.label("st_hav")
    a.ins16("STA_abs", PK_COST)
    a.ins16("LDA_abs", PK_BUDGET); a.ins("CMP_imm", PACK_LIMIT); a.br("BEQ","st_run")  # untouched budget = first phase -> run
    a.ins16("CMP_abs", PK_COST); a.br("BCS","st_run")                  # budget>=cost -> run (A still = budget)
    a.jmp("ph_ret")                                                     # else budget<cost -> return
    a.label("st_run")
    a.ins16("LDA_abs", PK_BUDGET); a.ins("SEC"); a.ins16("SBC_abs", PK_COST)
    a.br("BCS","st_nocl"); a.ins("LDA_imm",0); a.label("st_nocl"); a.ins16("STA_abs", PK_BUDGET)
    a.ins16("LDA_abs", ST2_PC)
    for pcval,lbl in [(0,"p_land1"),(1,"p_res1"),(2,"p_imm1"),(3,"p_base"),(4,"p_land2"),(5,"p_res2"),
                      (6,"p_shape"),(7,"p_buried"),(8,"p_read"),(9,"p_setup"),(10,"p_comb"),
                      (16,"p_delta"),(17,"p_delta2"),(11,"p_value"),(12,"p_cmp"),(14,"p_grav1"),(15,"p_grav2")]:
        a.ins("CMP_imm", pcval); a.br("BNE", f"n_{pcval}"); a.jmp(lbl); a.label(f"n_{pcval}")
    a.jmp("ph_ret")
    a.label("ph_ret")
    a.ins("RTS")

    def setpc(v): a.ins("LDA_imm", v); a.ins16("STA_abs", ST2_PC); a.jmp("st_rts")

    # PHASE 0 LAND1
    a.label("p_land1")
    a.jsr("cp_live_cur")
    a.ins16("LDA_abs",S_O1); a.ins("STA_zp",PO); a.ins16("LDA_abs",S_C1); a.ins("STA_zp",PC)
    a.ins16("LDA_abs",S_CA); a.ins("STA_zp",PCA); a.ins16("LDA_abs",S_CB); a.ins("STA_zp",PCB)
    a.jsr("land_place"); a.ins("CMP_imm",1); a.br("BEQ","pl1_ok")
    a.ins16("INC_abs",S_C1); a.ins16("LDA_abs",S_C1); a.ins("CMP_imm",8); a.br("BEQ","lret1"); a.jmp("st_rts"); a.label("lret1")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_C1); a.ins16("INC_abs",S_O1)
    a.ins16("LDA_abs",S_O1); a.ins("CMP_imm",4); a.br("BEQ","lret2"); a.jmp("st_rts"); a.label("lret2")
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
    a.jsr("base_info")
    a.jsr("vrdy_full")                                      # vertical readiness of WORK1
    a.ins16("LDA_abs", P.EV_VRDY_LO); a.ins16("STA_abs", D.BASE_VRDY_LO)
    a.ins16("LDA_abs", P.EV_VRDY_HI); a.ins16("STA_abs", D.BASE_VRDY_HI)
    a.jmp("b_adv")
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
    a.ins16("INC_abs",S_C2); a.ins16("LDA_abs",S_C2); a.ins("CMP_imm",8); a.br("BEQ","lret3"); a.jmp("st_rts"); a.label("lret3")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_C2); a.ins16("INC_abs",S_O2)
    a.ins16("LDA_abs",S_O2); a.ins("CMP_imm",4); a.br("BEQ","lret4"); a.jmp("st_rts"); a.label("lret4")
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
    a.jsr("vrdy_full")
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
    a.jmp("st_go")          # phase tail: loop back to the packer (which decides continue/return)

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
    a.jsr("shape"); a.jsr("buried"); a.jsr("vrdy_full")
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
    D.emit_vir_vrun2(a); D.emit_vrdy_new(a); D.emit_vrdy_old(a); D.emit_vrdy_full(a)
    D.emit_delta_terms(a); D.emit_delta_finish(a)
    # ---- frame-packing cost tables (read-only data; never executed) ----
    a.label("cost_pc")
    for v in cost_pc: a.raw(v)
    a.label("cost_base")
    for v in cost_base: a.raw(v)
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
