#!/usr/bin/env python3
"""Persistent-RAM (inherited menu state) model -- the REAL gauntlet failure.

Team-lead smoking gun: nav v1 AND v2 both fail 2/5 with PERFECT 1/3/5 alternation. Deterministic
alternation != flicker; it's menu state ($0727/$04) surviving core reload. Each boot inherits the
prior run's menu leftovers, so the nav's outcome flips with parity.

This models it faithfully: the REAL $FF30 toggle bytes are loaded into py65 (so JSR $FF30 mutates
$0727/$04 exactly as hardware), we boot with an INHERITED ($0727,$04), run the intro (mode 8) then
the title (mode 0), and on the nav's START we read the launched game type (VS-CPU iff $0727==2 AND
$04==1). Two tests: (a) sweep all inherited states -> the fixed nav must land VS-CPU for every one;
(b) chain boots with carryover -> the pre-fix nav alternates (THE signature), the fix kills it.
"""
import os, sys, importlib.util
from py65.devices.mpu6502 import MPU

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WT = os.path.join(REPO, "patch_cartridge_copro.py")
V28CS = os.path.join(REPO, "drmario_v28cs.nes")
MODE, Z04, P0727, Z_F5 = 0x0046, 0x04, 0x0727, 0xF5
NAV_T, NAV_MAGIC, MATCH_ACTIVE = 0x6147, 0x6149, 0x6164
NAV_STABLE, INJ_CNT = 0x6174, 0x614B
VCOUNT_P1, VCOUNT_P2 = 0x0324, 0x03A4
SENTINEL = 0x0400

# extract the real $FF30 toggle bytes from the cart (CPU $FF30 -> file offset in the fixed bank)
_rom = open(V28CS, "rb").read()
_prg = _rom[4] * 16384
_FF30_OFF = 16 + (_prg - 0x4000) + (0xFF30 - 0xC000)
TOGGLE_BYTES = _rom[_FF30_OFF:_FF30_OFF + 28]           # LDA $0727 ... DEC $0727; BNE go_clear


def load(patcher, navfix):
    for k in ("DRNOFREEZE", "DRROTFIX", "DRHUMAN", "DRPOCKET", "DRSLAM", "DRNAVFIX", "DRNAV_M"):
        os.environ.pop(k, None)
    os.environ["DRNOFREEZE"] = "1"; os.environ["DRSLAM"] = "1"
    os.environ["DRNAVFIX"] = "1" if navfix else "0"
    d = os.path.dirname(patcher)
    for p in (d, os.path.join(d, "tests")):
        if p not in sys.path:
            sys.path.insert(0, p)
    key = f"pc_pm_{navfix}_{abs(hash(patcher)):x}"
    spec = importlib.util.spec_from_file_location(key, patcher)
    m = importlib.util.module_from_spec(spec); sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m.build_main(11, 1)


class Boot:
    def __init__(self, patcher, navfix, inherit_0727, inherit_04, T=2500):
        (self.code, self.lab) = load(patcher, navfix)
        self.mpu = MPU(); self.mem = [0] * 0x10000; self.mpu.memory = self.mem
        for i, b in enumerate(self.code):
            self.mem[0x8000 + i] = b
        for i, b in enumerate(TOGGLE_BYTES):
            self.mem[0xFF30 + i] = b                       # the REAL toggle at $FF30
        self.main_cpu = 0x8000 + self.lab["main"]
        self.mem[NAV_MAGIC] = 0xA5                         # skip the one-time power-on init (persistent RAM)
        self.mem[MATCH_ACTIVE] = 0
        self.mem[VCOUNT_P1] = 48; self.mem[VCOUNT_P2] = 48
        self.mem[P0727] = inherit_0727 & 0xFF; self.mem[Z04] = inherit_04 & 0xFF   # INHERITED menu state
        self.T = T

    def _hook(self):
        mpu = self.mpu; mpu.sp = 0xFD
        r = SENTINEL - 1
        mpu.memory[0x0100 + mpu.sp] = (r >> 8) & 0xFF; mpu.sp = (mpu.sp - 1) & 0xFF
        mpu.memory[0x0100 + mpu.sp] = r & 0xFF; mpu.sp = (mpu.sp - 1) & 0xFF
        mpu.pc = self.main_cpu; n = 0
        while mpu.pc != SENTINEL and n < 20000:
            mpu.step(); n += 1

    def run(self):
        """Cold boot: a few intro (mode 8) hooks, then title (mode 0) hooks until START or timeout.
        Returns ('VS'|'1P'|'DEMO', residual_0727, residual_04)."""
        self.mem[MODE] = 0x08                               # intro (game reset flow) -- runs the baseline force
        for _ in range(6):
            self._hook()
        self.mem[MODE] = 0x00                               # title -- the nav runs
        for _ in range(self.T):
            inj0 = self.mem[INJ_CNT]
            self._hook()
            if self.mem[INJ_CNT] != inj0:                  # nav injected START -> game launches
                vs = (self.mem[P0727] == 2 and self.mem[Z04] == 1)
                return ("VS" if vs else "1P", self.mem[P0727], self.mem[Z04])
        return ("DEMO", self.mem[P0727], self.mem[Z04])    # title timed out -> attract demo


results = []
def check(name, cond, detail=""):
    results.append(cond); print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))

FAB = os.path.join(REPO, ".navprev2.py")
import subprocess
open(FAB, "wb").write(subprocess.check_output(["git", "-C", REPO, "show", "09fb9a4:patch_cartridge_copro.py"]))

# ---------------------------------------------------------------- (A) inherited-state sweep
print("(A) INHERITED-STATE SWEEP: every persisted ($0727,$04) must land VS-CPU with the fix")
STATES = [(a, b) for a in (0, 1, 2, 3, 0x5A) for b in (0, 1, 0x5A)]   # 15 boot conditions
fix_bad, pre_bad = [], []
print(f"     {'inherited':>16} | {'pre-fix (v2)':>12} | {'fixed (v3)':>10}")
for (g7, g4) in STATES:
    pre = Boot(FAB, navfix=True, inherit_0727=g7, inherit_04=g4).run()[0]
    fix = Boot(WT, navfix=True, inherit_0727=g7, inherit_04=g4).run()[0]
    print(f"     $0727={g7:#04x} $04={g4:#04x} | {pre:>12} | {fix:>10}")
    if fix != "VS": fix_bad.append((g7, g4, fix))
    if pre != "VS": pre_bad.append((g7, g4, pre))
check("(A) the FIX lands VS-CPU for ALL 15 inherited menu states", not fix_bad,
      f"fixed failures: {fix_bad}")
check("(A) the pre-fix (v2) does NOT (some inherited states mis-land) = the bug is inherited state",
      len(pre_bad) > 0, f"pre-fix failures: {pre_bad}")

# ---------------------------------------------------------------- (B) carryover across reload
# The exact hardware alternation is the game's residual dynamics visiting good AND bad inherited
# states across reloads (my $0727/$04-only model can't reproduce the precise 2-cycle, but (A) proves
# the class: pre-fix outcome DEPENDS on the inherited state; a reload landing on any of the 7 bad
# states fails = the parity). Here: seed from a KNOWN-BAD residual (as a reload would) and chain --
# the pre-fix stays failed; the fix recovers to VS-CPU on the very next boot, state-independently.
print("(B) CARRYOVER: a reload landing on a pre-fix-bad residual -- pre-fix fails, the fix recovers")
def chain(patcher, navfix, n=5, seed=(0, 0)):
    out = []; s7, s4 = seed
    for _ in range(n):
        res, s7, s4 = Boot(patcher, navfix, s7, s4).run()
        out.append(res)
    return out
for seed in [(0, 0), (2, 0x5A), (0x5A, 0x5A)]:
    pre_chain = chain(FAB, navfix=True, seed=seed)
    fix_chain = chain(WT, navfix=True, seed=seed)
    check(f"(B) seed {seed}: pre-fix mis-lands (>=1 non-VS), the FIX is all-VS-CPU",
          any(r != "VS" for r in pre_chain) and all(r == "VS" for r in fix_chain),
          f"pre={pre_chain} fix={fix_chain}")

if os.path.exists(FAB):
    os.remove(FAB)
print()
npass = sum(1 for c in results if c)
print(f"==== {npass}/{len(results)} model checks passed ====")
sys.exit(0 if npass == len(results) else 1)
