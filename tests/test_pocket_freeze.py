#!/usr/bin/env python3
"""Regression: the R47 Pocket HARD-FREEZE = the driver pinning GRAV_P2 for the WHOLE search (fix).

Root cause (2026-07-23): the Pocket cart is a FREEZE cart (NO_FREEZE=False). While the P2 copro is
searching (ARMED2!=0), act's legacy `else` branch pins GRAV_P2=0 every frame (search-while-frozen).
On the Pocket the copro is ~4x slower; a heavy R47 first-pill depth-3 search then holds that pin for
seconds..minutes (WDOG=~4min) = the mid-air hard-freeze. MiSTer is fine (fast copro DONEs quick); the
MiSTer AB cart never hits it (NO_FREEZE=1 anytime path). FIX: route ALL ROTFIX carts (every shipping
cart) through the anytime NO-PIN path -- fall under live gravity + weave toward the running argmax --
so a slow search can never freeze the capsule (the fairness rework; `if NO_FREEZE or ROTFIX:`).

Pre-fix (@7a64ba4): a never-DONE search pins GRAV_P2 every frame. Post-fix: never pins.
"""
import os, sys, subprocess, importlib.util
from py65.devices.mpu6502 import MPU

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V28CS = os.path.join(REPO, "drmario_v28cs.nes")
GRAV_P2, MODE, Z04, MATCH, VC1, VC2 = 0x0392, 0x46, 0x04, 0x6164, 0x0324, 0x03A4
ARMED2, PEND2, DELAY2, LASTY2, WDOG2, WDOGH2, MAGIC = 0x6161, 0x614F, 0x615F, 0x6155, 0x6162, 0x6166, 0x6149
PY2, PX2, STKX2, STKY2, ORI2 = 0x0386, 0x0385, 0x6159, 0x615A, 0x03A5
W_DONE, W_OR, W_COL = 0x5084, 0x5086, 0x5085   # DRPOCKET single window at $5000
_rom = open(V28CS, "rb").read(); _prg = _rom[4] * 16384
TOG = _rom[16 + (_prg - 0x4000) + (0xFF30 - 0xC000):][:28]


def load(src_bytes, tag):
    fn = os.path.join(REPO, f".pf_{tag}.py"); open(fn, "wb").write(src_bytes)
    for k in ("DRNOFREEZE","DRROTFIX","DRHUMAN","DRPOCKET","DRSLAM","DRNAVFIX","DRTRACE","DRPROBE","DRNAV_V4","DRNAV_HOLD"):
        os.environ.pop(k, None)
    os.environ.update(DRHUMAN="1", DRPOCKET="1", DRSLAM="1")
    for p in (REPO, os.path.join(REPO, "tests")):
        if p not in sys.path: sys.path.insert(0, p)
    for m in [m for m in sys.modules if m.startswith("pf_")]: del sys.modules[m]
    spec = importlib.util.spec_from_file_location(f"pf_{tag}", fn)
    mod = importlib.util.module_from_spec(spec); sys.modules[f"pf_{tag}"] = mod; spec.loader.exec_module(mod)
    os.remove(fn); return mod.build_main(11, 1)


def pinned_frames(src_bytes, tag, n=6):
    code, lab = load(src_bytes, tag)
    mpu = MPU(); mem = [0]*0x10000; mpu.memory = mem
    for i,b in enumerate(code): mem[0x8000+i] = b
    for i,b in enumerate(TOG): mem[0xFF30+i] = b
    mem[MAGIC]=0xA5; mem[MODE]=4; mem[Z04]=1; mem[MATCH]=1; mem[VC1]=48; mem[VC2]=48
    mem[ARMED2]=1; mem[PEND2]=0; mem[DELAY2]=0; mem[WDOG2]=0; mem[WDOGH2]=0
    mem[PY2]=0x40; mem[LASTY2]=0x40; mem[PX2]=0x08; mem[STKX2]=0x08; mem[STKY2]=0x40; mem[ORI2]=0
    mem[W_DONE]=0; mem[W_OR]=0xFF; mem[W_COL]=0x03
    SENT=0x400; mc=0x8000+lab["main"]; pins=0
    for _ in range(n):
        mem[GRAV_P2]=0x77; mem[W_DONE]=0; mem[ARMED2]=1           # never-DONE search in flight
        mpu.sp=0xFD; r=SENT-1
        mem[0x100+mpu.sp]=(r>>8)&0xFF; mpu.sp=(mpu.sp-1)&0xFF; mem[0x100+mpu.sp]=r&0xFF; mpu.sp=(mpu.sp-1)&0xFF
        mpu.pc=mc; k=0
        while mpu.pc!=SENT and k<20000: mpu.step(); k+=1
        if mem[GRAV_P2]==0: pins+=1
    return pins, n


before = subprocess.check_output(["git", "-C", REPO, "show", "7a64ba4:patch_cartridge_copro.py"])
after = open(os.path.join(REPO, "patch_cartridge_copro.py"), "rb").read()
pb, n = pinned_frames(before, "pre"); pa, _ = pinned_frames(after, "fix")
print(f"  pre-fix @7a64ba4: never-DONE search pins GRAV_P2 {pb}/{n} frames")
print(f"  post-fix        : never-DONE search pins GRAV_P2 {pa}/{n} frames")
c1 = pb > 0; c2 = pa == 0
print(f"  [{'PASS' if c1 else 'FAIL'}] pre-fix reproduces the freeze (pins the whole search)")
print(f"  [{'PASS' if c2 else 'FAIL'}] fix removes the pin (falls + weaves during the search)")
print(f"\n==== {c1+c2}/2 checks passed ====")
sys.exit(0 if (c1 and c2) else 1)
