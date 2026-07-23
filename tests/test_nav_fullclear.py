#!/usr/bin/env python3
"""Regression: the REAL nav mis-land = full-clear auto-advance false-firing at the title (v4 fix).

Silicon-confirmed root cause (2026-07-23): the full-clear auto-advance ("a virus count hit 0 -> inject
START to dismiss STAGE CLEAR") is mode-INDEPENDENT, gated only by MATCH_ACTIVE. At a cold boot MATCH_ACTIVE
is INHERITED != 0 (the power-on init clears it once-ever via the sticky magic; the mode-8 intro that also
clears it never runs at boot). At the title (virus counts read 0, VSEEN inherited) it false-fires, injects
START, and RTSs -- SKIPPING the autonav -> the title advances to a 1P game (nbPlayers never set to 2). That
is the ~1-in-3 sticky alternation. FIX (v4): gate the full-clear to play/post (mode>=4) so it never fires
in the menus. Closing silicon gauntlet with the fix: 8/8 VS-CPU (6 sticky + 2 fresh).

Pre-fix (@3999974, no gate): inherited MATCH_ACTIVE=1 mis-lands 1P. With the fix: lands VS.
"""
import os, sys, subprocess, importlib.util
from py65.devices.mpu6502 import MPU

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V28CS = os.path.join(REPO, "drmario_v28cs.nes")
MATCH_ACTIVE, VSEEN1, VSEEN2, VC1, VC2, MODE, P0727, Z04, F5, MAGIC = 0x6164, 0x616A, 0x616B, 0x0324, 0x03A4, 0x46, 0x0727, 0x04, 0xF5, 0x6149
_rom = open(V28CS, "rb").read(); _prg = _rom[4] * 16384
TOGGLE = _rom[16 + (_prg - 0x4000) + (0xFF30 - 0xC000):][:28]


def load(patcher):
    for k in ("DRNOFREEZE","DRROTFIX","DRHUMAN","DRPOCKET","DRSLAM","DRNAVFIX","DRTRACE","DRPROBE","DRNAV_V4","DRNAV_HOLD","DRNAV_M"):
        os.environ.pop(k, None)
    os.environ.update(DRNOFREEZE="1", DRSLAM="1", DRNAVFIX="1", DRNAV_V4="1", DRNAV_HOLD="1")
    for p in (REPO, os.path.join(REPO, "tests")):
        if p not in sys.path: sys.path.insert(0, p)
    key = f"pc_fc_{abs(hash(patcher)):x}"
    for m in [m for m in sys.modules if m.startswith("pc_fc_")]: del sys.modules[m]
    spec = importlib.util.spec_from_file_location(key, patcher)
    mod = importlib.util.module_from_spec(spec); sys.modules[key] = mod; spec.loader.exec_module(mod)
    return mod.build_main(11, 1)


def outcome(patcher, inh_match_active, T=40):
    code, lab = load(patcher)
    mpu = MPU(); mem = [0]*0x10000; mpu.memory = mem
    for i,b in enumerate(code): mem[0x8000+i] = b
    for i,b in enumerate(TOGGLE): mem[0xFF30+i] = b
    mem[MAGIC] = 0xA5
    mem[MATCH_ACTIVE] = inh_match_active; mem[VSEEN1] = 1; mem[VSEEN2] = 1   # inherited from the prior game
    mem[VC1] = 0; mem[VC2] = 0                                              # title: counts cleared to 0
    mem[MODE] = 0; mem[P0727] = 1; mem[Z04] = 0                             # title, reset to (1,0)
    SENT = 0x400; mainc = 0x8000 + lab["main"]
    for _ in range(T):
        mem[F5] = 0; mpu.sp = 0xFD; r = SENT-1
        mem[0x100+mpu.sp] = (r>>8)&0xFF; mpu.sp = (mpu.sp-1)&0xFF
        mem[0x100+mpu.sp] = r&0xFF; mpu.sp = (mpu.sp-1)&0xFF
        mpu.pc = mainc; n = 0
        while mpu.pc != SENT and n < 20000: mpu.step(); n += 1
    return "VS" if (mem[P0727] == 2 and mem[Z04] == 1) else "1P"


PRE = os.path.join(REPO, ".fcprev.py")
open(PRE, "wb").write(subprocess.check_output(["git", "-C", REPO, "show", "3999974:patch_cartridge_copro.py"]))
WT = os.path.join(REPO, "patch_cartridge_copro.py")
results = []
for ma in (1, 0):
    pre = outcome(PRE, ma); fix = outcome(WT, ma)
    print(f"  inherited MATCH_ACTIVE={ma}:  pre-fix(@3999974)={pre}  fixed={fix}")
    results.append(fix == "VS")
# the reproduction: pre-fix MUST mis-land on inherited MATCH_ACTIVE=1
repro = outcome(PRE, 1) == "1P"
os.path.exists(PRE) and os.remove(PRE)
print()
c1 = all(results); print(f"  [{'PASS' if c1 else 'FAIL'}] v4 fix lands VS-CPU for inherited MATCH_ACTIVE in {{0,1}}")
print(f"  [{'PASS' if repro else 'FAIL'}] pre-fix reproduces the mis-land (inherited MATCH_ACTIVE=1 -> 1P)")
ok = c1 and repro
print(f"\n==== {(2 if ok else (c1+repro))}/2 checks passed ====")
sys.exit(0 if ok else 1)
