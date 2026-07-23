#!/usr/bin/env python3
"""Regression: the "re-queue once per pill" watchdog latch (DRWRETRY, default OFF -> byte-exact).

Two bugs in the wretry (one-retry) latch that let a timed-out P2 search re-GO indefinitely (amplifies
the freeze on genuine ~48s timeouts; secondary to the re-entrancy guard):
  A  handle()'s _start epilogue clears `wretry` every search START -> a re-queued timeout clears the
     latch and re-queues again forever. FIX = don't clear wretry at _start (reset only per-pill).
  B  the P2 pill-lock reset writes WRETRY ($615D=P1) not WRETRY2 ($6163=P2) -- copy-paste bug, so P2's
     latch never resets per-pill. FIX = write WRETRY2 in the P2 path.

Asserts (A/B: DRWRETRY=1 vs the default DRWRETRY=0 pre-fix):
  1 _start epilogue : DRWRETRY=1 PRESERVES WRETRY2 across a search start; DRWRETRY=0 clears it (bug A)
  2 P2 pill-lock    : DRWRETRY=1 resets WRETRY2 + PRESERVES P1's WRETRY; DRWRETRY=0 resets P1's WRETRY (bug B)
  3 byte-exact      : DRWRETRY=0 == the default build (fix is off by default); DRWRETRY=1 changes bytes
"""
import os, sys, importlib.util, hashlib
from py65.devices.mpu6502 import MPU

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODE, Z04, MATCH, VC1, VC2, MAGIC = 0x46, 0x04, 0x6164, 0x0324, 0x03A4, 0x6149
ARMED2, PEND2, DELAY2, WDOG2, WDOGH2 = 0x6161, 0x614F, 0x615F, 0x6162, 0x6166
WRETRY, WRETRY2 = 0x615D, 0x6163           # P1 / P2 one-retry latches
PY2, PX2, STKX2, STKY2, LASTY2, ORI2 = 0x0386, 0x0385, 0x6159, 0x615A, 0x6155, 0x03A5
BOARD2_SRC, W_BOARD = 0x0500, 0x5000
_rom = open(os.path.join(REPO, "drmario_v28cs.nes"), "rb").read(); _prg = _rom[4] * 16384
TOG = _rom[16 + (_prg - 0x4000) + (0xFF30 - 0xC000):][:28]


def build(env):
    for k in [x for x in os.environ if x.startswith("DR")]: os.environ.pop(k, None)
    os.environ.update(DRHUMAN="1", DRPOCKET="1", DRSLAM="1"); os.environ.update(env)
    if REPO not in sys.path: sys.path.insert(0, REPO)
    sys.modules.pop("wr_fs", None)
    spec = importlib.util.spec_from_file_location("wr_fs", os.path.join(REPO, "patch_cartridge_copro.py"))
    mod = importlib.util.module_from_spec(spec); sys.modules["wr_fs"] = mod; spec.loader.exec_module(mod)
    code, lab = mod.build_main(11, 1)
    return code, lab, mod


def run(code, lab, setup):
    mpu = MPU(); mem = [0]*0x10000; mpu.memory = mem
    for i, b in enumerate(code): mem[0x8000+i] = b
    for i, b in enumerate(TOG): mem[0xFF30+i] = b
    mem[MAGIC]=0xA5; mem[MODE]=4; mem[Z04]=1; mem[MATCH]=1; mem[VC1]=48; mem[VC2]=48; mem[0x2002]=0x80
    setup(mem)
    SENT=0x400; mc=0x8000+lab["main"]
    mpu.sp=0xFD; r=SENT-1
    mem[0x100+mpu.sp]=(r>>8)&0xFF; mpu.sp=(mpu.sp-1)&0xFF; mem[0x100+mpu.sp]=r&0xFF; mpu.sp=(mpu.sp-1)&0xFF
    mpu.pc=mc; k=0
    while mpu.pc!=SENT and k<40000: mpu.step(); k+=1
    return mem


# scenario 1: search START (no pill-lock edge: LASTY2==PY2), WRETRY2 pre-set -> is it cleared?
def start_setup(mem):
    mem[LASTY2]=12; mem[PY2]=12; mem[PX2]=3; mem[STKX2]=3; mem[STKY2]=12; mem[ORI2]=0
    mem[ARMED2]=0; mem[PEND2]=1; mem[DELAY2]=0; mem[WDOG2]=0; mem[WDOGH2]=0
    for i in range(128): mem[BOARD2_SRC+i]=0x42
    mem[W_BOARD]=0; mem[WRETRY2]=1

# scenario 2: P2 pill-lock edge (PY2 > LASTY2), WRETRY2 + P1 WRETRY pre-set -> which resets?
def lock_setup(mem):
    mem[LASTY2]=2; mem[PY2]=12; mem[PX2]=3; mem[STKX2]=3; mem[STKY2]=12; mem[ORI2]=0
    mem[ARMED2]=0; mem[PEND2]=0; mem[DELAY2]=0
    mem[WRETRY2]=1; mem[WRETRY]=1

cf, lf, mf = build({"DRWRETRY": "1"})
cp, lp, mp = build({})                       # default -> DRWRETRY off (pre-fix)
assert mf.WRETRY_FIX and not mp.WRETRY_FIX

s1_fix = run(cf, lf, start_setup); s1_pre = run(cp, lp, start_setup)
c1 = (s1_fix[WRETRY2] == 1 and s1_pre[WRETRY2] == 0)          # fix preserves; pre-fix clears (bug A)

s2_fix = run(cf, lf, lock_setup); s2_pre = run(cp, lp, lock_setup)
c2 = (s2_fix[WRETRY2] == 0 and s2_fix[WRETRY] == 1 and s2_pre[WRETRY] == 0)   # fix resets P2 + keeps P1; pre-fix hits P1 (bug B)

def sha(env):
    c, _l, _m = build(env); return hashlib.sha256(bytes(c)).hexdigest()[:16]
default_h = sha({}); off_h = sha({"DRWRETRY": "0"}); on_h = sha({"DRWRETRY": "1"})
c3 = (default_h == off_h and on_h != off_h)                  # off == default (byte-exact); on changes bytes

print(f"  1 _start keeps WRETRY2 : fix={s1_fix[WRETRY2]} pre={s1_pre[WRETRY2]}  (want 1,0)")
print(f"  2 P2-lock resets P2    : fix WRETRY2={s2_fix[WRETRY2]} WRETRY(P1)={s2_fix[WRETRY]}  pre WRETRY(P1)={s2_pre[WRETRY]}  (want 0,1,0)")
print(f"  3 byte-exact           : default={default_h} off={off_h} on={on_h}  (off==default, on!=off)")
for n, ok in ((1, c1), (2, c2), (3, c3)):
    print(f"  [{'PASS' if ok else 'FAIL'}] scenario {n}")
print(f"\n==== {sum((c1, c2, c3))}/3 checks passed ====")
sys.exit(0 if all((c1, c2, c3)) else 1)
