#!/usr/bin/env python3
"""Resumable depth-2 phase machine: one <=8k chunk per `step` call, state in $6000
RAM. Validates (best_col,best_orient4) == the atomic build_search over random boards
by driving arm + step* until DONE.

PC states ($6140 ST2_PC): 0 LAND1 1 RES1 2 IMM1 4 LAND2 5 RES2 6 SHAPE 7 BURIED
8 READ(x3 RD_RGN) 9 SETUP(x4 SU_RGN) 10 COMB 11 VALUE 12 CMP 13 DONE.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import primitives as P
from patch_vs_cpu import Asm6502
from py65_harness import Cpu
from test_landplace import emit_landplace
import test_depth2 as D2
from test_depth2 import (CUR, WORK1, LIVE, S_O1,S_C1,S_O2,S_C2, S_CA,S_CB,S_NA,S_NB,
    S_IMM_LO,S_IMM_HI, S_BL_WIN,S_BL_LO,S_BL_HI,S_BL_SET, S_ANY2, S_BV_WIN,S_BV_LO,S_BV_HI,
    S_BEST_C,S_BEST_O, CAND_WIN,CAND_LO,CAND_HI, CI_LO,CI_HI, PO,PC,PCA,PCB, decide_d2_4, _rand_board)

ST2_PC = 0x6140
RD_RGN = 0x6141
SU_RGN = 0x6142
ARMED  = 0x6143
# readiness region table (start,end) x3 ; setup region (step,lstart,lend,nalong) x4
RD_REGIONS = [(0,43),(43,86),(86,128)]
SU_REGIONS = [(1,0,8,8),(1,8,16,8),(8,0,4,16),(8,4,8,16)]


def _adv(a, o_addr, c_addr, exhausted_label):
    """c++; if c==8 c=0,o++; if o==4 -> jmp exhausted_label (else fallthrough)."""
    a.ins16("INC_abs", c_addr); a.ins16("LDA_abs", c_addr); a.ins("CMP_imm", 8); a.br("BNE", None) if False else None
    # use explicit labels via caller; simpler inline:


def build_resumable():
    P.BOARD = CUR; P.LIVE_BOARD = CUR; P.MARK = 0x0780
    a = Asm6502(0x8000)
    # ---- arm: init search ----
    a.label("arm")
    a.ins("LDA_imm",0)
    for r in (S_O1,S_C1,S_BV_WIN): a.ins16("STA_abs", r)
    a.ins("LDA_imm",0xFF); a.ins16("STA_abs", S_BEST_O)
    a.ins("LDA_imm",0); a.ins16("STA_abs", ST2_PC); a.ins("LDA_imm",1); a.ins16("STA_abs", ARMED)
    a.ins("RTS")

    # ---- step: dispatch on ST2_PC, do one phase ----
    a.label("step")
    a.ins16("LDA_abs", ARMED); a.br("BNE","st_go"); a.ins("RTS")
    a.label("st_go")
    a.ins16("LDA_abs", ST2_PC)
    # jump table via compares
    for pcval,lbl in [(0,"p_land1"),(1,"p_res1"),(2,"p_imm1"),(4,"p_land2"),(5,"p_res2"),
                      (6,"p_shape"),(7,"p_buried"),(8,"p_read"),(9,"p_setup"),(10,"p_comb"),
                      (11,"p_value"),(12,"p_cmp")]:
        a.ins("CMP_imm", pcval); a.br("BNE", f"n_{pcval}"); a.jmp(lbl); a.label(f"n_{pcval}")
    a.ins("RTS")   # PC 13 DONE or unknown

    def setpc(v): a.ins("LDA_imm", v); a.ins16("STA_abs", ST2_PC); a.jmp("st_rts")
    def adv_outer_then(next_done):
        a.ins16("INC_abs", S_C1); a.ins16("LDA_abs", S_C1); a.ins("CMP_imm",8); a.br("BNE","ao_more")
        a.ins("LDA_imm",0); a.ins16("STA_abs", S_C1); a.ins16("INC_abs", S_O1)
        a.ins16("LDA_abs", S_O1); a.ins("CMP_imm",4); a.br("BNE","ao_more")
        a.ins("LDA_imm",13); a.ins16("STA_abs", ST2_PC); a.jmp(next_done)   # exhausted -> DONE/publish
        a.label("ao_more"); a.ins("LDA_imm",0); a.ins16("STA_abs", ST2_PC); a.jmp("st_rts")

    # PHASE 0 LAND1
    a.label("p_land1")
    a.jsr("cp_live_cur")
    a.ins16("LDA_abs",S_O1); a.ins("STA_zp",PO); a.ins16("LDA_abs",S_C1); a.ins("STA_zp",PC)
    a.ins16("LDA_abs",S_CA); a.ins("STA_zp",PCA); a.ins16("LDA_abs",S_CB); a.ins("STA_zp",PCB)
    a.jsr("land_place"); a.ins("CMP_imm",1); a.br("BEQ","pl1_ok")
    # illegal -> advance outer; if exhausted publish
    a.ins16("INC_abs",S_C1); a.ins16("LDA_abs",S_C1); a.ins("CMP_imm",8); a.br("BEQ","lret1"); a.ins("RTS"); a.label("lret1")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_C1); a.ins16("INC_abs",S_O1)
    a.ins16("LDA_abs",S_O1); a.ins("CMP_imm",4); a.br("BEQ","lret2"); a.ins("RTS"); a.label("lret2")
    a.ins("LDA_imm",13); a.ins16("STA_abs",ST2_PC); a.jmp("p_publish")
    a.label("pl1_ok"); setpc(1)

    # PHASE 1 RES1
    a.label("p_res1")
    a.jsr("resolve_capped"); setpc(2)

    # PHASE 2 IMM1
    a.label("p_imm1")
    a.jsr("calc_imm")
    a.ins16("LDA_abs",CI_LO); a.ins16("STA_abs",S_IMM_LO); a.ins16("LDA_abs",CI_HI); a.ins16("STA_abs",S_IMM_HI)
    a.jsr("has_virus"); a.ins16("LDA_abs",P.EV_VIRFLAG); a.br("BNE","pi1_notwon")
    a.ins("LDA_imm",1); a.ins16("STA_abs",CAND_WIN)
    a.ins16("LDA_abs",S_IMM_LO); a.ins16("STA_abs",CAND_LO); a.ins16("LDA_abs",S_IMM_HI); a.ins16("STA_abs",CAND_HI)
    a.ins("LDA_imm",12); a.ins16("STA_abs",ST2_PC); a.jmp("st_rts")
    a.label("pi1_notwon")
    a.jsr("cp_cur_work1")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_BL_SET); a.ins16("STA_abs",S_ANY2)
    a.ins16("STA_abs",S_O2); a.ins16("STA_abs",S_C2)
    setpc(4)

    # PHASE 4 LAND2
    a.label("p_land2")
    a.jsr("cp_work1_cur")
    a.ins16("LDA_abs",S_O2); a.ins("STA_zp",PO); a.ins16("LDA_abs",S_C2); a.ins("STA_zp",PC)
    a.ins16("LDA_abs",S_NA); a.ins("STA_zp",PCA); a.ins16("LDA_abs",S_NB); a.ins("STA_zp",PCB)
    a.jsr("land_place"); a.ins("CMP_imm",1); a.br("BEQ","pl2_ok")
    # illegal -> advance inner; if exhausted -> VALUE(11)
    a.ins16("INC_abs",S_C2); a.ins16("LDA_abs",S_C2); a.ins("CMP_imm",8); a.br("BEQ","lret3"); a.ins("RTS"); a.label("lret3")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_C2); a.ins16("INC_abs",S_O2)
    a.ins16("LDA_abs",S_O2); a.ins("CMP_imm",4); a.br("BEQ","lret4"); a.ins("RTS"); a.label("lret4")
    a.ins("LDA_imm",11); a.ins16("STA_abs",ST2_PC); a.jmp("st_rts")
    a.label("pl2_ok")
    a.ins("LDA_imm",1); a.ins16("STA_abs",S_ANY2); setpc(5)

    # PHASE 5 RES2 (+ init leaf accumulators)
    a.label("p_res2")
    a.jsr("resolve_capped"); a.jsr("calc_imm")   # CI = imm2
    a.ins("LDA_imm",0); a.ins16("STA_abs",P.EV_RDY_LO); a.ins16("STA_abs",P.EV_RDY_HI)
    a.ins16("STA_abs",P.EV_SET); a.ins16("STA_abs",RD_RGN); a.ins16("STA_abs",SU_RGN)
    setpc(6)

    # PHASE 6 SHAPE
    a.label("p_shape"); a.jsr("shape"); setpc(7)
    # PHASE 7 BURIED
    a.label("p_buried"); a.jsr("buried"); setpc(8)

    # PHASE 8 READ (3 regions)
    a.label("p_read")
    a.ins16("LDA_abs",RD_RGN); a.ins("ASL_A"); a.ins("TAX")   # idx*2 into region table addr
    a.jsr("set_rd_region"); a.jsr("readiness_rg")
    a.ins16("INC_abs",RD_RGN); a.ins16("LDA_abs",RD_RGN); a.ins("CMP_imm",3); a.br("BEQ","lret5"); a.ins("RTS"); a.label("lret5")
    setpc(9)
    # PHASE 9 SETUP (4 regions)
    a.label("p_setup")
    a.jsr("set_su_region"); a.jsr("setup_rg")
    a.ins16("INC_abs",SU_RGN); a.ins16("LDA_abs",SU_RGN); a.ins("CMP_imm",4); a.br("BEQ","lret6"); a.ins("RTS"); a.label("lret6")
    setpc(10)

    # PHASE 10 COMB
    a.label("p_comb")
    a.ins("LDA_imm",0); a.ins16("STA_abs",P.EV_SCO_LO); a.ins16("STA_abs",P.EV_SCO_HI)  # ensure
    a.ins("LDA_zp",P.EO_LO); a.ins16("STA_abs",P.EV_RDY_LO) if False else None  # readiness already in EV_RDY
    a.jsr("has_virus"); a.jsr("combine")
    # leaf=(EV_WIN, CI+EV_SCO)
    a.ins16("LDA_abs",CI_LO); a.ins("CLC"); a.ins16("ADC_abs",P.EV_SCO_LO); a.ins16("STA_abs",CAND_LO)
    a.ins16("LDA_abs",CI_HI); a.ins16("ADC_abs",P.EV_SCO_HI); a.ins16("STA_abs",CAND_HI)
    a.ins16("LDA_abs",P.EV_WIN); a.ins16("STA_abs",CAND_WIN)
    # update best_leaf (same as build_search inner)
    a.ins16("LDA_abs",S_BL_SET); a.br("BEQ","pc_setbl")
    a.ins16("LDA_abs",CAND_WIN); a.ins16("CMP_abs",S_BL_WIN); a.br("BCC","pc_adv2"); a.br("BNE","pc_setbl")
    a.ins16("LDA_abs",CAND_LO); a.ins16("CMP_abs",S_BL_LO)
    a.ins16("LDA_abs",CAND_HI); a.ins16("SBC_abs",S_BL_HI)
    a.br("BVC","pc_s1"); a.ins("EOR_imm",0x80); a.label("pc_s1"); a.br("BMI","pc_adv2")
    a.ins16("LDA_abs",CAND_LO); a.ins16("CMP_abs",S_BL_LO); a.br("BNE","pc_setbl")
    a.ins16("LDA_abs",CAND_HI); a.ins16("CMP_abs",S_BL_HI); a.br("BEQ","pc_adv2")
    a.label("pc_setbl")
    a.ins("LDA_imm",1); a.ins16("STA_abs",S_BL_SET)
    a.ins16("LDA_abs",CAND_WIN); a.ins16("STA_abs",S_BL_WIN)
    a.ins16("LDA_abs",CAND_LO); a.ins16("STA_abs",S_BL_LO); a.ins16("LDA_abs",CAND_HI); a.ins16("STA_abs",S_BL_HI)
    a.label("pc_adv2")
    # advance inner cursor -> if more PC4 else PC11
    a.ins16("INC_abs",S_C2); a.ins16("LDA_abs",S_C2); a.ins("CMP_imm",8); a.br("BNE","pc_more")
    a.ins("LDA_imm",0); a.ins16("STA_abs",S_C2); a.ins16("INC_abs",S_O2)
    a.ins16("LDA_abs",S_O2); a.ins("CMP_imm",4); a.br("BNE","pc_more")
    a.ins("LDA_imm",11); a.ins16("STA_abs",ST2_PC); a.jmp("st_rts")
    a.label("pc_more"); a.ins("LDA_imm",4); a.ins16("STA_abs",ST2_PC); a.jmp("st_rts")

    # PHASE 11 VALUE
    a.label("p_value")
    a.ins16("LDA_abs",S_ANY2); a.br("BNE","pv_have2")
    a.jsr("cp_work1_cur"); a.jsr("leaf_score_full")   # leaf_score on WORK1 (full eval helper)
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
    adv_outer_then("p_publish")

    # PHASE 13 publish
    a.label("p_publish")
    a.ins("LDA_imm",0); a.ins16("STA_abs",ARMED)   # mark done (test reads S_BEST_*)
    a.label("st_rts")
    a.ins("RTS")

    # ---- helpers: set readiness/setup region params from RD_RGN/SU_RGN ----
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

    # leaf_score_full: shape+buried+readiness(all)+setup(all)+has_virus+combine, atomically
    # (only used in the rare no-legal-p2 VALUE path; fits because it's rare).
    a.label("leaf_score_full")
    a.jsr("shape"); a.jsr("buried")
    a.ins("LDA_imm",0); a.ins16("STA_abs",P.EV_RDY_LO); a.ins16("STA_abs",P.EV_RDY_HI); a.ins16("STA_abs",P.EV_SET)
    for (st,en) in RD_REGIONS:
        a.ins("LDA_imm",st); a.ins16("STA_abs",P.RD_START); a.ins("LDA_imm",en); a.ins16("STA_abs",P.RD_END); a.jsr("readiness_rg")
    for (stp,ls,le,na) in SU_REGIONS:
        a.ins("LDA_imm",stp); a.ins16("STA_abs",P.SU_STEP); a.ins("LDA_imm",ls); a.ins16("STA_abs",P.SU_LSTART)
        a.ins("LDA_imm",le); a.ins16("STA_abs",P.SU_LEND); a.ins("LDA_imm",na); a.ins16("STA_abs",P.SU_NALONG); a.jsr("setup_rg")
    a.jsr("has_virus"); a.jsr("combine"); a.ins("RTS")

    # reuse atomic helpers
    D2._emit_calc_imm(a); D2._emit_cmp_update(a)
    D2._emit_copy(a,"cp_live_cur",LIVE,CUR); D2._emit_copy(a,"cp_cur_work1",CUR,WORK1); D2._emit_copy(a,"cp_work1_cur",WORK1,CUR)
    emit_landplace(a)
    P.emit_first_occ(a); P.emit_find_clears(a); P.emit_gravity(a); P.emit_shape(a)
    P.emit_resolve_capped(a)
    P.emit_buried(a); P.emit_readiness_resumable(a); P.emit_setup(a); P.emit_setup_resumable(a)
    P.emit_has_virus(a); P.emit_combine(a)
    code = a.assemble()
    return code, a.labels


def validate(nboards=4, seed=321):
    code, labels = build_resumable()
    cpu = Cpu(); cpu.load(0x8000, code)
    for i in range(17): cpu.mem[P.SQ_LO_ADDR+i]=(i*i)&0xFF; cpu.mem[P.SQ_HI_ADDR+i]=(i*i)>>8
    arm = 0x8000+labels["arm"]; step = 0x8000+labels["step"]
    rng = random.Random(seed); fails=0; cmax=0
    for t in range(nboards):
        b = _rand_board(rng); cA,cB,nA,nB=(rng.randint(0,2) for _ in range(4))
        cpu.set_board(b)
        for ad,v in [(S_CA,cA),(S_CB,cB),(S_NA,nA),(S_NB,nB)]: cpu.mem[ad]=v
        cpu.call(arm); n=0
        while cpu.mem[ARMED]!=0 and n<200000:
            cmax=max(cmax, cpu.call(step, max_steps=200000)); n+=1
        gc,go = decide_d2_4(b,cA,cB,nA,nB)
        bc,bo = cpu.mem[S_BEST_C], cpu.mem[S_BEST_O]
        if (bc,bo)!=(gc,go):
            fails+=1; print(f"  board {t}: resumable=({bc},{bo}) golden=({gc},{go}) steps={n}")
        else:
            print(f"  board {t}: OK ({bc},{bo}) in {n} steps")
    print(f"resumable: {nboards-fails}/{nboards} match; max step cyc={cmax}")
    return fails==0
