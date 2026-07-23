#!/usr/bin/env python3
"""Regression: the ATTRACT-DEMO mis-land + the waitFrames ($51) title-hold fix (v4-final).

Runs the REAL nav code against a faithful mock of the vanilla title mode-0 loop (labeled disasm,
verified vs our base at $98FE): waitFrames ($51) ++ per 256 frames; ==demoStart_delay($08) -> @toDemo
forces nbPlayers($0727)=1 => 1P; p1_btns_pressed($F5)==btn_start($10) -> mode 0->1 => VS iff nbPlayers==2.
DRNAV_HOLD=0 (pre-hold) mis-lands on the demo-win phase; DRNAV_HOLD=1 (fix: nav writes $51=0 each title
hook) lands VS for EVERY inherited (waitFrames,frameCounter) -- the demo can never trip.
"""
import os, sys, importlib.util
from py65.devices.mpu6502 import MPU

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V28CS = os.path.join(REPO, "drmario_v28cs.nes")
MODE, F5, WAITF, FRAMEC, P0727, Z04, NAV_MAGIC, MATCH = 0x46, 0xF5, 0x51, 0x43, 0x0727, 0x04, 0x6149, 0x6164
BTN_START, DEMO_DELAY, SENT = 0x10, 0x08, 0x0400
_rom = open(V28CS, "rb").read(); _prg = _rom[4] * 16384
TOGGLE = _rom[16 + (_prg - 0x4000) + (0xFF30 - 0xC000):][:28]


def load(hold):
    for k in ("DRNOFREEZE","DRROTFIX","DRHUMAN","DRPOCKET","DRSLAM","DRNAVFIX","DRTRACE","DRPROBE","DRNAV_V4","DRNAV_HOLD","DRNAV_M"):
        os.environ.pop(k, None)
    os.environ.update(DRNOFREEZE="1", DRSLAM="1", DRNAVFIX="1", DRNAV_V4="1", DRNAV_HOLD=("1" if hold else "0"))
    for p in (REPO, os.path.join(REPO, "tests")):
        if p not in sys.path: sys.path.insert(0, p)
    for m in [m for m in sys.modules if m.startswith("pc_dh")]: del sys.modules[m]
    spec = importlib.util.spec_from_file_location(f"pc_dh{hold}", os.path.join(REPO, "patch_cartridge_copro.py"))
    mod = importlib.util.module_from_spec(spec); sys.modules[f"pc_dh{hold}"] = mod; spec.loader.exec_module(mod)
    return mod.build_main(11, 1)


def boot(hold, inh_wait, inh_frame, T=3000):
    code, lab = load(hold)
    mpu = MPU(); mem = [0]*0x10000; mpu.memory = mem
    for i,b in enumerate(code): mem[0x8000+i] = b
    for i,b in enumerate(TOGGLE): mem[0xFF30+i] = b
    mainc = 0x8000 + lab["main"]
    mem[NAV_MAGIC] = 0xA5; mem[MATCH] = 0; mem[0x0324] = mem[0x03A4] = 48
    mem[P0727] = 1; mem[Z04] = 0                       # confirmed: every boot resets to (1,0)
    mem[WAITF] = inh_wait & 0xFF; mem[FRAMEC] = inh_frame & 0xFF   # inherited sticky demo-timer phase

    def hook():
        mpu.sp = 0xFD; r = SENT-1
        mem[0x0100+mpu.sp] = (r>>8)&0xFF; mpu.sp = (mpu.sp-1)&0xFF
        mem[0x0100+mpu.sp] = r&0xFF; mpu.sp = (mpu.sp-1)&0xFF
        mpu.pc = mainc; n = 0
        while mpu.pc != SENT and n < 20000: mpu.step(); n += 1

    mem[MODE] = 0x08
    for _ in range(3): hook()
    mem[MODE] = 0x00
    for _ in range(T):
        mem[F5] = 0
        for _ in range(5): hook()
        mem[FRAMEC] = (mem[FRAMEC] + 1) & 0xFF
        if mem[FRAMEC] == 0:
            mem[WAITF] = (mem[WAITF] + 1) & 0xFF
            if mem[WAITF] == DEMO_DELAY:
                return "1P"
        if mem[F5] == BTN_START:
            return "VS" if mem[P0727] == 2 else "1P"
    return "TIMEOUT"


STATES = [(w, fc) for w in (0, 4, 6, 7, 8) for fc in (0, 200, 253, 255)]
results = []
for hold in (0, 1):
    fails = [(w, fc, r) for (w, fc) in STATES for r in [boot(hold, w, fc)] if r != "VS"]
    tag = "HOLD=1 (fix)" if hold else "HOLD=0 (pre-hold)"
    if hold:
        ok = len(fails) == 0
        print(f"  [{'PASS' if ok else 'FAIL'}] {tag}: ALL {len(STATES)} inherited demo-timer states land VS-CPU"
              + (f"  -- FAILURES: {fails}" if fails else ""))
        results.append(ok)
    else:
        ok = len(fails) > 0
        print(f"  [{'PASS' if ok else 'FAIL'}] {tag}: reproduces the mis-land (>=1 non-VS)  -- {fails}")
        results.append(ok)

npass = sum(results)
print(f"\n==== {npass}/{len(results)} checks passed ====")
sys.exit(0 if npass == len(results) else 1)
