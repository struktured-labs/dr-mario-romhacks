#!/usr/bin/env python3
"""6502 port of the incremental delta-eval, validated in py65 against the Python delta model
(tests/test_incremental.py) and the golden full-eval terms. For a NON-CLEARING placement of 2
pill cells on a settled board, delta_eval reuses base terms (computed once per first-ply) +
cheap local deltas -> the 6 weighted terms -> combine -> EV_SCO. ~10x cheaper than a full
rescan per second-ply leaf, with IDENTICAL scores.

Pieces:
  base_info    -> per-column surface + virus count (once per first-ply)
  wq           -> is a 3-cell window a same-color run touching a same-color virus? (g_setup)
  row_wins/col_wins/setup_delta -> new qualifying windows through the placed cells
  vir_run2     -> readiness of one virus = max(hrun,vrun)^2 (g_readiness)
  readiness_delta -> affected viruses (placed cells' row/col, placed color), sum new-old run^2
  delta_eval   -> easy closed-form deltas (maxh/holes/toprisk/buried) + setup + readiness + combine
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from py65_harness import Cpu
from patch_vs_cpu import Asm6502
import primitives as P
from primitives import (SH_MAXH, SH_HOLES, SH_TOPRISK, EV_BUR_LO, EV_BUR_HI,
                        EV_RDY_LO, EV_RDY_HI, EV_SET, EV_VIRFLAG, EV_SCO_LO, EV_SCO_HI,
                        EV_WIN, emit_combine)
from test_incremental import (base_info as py_base_info, delta_easy, setup_delta as py_setup,
                              readiness_delta as py_rdy, _place, _clears, _rand_settled,
                              g_vreadiness, vreadiness_delta)
from test_shape_eval import golden_shape
from test_eval_terms import g_buried, g_setup, g_readiness
from nes_d2_golden import _landing

EMPTY = 0xFF
ROWS, COLS = 16, 8
BASE = 0x4000
BOARD = 0x0500

# --- base-info + base-term storage (RAM) ---
BI_SURF, BI_VC = 0x6160, 0x6168
BASE_MH, BASE_HO, BASE_TR, BASE_SET = 0x6170, 0x6171, 0x6172, 0x6173
BASE_BUR_LO, BASE_BUR_HI = 0x6174, 0x6175
BASE_RDY_LO, BASE_RDY_HI = 0x6176, 0x6177
BASE_VIRFLAG = 0x6178
BASE_VRDY_LO, BASE_VRDY_HI = 0x6179, 0x617A
VNEW_LO, VNEW_HI, VOLD_LO, VOLD_HI = 0x61C2, 0x61C3, 0x61C4, 0x61C5
NV2_SH, VLIST2 = 0x61C7, 0x61C8      # vertical-affected list (separate from readiness VLIST)
RSUM_LO, RSUM_HI = 0x6180, 0x6181
RUN2_LO, RUN2_HI = 0x6182, 0x6183
RNEW_LO, RNEW_HI = 0x6184, 0x6185
ROLD_LO, ROLD_HI = 0x6186, 0x6187
SAVA, SAVB = 0x6188, 0x6189
VISIT = 0x6190                       # 16-byte visited bitmap (readiness dedup)

# --- zp scratch (test-only map; remap to cart-safe zp at integration) ---
BI_COL, BI_FO, BI_VCC, BI_OFF, BI_ROW = 0xE2, 0xE3, 0xE4, 0xE5, 0xE6
Z_OFFA, Z_OFFB, COLA, COLB, DT, SA, SB = 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46
WQ_O0, WQ_STEP, WQ_EP, WQ_EN, WQ_COL, WQ_C1, WQ_C2, DSET = 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E
RA, RB, WROW, WCOL, WI, WJ, ILO, IHI, JLO, JHI = 0x4F, 0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58
CURCELL, PCOL, VO, LNIDX, CUROFF, TVMASK = 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E
RCOL, HRUN, VRUN, WOFF, RUN = 0x5F, 0x60, 0x61, 0x62, 0x63
NV, RAYOFF, NI = 0x64, 0x65, 0x66
SPAN, RUNON = 0x67, 0x68
VLIST = 0x61A0                       # up to 32 affected-virus offsets
NV_SH = 0x61C1                       # RAM shadow of NV (persists across the DELTA phase split)

DROP_SETUP = False        # set True for the production cart variant (drops the setup term)

_uid = [0]
def uid(tag):
    _uid[0] += 1
    return f"{tag}_{_uid[0]}"


def emit_base_info(a):
    a.label("base_info")
    a.ins("LDA_imm", 0); a.ins("STA_zp", BI_COL)
    a.label("bi_col")
    a.ins("LDA_imm", 16); a.ins("STA_zp", BI_FO)
    a.ins("LDA_imm", 0); a.ins("STA_zp", BI_VCC)
    a.ins("LDA_zp", BI_COL); a.ins("STA_zp", BI_OFF)
    a.ins("LDA_imm", 0); a.ins("STA_zp", BI_ROW)
    a.label("bi_row")
    a.ins("LDX_zp", BI_OFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "bi_rnext")
    a.ins("LDA_zp", BI_FO); a.ins("CMP_imm", 16); a.br("BNE", "bi_notfirst")
    a.ins("LDA_zp", BI_ROW); a.ins("STA_zp", BI_FO)
    a.label("bi_notfirst")
    a.ins("LDX_zp", BI_OFF); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BNE", "bi_rnext")
    a.ins("INC_zp", BI_VCC)
    a.label("bi_rnext")
    a.ins("LDA_zp", BI_OFF); a.ins("CLC"); a.ins("ADC_imm", 8); a.ins("STA_zp", BI_OFF)
    a.ins("INC_zp", BI_ROW); a.ins("LDA_zp", BI_ROW); a.ins("CMP_imm", ROWS); a.br("BNE", "bi_row")
    a.ins("LDX_zp", BI_COL)
    a.ins("LDA_zp", BI_FO); a.ins16("STA_absX", BI_SURF)
    a.ins("LDA_zp", BI_VCC); a.ins16("STA_absX", BI_VC)
    a.ins("INC_zp", BI_COL); a.ins("LDA_zp", BI_COL); a.ins("CMP_imm", COLS); a.br("BNE", "bi_col")
    a.ins("RTS")


def emit_wq(a):
    """Window-qualify: cells WQ_O0, +STEP, +2*STEP on BOARD; end-adj WQ_EP/WQ_EN (0xFF=none).
    INC DSET if the 3-cell same-color run touches a same-color virus."""
    a.label("wq")
    a.ins("LDX_zp", WQ_O0); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "wq_early")
    a.ins("AND_imm", 0x0F); a.ins("STA_zp", WQ_COL)
    a.ins("LDA_zp", WQ_O0); a.ins("CLC"); a.ins("ADC_zp", WQ_STEP); a.ins("STA_zp", WQ_C1); a.ins("TAX")
    a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "wq_early")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", WQ_COL); a.br("BNE", "wq_early")
    a.ins("LDA_zp", WQ_C1); a.ins("CLC"); a.ins("ADC_zp", WQ_STEP); a.ins("STA_zp", WQ_C2); a.ins("TAX")
    a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "wq_early")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", WQ_COL); a.br("BNE", "wq_early")
    a.jmp("wq_touch")
    a.label("wq_early")
    a.ins("RTS")
    a.label("wq_touch")
    # run confirmed; touch = any run cell is a virus (color already matches)
    a.ins("LDX_zp", WQ_O0); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BEQ", "wq_yes")
    a.ins("LDX_zp", WQ_C1); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BEQ", "wq_yes")
    a.ins("LDX_zp", WQ_C2); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BEQ", "wq_yes")
    # end-adjacent EP (must recheck color)
    a.ins("LDA_zp", WQ_EP); a.ins("CMP_imm", 0xFF); a.br("BEQ", "wq_ck_en")
    a.ins("TAX"); a.ins16("LDA_absX", BOARD); a.ins("TAY"); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BNE", "wq_ck_en")
    a.ins("TYA"); a.ins("AND_imm", 0x0F); a.ins("CMP_zp", WQ_COL); a.br("BEQ", "wq_yes")
    a.label("wq_ck_en")
    a.ins("LDA_zp", WQ_EN); a.ins("CMP_imm", 0xFF); a.br("BEQ", "wq_ret")
    a.ins("TAX"); a.ins16("LDA_absX", BOARD); a.ins("TAY"); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BNE", "wq_ret")
    a.ins("TYA"); a.ins("AND_imm", 0x0F); a.ins("CMP_zp", WQ_COL); a.br("BNE", "wq_ret")
    a.label("wq_yes")
    a.ins("INC_zp", DSET)
    a.label("wq_ret")
    a.ins("RTS")


def emit_row_wins(a):
    """Row windows in row WROW, window-start col WI in [ILO,IHI]. step=1."""
    a.label("row_wins")
    a.ins("LDA_zp", ILO); a.ins("STA_zp", WI)
    a.label("rw_top")
    a.ins("LDA_zp", WI); a.ins("CMP_zp", IHI); a.br("BEQ", "rw_body"); a.br("BCS", "rw_done")
    a.label("rw_body")
    a.ins("LDA_zp", WROW); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("CLC"); a.ins("ADC_zp", WI); a.ins("STA_zp", WQ_O0)
    a.ins("LDA_imm", 1); a.ins("STA_zp", WQ_STEP)
    a.ins("LDA_zp", WI); a.br("BEQ", "rw_noep")
    a.ins("LDA_zp", WQ_O0); a.ins("SEC"); a.ins("SBC_imm", 1); a.ins("STA_zp", WQ_EP); a.jmp("rw_en")
    a.label("rw_noep")
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", WQ_EP)
    a.label("rw_en")
    a.ins("LDA_zp", WI); a.ins("CMP_imm", 5); a.br("BCS", "rw_noen")
    a.ins("LDA_zp", WQ_O0); a.ins("CLC"); a.ins("ADC_imm", 3); a.ins("STA_zp", WQ_EN); a.jmp("rw_call")
    a.label("rw_noen")
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", WQ_EN)
    a.label("rw_call")
    a.jsr("wq")
    a.ins("INC_zp", WI); a.jmp("rw_top")
    a.label("rw_done")
    a.ins("RTS")


def emit_col_wins(a):
    """Col windows in col WCOL, window-start row WJ in [JLO,JHI]. step=8."""
    a.label("col_wins")
    a.ins("LDA_zp", JLO); a.ins("STA_zp", WJ)
    a.label("cw_top")
    a.ins("LDA_zp", WJ); a.ins("CMP_zp", JHI); a.br("BEQ", "cw_body"); a.br("BCS", "cw_done")
    a.label("cw_body")
    a.ins("LDA_zp", WJ); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("ASL_A"); a.ins("CLC"); a.ins("ADC_zp", WCOL); a.ins("STA_zp", WQ_O0)
    a.ins("LDA_imm", 8); a.ins("STA_zp", WQ_STEP)
    a.ins("LDA_zp", WJ); a.br("BEQ", "cw_noep")
    a.ins("LDA_zp", WQ_O0); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", WQ_EP); a.jmp("cw_en")
    a.label("cw_noep")
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", WQ_EP)
    a.label("cw_en")
    a.ins("LDA_zp", WJ); a.ins("CMP_imm", 13); a.br("BCS", "cw_noen")
    a.ins("LDA_zp", WQ_O0); a.ins("CLC"); a.ins("ADC_imm", 24); a.ins("STA_zp", WQ_EN); a.jmp("cw_call")
    a.label("cw_noen")
    a.ins("LDA_imm", 0xFF); a.ins("STA_zp", WQ_EN)
    a.label("cw_call")
    a.jsr("wq")
    a.ins("INC_zp", WJ); a.jmp("cw_top")
    a.label("cw_done")
    a.ins("RTS")


def _clamp_lo(a, src, dst):
    """dst = max(0, src-2)"""
    lab = uid("clo")
    a.ins("LDA_zp", src); a.ins("SEC"); a.ins("SBC_imm", 2); a.br("BCS", lab); a.ins("LDA_imm", 0)
    a.label(lab); a.ins("STA_zp", dst)

def _clamp_hi(a, src, M, dst):
    """dst = min(src, M)"""
    lab = uid("chi")
    a.ins("LDA_zp", src); a.ins("CMP_imm", M + 1); a.br("BCC", lab); a.ins("LDA_imm", M)
    a.label(lab); a.ins("STA_zp", dst)

def _min2(a, x, y, dst):
    lab = uid("mn")
    a.ins("LDA_zp", x); a.ins("CMP_zp", y); a.br("BCC", lab); a.ins("LDA_zp", y)
    a.label(lab); a.ins("STA_zp", dst)

def _max2(a, x, y, dst):
    lab = uid("mx")
    a.ins("LDA_zp", x); a.ins("CMP_zp", y); a.br("BCS", lab); a.ins("LDA_zp", y)
    a.label(lab); a.ins("STA_zp", dst)


def emit_setup_delta(a):
    """DSET = # new qualifying windows through offa/offb (union, no double-count)."""
    a.label("setup_delta")
    a.ins("LDA_imm", 0); a.ins("STA_zp", DSET)
    a.ins("LDA_zp", Z_OFFA); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("STA_zp", RA)
    a.ins("LDA_zp", Z_OFFB); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("STA_zp", RB)
    a.ins("LDA_zp", COLA); a.ins("CMP_zp", COLB); a.br("BNE", "sd_horiz")
    # VERTICAL: col=COLA; row windows through col for rows RA & RB; col windows over union rows
    _clamp_lo(a, COLA, ILO); _clamp_hi(a, COLA, 5, IHI)
    a.ins("LDA_zp", RA); a.ins("STA_zp", WROW); a.jsr("row_wins")
    a.ins("LDA_zp", RB); a.ins("STA_zp", WROW); a.jsr("row_wins")
    _min2(a, RA, RB, SA); _max2(a, RA, RB, SB)        # rmin/rmax in SA/SB
    _clamp_lo(a, SA, JLO); _clamp_hi(a, SB, 13, JHI)
    a.ins("LDA_zp", COLA); a.ins("STA_zp", WCOL); a.jsr("col_wins")
    a.ins("RTS")
    a.label("sd_horiz")
    # HORIZONTAL: row=RA; col windows through row for cols COLA & COLB; row windows over union cols
    _clamp_lo(a, RA, JLO); _clamp_hi(a, RA, 13, JHI)
    a.ins("LDA_zp", COLA); a.ins("STA_zp", WCOL); a.jsr("col_wins")
    a.ins("LDA_zp", COLB); a.ins("STA_zp", WCOL); a.jsr("col_wins")
    _min2(a, COLA, COLB, SA); _max2(a, COLA, COLB, SB)
    _clamp_lo(a, SA, ILO); _clamp_hi(a, SB, 5, IHI)
    a.ins("LDA_zp", RA); a.ins("STA_zp", WROW); a.jsr("row_wins")
    a.ins("RTS")


def emit_vir_run2(a):
    """RUN2 = max(hrun,vrun)^2 for the virus at VO on BOARD (g_readiness per-virus)."""
    a.label("vir_run2")
    a.ins("LDX_zp", VO); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0x0F); a.ins("STA_zp", RCOL)
    a.ins("LDA_imm", 1); a.ins("STA_zp", HRUN); a.ins("LDA_imm", 1); a.ins("STA_zp", VRUN)
    # horizontal left
    a.ins("LDA_zp", VO); a.ins("STA_zp", WOFF)
    a.label("vr_hl")
    a.ins("LDA_zp", WOFF); a.ins("AND_imm", 7); a.br("BEQ", "vr_hr")
    a.ins("DEC_zp", WOFF)
    a.ins("LDX_zp", WOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "vr_hr")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", RCOL); a.br("BNE", "vr_hr")
    a.ins("INC_zp", HRUN); a.jmp("vr_hl")
    a.label("vr_hr")
    a.ins("LDA_zp", VO); a.ins("STA_zp", WOFF)
    a.label("vr_hrr")
    a.ins("LDA_zp", WOFF); a.ins("AND_imm", 7); a.ins("CMP_imm", 7); a.br("BEQ", "vr_v")
    a.ins("INC_zp", WOFF)
    a.ins("LDX_zp", WOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "vr_v")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", RCOL); a.br("BNE", "vr_v")
    a.ins("INC_zp", HRUN); a.jmp("vr_hrr")
    a.label("vr_v")
    # vertical up
    a.ins("LDA_zp", VO); a.ins("STA_zp", WOFF)
    a.label("vr_vu")
    a.ins("LDA_zp", WOFF); a.ins("CMP_imm", 8); a.br("BCC", "vr_vd")
    a.ins("LDA_zp", WOFF); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", WOFF)
    a.ins("LDX_zp", WOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "vr_vd")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", RCOL); a.br("BNE", "vr_vd")
    a.ins("INC_zp", VRUN); a.jmp("vr_vu")
    a.label("vr_vd")
    a.ins("LDA_zp", VO); a.ins("STA_zp", WOFF)
    a.label("vr_vdd")
    a.ins("LDA_zp", WOFF); a.ins("CMP_imm", 120); a.br("BCS", "vr_mx")
    a.ins("LDA_zp", WOFF); a.ins("CLC"); a.ins("ADC_imm", 8); a.ins("STA_zp", WOFF)
    a.ins("LDX_zp", WOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "vr_mx")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", RCOL); a.br("BNE", "vr_mx")
    a.ins("INC_zp", VRUN); a.jmp("vr_vdd")
    a.label("vr_mx")
    a.ins("LDA_zp", HRUN); a.ins("CMP_zp", VRUN); a.br("BCS", "vr_hbig"); a.ins("LDA_zp", VRUN); a.jmp("vr_sq")
    a.label("vr_hbig"); a.ins("LDA_zp", HRUN)
    a.label("vr_sq")
    a.ins("STA_zp", RUN)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", RUN2_LO); a.ins16("STA_abs", RUN2_HI)
    a.ins("LDX_zp", RUN)
    a.label("vr_ml")
    a.ins16("LDA_abs", RUN2_LO); a.ins("CLC"); a.ins("ADC_zp", RUN); a.ins16("STA_abs", RUN2_LO)
    a.ins16("LDA_abs", RUN2_HI); a.ins("ADC_imm", 0); a.ins16("STA_abs", RUN2_HI)
    a.ins("DEX"); a.br("BNE", "vr_ml")
    a.ins("RTS")


def emit_vir_run2_ext(a):
    """RUN2 = extendability-aware readiness for the virus at VO: per direction run^2 only
    if the span of (EMPTY or same-low-nibble) cells through the virus >= 4, else 0."""
    a.label("vir_run2_ext")
    a.ins("LDX_zp", VO); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0x0F); a.ins("STA_zp", RCOL)
    # ---------- horizontal: run in HRUN, span in SPAN ----------
    a.ins("LDA_imm", 1); a.ins("STA_zp", HRUN); a.ins("STA_zp", SPAN)
    a.ins("LDA_imm", 1); a.ins("STA_zp", RUNON)              # still-in-run flag
    a.ins("LDA_zp", VO); a.ins("STA_zp", WOFF)
    a.label("vx_hl")                                          # walk left
    a.ins("LDA_zp", WOFF); a.ins("AND_imm", 7); a.br("BEQ", "vx_hr")
    a.ins("DEC_zp", WOFF)
    a.ins("LDX_zp", WOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "vx_hl_e")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", RCOL); a.br("BNE", "vx_hr")
    a.ins("INC_zp", SPAN)                                     # same color: span+, run+ if contiguous
    a.ins("LDA_zp", RUNON); a.br("BEQ", "vx_hl")
    a.ins("INC_zp", HRUN); a.jmp("vx_hl")
    a.label("vx_hl_e")
    a.ins("INC_zp", SPAN); a.ins("LDA_imm", 0); a.ins("STA_zp", RUNON); a.jmp("vx_hl")
    a.label("vx_hr")                                          # walk right
    a.ins("LDA_imm", 1); a.ins("STA_zp", RUNON)
    a.ins("LDA_zp", VO); a.ins("STA_zp", WOFF)
    a.label("vx_hrl")
    a.ins("LDA_zp", WOFF); a.ins("AND_imm", 7); a.ins("CMP_imm", 7); a.br("BEQ", "vx_hd")
    a.ins("INC_zp", WOFF)
    a.ins("LDX_zp", WOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "vx_hr_e")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", RCOL); a.br("BNE", "vx_hd")
    a.ins("INC_zp", SPAN)
    a.ins("LDA_zp", RUNON); a.br("BEQ", "vx_hrl")
    a.ins("INC_zp", HRUN); a.jmp("vx_hrl")
    a.label("vx_hr_e")
    a.ins("INC_zp", SPAN); a.ins("LDA_imm", 0); a.ins("STA_zp", RUNON); a.jmp("vx_hrl")
    a.label("vx_hd")
    a.ins("LDA_zp", SPAN); a.ins("CMP_imm", 4); a.br("BCS", "vx_hok")
    a.ins("LDA_imm", 0); a.ins("STA_zp", HRUN)                # dead direction
    a.label("vx_hok")
    # ---------- vertical: run in VRUN, span in SPAN ----------
    a.ins("LDA_imm", 1); a.ins("STA_zp", VRUN); a.ins("STA_zp", SPAN)
    a.ins("LDA_imm", 1); a.ins("STA_zp", RUNON)
    a.ins("LDA_zp", VO); a.ins("STA_zp", WOFF)
    a.label("vx_vu")
    a.ins("LDA_zp", WOFF); a.ins("CMP_imm", 8); a.br("BCC", "vx_vd")
    a.ins("LDA_zp", WOFF); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", WOFF)
    a.ins("LDX_zp", WOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "vx_vu_e")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", RCOL); a.br("BNE", "vx_vd")
    a.ins("INC_zp", SPAN)
    a.ins("LDA_zp", RUNON); a.br("BEQ", "vx_vu")
    a.ins("INC_zp", VRUN); a.jmp("vx_vu")
    a.label("vx_vu_e")
    a.ins("INC_zp", SPAN); a.ins("LDA_imm", 0); a.ins("STA_zp", RUNON); a.jmp("vx_vu")
    a.label("vx_vd")
    a.ins("LDA_imm", 1); a.ins("STA_zp", RUNON)
    a.ins("LDA_zp", VO); a.ins("STA_zp", WOFF)
    a.label("vx_vdl")
    a.ins("LDA_zp", WOFF); a.ins("CMP_imm", 120); a.br("BCS", "vx_vfin")
    a.ins("LDA_zp", WOFF); a.ins("CLC"); a.ins("ADC_imm", 8); a.ins("STA_zp", WOFF)
    a.ins("LDX_zp", WOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "vx_vd_e")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", RCOL); a.br("BNE", "vx_vfin")
    a.ins("INC_zp", SPAN)
    a.ins("LDA_zp", RUNON); a.br("BEQ", "vx_vdl")
    a.ins("INC_zp", VRUN); a.jmp("vx_vdl")
    a.label("vx_vd_e")
    a.ins("INC_zp", SPAN); a.ins("LDA_imm", 0); a.ins("STA_zp", RUNON); a.jmp("vx_vdl")
    a.label("vx_vfin")
    a.ins("LDA_zp", SPAN); a.ins("CMP_imm", 4); a.br("BCS", "vx_vok")
    a.ins("LDA_imm", 0); a.ins("STA_zp", VRUN)
    a.label("vx_vok")
    # ---------- RUN2 = max(HRUN,VRUN)^2 ----------
    a.ins("LDA_zp", HRUN); a.ins("CMP_zp", VRUN); a.br("BCS", "vx_h"); a.ins("LDA_zp", VRUN); a.jmp("vx_sq")
    a.label("vx_h"); a.ins("LDA_zp", HRUN)
    a.label("vx_sq")
    a.ins("STA_zp", RUN)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", RUN2_LO); a.ins16("STA_abs", RUN2_HI)
    a.ins("LDA_zp", RUN); a.br("BEQ", "vx_done")              # dead both ways -> 0
    a.ins("LDX_zp", RUN)
    a.label("vx_ml")
    a.ins16("LDA_abs", RUN2_LO); a.ins("CLC"); a.ins("ADC_zp", RUN); a.ins16("STA_abs", RUN2_LO)
    a.ins16("LDA_abs", RUN2_HI); a.ins("ADC_imm", 0); a.ins16("STA_abs", RUN2_HI)
    a.ins("DEX"); a.br("BNE", "vx_ml")
    a.label("vx_done")
    a.ins("RTS")


def emit_vir_vrun2(a):
    """RUN2 = vertical-only readiness (vrun^2) for the virus at VO."""
    a.label("vir_vrun2")
    a.ins("LDX_zp", VO); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0x0F); a.ins("STA_zp", RCOL)
    a.ins("LDA_imm", 1); a.ins("STA_zp", VRUN)
    a.ins("LDA_zp", VO); a.ins("STA_zp", WOFF)
    a.label("vv_u")
    a.ins("LDA_zp", WOFF); a.ins("CMP_imm", 8); a.br("BCC", "vv_d")
    a.ins("LDA_zp", WOFF); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", WOFF)
    a.ins("LDX_zp", WOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "vv_d")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", RCOL); a.br("BNE", "vv_d")
    a.ins("INC_zp", VRUN); a.jmp("vv_u")
    a.label("vv_d")
    a.ins("LDA_zp", VO); a.ins("STA_zp", WOFF)
    a.label("vv_dl")
    a.ins("LDA_zp", WOFF); a.ins("CMP_imm", 120); a.br("BCS", "vv_sq")
    a.ins("LDA_zp", WOFF); a.ins("CLC"); a.ins("ADC_imm", 8); a.ins("STA_zp", WOFF)
    a.ins("LDX_zp", WOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "vv_sq")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", RCOL); a.br("BNE", "vv_sq")
    a.ins("INC_zp", VRUN); a.jmp("vv_dl")
    a.label("vv_sq")
    a.ins("LDA_zp", VRUN); a.ins("STA_zp", RUN)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", RUN2_LO); a.ins16("STA_abs", RUN2_HI)
    a.ins("LDX_zp", RUN)
    a.label("vv_ml")
    a.ins16("LDA_abs", RUN2_LO); a.ins("CLC"); a.ins("ADC_zp", RUN); a.ins16("STA_abs", RUN2_LO)
    a.ins16("LDA_abs", RUN2_HI); a.ins("ADC_imm", 0); a.ins16("STA_abs", RUN2_HI)
    a.ins("DEX"); a.br("BNE", "vv_ml")
    a.ins("RTS")


def emit_vrdy_new(a):
    """Collect same-color viruses vertically contiguous to each placed cell (walk up/down
    through same-nibble cells) into VLIST2; sum their NEW vrun2 into VNEW."""
    a.label("vrdy_new")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", VNEW_LO); a.ins16("STA_abs", VNEW_HI); a.ins("STA_zp", NV)
    a.jsr("clear_visit")                 # dedup (vertical pills walk across each other's cells)
    a.label("vn_body")
    for i, zoff in enumerate(("A", "B")):
        src = Z_OFFA if zoff == "A" else Z_OFFB
        a.ins("LDA_zp", src); a.ins("STA_zp", CURCELL)
        a.ins("LDX_zp", src); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0x0F); a.ins("STA_zp", PCOL)
        for dname, guard, step in (("u", "up", -8), ("d", "dn", 8)):
            a.ins("LDA_zp", CURCELL); a.ins("STA_zp", RAYOFF)
            a.label(f"vn_{zoff}{dname}")
            if step < 0:
                a.ins("LDA_zp", RAYOFF); a.ins("CMP_imm", 8); a.br("BCC", f"vn_{zoff}{dname}_x")
                a.ins("LDA_zp", RAYOFF); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", RAYOFF)
            else:
                a.ins("LDA_zp", RAYOFF); a.ins("CMP_imm", 120); a.br("BCS", f"vn_{zoff}{dname}_x")
                a.ins("LDA_zp", RAYOFF); a.ins("CLC"); a.ins("ADC_imm", 8); a.ins("STA_zp", RAYOFF)
            a.ins("LDX_zp", RAYOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", f"vn_{zoff}{dname}_x")
            a.ins("AND_imm", 0x0F); a.ins("CMP_zp", PCOL); a.br("BNE", f"vn_{zoff}{dname}_x")
            # same-color: virus? -> record (dedup by simple linear check is overkill; columns
            # of A and B may overlap only when vertical pill: dedup via VISIT bitmap reuse)
            a.ins("LDX_zp", RAYOFF); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BNE", f"vn_{zoff}{dname}")
            # VISIT dedup: bit (off&7) of byte (off>>3)
            a.ins("LDA_zp", RAYOFF); a.ins("AND_imm", 7); a.ins("TAY"); a.ins("LDA_imm", 1)
            a.label(f"vn_{zoff}{dname}_sh")
            a.ins("DEY"); a.br("BMI", f"vn_{zoff}{dname}_shd"); a.ins("ASL_A"); a.jmp(f"vn_{zoff}{dname}_sh")
            a.label(f"vn_{zoff}{dname}_shd")
            a.ins("STA_zp", TVMASK)
            a.ins("LDA_zp", RAYOFF); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("TAX")
            a.ins16("LDA_absX", VISIT); a.ins("AND_zp", TVMASK); a.br("BNE", f"vn_{zoff}{dname}")
            a.ins16("LDA_absX", VISIT); a.ins("ORA_zp", TVMASK); a.ins16("STA_absX", VISIT)
            a.ins("LDX_zp", NV); a.ins("LDA_zp", RAYOFF); a.ins16("STA_absX", VLIST2); a.ins("INC_zp", NV)
            a.ins("LDA_zp", RAYOFF); a.ins("STA_zp", VO); a.jsr("vir_vrun2")
            a.ins16("LDA_abs", VNEW_LO); a.ins("CLC"); a.ins16("ADC_abs", RUN2_LO); a.ins16("STA_abs", VNEW_LO)
            a.ins16("LDA_abs", VNEW_HI); a.ins16("ADC_abs", RUN2_HI); a.ins16("STA_abs", VNEW_HI)
            a.jmp(f"vn_{zoff}{dname}")
            a.label(f"vn_{zoff}{dname}_x")
    a.ins("LDA_zp", NV); a.ins16("STA_abs", NV2_SH)
    a.ins("RTS")


def emit_vrdy_old(a):
    """Mask placed cells, re-score VLIST2 on the old board -> VOLD; EV_VRDY = BASE_VRDY +
    VNEW - VOLD; restore cells."""
    a.label("vrdy_old")
    a.ins("LDX_zp", Z_OFFA); a.ins16("LDA_absX", BOARD); a.ins16("STA_abs", SAVA); a.ins("LDA_imm", EMPTY); a.ins16("STA_absX", BOARD)
    a.ins("LDX_zp", Z_OFFB); a.ins16("LDA_absX", BOARD); a.ins16("STA_abs", SAVB); a.ins("LDA_imm", EMPTY); a.ins16("STA_absX", BOARD)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", VOLD_LO); a.ins16("STA_abs", VOLD_HI); a.ins("STA_zp", NI)
    a.label("vo_lp")
    a.ins("LDA_zp", NI); a.ins16("CMP_abs", NV2_SH); a.br("BCS", "vo_done")
    a.ins("LDX_zp", NI); a.ins16("LDA_absX", VLIST2); a.ins("STA_zp", VO); a.jsr("vir_vrun2")
    a.ins16("LDA_abs", VOLD_LO); a.ins("CLC"); a.ins16("ADC_abs", RUN2_LO); a.ins16("STA_abs", VOLD_LO)
    a.ins16("LDA_abs", VOLD_HI); a.ins16("ADC_abs", RUN2_HI); a.ins16("STA_abs", VOLD_HI)
    a.ins("INC_zp", NI); a.jmp("vo_lp")
    a.label("vo_done")
    a.ins("LDX_zp", Z_OFFA); a.ins16("LDA_abs", SAVA); a.ins16("STA_absX", BOARD)
    a.ins("LDX_zp", Z_OFFB); a.ins16("LDA_abs", SAVB); a.ins16("STA_absX", BOARD)
    a.ins16("LDA_abs", BASE_VRDY_LO); a.ins("CLC"); a.ins16("ADC_abs", VNEW_LO); a.ins16("STA_abs", P.EV_VRDY_LO)
    a.ins16("LDA_abs", BASE_VRDY_HI); a.ins16("ADC_abs", VNEW_HI); a.ins16("STA_abs", P.EV_VRDY_HI)
    a.ins16("LDA_abs", P.EV_VRDY_LO); a.ins("SEC"); a.ins16("SBC_abs", VOLD_LO); a.ins16("STA_abs", P.EV_VRDY_LO)
    a.ins16("LDA_abs", P.EV_VRDY_HI); a.ins16("SBC_abs", VOLD_HI); a.ins16("STA_abs", P.EV_VRDY_HI)
    a.ins("RTS")


def emit_vrdy_full(a):
    """EV_VRDY = sum of vertical run^2 over all viruses on BOARD (full scan)."""
    a.label("vrdy_full")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", P.EV_VRDY_LO); a.ins16("STA_abs", P.EV_VRDY_HI)
    a.ins("LDA_imm", 0); a.ins("STA_zp", VO)
    a.label("vf_lp")
    a.ins("LDX_zp", VO); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "vf_nx")
    a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BNE", "vf_nx")
    a.jsr("vir_vrun2")
    a.ins16("LDA_abs", P.EV_VRDY_LO); a.ins("CLC"); a.ins16("ADC_abs", RUN2_LO); a.ins16("STA_abs", P.EV_VRDY_LO)
    a.ins16("LDA_abs", P.EV_VRDY_HI); a.ins16("ADC_abs", RUN2_HI); a.ins16("STA_abs", P.EV_VRDY_HI)
    a.label("vf_nx")
    a.ins("INC_zp", VO); a.ins("LDA_zp", VO); a.ins("CMP_imm", 128); a.br("BNE", "vf_lp")
    a.ins("RTS")


def emit_collect_virus(a):
    """VO is a same-low-nibble cell contiguous to a placed cell. If it's a virus not yet visited:
    mark, append offset to VLIST, add its new run2 to RSUM."""
    a.label("collect_virus")
    a.ins("LDX_zp", VO); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0xF0); a.ins("CMP_imm", 0xD0); a.br("BNE", "cv_ret")
    a.ins("LDA_zp", VO); a.ins("AND_imm", 7); a.ins("TAY"); a.ins("LDA_imm", 1)
    a.label("cv_shift")
    a.ins("DEY"); a.br("BMI", "cv_shd"); a.ins("ASL_A"); a.jmp("cv_shift")
    a.label("cv_shd")
    a.ins("STA_zp", TVMASK)
    a.ins("LDA_zp", VO); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("TAX")
    a.ins16("LDA_absX", VISIT); a.ins("AND_zp", TVMASK); a.br("BNE", "cv_ret")     # already visited
    a.ins16("LDA_absX", VISIT); a.ins("ORA_zp", TVMASK); a.ins16("STA_absX", VISIT)
    a.ins("LDX_zp", NV); a.ins("LDA_zp", VO); a.ins16("STA_absX", VLIST); a.ins("INC_zp", NV)
    a.jsr("vir_run2")
    a.ins16("LDA_abs", RSUM_LO); a.ins("CLC"); a.ins16("ADC_abs", RUN2_LO); a.ins16("STA_abs", RSUM_LO)
    a.ins16("LDA_abs", RSUM_HI); a.ins16("ADC_abs", RUN2_HI); a.ins16("STA_abs", RSUM_HI)
    a.label("cv_ret")
    a.ins("RTS")


def emit_collect_cell(a):
    """Scan the 4 rays (L/R/U/D) from CURCELL through same-low-nibble (PCOL) cells; collect the
    viruses among them (the only viruses whose run the placed cell can change)."""
    a.label("collect_cell")
    a.ins("LDA_zp", CURCELL); a.ins("STA_zp", RAYOFF)                              # LEFT
    a.label("cc_l")
    a.ins("LDA_zp", RAYOFF); a.ins("AND_imm", 7); a.br("BEQ", "cc_ri")
    a.ins("DEC_zp", RAYOFF)
    a.ins("LDX_zp", RAYOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "cc_ri")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", PCOL); a.br("BNE", "cc_ri")
    a.ins("LDA_zp", RAYOFF); a.ins("STA_zp", VO); a.jsr("collect_virus"); a.jmp("cc_l")
    a.label("cc_ri")
    a.ins("LDA_zp", CURCELL); a.ins("STA_zp", RAYOFF)                              # RIGHT
    a.label("cc_r")
    a.ins("LDA_zp", RAYOFF); a.ins("AND_imm", 7); a.ins("CMP_imm", 7); a.br("BEQ", "cc_ui")
    a.ins("INC_zp", RAYOFF)
    a.ins("LDX_zp", RAYOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "cc_ui")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", PCOL); a.br("BNE", "cc_ui")
    a.ins("LDA_zp", RAYOFF); a.ins("STA_zp", VO); a.jsr("collect_virus"); a.jmp("cc_r")
    a.label("cc_ui")
    a.ins("LDA_zp", CURCELL); a.ins("STA_zp", RAYOFF)                              # UP
    a.label("cc_u")
    a.ins("LDA_zp", RAYOFF); a.ins("CMP_imm", 8); a.br("BCC", "cc_di")
    a.ins("LDA_zp", RAYOFF); a.ins("SEC"); a.ins("SBC_imm", 8); a.ins("STA_zp", RAYOFF)
    a.ins("LDX_zp", RAYOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "cc_di")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", PCOL); a.br("BNE", "cc_di")
    a.ins("LDA_zp", RAYOFF); a.ins("STA_zp", VO); a.jsr("collect_virus"); a.jmp("cc_u")
    a.label("cc_di")
    a.ins("LDA_zp", CURCELL); a.ins("STA_zp", RAYOFF)                              # DOWN
    a.label("cc_d")
    a.ins("LDA_zp", RAYOFF); a.ins("CMP_imm", 120); a.br("BCS", "cc_done")
    a.ins("LDA_zp", RAYOFF); a.ins("CLC"); a.ins("ADC_imm", 8); a.ins("STA_zp", RAYOFF)
    a.ins("LDX_zp", RAYOFF); a.ins16("LDA_absX", BOARD); a.ins("CMP_imm", EMPTY); a.br("BEQ", "cc_done")
    a.ins("AND_imm", 0x0F); a.ins("CMP_zp", PCOL); a.br("BNE", "cc_done")
    a.ins("LDA_zp", RAYOFF); a.ins("STA_zp", VO); a.jsr("collect_virus"); a.jmp("cc_d")
    a.label("cc_done")
    a.ins("RTS")


def emit_clear_visit(a):
    a.label("clear_visit")
    a.ins("LDX_imm", 15); a.ins("LDA_imm", 0)
    a.label("cv_lp")
    a.ins16("STA_absX", VISIT); a.ins("DEX"); a.br("BPL", "cv_lp")
    a.ins("RTS")


def emit_readiness_delta(a):
    """EV_RDY = BASE_RDY + sum_affected(run2_new - run2_old)."""
    a.label("readiness_delta")            # standalone (unit test): both passes back-to-back
    a.jsr("readiness_new"); a.jsr("readiness_old"); a.ins("RTS")


def emit_readiness_new(a):
    """NEW pass: collect affected viruses (contiguous to placed cells) + sum new run2. Persists
    VLIST/NV_SH/RNEW in RAM so the OLD pass can run in a later NMI frame."""
    a.label("readiness_new")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", RSUM_LO); a.ins16("STA_abs", RSUM_HI); a.ins("STA_zp", NV)
    a.jsr("clear_visit")
    a.ins("LDA_zp", Z_OFFA); a.ins("STA_zp", CURCELL); a.ins("LDX_zp", Z_OFFA); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0x0F); a.ins("STA_zp", PCOL); a.jsr("collect_cell")
    a.ins("LDA_zp", Z_OFFB); a.ins("STA_zp", CURCELL); a.ins("LDX_zp", Z_OFFB); a.ins16("LDA_absX", BOARD); a.ins("AND_imm", 0x0F); a.ins("STA_zp", PCOL); a.jsr("collect_cell")
    a.ins16("LDA_abs", RSUM_LO); a.ins16("STA_abs", RNEW_LO); a.ins16("LDA_abs", RSUM_HI); a.ins16("STA_abs", RNEW_HI)
    a.ins("LDA_zp", NV); a.ins16("STA_abs", NV_SH)
    a.ins("RTS")


def emit_readiness_old(a):
    """OLD pass: re-score exactly the collected viruses on the masked board -> EV_RDY."""
    a.label("readiness_old")
    a.ins("LDX_zp", Z_OFFA); a.ins16("LDA_absX", BOARD); a.ins16("STA_abs", SAVA); a.ins("LDA_imm", EMPTY); a.ins16("STA_absX", BOARD)
    a.ins("LDX_zp", Z_OFFB); a.ins16("LDA_absX", BOARD); a.ins16("STA_abs", SAVB); a.ins("LDA_imm", EMPTY); a.ins16("STA_absX", BOARD)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", RSUM_LO); a.ins16("STA_abs", RSUM_HI); a.ins("STA_zp", NI)
    a.label("rd_old")
    a.ins("LDA_zp", NI); a.ins16("CMP_abs", NV_SH); a.br("BCS", "rd_old_done")
    a.ins("LDX_zp", NI); a.ins16("LDA_absX", VLIST); a.ins("STA_zp", VO); a.jsr("vir_run2")
    a.ins16("LDA_abs", RSUM_LO); a.ins("CLC"); a.ins16("ADC_abs", RUN2_LO); a.ins16("STA_abs", RSUM_LO)
    a.ins16("LDA_abs", RSUM_HI); a.ins16("ADC_abs", RUN2_HI); a.ins16("STA_abs", RSUM_HI)
    a.ins("INC_zp", NI); a.jmp("rd_old")
    a.label("rd_old_done")
    a.ins16("LDA_abs", RSUM_LO); a.ins16("STA_abs", ROLD_LO); a.ins16("LDA_abs", RSUM_HI); a.ins16("STA_abs", ROLD_HI)
    a.ins("LDX_zp", Z_OFFA); a.ins16("LDA_abs", SAVA); a.ins16("STA_absX", BOARD)
    a.ins("LDX_zp", Z_OFFB); a.ins16("LDA_abs", SAVB); a.ins16("STA_absX", BOARD)
    a.ins16("LDA_abs", BASE_RDY_LO); a.ins("CLC"); a.ins16("ADC_abs", RNEW_LO); a.ins16("STA_abs", EV_RDY_LO)
    a.ins16("LDA_abs", BASE_RDY_HI); a.ins16("ADC_abs", RNEW_HI); a.ins16("STA_abs", EV_RDY_HI)
    a.ins16("LDA_abs", EV_RDY_LO); a.ins("SEC"); a.ins16("SBC_abs", ROLD_LO); a.ins16("STA_abs", EV_RDY_LO)
    a.ins16("LDA_abs", EV_RDY_HI); a.ins16("SBC_abs", ROLD_HI); a.ins16("STA_abs", EV_RDY_HI)
    a.ins("RTS")


def emit_delta_terms(a):
    """First DELTA half: easy deltas (maxh/holes/toprisk/buried) + setup + readiness_new.
    BOARD=nb, offa/offb set, base terms + base_info precomputed. Writes SH_* (zp) + EV_BUR/EV_SET."""
    a.label("delta_terms")
    # toprisk = BASE_TR + (offa<24) + (offb<24)
    a.ins16("LDA_abs", BASE_TR); a.ins("STA_zp", SH_TOPRISK)
    a.ins("LDA_zp", Z_OFFA); a.ins("CMP_imm", 24); a.br("BCS", "de_a24"); a.ins("INC_zp", SH_TOPRISK)
    a.label("de_a24")
    a.ins("LDA_zp", Z_OFFB); a.ins("CMP_imm", 24); a.br("BCS", "de_b24"); a.ins("INC_zp", SH_TOPRISK)
    a.label("de_b24")
    # maxh = max(BASE_MH, 16-(offa>>3), 16-(offb>>3))
    a.ins16("LDA_abs", BASE_MH); a.ins("STA_zp", SH_MAXH)
    a.ins("LDA_zp", Z_OFFA); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("STA_zp", DT)
    a.ins("SEC"); a.ins("LDA_imm", 16); a.ins("SBC_zp", DT); a.ins("CMP_zp", SH_MAXH); a.br("BCC", "de_ha"); a.ins("STA_zp", SH_MAXH)
    a.label("de_ha")
    a.ins("LDA_zp", Z_OFFB); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("LSR_A"); a.ins("STA_zp", DT)
    a.ins("SEC"); a.ins("LDA_imm", 16); a.ins("SBC_zp", DT); a.ins("CMP_zp", SH_MAXH); a.br("BCC", "de_hb"); a.ins("STA_zp", SH_MAXH)
    a.label("de_hb")
    # cola/colb
    a.ins("LDA_zp", Z_OFFA); a.ins("AND_imm", 7); a.ins("STA_zp", COLA)
    a.ins("LDA_zp", Z_OFFB); a.ins("AND_imm", 7); a.ins("STA_zp", COLB)
    a.ins("LDA_zp", COLA); a.ins("CMP_zp", COLB); a.br("BNE", "de_horiz")
    # vertical: holes unchanged; buried += 2*vc[col]
    a.ins16("LDA_abs", BASE_HO); a.ins("STA_zp", SH_HOLES)
    a.ins("LDX_zp", COLA); a.ins16("LDA_absX", BI_VC); a.ins("ASL_A"); a.ins("STA_zp", DT); a.jmp("de_bur")
    a.label("de_horiz")
    # holes += |surf[cola]-surf[colb]| ; buried += vc[cola]+vc[colb]
    a.ins("LDX_zp", COLA); a.ins16("LDA_absX", BI_SURF); a.ins("STA_zp", SA)
    a.ins("LDX_zp", COLB); a.ins16("LDA_absX", BI_SURF); a.ins("STA_zp", SB)
    a.ins("LDA_zp", SA); a.ins("CMP_zp", SB); a.br("BCS", "de_hopos")
    a.ins("LDA_zp", SB); a.ins("SEC"); a.ins("SBC_zp", SA); a.jmp("de_hohave")
    a.label("de_hopos")
    a.ins("LDA_zp", SA); a.ins("SEC"); a.ins("SBC_zp", SB)
    a.label("de_hohave")
    a.ins("CLC"); a.ins16("ADC_abs", BASE_HO); a.ins("STA_zp", SH_HOLES)
    a.ins("LDX_zp", COLA); a.ins16("LDA_absX", BI_VC); a.ins("STA_zp", DT)
    a.ins("LDX_zp", COLB); a.ins16("LDA_absX", BI_VC); a.ins("CLC"); a.ins("ADC_zp", DT); a.ins("STA_zp", DT)
    a.label("de_bur")
    # EV_BUR = BASE_BUR + DT
    a.ins("LDA_zp", DT); a.ins("CLC"); a.ins16("ADC_abs", BASE_BUR_LO); a.ins16("STA_abs", EV_BUR_LO)
    a.ins16("LDA_abs", BASE_BUR_HI); a.ins("ADC_imm", 0); a.ins16("STA_abs", EV_BUR_HI)
    # setup delta -> EV_SET  (DROP_SETUP: setup actively hurts L11 clear-rate; omit the term)
    if DROP_SETUP:
        a.ins("LDA_imm", 0); a.ins16("STA_abs", EV_SET)
    else:
        a.jsr("setup_delta")
        a.ins16("LDA_abs", BASE_SET); a.ins("CLC"); a.ins("ADC_zp", DSET); a.ins16("STA_abs", EV_SET)
    a.jsr("readiness_new")               # heavy half 1 (collect + new run2); split point on the cart
    a.jsr("vrdy_new")                    # vertical-readiness new pass (VLIST2, uses NV after readiness saved it)
    a.ins("RTS")


def emit_delta_eval(a):
    """Standalone incremental leaf (unit test / py65): both halves back-to-back."""
    a.label("delta_eval")
    a.jsr("delta_terms"); a.jsr("delta_finish"); a.ins("RTS")


def emit_delta_finish(a):
    """Second DELTA half (own NMI frame on the cart): old readiness pass + combine.
    Assumes SH_MAXH/HOLES/TOPRISK restored, EV_BUR/EV_SET/BASE_* still in RAM, offa/offb set."""
    a.label("delta_finish")
    a.jsr("readiness_old")               # heavy half 2 (old run2) -> EV_RDY
    a.jsr("vrdy_old")                    # vertical-readiness old pass -> EV_VRDY
    a.ins16("LDA_abs", BASE_VIRFLAG); a.ins16("STA_abs", EV_VIRFLAG)   # virflag unchanged (non-clearing)
    a.jsr("combine")
    a.ins("RTS")


def build():
    a = Asm6502(BASE)
    emit_base_info(a); emit_wq(a); emit_row_wins(a); emit_col_wins(a); emit_setup_delta(a)
    emit_vir_run2(a); emit_collect_virus(a); emit_collect_cell(a); emit_clear_visit(a)
    emit_readiness_new(a); emit_readiness_old(a); emit_readiness_delta(a)
    emit_vir_vrun2(a); emit_vrdy_new(a); emit_vrdy_old(a); emit_vrdy_full(a)
    emit_delta_terms(a); emit_delta_finish(a); emit_delta_eval(a); emit_combine(a)
    return a, a.assemble()


def py_leaf(b, nb, orient2, col, offa, offb):
    """Python full-eval leaf score on nb (matches combine)."""
    surf, vc = py_base_info(b)
    mh0, ho0, tr0 = golden_shape(b); bur0 = g_buried(b)
    base = (surf, vc, mh0, ho0, tr0, bur0)
    mh, ho, tr, bur = delta_easy(b, orient2, col, base)
    st = py_setup(nb, offa, offb, g_setup(b))
    rd = py_rdy(b, nb, offa, offb, g_readiness(b))
    vr = vreadiness_delta(b, nb, offa, offb, g_vreadiness(b))
    virfree = not any((x & 0xF0) == 0xD0 for x in nb)
    if virfree:
        return 0, mh, ho, tr, bur, st, rd, vr
    sco = 5000 - 12*mh - 25*ho - 45*tr + 40*st - 30*bur + 4*rd + 12*vr
    return sco, mh, ho, tr, bur, st, rd, vr


def s16(lo, hi):
    v = lo | (hi << 8)
    return v - 0x10000 if v & 0x8000 else v


def main():
    P.BOARD = BOARD
    a, code = build()
    cpu = Cpu(); cpu.load(BASE, code)
    A_binfo = BASE + a.labels["base_info"]
    A_delta = BASE + a.labels["delta_eval"]
    rng = random.Random(77); fails = 0; tested = 0
    term_fail = 0
    for t in range(2500):
        b = _rand_settled(rng)
        # base terms on b, via py + poked into RAM (cart will compute these once per first-ply)
        surf, vc = py_base_info(b)
        mh0, ho0, tr0 = golden_shape(b); bur0 = g_buried(b); set0 = g_setup(b); rdy0 = g_readiness(b)
        virflag = 1 if any((x & 0xF0) == 0xD0 for x in b) else 0
        cpu.set_board(b); cpu.call(A_binfo)                       # 6502 base_info -> BI_SURF/BI_VC
        cpu.mem[BASE_MH] = mh0 & 0xFF; cpu.mem[BASE_HO] = ho0 & 0xFF
        cpu.mem[BASE_TR] = tr0 & 0xFF; cpu.mem[BASE_SET] = set0 & 0xFF
        cpu.mem[BASE_BUR_LO] = bur0 & 0xFF; cpu.mem[BASE_BUR_HI] = (bur0 >> 8) & 0xFF
        cpu.mem[BASE_RDY_LO] = rdy0 & 0xFF; cpu.mem[BASE_RDY_HI] = (rdy0 >> 8) & 0xFF
        vrdy0 = g_vreadiness(b)
        cpu.mem[BASE_VRDY_LO] = vrdy0 & 0xFF; cpu.mem[BASE_VRDY_HI] = (vrdy0 >> 8) & 0xFF
        cpu.mem[BASE_VIRFLAG] = virflag
        ta, tb = rng.randint(0, 2), rng.randint(0, 2)
        for orient2 in (0, 1):
            for col in range(COLS):
                land = _landing(b, orient2, col)
                if land is None:
                    continue
                offa, offb = land
                nb = _place(b, orient2, col, ta, tb)
                if _clears(nb, offa, offb):
                    continue
                cpu.set_board(nb)
                cpu.mem[Z_OFFA] = offa; cpu.mem[Z_OFFB] = offb
                cpu.call(A_delta)
                got = (cpu.mem[SH_MAXH], cpu.mem[SH_HOLES], cpu.mem[SH_TOPRISK],
                       cpu.mem[EV_BUR_LO] | (cpu.mem[EV_BUR_HI] << 8),
                       cpu.mem[EV_SET], cpu.mem[EV_RDY_LO] | (cpu.mem[EV_RDY_HI] << 8),
                       cpu.mem[P.EV_VRDY_LO] | (cpu.mem[P.EV_VRDY_HI] << 8))
                sco = s16(cpu.mem[EV_SCO_LO], cpu.mem[EV_SCO_HI])
                esco, emh, eho, etr, ebur, est, erd, evr = py_leaf(b, nb, orient2, col, offa, offb)
                exp = (emh, eho, etr, ebur, est, erd, evr)
                tested += 1
                if got != exp:
                    term_fail += 1
                    if term_fail <= 6:
                        print(f"  TERMS o{orient2} c{col} off{offa},{offb}: got {got} exp {exp}")
                if sco != esco:
                    fails += 1
                    if fails <= 6:
                        print(f"  SCORE o{orient2} c{col}: got {sco} exp {esco}  terms got{got} exp{exp}")
    print(f"delta_eval terms: {tested-term_fail}/{tested} | SCORE: {tested-fails}/{tested}")
    sys.exit(1 if (fails or term_fail) else 0)


if __name__ == "__main__":
    main()
