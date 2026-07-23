#!/usr/bin/env python3
"""Regression: RE-ENTRANCY GUARD on the driver trampoline (THE R47 Pocket HARD-FREEZE fix).

Root cause (combo-port co-sim proven): the 0x37CF hook fires from BOTH the NMI and the main loop with no
guard, so a main-loop driver invocation gets INTERRUPTED by the NMI which RE-ENTERS the driver and clobbers
the shared abs-addr state (armed/pend/wdog) -> the driver re-issues GO every hook -> the ~83M-clk search
never DONEs -> the game spins on $5084 = the hard freeze. Cadence not silicon (div2 froze identically);
SEI can't help (NMI is non-maskable). FIX (build_wrapper): a BUSY latch -> the trampoline bails on re-entry
BEFORE the bank switch. Cold-boot bootstrap: NAV_MAGIC!=$A5 forces BUSY=0 (else garbage BUSY = deadlock).

Drives the REAL trampoline ($FF54 -> JSR main). Witness = NAV_T ($6147), incremented once per real main().
  1 re-entrant (BUSY set, warm)   -> trampoline BAILS: NAV_T unchanged, no driver run
  2 normal (BUSY clear, warm)     -> runs: NAV_T +1, BUSY cleared on exit
  3 cold boot (BUSY garbage-set)  -> bootstrap clears BUSY, runs: NAV_T=1, NAV_MAGIC=$A5 (NO deadlock)
  4 DRREENTRY=0 (pre-fix, BUSY set)-> runs ANYWAY (re-enters): NAV_T +1  [proves the guard is what bails]
"""
import os, sys, importlib.util
from py65.devices.mpu6502 import MPU

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAV_T, NAV_MAGIC, BUSY = 0x6147, 0x6149, 0x6176
MODE, Z04, MATCH, VC1, VC2 = 0x46, 0x04, 0x6164, 0x0324, 0x03A4
ARMED2, PEND2, DELAY2 = 0x6161, 0x614F, 0x615F
PY2, PX2, STKX2, STKY2, LASTY2, ORI2 = 0x0386, 0x0385, 0x6159, 0x615A, 0x6155, 0x03A5
_rom = open(os.path.join(REPO, "drmario_v28cs.nes"), "rb").read(); _prg = _rom[4] * 16384
TOG = _rom[16 + (_prg - 0x4000) + (0xFF30 - 0xC000):][:28]
WRAP_CPU = 0xFF54


def build(env):
    for k in [x for x in os.environ if x.startswith("DR")]: os.environ.pop(k, None)
    os.environ.update(DRHUMAN="1", DRPOCKET="1", DRSLAM="1"); os.environ.update(env)
    if REPO not in sys.path: sys.path.insert(0, REPO)
    sys.modules.pop("re_fs", None)
    spec = importlib.util.spec_from_file_location("re_fs", os.path.join(REPO, "patch_cartridge_copro.py"))
    mod = importlib.util.module_from_spec(spec); sys.modules["re_fs"] = mod; spec.loader.exec_module(mod)
    code, lab = mod.build_main(11, 1)
    wrap = mod.build_wrapper(0x8000 + lab["main"])
    return code, lab, wrap, mod


def run_trampoline(code, wrap, setup):
    """Drive the trampoline at $FF54 (which JSRs main); return mem after it returns."""
    mpu = MPU(); mem = [0]*0x10000; mpu.memory = mem
    for i, b in enumerate(code): mem[0x8000+i] = b
    for i, b in enumerate(wrap): mem[WRAP_CPU+i] = b
    for i, b in enumerate(TOG): mem[0xFF30+i] = b
    mem[MODE]=4; mem[Z04]=1; mem[MATCH]=1; mem[VC1]=48; mem[VC2]=48
    mem[ARMED2]=0; mem[PEND2]=0; mem[DELAY2]=0
    mem[PY2]=0x0C; mem[LASTY2]=0x0C; mem[PX2]=0x03; mem[STKX2]=0x03; mem[STKY2]=0x0C; mem[ORI2]=0
    setup(mem)
    SENT = 0x400
    mpu.sp = 0xFD; r = SENT-1
    mem[0x100+mpu.sp]=(r>>8)&0xFF; mpu.sp=(mpu.sp-1)&0xFF; mem[0x100+mpu.sp]=r&0xFF; mpu.sp=(mpu.sp-1)&0xFF
    mpu.pc = WRAP_CPU; k = 0
    while mpu.pc != SENT and k < 60000: mpu.step(); k += 1
    return mem


cf, lf, wf, mf = build({})                         # DRREENTRY default ON
assert mf.REENTRY_GUARD

# 1 re-entrant: warm (MAGIC set) + BUSY already set -> must BAIL (NAV_T frozen)
m1 = run_trampoline(cf, wf, lambda m: (m.__setitem__(NAV_MAGIC, 0xA5), m.__setitem__(NAV_T, 5), m.__setitem__(BUSY, 1)))
c1 = (m1[NAV_T] == 5)

# 2 normal: warm + BUSY clear -> runs once, BUSY cleared on exit
m2 = run_trampoline(cf, wf, lambda m: (m.__setitem__(NAV_MAGIC, 0xA5), m.__setitem__(NAV_T, 5), m.__setitem__(BUSY, 0)))
c2 = (m2[NAV_T] == 6 and m2[BUSY] == 0)

# 3 cold boot: MAGIC garbage + BUSY garbage-SET -> bootstrap clears BUSY, driver runs (NO deadlock)
m3 = run_trampoline(cf, wf, lambda m: (m.__setitem__(NAV_MAGIC, 0x00), m.__setitem__(NAV_T, 99), m.__setitem__(BUSY, 1)))
c3 = (m3[NAV_MAGIC] == 0xA5 and m3[NAV_T] == 1 and m3[BUSY] == 0)

# 4 pre-fix (DRREENTRY=0): BUSY set does NOT bail -> re-enters (NAV_T advances) [guard is what bails]
cp, lp, wp, mp = build({"DRREENTRY": "0"})
assert not mp.REENTRY_GUARD
m4 = run_trampoline(cp, wp, lambda m: (m.__setitem__(NAV_MAGIC, 0xA5), m.__setitem__(NAV_T, 5), m.__setitem__(BUSY, 1)))
c4 = (m4[NAV_T] == 6)

print(f"  BUSY=${BUSY:04X}  REENTRY_GUARD default={mf.REENTRY_GUARD}")
print(f"  1 re-entrant (BUSY set, warm) -> bail : NAV_T {5}->{m1[NAV_T]}  (want 5)")
print(f"  2 normal (BUSY clear, warm)   -> run  : NAV_T {5}->{m2[NAV_T]} BUSY={m2[BUSY]}  (want 6,0)")
print(f"  3 cold boot (BUSY garbage)    -> boot : NAV_T=?->{m3[NAV_T]} MAGIC={m3[NAV_MAGIC]:#x} BUSY={m3[BUSY]}  (want 1,0xa5,0)")
print(f"  4 DRREENTRY=0 (BUSY set)      -> runs : NAV_T {5}->{m4[NAV_T]}  (want 6, re-enters)")
for n, ok in ((1, c1), (2, c2), (3, c3), (4, c4)):
    print(f"  [{'PASS' if ok else 'FAIL'}] scenario {n}")
print(f"\n==== {sum((c1, c2, c3, c4))}/4 checks passed ====")
sys.exit(0 if all((c1, c2, c3, c4)) else 1)
