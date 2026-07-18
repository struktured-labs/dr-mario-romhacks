#!/usr/bin/env python3
"""emit_search_d3: the 6502 depth-3 search = the 91.7% config on copro hardware:
ply1 rank + top-8 select (Pass 0) x [ply2 rank + top-8 select + expectimax over 8 pills],
TARGETED capped resolve, 16-bit WIN=30000, integer expectimax. Validated vs decide_d3
(firmware-faithful golden). Reuses the validated leaf_score_d3 + land/resolve/calc_imm."""
import sys, random
HERE = "/home/struktured/projects/dr-mario-mods"
sys.path.insert(0, HERE + "/tests"); sys.path.insert(0, HERE)
import primitives as P
from patch_vs_cpu import Asm6502
import patch_vs_cpu
patch_vs_cpu.OPS.setdefault("CLD", 0xD8)
patch_vs_cpu.OPS.setdefault("SBC_absX", 0xFD)
patch_vs_cpu.OPS.setdefault("CMP_absX", 0xDD)
patch_vs_cpu.OPS.setdefault("ADC_absX", 0x7D)
patch_vs_cpu.OPS.setdefault("ROR_zp", 0x66)
patch_vs_cpu.OPS.setdefault("ROL_zp", 0x26)
patch_vs_cpu.OPS.setdefault("LSR_zp", 0x46)
patch_vs_cpu.OPS.setdefault("ASL_zp", 0x06)
patch_vs_cpu.OPS.setdefault("ORA_zp", 0x05)
patch_vs_cpu.OPS.setdefault("EOR_zp", 0x45)
from py65_harness import Cpu
from test_depth2 import (S_BEST_C, S_BEST_O,
                         _rand_board, _emit_calc_imm, _emit_copy, emit_landplace,
                         S_CA, S_CB, S_NA, S_NB, CI_LO, CI_HI, PO, PC, PCA, PCB)
from test_leaf_d3 import emit_leaf_score_d3, emit_combine_d3, EV_POL_LO, EV_POL_HI
from test_pollution import emit_pollution
from test_readiness_ext import emit_readiness_ext, emit_walk
from test_vrdy import emit_vrdy
import nes_d3_golden as G3

# HW CONSTRAINT (CoproDrMario.sv folds 4KB wram): copro $6100-$61FF == $0800-$08FF are the
# SAME bytes -> the $08xx page is FORBIDDEN (aliases EV_*/S_*/results/DONE state). WORK2
# lives at $0B00 (TK/TK1/pills end at $0A7F).
LIVE, WORK1, CUR, WORK2 = 0x0500, 0x0600, 0x0700, 0x0B00
WIN = 30000
NPILLS, SHIFT = 4, 2     # expectimax pill count (power of 2 -> /NPILLS = >>SHIFT); test overrides to 2,1
# 4-pill measured 24/24=100% solo (isoD 2026-07-11) vs 8-pill 22/24 -- half the ply3 cost, free.
# TK candidate arrays (index 0..count-1, count<=32): ply2 rank (per ply1 candidate)
TK_KL, TK_KH, TK_O, TK_C, TK_IL, TK_IH = 0x0900, 0x0920, 0x0940, 0x0960, 0x0980, 0x09A0
PILLA, PILLB = 0x09C0, 0x09C8   # 8-pill table (host-loaded, like SQ)
# TK1 arrays: ply1 rank (Pass 0, filled once per decision)
TK1_KL, TK1_KH, TK1_O, TK1_C = 0x0A00, 0x0A20, 0x0A40, 0x0A60
# d3 state: TRUE zero page $40-$65 (zp operands are 1 byte -- a $61xx value would be
# silently truncated by ins()). $40-$65 is free: primitives scratch is $CA-$F1, stack $01xx.
(D_C1, D_O1, D_I1L, D_I1H, D_BVL, D_BVH, D_BC, D_BO, D_C2, D_O2, D_C3, D_O3, D_TKC,
 D_B2L, D_B2H, D_KL, D_KH, D_I2L, D_I2H, D_MKL, D_MKH, D_MI, D_J, D_PI, D_SL, D_SM, D_SH,
 D_EBL, D_EBH, D_EA, D_V3L, D_V3H, D_EL, D_EH, D_V1L, D_V1H, D_J1, D_T1C,
 D_SEED, D_JT) = range(0x40, 0x68)
D_L1L, D_L1H = 0x68, 0x69     # ply-1 leaf (for the temporal discount)
DISC = False                   # emit discounted combine (set by build_copro_d3)

THIRD = [(0, 1), (1, 2), (2, 0), (1, 1)]   # stratified 4-pill subset (3 mixed + 1 double), /4=shift
RESOLVE_LBL = "resolve_capped"   # TARGETED (deploy config, isolation 12/12); "resolve_capped_full" for full
USE_ACCEL = False                # True: leaf via the LeafEval RTL block at $70xx
USE_ENGINE = False               # True: FULL BoardEngine (copies/land/resolve/leaf all RTL)
LEV_BOARD, LEV_SCO, LEV_WIN_R, LEV_GO = 0x7000, 0x70F0, 0x70F2, 0x70F8
LEV_A_O4, LEV_A_COL, LEV_A_CA, LEV_A_CB, LEV_A_SL = 0x70E0, 0x70E1, 0x70E2, 0x70E3, 0x70E4
LEV_LEGAL, LEV_RVC, LEV_RVV, LEV_IMM = 0x70E8, 0x70E9, 0x70EA, 0x70EB
LEV_WSLOT, LEV_CMD = 0x70F3, 0x70F4
TOPK1 = 32   # ply1 keep-width; 32 = FULL (T1C <= 30). MEASURED (isolation 2026-07-10):
             # topk1=8 = 70% clears vs FULL = 91% (n=24, FW model) -- the depth-1 Pass-0 key
             # under-ranks setup moves; ply1 pruning is NOT quality-safe at depth-3. Cost:
             # dense first pill ~95s @85.9MHz (declines fast as viruses die).


def build():
    a = Asm6502(0x8000)
    if USE_ENGINE:
        # everything board-related runs in the BoardEngine; the 6502 is pure control
        _emit_search_d3_engine(a)
        _emit_expectimax_engine(a)
        return a.assemble(), a.labels
    # ALL primitives + leaf eval operate on CUR ($0700); LIVE ($0500) is the preserved input.
    import test_pollution, test_readiness_ext, test_vrdy
    P.BOARD = CUR; P.LIVE_BOARD = CUR; P.MARK = 0x0780
    test_pollution.BOARD = CUR; test_readiness_ext.BOARD = CUR; test_vrdy.BOARD = CUR
    # ---- search entry ----
    _emit_search_d3(a)
    _emit_expectimax(a)
    # ---- reused machinery ----
    _emit_calc_imm(a)
    emit_landplace(a)
    P.emit_first_occ(a); P.emit_find_clears(a); P.emit_gravity(a); P.emit_shape(a)
    P.emit_resolve_capped_full(a); P.emit_resolve_capped(a)
    P.emit_buried(a); P.emit_setup(a); P.emit_has_virus(a)
    if USE_ACCEL:
        _emit_leaf_accel(a)
        P.emit_combine(a)        # dead soft-combine, but calc_imm JSRs its cm_mul helper
    else:
        emit_leaf_score_d3(a); emit_readiness_ext(a); emit_walk(a); emit_vrdy(a); emit_pollution(a)
        emit_combine_d3(a)
    _emit_copy(a, "cp_live_cur", LIVE, CUR)
    _emit_copy(a, "cp_cur_work1", CUR, WORK1)
    _emit_copy(a, "cp_work1_cur", WORK1, CUR)
    _emit_copy(a, "cp_cur_work2", CUR, WORK2)
    _emit_copy(a, "cp_work2_cur", WORK2, CUR)
    return a.assemble(), a.labels


_ec = [0]


def _e_poll(a):
    n = _ec[0]; _ec[0] += 1
    a.label(f"ep{n}"); a.ins16("LDA_abs", LEV_GO); a.br("BEQ", f"ep{n}")


def _e_copy(a, sl, to_cur):
    a.ins("LDA_imm", sl); a.ins16("STA_abs", LEV_A_SL)
    a.ins("LDA_imm", 2 if to_cur else 3); a.ins16("STA_abs", LEV_CMD)
    _e_poll(a)


def _e_score(a):
    """(win ? WIN : sco) -> D_V3 from the engine result regs."""
    n = _ec[0]; _ec[0] += 1
    a.ins16("LDA_abs", LEV_WIN_R); a.br("BEQ", f"esn{n}")
    a.ins("LDA_imm", WIN & 0xFF); a.ins("STA_zp", D_V3L)
    a.ins("LDA_imm", (WIN >> 8) & 0xFF); a.ins("STA_zp", D_V3H); a.jmp(f"esd{n}")
    a.label(f"esn{n}")
    a.ins16("LDA_abs", LEV_SCO); a.ins("STA_zp", D_V3L)
    a.ins16("LDA_abs", LEV_SCO + 1); a.ins("STA_zp", D_V3H)
    a.label(f"esd{n}")


def _e_node(a, o_zp, c_zp, ca_abs, cb_abs):
    """args from zp orient/col + abs color sources (masked), CMD 4, poll."""
    a.ins("LDA_zp", o_zp); a.ins16("STA_abs", LEV_A_O4)
    a.ins("LDA_zp", c_zp); a.ins16("STA_abs", LEV_A_COL)
    a.ins16("LDA_abs", ca_abs); a.ins("AND_imm", 0x0F); a.ins16("STA_abs", LEV_A_CA)
    a.ins16("LDA_abs", cb_abs); a.ins("AND_imm", 0x0F); a.ins16("STA_abs", LEV_A_CB)
    a.ins("LDA_imm", 4); a.ins16("STA_abs", LEV_CMD)
    _e_poll(a)


def _emit_search_d3_engine(a):
    a.label("search")
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", D_BO)
    a.ins16("STA_abs", S_BEST_O)                    # ANYTIME: live mailbox invalid until 1st cand
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", D_BVL); a.ins("LDA_imm", 0x80); a.ins("STA_zp", D_BVH)
    # tie-break seed (same as soft build)
    a.ins16("LDA_abs", S_CA); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("STA_zp", D_SEED)
    a.ins16("LDA_abs", S_CB); a.ins("AND_imm", 0xF0); a.ins("ORA_zp", D_SEED); a.ins("STA_zp", D_SEED)
    # upload LIVE ($0500) -> engine slot 1
    a.ins("LDA_imm", 1); a.ins16("STA_abs", LEV_WSLOT)
    a.ins("LDX_imm", 0)
    a.label("up_l")
    a.ins16("LDA_absX", LIVE); a.ins16("STA_absX", LEV_BOARD)
    a.ins("INX"); a.ins("CPX_imm", 128); a.br("BNE", "up_l")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", LEV_WSLOT)
    # ---- Pass 0 ----
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_T1C); a.ins("STA_zp", D_O1)
    a.label("p0_o"); a.ins("LDA_imm", 0); a.ins("STA_zp", D_C1)
    a.label("p0_c")
    _e_copy(a, 1, True)
    _e_node(a, D_O1, D_C1, S_CA, S_CB)
    a.ins16("LDA_abs", LEV_LEGAL); a.br("BNE", "p0_leg"); a.jmp("p0_next")
    a.label("p0_leg")
    _e_score(a)
    a.ins("CLC"); a.ins16("LDA_abs", LEV_IMM); a.ins("ADC_zp", D_V3L); a.ins("STA_zp", D_KL)
    a.ins16("LDA_abs", LEV_IMM + 1); a.ins("ADC_zp", D_V3H); a.ins("STA_zp", D_KH)
    a.ins("LDX_zp", D_T1C)
    a.ins("LDA_zp", D_KL); a.ins16("STA_absX", TK1_KL); a.ins("LDA_zp", D_KH); a.ins16("STA_absX", TK1_KH)
    a.ins("LDA_zp", D_O1); a.ins16("STA_absX", TK1_O); a.ins("LDA_zp", D_C1); a.ins16("STA_absX", TK1_C)
    a.ins("INC_zp", D_T1C)
    a.label("p0_next")
    a.ins("INC_zp", D_C1); a.ins("LDA_zp", D_C1); a.ins("CMP_imm", 8); a.br("BEQ", "p0_oc"); a.jmp("p0_c")
    a.label("p0_oc")
    a.ins("INC_zp", D_O1); a.ins("LDA_zp", D_O1); a.ins("CMP_imm", 4); a.br("BEQ", "p0_done"); a.jmp("p0_o")
    a.label("p0_done")
    # ---- select loop ----
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_J1)
    a.label("s_loop")
    a.ins("LDA_zp", D_J1); a.ins("CMP_imm", TOPK1); a.br("BCC", "s_c1"); a.jmp("o_done"); a.label("s_c1")
    a.ins("LDA_zp", D_J1); a.ins("CMP_zp", D_T1C); a.br("BCC", "s_c2"); a.jmp("o_done"); a.label("s_c2")
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", D_MKL); a.ins("LDA_imm", 0x80); a.ins("STA_zp", D_MKH)
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", D_MI)
    a.ins("LDX_imm", 0)
    a.label("mx1_loop")
    a.ins("CPX_zp", D_T1C); a.br("BEQ", "mx1_done")
    a.ins("LDA_zp", D_MKL); a.ins("SEC"); a.ins16("SBC_absX", TK1_KL)
    a.ins("LDA_zp", D_MKH); a.ins16("SBC_absX", TK1_KH)
    a.br("BVC", "mx1_s1"); a.ins("EOR_imm", 0x80); a.label("mx1_s1")
    a.br("BPL", "mx1_nx")
    a.ins16("LDA_absX", TK1_KL); a.ins("STA_zp", D_MKL); a.ins16("LDA_absX", TK1_KH); a.ins("STA_zp", D_MKH)
    a.ins("STX_zp", D_MI)
    a.label("mx1_nx")
    a.ins("INX"); a.jmp("mx1_loop")
    a.label("mx1_done")
    a.ins("LDX_zp", D_MI)
    a.ins("LDA_imm", 0x00); a.ins16("STA_absX", TK1_KL); a.ins("LDA_imm", 0x80); a.ins16("STA_absX", TK1_KH)
    a.ins16("LDA_absX", TK1_O); a.ins("STA_zp", D_O1); a.ins16("LDA_absX", TK1_C); a.ins("STA_zp", D_C1)
    # replay ply1
    _e_copy(a, 1, True)
    _e_node(a, D_O1, D_C1, S_CA, S_CB)
    a.ins16("LDA_abs", LEV_IMM); a.ins("STA_zp", D_I1L); a.ins16("LDA_abs", LEV_IMM + 1); a.ins("STA_zp", D_I1H)
    if DISC:
        a.ins16("LDA_abs", LEV_SCO); a.ins("STA_zp", D_L1L)
        a.ins16("LDA_abs", LEV_SCO + 1); a.ins("STA_zp", D_L1H)
    a.ins16("LDA_abs", LEV_WIN_R); a.br("BEQ", "o_nw")
    a.ins("CLC"); a.ins("LDA_zp", D_I1L); a.ins("ADC_imm", WIN & 0xFF); a.ins("STA_zp", D_V1L)
    a.ins("LDA_zp", D_I1H); a.ins("ADC_imm", (WIN >> 8) & 0xFF); a.ins("STA_zp", D_V1H)
    a.jmp("o_cand")
    a.label("o_nw")
    _e_copy(a, 2, False)                                   # w1 <- cur
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_TKC); a.ins("STA_zp", D_O2)
    a.label("i_outer"); a.ins("LDA_imm", 0); a.ins("STA_zp", D_C2)
    a.label("i_inner")
    _e_copy(a, 2, True)                                    # cur <- w1
    _e_node(a, D_O2, D_C2, S_NA, S_NB)
    a.ins16("LDA_abs", LEV_LEGAL); a.br("BNE", "i_leg"); a.jmp("i_next")
    a.label("i_leg")
    _e_score(a)
    a.ins("CLC"); a.ins16("LDA_abs", LEV_IMM); a.ins("ADC_zp", D_V3L); a.ins("STA_zp", D_KL)
    a.ins16("LDA_abs", LEV_IMM + 1); a.ins("ADC_zp", D_V3H); a.ins("STA_zp", D_KH)
    a.ins("LDX_zp", D_TKC)
    a.ins("LDA_zp", D_KL); a.ins16("STA_absX", TK_KL); a.ins("LDA_zp", D_KH); a.ins16("STA_absX", TK_KH)
    a.ins16("LDA_abs", LEV_IMM); a.ins16("STA_absX", TK_IL); a.ins16("LDA_abs", LEV_IMM + 1); a.ins16("STA_absX", TK_IH)
    a.ins("LDA_zp", D_O2); a.ins16("STA_absX", TK_O); a.ins("LDA_zp", D_C2); a.ins16("STA_absX", TK_C)
    a.ins("INC_zp", D_TKC)
    a.label("i_next")
    a.ins("INC_zp", D_C2); a.ins("LDA_zp", D_C2); a.ins("CMP_imm", 8); a.br("BEQ", "i_oc"); a.jmp("i_inner")
    a.label("i_oc")
    a.ins("INC_zp", D_O2); a.ins("LDA_zp", D_O2); a.ins("CMP_imm", 4); a.br("BEQ", "i_done"); a.jmp("i_outer")
    a.label("i_done")
    a.ins("LDA_zp", D_TKC); a.br("BNE", "have2")
    _e_copy(a, 2, True)
    a.ins("LDA_imm", 1); a.ins16("STA_abs", LEV_CMD); _e_poll(a)      # CMD 1: leaf on CUR
    _e_score(a)
    a.ins("CLC"); a.ins("LDA_zp", D_I1L); a.ins("ADC_zp", D_V3L); a.ins("STA_zp", D_V1L)
    a.ins("LDA_zp", D_I1H); a.ins("ADC_zp", D_V3H); a.ins("STA_zp", D_V1H)
    a.jmp("o_cand")
    a.label("have2")
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", D_B2L); a.ins("LDA_imm", 0x80); a.ins("STA_zp", D_B2H)
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_J)
    a.label("k_loop")
    a.ins("LDA_zp", D_J); a.ins("CMP_imm", 8); a.br("BCC", "k_c1"); a.jmp("k_done"); a.label("k_c1")
    a.ins("LDA_zp", D_J); a.ins("CMP_zp", D_TKC); a.br("BCC", "k_c2"); a.jmp("k_done"); a.label("k_c2")
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", D_MKL); a.ins("LDA_imm", 0x80); a.ins("STA_zp", D_MKH)
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", D_MI)
    a.ins("LDX_imm", 0)
    a.label("mx_loop")
    a.ins("CPX_zp", D_TKC); a.br("BEQ", "mx_done")
    a.ins("LDA_zp", D_MKL); a.ins("SEC"); a.ins16("SBC_absX", TK_KL)
    a.ins("LDA_zp", D_MKH); a.ins16("SBC_absX", TK_KH)
    a.br("BVC", "mx_s1"); a.ins("EOR_imm", 0x80); a.label("mx_s1")
    a.br("BPL", "mx_nx")
    a.ins16("LDA_absX", TK_KL); a.ins("STA_zp", D_MKL); a.ins16("LDA_absX", TK_KH); a.ins("STA_zp", D_MKH)
    a.ins("STX_zp", D_MI)
    a.label("mx_nx")
    a.ins("INX"); a.jmp("mx_loop")
    a.label("mx_done")
    a.ins("LDX_zp", D_MI)
    a.ins("LDA_imm", 0x00); a.ins16("STA_absX", TK_KL); a.ins("LDA_imm", 0x80); a.ins16("STA_absX", TK_KH)
    a.ins16("LDA_absX", TK_IL); a.ins("STA_zp", D_I2L); a.ins16("LDA_absX", TK_IH); a.ins("STA_zp", D_I2H)
    a.ins16("LDA_absX", TK_O); a.ins("STA_zp", D_O2); a.ins16("LDA_absX", TK_C); a.ins("STA_zp", D_C2)
    _e_copy(a, 2, True)
    _e_node(a, D_O2, D_C2, S_NA, S_NB)
    a.ins16("LDA_abs", LEV_WIN_R); a.br("BEQ", "k_ex")
    a.ins("CLC"); a.ins("LDA_zp", D_I2L); a.ins("ADC_imm", WIN & 0xFF); a.ins("STA_zp", D_V3L)
    a.ins("LDA_zp", D_I2H); a.ins("ADC_imm", (WIN >> 8) & 0xFF); a.ins("STA_zp", D_V3H)
    a.jmp("k_haveval")
    a.label("k_ex")
    a.jsr("expectimax")
    a.ins("CLC"); a.ins("LDA_zp", D_I2L); a.ins("ADC_zp", D_EL); a.ins("STA_zp", D_V3L)
    a.ins("LDA_zp", D_I2H); a.ins("ADC_zp", D_EH); a.ins("STA_zp", D_V3H)
    a.label("k_haveval")
    a.ins("LDA_zp", D_B2L); a.ins("SEC"); a.ins("SBC_zp", D_V3L); a.ins("LDA_zp", D_B2H); a.ins("SBC_zp", D_V3H)
    a.br("BVC", "k_s1"); a.ins("EOR_imm", 0x80); a.label("k_s1"); a.br("BPL", "k_nx")
    a.ins("LDA_zp", D_V3L); a.ins("STA_zp", D_B2L); a.ins("LDA_zp", D_V3H); a.ins("STA_zp", D_B2H)
    a.label("k_nx")
    a.ins("INC_zp", D_J); a.jmp("k_loop")
    a.label("k_done")
    if DISC:
        # val1 = imm1 + leaf1 + asr16(best2 - leaf1)   [d = 0.5 temporal discount]
        a.ins("SEC"); a.ins("LDA_zp", D_B2L); a.ins("SBC_zp", D_L1L); a.ins("STA_zp", D_V1L)
        a.ins("LDA_zp", D_B2H); a.ins("SBC_zp", D_L1H)
        a.ins("CMP_imm", 0x80); a.ins("ROR_A"); a.ins("STA_zp", D_V1H)   # asr hi (sign-preserving)
        a.ins("LDA_zp", D_V1L); a.ins("ROR_A"); a.ins("STA_zp", D_V1L)   # ror lo with carry
        a.ins("CLC"); a.ins("LDA_zp", D_V1L); a.ins("ADC_zp", D_L1L); a.ins("STA_zp", D_V1L)
        a.ins("LDA_zp", D_V1H); a.ins("ADC_zp", D_L1H); a.ins("STA_zp", D_V1H)
        a.ins("CLC"); a.ins("LDA_zp", D_V1L); a.ins("ADC_zp", D_I1L); a.ins("STA_zp", D_V1L)
        a.ins("LDA_zp", D_V1H); a.ins("ADC_zp", D_I1H); a.ins("STA_zp", D_V1H)
    else:
        a.ins("CLC"); a.ins("LDA_zp", D_I1L); a.ins("ADC_zp", D_B2L); a.ins("STA_zp", D_V1L)
        a.ins("LDA_zp", D_I1H); a.ins("ADC_zp", D_B2H); a.ins("STA_zp", D_V1H)
    a.label("o_cand")
    a.ins("LDA_zp", D_SEED); a.br("BEQ", "o_nj")
    a.ins("LDA_zp", D_O1); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ORA_zp", D_C1)
    a.ins("EOR_zp", D_SEED); a.ins("STA_zp", D_JT)
    a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("EOR_zp", D_JT); a.ins("AND_imm", 0x03)
    a.ins("CLC"); a.ins("ADC_zp", D_V1L); a.ins("STA_zp", D_V1L)
    a.ins("LDA_zp", D_V1H); a.ins("ADC_imm", 0); a.ins("STA_zp", D_V1H)
    a.label("o_nj")
    a.ins("LDA_zp", D_BVL); a.ins("SEC"); a.ins("SBC_zp", D_V1L); a.ins("LDA_zp", D_BVH); a.ins("SBC_zp", D_V1H)
    a.br("BVC", "o_s1"); a.ins("EOR_imm", 0x80); a.label("o_s1"); a.br("BPL", "s_next")
    a.ins("LDA_zp", D_V1L); a.ins("STA_zp", D_BVL); a.ins("LDA_zp", D_V1H); a.ins("STA_zp", D_BVH)
    a.ins("LDA_zp", D_C1); a.ins("STA_zp", D_BC); a.ins("LDA_zp", D_O1); a.ins("STA_zp", D_BO)
    a.ins("LDA_zp", D_BC); a.ins16("STA_abs", S_BEST_C)     # ANYTIME: live-publish running best
    a.ins("LDA_zp", D_BO); a.ins16("STA_abs", S_BEST_O)
    a.label("s_next")
    a.ins("INC_zp", D_J1); a.jmp("s_loop")
    a.label("o_done"); a.ins("RTS")


def _emit_expectimax_engine(a):
    a.label("expectimax")
    _e_copy(a, 3, False)                                   # w2 <- cur
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_SL); a.ins("STA_zp", D_SM); a.ins("STA_zp", D_SH)
    a.ins("STA_zp", D_PI)
    a.label("ex_pill")
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", D_EBL); a.ins("LDA_imm", 0x80); a.ins("STA_zp", D_EBH)
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_EA); a.ins("STA_zp", D_O3)
    a.label("ex_o"); a.ins("LDA_imm", 0); a.ins("STA_zp", D_C3)
    a.label("ex_c")
    _e_copy(a, 3, True)                                    # cur <- w2
    a.ins("LDA_zp", D_O3); a.ins16("STA_abs", LEV_A_O4)
    a.ins("LDA_zp", D_C3); a.ins16("STA_abs", LEV_A_COL)
    a.ins("LDX_zp", D_PI); a.ins16("LDA_absX", PILLA); a.ins16("STA_abs", LEV_A_CA)
    a.ins16("LDA_absX", PILLB); a.ins16("STA_abs", LEV_A_CB)
    a.ins("LDA_imm", 4); a.ins16("STA_abs", LEV_CMD); _e_poll(a)
    a.ins16("LDA_abs", LEV_LEGAL); a.br("BNE", "ex_leg"); a.jmp("ex_cnext")
    a.label("ex_leg")
    a.ins("LDA_imm", 1); a.ins("STA_zp", D_EA)
    _e_score(a)
    a.ins("CLC"); a.ins16("LDA_abs", LEV_IMM); a.ins("ADC_zp", D_V3L); a.ins("STA_zp", D_V3L)
    a.ins16("LDA_abs", LEV_IMM + 1); a.ins("ADC_zp", D_V3H); a.ins("STA_zp", D_V3H)
    a.ins("LDA_zp", D_EBL); a.ins("SEC"); a.ins("SBC_zp", D_V3L); a.ins("LDA_zp", D_EBH); a.ins("SBC_zp", D_V3H)
    a.br("BVC", "ex_s1"); a.ins("EOR_imm", 0x80); a.label("ex_s1"); a.br("BPL", "ex_cnext")
    a.ins("LDA_zp", D_V3L); a.ins("STA_zp", D_EBL); a.ins("LDA_zp", D_V3H); a.ins("STA_zp", D_EBH)
    a.label("ex_cnext")
    a.ins("INC_zp", D_C3); a.ins("LDA_zp", D_C3); a.ins("CMP_imm", 8); a.br("BEQ", "ex_ocheck"); a.jmp("ex_c")
    a.label("ex_ocheck")
    a.ins("INC_zp", D_O3); a.ins("LDA_zp", D_O3); a.ins("CMP_imm", 4); a.br("BEQ", "ex_odone"); a.jmp("ex_o")
    a.label("ex_odone")
    a.ins("LDA_zp", D_EA); a.br("BNE", "ex_term")
    _e_copy(a, 3, True)
    a.ins("LDA_imm", 1); a.ins16("STA_abs", LEV_CMD); _e_poll(a)
    _e_score(a)
    a.ins("LDA_zp", D_V3L); a.ins("STA_zp", D_EBL); a.ins("LDA_zp", D_V3H); a.ins("STA_zp", D_EBH)
    a.label("ex_term")
    a.ins("CLC"); a.ins("LDA_zp", D_SL); a.ins("ADC_zp", D_EBL); a.ins("STA_zp", D_SL)
    a.ins("LDA_zp", D_SM); a.ins("ADC_zp", D_EBH); a.ins("STA_zp", D_SM)
    a.ins("LDA_zp", D_EBH); a.br("BPL", "ex_pos")
    a.ins("LDA_zp", D_SH); a.ins("ADC_imm", 0xFF); a.ins("STA_zp", D_SH); a.jmp("ex_padd")
    a.label("ex_pos")
    a.ins("LDA_zp", D_SH); a.ins("ADC_imm", 0x00); a.ins("STA_zp", D_SH)
    a.label("ex_padd")
    a.ins("INC_zp", D_PI); a.ins("LDA_zp", D_PI); a.ins("CMP_imm", NPILLS); a.br("BEQ", "ex_div"); a.jmp("ex_pill")
    a.label("ex_div")
    for _ in range(SHIFT):
        a.ins("LDA_zp", D_SH); a.ins("CMP_imm", 0x80)
        a.ins("ROR_zp", D_SH); a.ins("ROR_zp", D_SM); a.ins("ROR_zp", D_SL)
    a.ins("LDA_zp", D_SL); a.ins("STA_zp", D_EL); a.ins("LDA_zp", D_SM); a.ins("STA_zp", D_EH)
    a.ins("RTS")


def attach_engine_emu(cpu):
    """python model of the full BoardEngine at $70xx: slots as NES-byte boards, commands
    executed via the SAME goldens (_landing/_place/_cap1_targeted/leaf_d3)."""
    from py65.memory import ObservableMemory
    from nes_d2_golden import _landing, _place, _virus_count
    from nes_d3_golden import _cap1_targeted
    base = cpu.mem
    obs = ObservableMemory(subject=base)
    st = {"wslot": 0, "slots": [[0xFF] * 128 for _ in range(4)],
          "o4": 0, "col": 0, "ca": 0, "cb": 0, "sl": 0}

    def wr_board(addr, value):
        st["slots"][st["wslot"]][addr - LEV_BOARD] = value & 0xFF

    def wr_wslot(addr, value):
        st["wslot"] = value & 3

    def wr_arg(addr, value):
        k = ("o4", "col", "ca", "cb", "sl")[addr - LEV_A_O4]
        st[k] = value

    def post(legal, cells=0, vir=0, sco=0, win=0):
        imm = 180 * vir + 10 * cells
        base[LEV_LEGAL] = legal; base[LEV_RVC] = cells; base[LEV_RVV] = vir
        base[LEV_IMM] = imm & 0xFF; base[LEV_IMM + 1] = (imm >> 8) & 0xFF
        base[LEV_SCO] = sco & 0xFF; base[LEV_SCO + 1] = (sco >> 8) & 0xFF
        base[LEV_WIN_R] = win; base[LEV_GO] = 1

    def leaf_of(b):
        win = 1 if _virus_count(b) == 0 else 0
        sco = 0 if win else (G3.leaf_d3(b) & 0xFFFF)
        return sco, win

    def wr_cmd(addr, value):
        cmd = value & 0x0F
        cur = st["slots"][0]
        if cmd == 2:
            st["slots"][0] = list(st["slots"][st["sl"] & 3]); base[LEV_GO] = 1
        elif cmd == 3:
            st["slots"][st["sl"] & 3] = list(cur); base[LEV_GO] = 1
        elif cmd == 1:
            sco, win = leaf_of(cur); post(1, 0, 0, sco, win)
        elif cmd == 4:
            o4, col = st["o4"] & 3, st["col"] & 7
            orient = 0 if o4 < 2 else 1
            land = _landing(cur, orient, col)
            if land is None:
                post(0); return
            offa, offb = land
            ca, cb = st["ca"] & 3, st["cb"] & 3
            ta, tb = (cb, ca) if (o4 & 1) else (ca, cb)
            nb = _place(cur, offa, offb, ta, tb)
            cells, vir = _cap1_targeted(nb, offa, offb)
            st["slots"][0] = nb
            sco, win = leaf_of(nb)
            post(1, cells, vir, sco, win)

    obs.subscribe_to_write(range(LEV_BOARD, LEV_BOARD + 128), wr_board)
    obs.subscribe_to_write([LEV_WSLOT], wr_wslot)
    obs.subscribe_to_write(range(LEV_A_O4, LEV_A_SL + 1), wr_arg)
    obs.subscribe_to_write([LEV_CMD], wr_cmd)
    cpu.mpu.memory = obs
    cpu.mem = obs


def _emit_leaf_accel(a):
    """leaf_score_d3 via the LeafEval RTL block: copy CUR -> $7000, START, poll DONE,
    read EV_SCO/EV_WIN back. Same label + EV_ contract as the soft leaf (~3.5k cyc vs ~50k)."""
    a.label("leaf_score_d3")
    a.ins("LDX_imm", 0)
    a.label("la_cp")
    a.ins16("LDA_absX", CUR); a.ins16("STA_absX", LEV_BOARD)
    a.ins("INX"); a.ins("CPX_imm", 128); a.br("BNE", "la_cp")
    a.ins16("STA_abs", LEV_GO)                 # START (value irrelevant)
    a.label("la_poll")
    a.ins16("LDA_abs", LEV_GO); a.br("BEQ", "la_poll")
    a.ins16("LDA_abs", LEV_SCO); a.ins16("STA_abs", P.EV_SCO_LO)
    a.ins16("LDA_abs", LEV_SCO + 1); a.ins16("STA_abs", P.EV_SCO_HI)
    a.ins16("LDA_abs", LEV_WIN_R); a.ins16("STA_abs", P.EV_WIN)
    a.ins("RTS")


def attach_accel_emu(cpu):
    """py65-side emulation of the LeafEval block: a write to $70F8 computes leaf_d3 on
    the NES-encoded board at $7000-$707F and posts sco/win/done -- so the ACCEL firmware
    validates end-to-end in py65 against the same golden."""
    from py65.memory import ObservableMemory
    base = cpu.mem
    obs = ObservableMemory(subject=base)

    def on_go(addr, value):
        b = [base[LEV_BOARD + i] for i in range(128)]
        win = 1 if all((x & 0xF0) != 0xD0 for x in b if x != 0xFF) else 0
        v = 0 if win else (G3.leaf_d3(b) & 0xFFFF)
        base[LEV_SCO] = v & 0xFF; base[LEV_SCO + 1] = (v >> 8) & 0xFF
        base[LEV_WIN_R] = win; base[LEV_GO] = 1

    obs.subscribe_to_write([LEV_GO], on_go)
    cpu.mpu.memory = obs
    cpu.mem = obs


_sc_ctr = [0]


def _score_to_ac(a):
    """after leaf_score_d3: put (WIN if EV_WIN else EV_SCO) into (D_V3L,D_V3H). Unique labels/call."""
    n = _sc_ctr[0]; _sc_ctr[0] += 1
    nw, dn = f"sc_nw{n}", f"sc_d{n}"
    a.ins16("LDA_abs", P.EV_WIN); a.br("BEQ", nw)
    a.ins("LDA_imm", WIN & 0xFF); a.ins("STA_zp", D_V3L); a.ins("LDA_imm", (WIN >> 8) & 0xFF); a.ins("STA_zp", D_V3H)
    a.jmp(dn)
    a.label(nw)
    a.ins16("LDA_abs", P.EV_SCO_LO); a.ins("STA_zp", D_V3L); a.ins16("LDA_abs", P.EV_SCO_HI); a.ins("STA_zp", D_V3H)
    a.label(dn)


def _emit_search_d3(a):
    a.label("search")
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", D_BO)
    a.ins16("STA_abs", S_BEST_O)                    # ANYTIME: live mailbox invalid until 1st cand
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", D_BVL); a.ins("LDA_imm", 0x80); a.ins("STA_zp", D_BVH)   # best_val=-32768
    # tie-break seed rides the color bytes' HIGH nibbles: SEED = (S_CB&$F0)|(S_CA>>4); 0=off
    a.ins16("LDA_abs", S_CA); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("STA_zp", D_SEED)
    a.ins16("LDA_abs", S_CB); a.ins("AND_imm", 0xF0); a.ins("ORA_zp", D_SEED); a.ins("STA_zp", D_SEED)
    # ---- Pass 0: rank ALL ply1 placements by imm1+leaf into TK1 (topk1=8 select below) ----
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_T1C); a.ins("STA_zp", D_O1)
    a.label("p0_o"); a.ins("LDA_imm", 0); a.ins("STA_zp", D_C1)
    a.label("p0_c")
    a.jsr("cp_live_cur")
    a.ins("LDA_zp", D_O1); a.ins("STA_zp", PO); a.ins("LDA_zp", D_C1); a.ins("STA_zp", PC)
    a.ins16("LDA_abs", S_CA); a.ins("AND_imm", 0x0F); a.ins("STA_zp", PCA)
    a.ins16("LDA_abs", S_CB); a.ins("AND_imm", 0x0F); a.ins("STA_zp", PCB)
    a.jsr("land_place"); a.ins("CMP_imm", 1); a.br("BEQ", "p0_leg"); a.jmp("p0_next")
    a.label("p0_leg")
    a.jsr(RESOLVE_LBL); a.jsr("calc_imm")
    a.jsr("leaf_score_d3"); _score_to_ac(a)               # D_V3 = leaf score (WIN or SCO)
    # key1 = imm1 + score -> TK1[T1C]
    a.ins("CLC"); a.ins16("LDA_abs", CI_LO); a.ins("ADC_zp", D_V3L); a.ins("STA_zp", D_KL)
    a.ins16("LDA_abs", CI_HI); a.ins("ADC_zp", D_V3H); a.ins("STA_zp", D_KH)
    a.ins("LDX_zp", D_T1C)
    a.ins("LDA_zp", D_KL); a.ins16("STA_absX", TK1_KL); a.ins("LDA_zp", D_KH); a.ins16("STA_absX", TK1_KH)
    a.ins("LDA_zp", D_O1); a.ins16("STA_absX", TK1_O); a.ins("LDA_zp", D_C1); a.ins16("STA_absX", TK1_C)
    a.ins("INC_zp", D_T1C)
    a.label("p0_next")
    a.ins("INC_zp", D_C1); a.ins("LDA_zp", D_C1); a.ins("CMP_imm", 8); a.br("BEQ", "p0_oc"); a.jmp("p0_c")
    a.label("p0_oc")
    a.ins("INC_zp", D_O1); a.ins("LDA_zp", D_O1); a.ins("CMP_imm", 4); a.br("BEQ", "p0_done"); a.jmp("p0_o")
    a.label("p0_done")
    # ---- select loop: top-8 of TK1, full ply2+expectimax treatment for each ----
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_J1)
    a.label("s_loop")
    a.ins("LDA_zp", D_J1); a.ins("CMP_imm", TOPK1); a.br("BCC", "s_c1"); a.jmp("o_done"); a.label("s_c1")
    a.ins("LDA_zp", D_J1); a.ins("CMP_zp", D_T1C); a.br("BCC", "s_c2"); a.jmp("o_done"); a.label("s_c2")
    # first-max scan of TK1 (stable: strict > only)
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", D_MKL); a.ins("LDA_imm", 0x80); a.ins("STA_zp", D_MKH)
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", D_MI)
    a.ins("LDX_imm", 0)
    a.label("mx1_loop")
    a.ins("CPX_zp", D_T1C); a.br("BEQ", "mx1_done")
    a.ins("LDA_zp", D_MKL); a.ins("SEC"); a.ins16("SBC_absX", TK1_KL)
    a.ins("LDA_zp", D_MKH); a.ins16("SBC_absX", TK1_KH)
    a.br("BVC", "mx1_s1"); a.ins("EOR_imm", 0x80); a.label("mx1_s1")
    a.br("BPL", "mx1_nx")     # MK-TK >=0 -> TK<=MK -> skip
    a.ins16("LDA_absX", TK1_KL); a.ins("STA_zp", D_MKL); a.ins16("LDA_absX", TK1_KH); a.ins("STA_zp", D_MKH)
    a.ins("STX_zp", D_MI)
    a.label("mx1_nx")
    a.ins("INX"); a.jmp("mx1_loop")
    a.label("mx1_done")
    a.ins("LDX_zp", D_MI)
    a.ins("LDA_imm", 0x00); a.ins16("STA_absX", TK1_KL); a.ins("LDA_imm", 0x80); a.ins16("STA_absX", TK1_KH)  # mark used
    a.ins16("LDA_absX", TK1_O); a.ins("STA_zp", D_O1); a.ins16("LDA_absX", TK1_C); a.ins("STA_zp", D_C1)
    # replay ply1 (legal by construction): b1 in CUR, imm1 recomputed
    a.jsr("cp_live_cur")
    a.ins("LDA_zp", D_O1); a.ins("STA_zp", PO); a.ins("LDA_zp", D_C1); a.ins("STA_zp", PC)
    a.ins16("LDA_abs", S_CA); a.ins("AND_imm", 0x0F); a.ins("STA_zp", PCA)
    a.ins16("LDA_abs", S_CB); a.ins("AND_imm", 0x0F); a.ins("STA_zp", PCB)
    a.jsr("land_place"); a.jsr(RESOLVE_LBL); a.jsr("calc_imm")
    a.ins16("LDA_abs", CI_LO); a.ins("STA_zp", D_I1L); a.ins16("LDA_abs", CI_HI); a.ins("STA_zp", D_I1H)
    a.jsr("has_virus"); a.ins16("LDA_abs", P.EV_VIRFLAG); a.br("BNE", "o_nw")
    # won ply1: val1 = imm1 + WIN
    a.ins("CLC"); a.ins("LDA_zp", D_I1L); a.ins("ADC_imm", WIN & 0xFF); a.ins("STA_zp", D_V1L)
    a.ins("LDA_zp", D_I1H); a.ins("ADC_imm", (WIN >> 8) & 0xFF); a.ins("STA_zp", D_V1H)
    a.jmp("o_cand")
    a.label("o_nw")
    a.jsr("cp_cur_work1")
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_TKC); a.ins("STA_zp", D_O2)
    # ---- Pass A: rank all ply2, store into TK ----
    a.label("i_outer"); a.ins("LDA_imm", 0); a.ins("STA_zp", D_C2)
    a.label("i_inner")
    a.jsr("cp_work1_cur")
    a.ins("LDA_zp", D_O2); a.ins("STA_zp", PO); a.ins("LDA_zp", D_C2); a.ins("STA_zp", PC)
    a.ins16("LDA_abs", S_NA); a.ins("AND_imm", 0x0F); a.ins("STA_zp", PCA)
    a.ins16("LDA_abs", S_NB); a.ins("AND_imm", 0x0F); a.ins("STA_zp", PCB)
    a.jsr("land_place"); a.ins("CMP_imm", 1); a.br("BEQ", "i_leg"); a.jmp("i_next")
    a.label("i_leg")
    a.jsr(RESOLVE_LBL); a.jsr("calc_imm")
    a.ins16("LDA_abs", CI_LO); a.ins("STA_zp", D_I2L); a.ins16("LDA_abs", CI_HI); a.ins("STA_zp", D_I2H)
    a.jsr("leaf_score_d3"); _score_to_ac(a)               # D_V3 = score(WIN or SCO)
    # key = imm2 + score
    a.ins("CLC"); a.ins("LDA_zp", D_I2L); a.ins("ADC_zp", D_V3L); a.ins("STA_zp", D_KL)
    a.ins("LDA_zp", D_I2H); a.ins("ADC_zp", D_V3H); a.ins("STA_zp", D_KH)
    # store TK[TKC] = key,imm2,o2,c2
    a.ins("LDX_zp", D_TKC)
    a.ins("LDA_zp", D_KL); a.ins16("STA_absX", TK_KL); a.ins("LDA_zp", D_KH); a.ins16("STA_absX", TK_KH)
    a.ins("LDA_zp", D_I2L); a.ins16("STA_absX", TK_IL); a.ins("LDA_zp", D_I2H); a.ins16("STA_absX", TK_IH)
    a.ins("LDA_zp", D_O2); a.ins16("STA_absX", TK_O); a.ins("LDA_zp", D_C2); a.ins16("STA_absX", TK_C)
    a.ins("INC_zp", D_TKC)
    a.label("i_next")
    a.ins("INC_zp", D_C2); a.ins("LDA_zp", D_C2); a.ins("CMP_imm", 8); a.br("BEQ", "i_oc"); a.jmp("i_inner")
    a.label("i_oc")
    a.ins("INC_zp", D_O2); a.ins("LDA_zp", D_O2); a.ins("CMP_imm", 4); a.br("BEQ", "i_done"); a.jmp("i_outer")
    a.label("i_done")
    # if TKC==0: val1 = imm1 + leaf_score_d3(WORK1)
    a.ins("LDA_zp", D_TKC); a.br("BNE", "have2")
    a.jsr("cp_work1_cur"); a.jsr("leaf_score_d3"); _score_to_ac(a)
    a.ins("CLC"); a.ins("LDA_zp", D_I1L); a.ins("ADC_zp", D_V3L); a.ins("STA_zp", D_V1L)
    a.ins("LDA_zp", D_I1H); a.ins("ADC_zp", D_V3H); a.ins("STA_zp", D_V1H)
    a.jmp("o_cand")
    a.label("have2")
    # best2 = -32768 ; j=0
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", D_B2L); a.ins("LDA_imm", 0x80); a.ins("STA_zp", D_B2H)
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_J)
    a.label("k_loop")
    # if j >= min(8,TKC) done  (BCC-over-JMP: k_done is >127 bytes away)
    a.ins("LDA_zp", D_J); a.ins("CMP_imm", 8); a.br("BCC", "k_c1"); a.jmp("k_done"); a.label("k_c1")
    a.ins("LDA_zp", D_J); a.ins("CMP_zp", D_TKC); a.br("BCC", "k_c2"); a.jmp("k_done"); a.label("k_c2")
    # find max key over TK[0..TKC-1] (unmarked = key != 0x8000 sentinel? use maxkey=-32768, scan)
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", D_MKL); a.ins("LDA_imm", 0x80); a.ins("STA_zp", D_MKH)
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", D_MI)     # max idx (0xFF=none)
    a.ins("LDX_imm", 0)
    a.label("mx_loop")
    a.ins("CPX_zp", D_TKC); a.br("BEQ", "mx_done")
    # signed compare TK_KEY[X] vs MK: MK - TK ; if result <0 then TK>MK -> take
    a.ins("LDA_zp", D_MKL); a.ins("SEC"); a.ins16("SBC_absX", TK_KL)
    a.ins("LDA_zp", D_MKH); a.ins16("SBC_absX", TK_KH)
    a.br("BVC", "mx_s1"); a.ins("EOR_imm", 0x80); a.label("mx_s1")
    a.br("BPL", "mx_nx")     # MK-TK >=0 -> TK<=MK -> skip
    # TK > MK: update
    a.ins16("LDA_absX", TK_KL); a.ins("STA_zp", D_MKL); a.ins16("LDA_absX", TK_KH); a.ins("STA_zp", D_MKH)
    a.ins("STX_zp", D_MI)
    a.label("mx_nx")
    a.ins("INX"); a.jmp("mx_loop")
    a.label("mx_done")
    # mark chosen used: TK_KEY[maxidx] = 0x8000
    a.ins("LDX_zp", D_MI)
    a.ins("LDA_imm", 0x00); a.ins16("STA_absX", TK_KL); a.ins("LDA_imm", 0x80); a.ins16("STA_absX", TK_KH)
    # load imm2,o2,c2 of chosen
    a.ins16("LDA_absX", TK_IL); a.ins("STA_zp", D_I2L); a.ins16("LDA_absX", TK_IH); a.ins("STA_zp", D_I2H)
    a.ins16("LDA_absX", TK_O); a.ins("STA_zp", D_O2); a.ins16("LDA_absX", TK_C); a.ins("STA_zp", D_C2)
    # replay ply2: cp WORK1->CUR, land, resolve -> b2
    a.jsr("cp_work1_cur")
    a.ins("LDA_zp", D_O2); a.ins("STA_zp", PO); a.ins("LDA_zp", D_C2); a.ins("STA_zp", PC)
    a.ins16("LDA_abs", S_NA); a.ins("AND_imm", 0x0F); a.ins("STA_zp", PCA)
    a.ins16("LDA_abs", S_NB); a.ins("AND_imm", 0x0F); a.ins("STA_zp", PCB)
    a.jsr("land_place"); a.jsr(RESOLVE_LBL)
    # val2: if virus-free -> imm2+WIN ; else imm2 + expectimax
    a.jsr("has_virus"); a.ins16("LDA_abs", P.EV_VIRFLAG); a.br("BNE", "k_ex")
    a.ins("CLC"); a.ins("LDA_zp", D_I2L); a.ins("ADC_imm", WIN & 0xFF); a.ins("STA_zp", D_V3L)
    a.ins("LDA_zp", D_I2H); a.ins("ADC_imm", (WIN >> 8) & 0xFF); a.ins("STA_zp", D_V3H)
    a.jmp("k_haveval")
    a.label("k_ex")
    a.jsr("expectimax")     # -> D_EL,D_EH
    a.ins("CLC"); a.ins("LDA_zp", D_I2L); a.ins("ADC_zp", D_EL); a.ins("STA_zp", D_V3L)
    a.ins("LDA_zp", D_I2H); a.ins("ADC_zp", D_EH); a.ins("STA_zp", D_V3H)
    a.label("k_haveval")
    # if val2 (D_V3) > best2 (D_B2): best2 = val2
    a.ins("LDA_zp", D_B2L); a.ins("SEC"); a.ins("SBC_zp", D_V3L); a.ins("LDA_zp", D_B2H); a.ins("SBC_zp", D_V3H)
    a.br("BVC", "k_s1"); a.ins("EOR_imm", 0x80); a.label("k_s1"); a.br("BPL", "k_nx")
    a.ins("LDA_zp", D_V3L); a.ins("STA_zp", D_B2L); a.ins("LDA_zp", D_V3H); a.ins("STA_zp", D_B2H)
    a.label("k_nx")
    a.ins("INC_zp", D_J); a.jmp("k_loop")
    a.label("k_done")
    # val1 = imm1 + best2
    a.ins("CLC"); a.ins("LDA_zp", D_I1L); a.ins("ADC_zp", D_B2L); a.ins("STA_zp", D_V1L)
    a.ins("LDA_zp", D_I1H); a.ins("ADC_zp", D_B2H); a.ins("STA_zp", D_V1H)
    a.label("o_cand")
    # seeded tie-break: val1 += (t ^ (t>>3)) & 3, t = seed ^ ((o1<<3)|c1); seed==0 -> off
    a.ins("LDA_zp", D_SEED); a.br("BEQ", "o_nj")
    a.ins("LDA_zp", D_O1); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ORA_zp", D_C1)
    a.ins("EOR_zp", D_SEED); a.ins("STA_zp", D_JT)
    a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("EOR_zp", D_JT); a.ins("AND_imm", 0x03)
    a.ins("CLC"); a.ins("ADC_zp", D_V1L); a.ins("STA_zp", D_V1L)
    a.ins("LDA_zp", D_V1H); a.ins("ADC_imm", 0); a.ins("STA_zp", D_V1H)
    a.label("o_nj")
    # if val1 (D_V1) > best_val (D_BV): best_val=val1, best_c/o=c1/o1
    a.ins("LDA_zp", D_BVL); a.ins("SEC"); a.ins("SBC_zp", D_V1L); a.ins("LDA_zp", D_BVH); a.ins("SBC_zp", D_V1H)
    a.br("BVC", "o_s1"); a.ins("EOR_imm", 0x80); a.label("o_s1"); a.br("BPL", "s_next")
    a.ins("LDA_zp", D_V1L); a.ins("STA_zp", D_BVL); a.ins("LDA_zp", D_V1H); a.ins("STA_zp", D_BVH)
    a.ins("LDA_zp", D_C1); a.ins("STA_zp", D_BC); a.ins("LDA_zp", D_O1); a.ins("STA_zp", D_BO)
    a.ins("LDA_zp", D_BC); a.ins16("STA_abs", S_BEST_C)     # ANYTIME: live-publish running best
    a.ins("LDA_zp", D_BO); a.ins16("STA_abs", S_BEST_O)
    a.label("s_next")
    a.ins("INC_zp", D_J1); a.jmp("s_loop")
    a.label("o_done"); a.ins("RTS")


def _emit_expectimax(a):
    # in: b2 in CUR. out: expected (16-bit signed) in D_EL,D_EH
    a.label("expectimax")
    a.jsr("cp_cur_work2")
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_SL); a.ins("STA_zp", D_SM); a.ins("STA_zp", D_SH)
    a.ins("STA_zp", D_PI)
    a.label("ex_pill")
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", D_EBL); a.ins("LDA_imm", 0x80); a.ins("STA_zp", D_EBH)   # -32768
    a.ins("LDA_imm", 0); a.ins("STA_zp", D_EA); a.ins("STA_zp", D_O3)
    a.label("ex_o"); a.ins("LDA_imm", 0); a.ins("STA_zp", D_C3)
    a.label("ex_c")
    a.jsr("cp_work2_cur")
    a.ins("LDA_zp", D_O3); a.ins("STA_zp", PO); a.ins("LDA_zp", D_C3); a.ins("STA_zp", PC)
    a.ins("LDX_zp", D_PI); a.ins16("LDA_absX", PILLA); a.ins("STA_zp", PCA)
    a.ins("LDX_zp", D_PI); a.ins16("LDA_absX", PILLB); a.ins("STA_zp", PCB)
    a.jsr("land_place"); a.ins("CMP_imm", 1); a.br("BEQ", "ex_leg"); a.jmp("ex_cnext")
    a.label("ex_leg")
    a.ins("LDA_imm", 1); a.ins("STA_zp", D_EA)
    a.jsr(RESOLVE_LBL); a.jsr("calc_imm")
    a.jsr("leaf_score_d3"); _score_to_ac(a)              # D_V3 = score
    # v3 = imm3 + score
    a.ins("CLC"); a.ins16("LDA_abs", CI_LO); a.ins("ADC_zp", D_V3L); a.ins("STA_zp", D_V3L)
    a.ins16("LDA_abs", CI_HI); a.ins("ADC_zp", D_V3H); a.ins("STA_zp", D_V3H)
    # if v3 > ex_best3: ex_best3 = v3
    a.ins("LDA_zp", D_EBL); a.ins("SEC"); a.ins("SBC_zp", D_V3L); a.ins("LDA_zp", D_EBH); a.ins("SBC_zp", D_V3H)
    a.br("BVC", "ex_s1"); a.ins("EOR_imm", 0x80); a.label("ex_s1"); a.br("BPL", "ex_cnext")
    a.ins("LDA_zp", D_V3L); a.ins("STA_zp", D_EBL); a.ins("LDA_zp", D_V3H); a.ins("STA_zp", D_EBH)
    a.label("ex_cnext")
    a.ins("INC_zp", D_C3); a.ins("LDA_zp", D_C3); a.ins("CMP_imm", 8); a.br("BEQ", "ex_ocheck"); a.jmp("ex_c")
    a.label("ex_ocheck")
    a.ins("INC_zp", D_O3); a.ins("LDA_zp", D_O3); a.ins("CMP_imm", 4); a.br("BEQ", "ex_odone"); a.jmp("ex_o")
    a.label("ex_odone")
    # term = ex_best3 if any else leaf_score_d3(WORK2/b2)
    a.ins("LDA_zp", D_EA); a.br("BNE", "ex_term")
    a.jsr("cp_work2_cur"); a.jsr("leaf_score_d3"); _score_to_ac(a)
    a.ins("LDA_zp", D_V3L); a.ins("STA_zp", D_EBL); a.ins("LDA_zp", D_V3H); a.ins("STA_zp", D_EBH)
    a.label("ex_term")
    # sum24 += ex_best3 (sign-extend hi)
    a.ins("CLC"); a.ins("LDA_zp", D_SL); a.ins("ADC_zp", D_EBL); a.ins("STA_zp", D_SL)
    a.ins("LDA_zp", D_SM); a.ins("ADC_zp", D_EBH); a.ins("STA_zp", D_SM)
    # sign-extend: add carry + (0xFF if EBH<0 else 0x00) into SH  (carry from the SM add is preserved)
    a.ins("LDA_zp", D_EBH); a.br("BPL", "ex_pos")
    a.ins("LDA_zp", D_SH); a.ins("ADC_imm", 0xFF); a.ins("STA_zp", D_SH); a.jmp("ex_padd")
    a.label("ex_pos")
    a.ins("LDA_zp", D_SH); a.ins("ADC_imm", 0x00); a.ins("STA_zp", D_SH)
    a.label("ex_padd")
    a.ins("INC_zp", D_PI); a.ins("LDA_zp", D_PI); a.ins("CMP_imm", NPILLS); a.br("BEQ", "ex_div"); a.jmp("ex_pill")
    a.label("ex_div")
    # expected = sum24 >> SHIFT (arithmetic): rotate sign into carry each time.
    for _ in range(SHIFT):
        a.ins("LDA_zp", D_SH); a.ins("CMP_imm", 0x80)   # carry = sign bit of the 24-bit sum
        a.ins("ROR_zp", D_SH); a.ins("ROR_zp", D_SM); a.ins("ROR_zp", D_SL)
    a.ins("LDA_zp", D_SL); a.ins("STA_zp", D_EL); a.ins("LDA_zp", D_SM); a.ins("STA_zp", D_EH)
    a.ins("RTS")


def s16(x):
    return x - 0x10000 if x >= 0x8000 else x


def make_fewlegal(rng, FaithfulBoard):
    """Mostly-full board with 2 open columns -> few legal placements -> fast py65 search
    (still exercises top-K, expectimax, wins). Singletons keep faithful==nes gravity."""
    b = FaithfulBoard(16, 8)
    b.color[:] = 0; b.is_virus[:] = False
    open_cols = rng.sample(range(8), 2)
    for c in range(8):
        h = rng.randint(6, 11) if c in open_cols else 16
        for r in range(16 - h, 16):
            b.color[r, c] = rng.randint(1, 3)
            b.is_virus[r, c] = rng.random() < 0.25
    return b


def main():
    global NPILLS, SHIFT, USE_ACCEL
    import os
    global USE_ENGINE
    if os.environ.get("ACCEL"):
        USE_ACCEL = True
        print("ACCEL mode: leaf via emulated LeafEval block")
    if os.environ.get("ENGINE"):
        USE_ENGINE = True
        print("ENGINE mode: full BoardEngine emulated")
    NPILLS, SHIFT = 2, 1                       # fast validation config (deploy uses 8,3)
    THIRD_T = [(0, 1), (1, 2)]
    G3.USE_VRDY = True
    code, labels = build()
    sq = [i * i for i in range(17)]
    pa = [p[0] for p in THIRD_T]; pb = [p[1] for p in THIRD_T]
    from nes_d2_golden import _make_board, _action_to_key
    sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/src")
    sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/tmp")
    from drmario.faithful_game import FaithfulBoard
    from xcheck_terms import faithful_to_nes
    rng = random.Random(77); agree = 0; N = 30; dis = []
    for t in range(N):
        fb = make_fewlegal(rng, FaithfulBoard)
        ca, cb = rng.randint(1, 3), rng.randint(1, 3); na, nb_ = rng.randint(1, 3), rng.randint(1, 3)
        seed = 0 if t < N // 2 else rng.randint(1, 255)   # half regression, half seeded
        nes = faithful_to_nes(fb)
        # NB: golden topk1 must equal the 6502 TOPK1 (even "full"=32 keeps the 6502's
        # descending-key selection order for tie-breaks -- do NOT pass topk1=0 here)
        gk = G3.decide_d3(list(nes), ca - 1, cb - 1, na - 1, nb_ - 1, topk1=TOPK1, topk2=8,
                          third=THIRD_T, seed=seed)
        cpu = Cpu(); cpu.load(0x8000, code); cpu.set_board(nes)
        if USE_ENGINE:
            attach_engine_emu(cpu)
        elif USE_ACCEL:
            attach_accel_emu(cpu)
        for i in range(17):
            cpu.mem[sq_a := (P.SQ_LO_ADDR + i)] = sq[i] & 0xFF; cpu.mem[P.SQ_HI_ADDR + i] = sq[i] >> 8
        for i in range(NPILLS):
            cpu.mem[PILLA + i] = pa[i]; cpu.mem[PILLB + i] = pb[i]
        cpu.mem[S_CA] = (ca - 1) | ((seed & 0x0F) << 4)   # seed rides the color high nibbles
        cpu.mem[S_CB] = (cb - 1) | (seed & 0xF0)
        cpu.mem[S_NA] = na - 1; cpu.mem[S_NB] = nb_ - 1
        cpu.call(0x8000 + labels["search"], max_steps=500_000_000)
        ek = (cpu.mem[D_BC], cpu.mem[D_BO]) if cpu.mem[D_BO] != 0xFF else None
        if ek == gk:
            agree += 1
        else:
            dis.append((t, ek, gk))
    print(f"emit_search_d3 vs decide_d3: {agree}/{N} MATCH  ({'PASS' if agree == N else 'FAIL'})")
    for t, ek, gk in dis[:12]:
        print(f"  t={t}: 6502={ek} golden={gk}")


if __name__ == "__main__":
    main()
