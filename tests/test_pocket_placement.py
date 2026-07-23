#!/usr/bin/env python3
"""Regression: the R47 Pocket MISPLACEMENT = the freeze fix's incomplete symmetry (fix).

Root cause (2026-07-23): the confidence-gated slam (dn_p2) was NO_FREEZE-only. The R47 freeze fix
(2d71333) routed ROTFIX freeze-carts (Pocket, NO_FREEZE=0) through the no-pin anytime path but did
NOT extend that gate too, so the now-unpinned pill soft-drops (dn_p2 -> LDY #4) off the ~MIN_THINK
shallow argmax instead of weaving until the argmax is confidently stable. Plus the orient LATCHES at
MIN_THINK (high, by design) and act_p2 never re-rotates, so a slow copro whose orient converges after
the latch places the shallow orient forever.

FIX (both freeze-cart-only / ROTFIX-gated, MiSTer-AB byte-exact):
  COLGATE   : extend the dn_p2 confidence gate to ROTFIX  -> no premature soft-drop (fixes the column)
  RECOMMIT  : at DONE, if the capsule is still HIGH (Y >= CROSS_LOWY) and the converged orient differs,
              re-open the orient latch so act_p2 rotates once to the converged orient (fixes the orient
              -- self-activates when the search converges above the safe-rotate line, i.e. the delta).

Asserts, A/B against the same source built with DRCOLGATE=0 DRRECOMMIT=0 (pre-fix behavior):
  1 COLGATE holds  : searching + orient-locked + column-aligned + argmax-unstable -> fixed does NOT
                     press DOWN (weaves at gravity); pre-fix presses DOWN (soft-drops the shallow argmax)
  2 RECOMMIT high  : DONE + latched + capsule HIGH + converged orient differs -> fixed re-opens ROT_DONE2
  3 RECOMMIT low   : same but capsule LOW -> fixed KEEPS ROT_DONE2 (no backwards-lock); pre-fix never re-opens
  4 byte-exact     : NO_FREEZE=1 (MiSTer AB) build identical with/without the flags
"""
import os, sys, importlib.util, hashlib
from py65.devices.mpu6502 import MPU

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F6 = 0xF6
GRAV_P2, MODE, Z04, MATCH, VC1, VC2 = 0x0392, 0x46, 0x04, 0x6164, 0x0324, 0x03A4
ARMED2, PEND2, DELAY2, LASTY2, WDOG2, WDOGH2, MAGIC = 0x6161, 0x614F, 0x615F, 0x6155, 0x6162, 0x6166, 0x6149
PY2, PX2, STKX2, STKY2, ORI2 = 0x0386, 0x0385, 0x6159, 0x615A, 0x03A5
TGT_C2, TGT_O2, ROT_DONE2, STABLE_CT2, SLAM_ARM = 0x6152, 0x6153, 0x616E, 0x6171, 0x6172
LAST_COL2, LAST_ORI2 = 0x616F, 0x6170
W_DONE, W_COL, W_OR = 0x5084, 0x5085, 0x5086       # DRPOCKET single window at $5000
_rom = open(os.path.join(REPO, "drmario_v28cs.nes"), "rb").read(); _prg = _rom[4] * 16384
TOG = _rom[16 + (_prg - 0x4000) + (0xFF30 - 0xC000):][:28]
GAMEMAP = {0: 3, 1: 1, 2: 0, 3: 2}


def build(env):
    for k in ("DRNOFREEZE","DRROTFIX","DRHUMAN","DRPOCKET","DRSLAM","DRNAVFIX","DRTRACE","DRPROBE",
              "DRNAV_V4","DRNAV_HOLD","DRCOLGATE","DRRECOMMIT"):
        os.environ.pop(k, None)
    os.environ.update(DRHUMAN="1", DRPOCKET="1", DRSLAM="1"); os.environ.update(env)
    if REPO not in sys.path: sys.path.insert(0, REPO)
    sys.modules.pop("pp_fs", None)
    spec = importlib.util.spec_from_file_location("pp_fs", os.path.join(REPO, "patch_cartridge_copro.py"))
    mod = importlib.util.module_from_spec(spec); sys.modules["pp_fs"] = mod; spec.loader.exec_module(mod)
    code, lab = mod.build_main(11, 1)
    return code, lab, mod


def run_hook(code, lab, setup):
    """Run ONE driver hook over a mock state; return (mem, F6-button)."""
    mpu = MPU(); mem = [0]*0x10000; mpu.memory = mem
    for i, b in enumerate(code): mem[0x8000+i] = b
    for i, b in enumerate(TOG): mem[0xFF30+i] = b
    mem[MAGIC]=0xA5; mem[MODE]=4; mem[Z04]=1; mem[MATCH]=1; mem[VC1]=48; mem[VC2]=48
    mem[PEND2]=0; mem[DELAY2]=0; mem[WDOG2]=0; mem[WDOGH2]=1     # >256 hooks searched (past cold)
    setup(mem)
    SENT=0x400; mc=0x8000+lab["main"]
    mpu.sp=0xFD; r=SENT-1
    mem[0x100+mpu.sp]=(r>>8)&0xFF; mpu.sp=(mpu.sp-1)&0xFF; mem[0x100+mpu.sp]=r&0xFF; mpu.sp=(mpu.sp-1)&0xFF
    mem[F6]=0; mpu.pc=mc; k=0
    while mpu.pc!=SENT and k<20000: mpu.step(); k+=1
    return mem, mem[F6]


_c0, _l0, _m0 = build({})
LOWY = _m0.CROSS_LOWY

# ---- scenario 1: COLGATE -- searching, orient-locked, column-aligned, argmax UNSTABLE, capsule HIGH ----
def colgate_setup(mem):
    mem[ARMED2]=1; mem[W_DONE]=0; mem[W_OR]=2; mem[W_COL]=5     # searching; running argmax published (col 5)
    mem[ROT_DONE2]=1; mem[ORI2]=GAMEMAP[2]; mem[TGT_O2]=GAMEMAP[2]
    mem[PX2]=5; mem[TGT_C2]=5; mem[STKX2]=5; mem[STKY2]=LOWY+4; mem[PY2]=LOWY+4   # aligned, HIGH (not crossover)
    mem[LASTY2]=LOWY+4
    mem[STABLE_CT2]=0; mem[LAST_COL2]=0xFE; mem[LAST_ORI2]=0xFE  # argmax just changed -> unstable (STABLE stays low)
    mem[SLAM_ARM]=1
cf, lf, mf = build({}); cp, lp, mp = build({"DRCOLGATE":"0","DRRECOMMIT":"0"})
_, colgate_fix = run_hook(cf, lf, colgate_setup)
_, colgate_pre = run_hook(cp, lp, colgate_setup)
DOWN = 0x04
c1 = (colgate_fix & DOWN) == 0 and (colgate_pre & DOWN) != 0

# ---- scenario 2/3: RECOMMIT -- DONE arrives, orient latched to a SHALLOW value, converged orient differs ----
def recommit_setup(y):
    def s(mem):
        mem[ARMED2]=1; mem[W_DONE]=1; mem[W_COL]=6; mem[W_OR]=2   # DONE; converged copro-orient 2 -> game 0
        mem[ROT_DONE2]=1
        mem[ORI2]=GAMEMAP[1]          # capsule physically at a SHALLOW orient (game 1) != converged game 0
        mem[TGT_O2]=GAMEMAP[1]; mem[TGT_C2]=6
        mem[PX2]=6; mem[STKX2]=6; mem[STKY2]=y; mem[PY2]=y; mem[LASTY2]=y
    return s
cf2, lf2, mf2 = build({}); cp2, lp2, mp2 = build({"DRCOLGATE":"0","DRRECOMMIT":"0"})
mem_hi_fix, _ = run_hook(cf2, lf2, recommit_setup(LOWY + 4))    # HIGH
mem_lo_fix, _ = run_hook(cf2, lf2, recommit_setup(LOWY - 4))    # LOW
mem_hi_pre, _ = run_hook(cp2, lp2, recommit_setup(LOWY + 4))
c2 = mem_hi_fix[ROT_DONE2] == 0                      # fixed: HIGH + differ -> re-opened
c3 = mem_lo_fix[ROT_DONE2] == 1 and mem_hi_pre[ROT_DONE2] == 1   # fixed LOW keeps; pre-fix never re-opens

# ---- scenario 4: byte-exactness -- NO_FREEZE=1 (MiSTer AB) unaffected ----
def sha(env):
    c, _l, _m = build(env); return hashlib.sha256(bytes(c)).hexdigest()[:16]
ab_on  = sha({"DRNOFREEZE": "1"})
ab_off = sha({"DRNOFREEZE": "1", "DRCOLGATE": "0", "DRRECOMMIT": "0"})
c4 = ab_on == ab_off

print(f"  MIN_THINK={mf.MIN_THINK} hooks  CROSS_LOWY={LOWY}  (safe-rotate line)")
print(f"  1 COLGATE hold   : fixed DOWN={bool(colgate_fix & DOWN)}  pre-fix DOWN={bool(colgate_pre & DOWN)}")
print(f"  2 RECOMMIT high  : fixed ROT_DONE2(Y=hi) = {mem_hi_fix[ROT_DONE2]}  (0 = re-opened)")
print(f"  3 RECOMMIT low   : fixed ROT_DONE2(Y=lo) = {mem_lo_fix[ROT_DONE2]}  pre-fix(Y=hi) = {mem_hi_pre[ROT_DONE2]}  (both 1)")
print(f"  4 byte-exact AB  : NO_FREEZE=1 {ab_on} == {ab_off}  -> {c4}")
for n, ok in ((1, c1), (2, c2), (3, c3), (4, c4)):
    print(f"  [{'PASS' if ok else 'FAIL'}] scenario {n}")
print(f"\n==== {sum((c1,c2,c3,c4))}/4 checks passed ====")
sys.exit(0 if all((c1, c2, c3, c4)) else 1)
