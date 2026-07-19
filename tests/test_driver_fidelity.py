#!/usr/bin/env python3
"""Deterministic validation of the DRROTFIX P2 driver-fidelity fixes.

Runs the REAL unit-1 6502 driver (build_main output) inside py65, scripting the
P2 copro mailbox ($5284 DONE / $5285 COL / $5286 OR) and a minimal capsule mock
(freeze-vs-fall, rotate-with-flush-failure, slide). Asserts the three fixes:
  1 pre-phase       : rotations complete while frozen HIGH (never attempted low)
  2 feasibility gate: a late orient retarget after commit is IGNORED (no backwards lock)
  3 min-think gate  : no lateral / no commit until DONE or WDOG2 >= MIN_THINK

Also runs scenario 2/3 against DRROTFIX=0 to show the OLD driver exhibits the
low-rotation backwards-lock the fix removes.
"""
import os, sys, importlib.util
from py65.devices.mpu6502 import MPU

# use the worktree patcher (has the fixes)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WT = os.path.join(REPO, "patch_cartridge_copro.py")

# addresses (mirror the patcher)
Z_F5, Z_F6, Z_F7, Z_F8 = 0xF5, 0xF6, 0xF7, 0xF8
GRAV_P2 = 0x0392
P2X, P2Y, P2O = 0x0385, 0x0386, 0x03A5
W2 = 0x5200
W2_DONE, W2_COL, W2_OR = W2 + 0x84, W2 + 0x85, W2 + 0x86
ARMED2, WDOG2, WDOGH2 = 0x6161, 0x6162, 0x6166
PEND2, DELAY2 = 0x614F, 0x615F
TGT_C2, TGT_O2 = 0x6152, 0x6153
ROT_DONE2 = 0x616E
STK2 = 0x615B
LASTY1, LASTY2 = 0x6154, 0x6155
P1Y = 0x0306
NAV_MAGIC, MATCH_ACTIVE = 0x6149, 0x6164
VCOUNT_P1, VCOUNT_P2 = 0x0324, 0x03A4
MODE = 0x0046
SENTINEL = 0x0400
FLUSH_Y = 0x08          # mock: capsule can rotate only while Y (height) > FLUSH_Y


def load_build(rotfix):
    for k in ("DRNOFREEZE", "DRROTFIX", "DRHUMAN", "DRPOCKET"):
        os.environ.pop(k, None)
    os.environ["DRNOFREEZE"] = "1"
    os.environ["DRROTFIX"] = "1" if rotfix else "0"
    wtdir = os.path.dirname(WT)
    for p in (wtdir, os.path.join(wtdir, "tests")):
        if p not in sys.path:
            sys.path.insert(0, p)
    spec = importlib.util.spec_from_file_location(f"pc_{rotfix}", WT)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    code, lab = m.build_main(11, 1)
    return code, lab


class Sim:
    def __init__(self, rotfix):
        self.code, self.lab = load_build(rotfix)
        self.mpu = MPU()
        self.mem = [0] * 0x10000
        for i, b in enumerate(self.code):
            self.mem[0x8000 + i] = b
        self.mpu.memory = self.mem
        self.main_cpu = 0x8000 + self.lab["main"]
        # baseline game state: VS-CPU play, init already done
        self.mem[NAV_MAGIC] = 0xA5          # skip power-on init
        self.mem[MODE] = 0x04               # play
        self.mem[0x04] = 0x01               # VS-CPU active -> AI runs
        self.mem[MATCH_ACTIVE] = 1
        self.mem[VCOUNT_P1] = 40
        self.mem[VCOUNT_P2] = 40
        # keep P1 copro ($5000) benign / P1 not pending so handle1/act_p1 are quiet
        # frozen A-press edge bookkeeping not modeled; we read raw $F6 writes.
        self.presses = []                   # ($F6) each frame
        self.grav_period = 1                # hooks per 1-row fall (1=every frame; macro test slows it
        self.gcount = 0                     #  to ~L11 so the driver has time to commit + steer)

    def run_main(self, maxins=20000):
        mpu = self.mpu
        mpu.sp = 0xFD
        r = SENTINEL - 1
        mpu.memory[0x0100 + mpu.sp] = (r >> 8) & 0xFF; mpu.sp = (mpu.sp - 1) & 0xFF
        mpu.memory[0x0100 + mpu.sp] = r & 0xFF; mpu.sp = (mpu.sp - 1) & 0xFF
        mpu.pc = self.main_cpu
        n = 0
        while mpu.pc != SENTINEL and n < maxins:
            mpu.step(); n += 1
        assert n < maxins, "main did not return (runaway)"

    def frame(self, apply_physics=True):
        """One hook call + minimal capsule physics based on the driver's output."""
        self.mem[GRAV_P2] = 0x20            # game reloads a nonzero drop timer each frame
        self.mem[Z_F6] = 0; self.mem[Z_F8] = 0
        self.run_main()
        f6 = self.mem[Z_F6]
        self.presses.append(f6)
        froze = (self.mem[GRAV_P2] == 0)    # driver pinned the drop timer this frame
        if not hasattr(self, "froze_hist"):
            self.froze_hist = []
        self.froze_hist.append(froze)       # FAIRNESS audit: was gravity pinned this frame?
        if apply_physics:
            if f6 & 0x80:                   # A -> rotate, but NES rotation fails flush (low)
                if self.mem[P2Y] > FLUSH_Y:
                    self.mem[P2O] = (self.mem[P2O] + 1) & 0x03
                # else: silent failure (orient unchanged) == backwards-lock risk
            if f6 & 0x02 and self.mem[P2X] > 0:      # LEFT
                self.mem[P2X] -= 1
            if f6 & 0x01 and self.mem[P2X] < 7:      # RIGHT
                self.mem[P2X] += 1
            if not froze:                   # gravity: fall one row every grav_period hooks
                self.gcount += 1
                if self.gcount >= self.grav_period:
                    self.gcount = 0
                    if self.mem[P2Y] > 0:
                        self.mem[P2Y] -= 1
        return dict(f6=f6, froze=froze, y=self.mem[P2Y], x=self.mem[P2X],
                    o=self.mem[P2O], rot=self.mem[ROT_DONE2], tgt_o=self.mem[TGT_O2],
                    tgt_c=self.mem[TGT_C2], wdog=self.mem[WDOG2], armed=self.mem[ARMED2])


def spawn_pill(s, y=0x0D, x=3, orient=0):
    """Set up a freshly-searched P2 pill: search ARMED, no candidate yet."""
    s.mem[P2Y] = y; s.mem[P2X] = x; s.mem[P2O] = orient
    s.mem[LASTY2] = y; s.mem[LASTY1] = s.mem[P1Y]   # no spurious pill-lock edge on frame 1
    s.mem[PEND2] = 0; s.mem[DELAY2] = 0
    s.mem[ARMED2] = 1; s.mem[WDOG2] = 0; s.mem[WDOGH2] = 0
    s.mem[ROT_DONE2] = 0; s.mem[STK2] = 0
    s.mem[W2_DONE] = 0; s.mem[W2_OR] = 0xFF; s.mem[W2_COL] = 0  # no candidate
    s.mem[TGT_C2] = 3; s.mem[TGT_O2] = orient


# scenarios speak GAME orient; the copro mailbox is copro-space and the driver maps it
# ({0:3,1:1,2:0,3:2}). Route game->copro (inverse) so both the DONE path (handle) and the live
# path (nf2, now mapped) land on the intended game orient in TGT_O2.
INV = {3: 0, 1: 1, 0: 2, 2: 3}


def publish_live(s, col, orient):
    s.mem[W2_DONE] = 0; s.mem[W2_COL] = col; s.mem[W2_OR] = INV[orient]   # best-so-far, searching


def publish_done(s, col, orient):
    s.mem[W2_DONE] = 1; s.mem[W2_COL] = col; s.mem[W2_OR] = INV[orient]   # DONE


results = []
def check(name, cond, detail=""):
    results.append((name, cond, detail))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


# ---------------------------------------------------------------- scenario 1: pre-phase
print("SCENARIO 1 (DRROTFIX=1): rotation pre-phase -- rotate to target orient while HIGH")
s = Sim(rotfix=True)
spawn_pill(s, y=0x0D, x=3, orient=0)
# copro's target orient is 2 (needs 2 rotations from 0). live-publish it immediately.
publish_live(s, col=3, orient=2)   # game-orient mapping handled in handle(); nf2 uses raw mailbox
rot_ys = []
low_rot = False
for _ in range(60):
    st = s.frame()
    if st["f6"] & 0x80:                       # A pressed this frame
        rot_ys.append(st["y"])
        if st["y"] <= FLUSH_Y:
            low_rot = True
    if st["o"] == s.mem[TGT_O2] and st["rot"]:  # orient reached & committed
        break
check("orient reached target", s.mem[P2O] == s.mem[TGT_O2], f"P2O={s.mem[P2O]} TGT_O2={s.mem[TGT_O2]}")
check("all rotations happened HIGH (Y>FLUSH)", not low_rot, f"rotate Ys={rot_ys}, FLUSH_Y={FLUSH_Y}")
check("FAIRNESS: gravity NEVER pinned during rotate/min-think", not any(s.froze_hist),
      f"pinned frames={sum(s.froze_hist)}/{len(s.froze_hist)} (rotations ran UNDER live gravity)")

# ---------------------------------------------------------------- scenario 2: min-think gate
print("SCENARIO 2 (DRROTFIX=1): min-think -- no lateral until WDOG2>=MIN_THINK or DONE")
s = Sim(rotfix=True)
spawn_pill(s, y=0x0D, x=3, orient=0)
publish_live(s, col=0, orient=0)      # shallow early argmax: col 0 (far left), orient already 0
lateral_before_gate = []
committed_frame = None
for i in range(140):
    st = s.frame(apply_physics=False)     # hold state; we only watch the DECISION vs WDOG2
    if st["rot"] and committed_frame is None:
        committed_frame = i
    if st["f6"] & 0x03:                    # any L/R press
        lateral_before_gate.append((i, st["wdog"], st["rot"]))
# any lateral BEFORE ROT_DONE2 latched is a min-think violation
early_lat = [t for t in lateral_before_gate if not t[2]]
check("no lateral before commit", len(early_lat) == 0, f"early L/R frames={early_lat[:3]}")
check("commit gated by MIN_THINK", committed_frame is not None and committed_frame >= 1,
      f"committed at frame {committed_frame} (WDOG2 accrues ~1/frame here)")

print("SCENARIO 2b (DRROTFIX=1): DONE opens the gate immediately")
s = Sim(rotfix=True)
spawn_pill(s, y=0x0D, x=3, orient=0)
publish_done(s, col=5, orient=0)      # DONE fires with final target col 5
# handle2 latches TGT from mailbox (mapped) and clears ARMED2; act then rotates-if-needed & commits.
# WDOG2 stays ~0 here, so ONLY the DONE branch (ARMED2==0) can open the commit gate.
for i in range(30):
    st = s.frame(apply_physics=True)
    if st["rot"]:
        break
check("DONE (WDOG2~0) still opens commit gate", s.mem[ROT_DONE2] == 1,
      f"ROT_DONE2={s.mem[ROT_DONE2]} WDOG2={s.mem[WDOG2]} armed={s.mem[ARMED2]}")

# ---------------------------------------------------------------- scenario 3: late-retarget feasibility
print("SCENARIO 3 (DRROTFIX=1): late orient retarget when LOW is ignored (no backwards lock)")
s = Sim(rotfix=True)
spawn_pill(s, y=0x0D, x=4, orient=0)
publish_live(s, col=4, orient=0)      # first target: orient 0 (already there), col 4
# let min-think elapse & commit, then let it descend to LOW
for _ in range(140):
    s.frame()
    if s.mem[ROT_DONE2] and s.mem[P2Y] <= FLUSH_Y:
        break
committed_o = s.mem[P2O]
low_y = s.mem[P2Y]
# NOW a late candidate wants a different orient while the capsule is LOW
publish_live(s, col=4, orient=2)
a_pressed_low = False
for _ in range(20):
    st = s.frame()
    if st["f6"] & 0x80 and st["y"] <= FLUSH_Y:
        a_pressed_low = True
check("committed while low", low_y <= FLUSH_Y and s.mem[ROT_DONE2] == 1, f"Y={low_y} ROT_DONE2={s.mem[ROT_DONE2]}")
check("orient NOT changed by late retarget", s.mem[P2O] == committed_o, f"P2O={s.mem[P2O]} committed={committed_o}")
check("NO A-press attempted while low (no backwards-lock)", not a_pressed_low)

# ---------------------------------------------------------------- scenario 4: FAIRNESS (no world-stop)
print("SCENARIO 4 (DRROTFIX=1): FAIRNESS -- the driver never pins P2 gravity in the steering path")
s = Sim(rotfix=True)
spawn_pill(s, y=0x0D, x=2, orient=1)       # needs a rotation; PEND2=0 so freeze_pending is inactive
publish_live(s, col=6, orient=3)           # target = rotate + far slide, search never DONE
for _ in range(120):                       # full lifecycle: rotate -> min-think -> commit -> descend
    s.frame()
check("gravity pinned 0 frames across a full pill (rotate+min-think+descend)", not any(s.froze_hist),
      f"pinned={sum(s.froze_hist)}/{len(s.froze_hist)} frames -- everything ran under live gravity")
# control: the ONE remaining pin is freeze_pending's PEND2 settle (deployed, inside the spawn no-fall window)
s2 = Sim(rotfix=True)
spawn_pill(s2, y=0x0D, x=3, orient=0)
s2.mem[PEND2] = 1                          # pill still PENDING its search
s2.frame(apply_physics=False)
check("PENDING settle IS pinned (freeze_pending, the one deployed in-window pin)", s2.froze_hist[-1] is True,
      "bounded by DELAY2 ~15 hooks ~3 frames, entirely inside the ~20f spawn animation")

# ---------------------------------------------------------------- OLD driver regression demo
print("SCENARIO 3-OLD (DRROTFIX=0): same late retarget -> OLD driver rotates LOW (backwards-lock)")
s0 = Sim(rotfix=False)
spawn_pill(s0, y=0x0D, x=4, orient=0)
publish_live(s0, col=4, orient=0)
for _ in range(60):
    s0.frame()
    if s0.mem[P2Y] <= FLUSH_Y:
        break
# late retarget to a different orient while LOW
publish_live(s0, col=4, orient=2)
old_a_low = False
for _ in range(20):
    st = s0.frame()
    if st["f6"] & 0x80 and st["y"] <= FLUSH_Y:
        old_a_low = True
check("OLD driver DID attempt low rotation (the bug)", old_a_low,
      "old anytime driver chases the late orient even when flush -> silent-fail backwards lock")

# ---------------------------------------------------------------- MACRO: full-pill placed orientation
# The gate this incident was missing. The clear-regression (MiSTer A/B 2026-07-19: DRROTFIX=1 P2
# cleared ~0) was a wrong LANDED orientation -- the anytime path stored the copro orient UNMAPPED,
# and the orient-lock froze it before handle()'s DONE-time map could correct it. A decision-level
# test can't see that; only driving a REAL pill through the REAL driver to LANDING and checking the
# PLACED orientation+column can. Removing the nf2 copro->game map makes 3/4 of these FAIL (the pill
# lands the raw copro orient instead of the intended game orient).
print("MACRO (DRROTFIX=1): full pill -> LANDED orientation+column == mapped copro target")
def land_pill(game_orient, col, spawn_orient=0, spawn_x=3, rotfix=True):
    s = Sim(rotfix=rotfix)
    s.grav_period = 12                              # ~L11 MED: room to commit (min-think) then steer
    spawn_pill(s, y=0x0D, x=spawn_x, orient=spawn_orient)
    publish_live(s, col=col, orient=game_orient)    # ANYTIME path (the nf2 map under test); never DONE
    for _ in range(400):
        s.frame(apply_physics=True)
        if s.mem[P2Y] == 0:                         # no board modeled -> floor == landed
            break
    return s.mem[P2O], s.mem[P2X]
# every game orient (copro->game map {0:3,1:1,2:0,3:2} -- only 1 is identity) x both slide directions
for (G, C, so, sx) in [(3, 6, 0, 3), (0, 1, 0, 4), (2, 5, 0, 2), (1, 7, 0, 0)]:
    o, x = land_pill(G, C, spawn_orient=so, spawn_x=sx)
    check(f"pill LANDS orient={G} col={C} (spawn o={so} x={sx})", o == G and x == C,
          f"landed orient={o} col={x}  <- would be raw/unmapped if the nf2 map regressed")

print()
npass = sum(1 for _, c, _ in results if c)
print(f"==== {npass}/{len(results)} checks passed ====")
sys.exit(0 if npass == len(results) else 1)
