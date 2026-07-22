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
LAST_COL2, LAST_ORI2, STABLE_CT2 = 0x616F, 0x6170, 0x6171   # DRSLAM argmax-stability state
SLAM_OK = 0x6172                                             # DRSLAM_COLDGUARD "pipeline validated" latch
STK2 = 0x615B
LASTY1, LASTY2 = 0x6154, 0x6155
P1Y = 0x0306
NAV_MAGIC, MATCH_ACTIVE = 0x6149, 0x6164
VCOUNT_P1, VCOUNT_P2 = 0x0324, 0x03A4
MODE = 0x0046
SENTINEL = 0x0400
FLUSH_Y = 0x08          # mock: capsule can rotate only while Y (height) > FLUSH_Y


_KNOB_ENV = {"kopen": "DRSLAM_KOPEN", "kend": "DRSLAM_KEND", "kcross": "DRSLAM_KCROSS",
             "vcend": "DRSLAM_VCEND", "lowy": "DRSLAM_LOWY", "minthink": "DRMINTHINK"}


def load_build(rotfix, slam=True, coldguard=True, human=False, pocket=False, patcher=WT, **knobs):
    """Import the patcher fresh (module-level env is read at import) and return build_main bytes.
    slam=True/False sets DRSLAM; coldguard=True/False sets DRSLAM_COLDGUARD (the first-DONE gate);
    human/pocket select the shipped variants (DRHUMAN/DRPOCKET); **knobs override the phase table
    (kopen/kend/kcross/vcend/lowy) and the min-think floor (minthink) so scenarios stay deterministic."""
    for k in ("DRNOFREEZE", "DRROTFIX", "DRHUMAN", "DRPOCKET", "DRSLAM", "DRSLAM_COLDGUARD", *_KNOB_ENV.values()):
        os.environ.pop(k, None)
    os.environ["DRNOFREEZE"] = "1"
    os.environ["DRROTFIX"] = "1" if rotfix else "0"
    os.environ["DRSLAM"] = "1" if slam else "0"
    os.environ["DRSLAM_COLDGUARD"] = "1" if coldguard else "0"
    if human:
        os.environ["DRHUMAN"] = "1"
    if pocket:
        os.environ["DRPOCKET"] = "1"
    for name, val in knobs.items():
        os.environ[_KNOB_ENV[name]] = str(val)
    wtdir = os.path.dirname(patcher)
    for p in (wtdir, os.path.join(wtdir, "tests")):
        if p not in sys.path:
            sys.path.insert(0, p)
    # unique module name per (patcher, config) so env changes take effect (module body re-runs)
    key = f"pc_{abs(hash((patcher, rotfix, slam, coldguard, human, pocket, tuple(sorted(knobs.items()))))):x}"
    spec = importlib.util.spec_from_file_location(key, patcher)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    code, lab = m.build_main(11, 1)
    return code, lab


class Sim:
    def __init__(self, rotfix, slam=True, **knobs):
        self.code, self.lab = load_build(rotfix, slam=slam, **knobs)
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
        self.soft_drop = False              # SLAM tests: model DOWN($04)-held soft-drop (fixed 2 f/row,
        self.soft_period = 2                #  speed-invariant per TEMPO_DESIGN §2.1) vs natural gravity
        self.scount = 0

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
            if not froze:                   # gravity: fall one row per period (soft-drop if DOWN held)
                if self.soft_drop and (f6 & 0x04):   # DOWN = fixed soft-drop rate (faster than natural)
                    self.scount += 1
                    if self.scount >= self.soft_period:
                        self.scount = 0
                        if self.mem[P2Y] > 0:
                            self.mem[P2Y] -= 1
                else:
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
    s.mem[SLAM_OK] = 1   # normal mid-match: the pipeline has DONE'd before -> slam armed. Cold-entry
                         #   scenarios below clear this to test DRSLAM_COLDGUARD explicitly.


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

# ================================================================ DRSLAM confidence-gated slam ====
# The macro gate above (16 checks) is the pre-existing DRROTFIX suite and MUST stay green with the
# slam default-on -- that is task item (e). The scenarios below add the DRSLAM behavior (a)-(d),(f)
# plus the DRSLAM=0 byte-exactness gate. Knobs are shrunk (small K / min-think) so each runs fast.

# ---------------------------------------------------------------- (a) engages only after the gate
print("SCENARIO A (DRSLAM=1): slam engages ONLY after stability + min-think + aligned + rotated")
s = Sim(rotfix=True, slam=True, minthink=30, kopen=6, vcend=10, lowy=8)
s.soft_drop = True
s.grav_period = 25                     # keep the capsule HIGH (Y>=8) until min-think opens, so the
spawn_pill(s, y=0x0D, x=3, orient=0)    #   commit is the MIN-THINK floor, not the low-Y crossover
publish_live(s, col=3, orient=2)       # aligned column (x=3=col 3); orient needs 2 rotations first
downs = []                             # (frame, ROT_DONE2, y) for every DOWN-held frame
for i in range(140):
    st = s.frame(apply_physics=True)
    if st["f6"] & 0x04:
        downs.append((i, st["rot"], st["y"]))
    if st["y"] == 0:
        break
early = [d for d in downs if not d[1]]  # any DOWN before ROT_DONE2 = a min-think-floor breach
check("A: no slam before ROT_DONE2 (min-think floor + rotation-complete are prerequisites)",
      len(early) == 0, f"early-DOWN frames={early[:3]}")
check("A: slam DID engage once committed+aligned+stable", len(downs) > 0 and downs[0][1] == 1,
      f"first DOWN at frame={downs[0][0] if downs else None} rot={downs[0][1] if downs else '-'}")
ys = [d[2] for d in downs]
span = (ys[0] - ys[-1]) if len(ys) >= 4 else 0
rate = (len(ys) - 1) / span if span else 999   # frames-per-row under sustained DOWN
check("A: under DOWN the capsule descends ~2 f/row (soft-drop, vs natural 25 f/row)",
      1.5 <= rate <= 3.0, f"measured {rate:.2f} f/row over {len(ys)} DOWN frames (spawn grav=25 f/row)")

# ---------------------------------------------------------------- (b) aborts + re-steers on change
print("SCENARIO B (DRSLAM=1): slam ABORTS + re-steers if the stable argmax changes pre-lock")
s = Sim(rotfix=True, slam=True, minthink=8, kopen=4, vcend=10, lowy=6)
s.grav_period = 40                     # high Y: exercise the OPEN-K abort (not the crossover)
spawn_pill(s, y=0x0D, x=3, orient=0)
publish_live(s, col=3, orient=0)       # aligned, no rotation -> commit fast, then slam on stability
slam_frame = None
for i in range(90):
    st = s.frame(apply_physics=True)
    if (st["f6"] & 0x04) and st["rot"]:
        slam_frame = i
        break
check("B: reached the slam state (DOWN held while committed + still armed)", slam_frame is not None,
      f"slam_frame={slam_frame}")
publish_live(s, col=6, orient=0)       # search changes its mind: a NEW column
released = resteered = reslam_instant = False
for i in range(14):
    st = s.frame(apply_physics=True)
    if not (st["f6"] & 0x04):
        released = True
    if st["f6"] & 0x01:                # RIGHT toward the new column 6
        resteered = True
    if i == 0 and (st["f6"] & 0x04):
        reslam_instant = True
check("B: DOWN releases on argmax change; no instant re-slam (STABLE_CT2 was zeroed)",
      released and not reslam_instant, f"released={released} reslam_instant={reslam_instant}")
check("B: re-steers toward the new column (TGT_C2 refreshed -> un-aligned -> mv_p2)", resteered,
      f"TGT_C2={s.mem[TGT_C2]} STABLE_CT2={s.mem[STABLE_CT2]}")

# ---------------------------------------------------------------- (c) never-DONE crossover
print("SCENARIO C (DRSLAM=1): never-DONE crossover -- min-think yields + gate commits, no drift-lock")
# HIGH min-think that never opens + never DONE + fast gravity: without the crossover escapes the
# orient would never lock and the pill would drift-lock. With them: commit low, slam the stable argmax.
s = Sim(rotfix=True, slam=True, minthink=250, kopen=250, kcross=6, vcend=10, lowy=8)
s.soft_drop = True; s.grav_period = 4
spawn_pill(s, y=0x0D, x=5, orient=0)
publish_live(s, col=5, orient=0)       # aligned; only the low-Y crossover paths can commit / slam
committed_y = slam_y = None
for i in range(140):
    st = s.frame(apply_physics=True)
    if st["rot"] and committed_y is None:
        committed_y = st["y"]
    if (st["f6"] & 0x04) and slam_y is None:
        slam_y = st["y"]
    if st["y"] == 0:
        break
check("C: min-think YIELDS under fast gravity (ROT_DONE2 latches though it never opened + never DONE)",
      committed_y is not None and committed_y < 8 and s.mem[ARMED2] != 0,
      f"committed at Y={committed_y} armed={s.mem[ARMED2]}")
check("C: gate commits on stability alone (slam fired LOW, never DONE, lands at target = no drift-lock)",
      slam_y is not None and slam_y < 8 and s.mem[P2X] == 5, f"slam Y={slam_y} landed col={s.mem[P2X]} (target 5)")
# steering variant: reaches a FAR target under never-DONE fast gravity (drift-lock would miss it)
s2 = Sim(rotfix=True, slam=True, minthink=6, kopen=250, kcross=6, vcend=10, lowy=8)
s2.soft_drop = True; s2.grav_period = 6
spawn_pill(s2, y=0x0D, x=2, orient=0)
publish_live(s2, col=6, orient=0)
for i in range(180):
    st = s2.frame(apply_physics=True)
    if st["y"] == 0:
        break
check("C: never-DONE, still steers to a far column + lands there (col 6 from spawn 2)",
      s2.mem[P2X] == 6 and s2.mem[ARMED2] != 0, f"landed col={s2.mem[P2X]} armed={s2.mem[ARMED2]}")

# ---------------------------------------------------------------- (d) endgame requires DONE
print("SCENARIO D (DRSLAM=1): endgame (low virus count) requires DONE -- no stability slam above the crossover")
s = Sim(rotfix=True, slam=True, minthink=5, kopen=3, kend=255, vcend=10, lowy=8)
s.mem[VCOUNT_P2] = 5                    # endgame: vc < VC_ENDGAME(10)
spawn_pill(s, y=0x0D, x=3, orient=0)    # aligned, no rotation
publish_live(s, col=3, orient=0)        # perfectly stable argmax -- but endgame + high Y must NOT slam
endgame_downs = 0
for i in range(320):                    # long enough that STABLE_CT2 hits its 0xFE ceiling
    st = s.frame(apply_physics=False)   # Y frozen HIGH (13): no crossover -> pure endgame-DONE policy
    if st["f6"] & 0x04:
        endgame_downs += 1
check("D: endgame never slams on stability, even at the STABLE_CT2 ceiling (K_END=255 => DONE-only)",
      endgame_downs == 0 and s.mem[STABLE_CT2] == 0xFE,
      f"DOWN frames while endgame+armed+stable+high = {endgame_downs}; STABLE_CT2 saturated at "
      f"{s.mem[STABLE_CT2]} (0xFE, < K_END=255 => the compare can never fire)")
publish_done(s, col=3, orient=0)        # DONE arrives -> the ceiling slam still fires
done_slam = False
for i in range(10):
    st = s.frame(apply_physics=False)
    if st["f6"] & 0x04:
        done_slam = True
check("D: DONE still opens the ceiling slam in endgame", done_slam,
      f"DOWN after DONE={done_slam} armed={s.mem[ARMED2]}")

# ---------------------------------------------------------------- (f) fairness: gravity-pin audit
print("SCENARIO F (DRSLAM=1): FAIRNESS gravity-pin audit -- the SLAM path pins gravity 0 frames")
s = Sim(rotfix=True, slam=True, minthink=8, kopen=4, kcross=6, vcend=10, lowy=8)
s.soft_drop = True; s.grav_period = 6
spawn_pill(s, y=0x0D, x=2, orient=1)    # full lifecycle: rotate + slide + min-think + commit + slam
publish_live(s, col=6, orient=3)        # never DONE -> also drives the crossover slam path
for i in range(220):
    st = s.frame(apply_physics=True)
    if st["y"] == 0:
        break
check("F: ZERO gravity pins across a full SLAM-path pill (rotate+min-think+slam, all under live gravity)",
      not any(s.froze_hist), f"pinned={sum(s.froze_hist)}/{len(s.froze_hist)} frames")

# ---------------------------------------------------------------- (g) DRSLAM_COLDGUARD gate
print("SCENARIO G (DRSLAM_COLDGUARD): the confidence slam is HELD until P2's first DONE of the match")
s = Sim(rotfix=True, slam=True, coldguard=True, minthink=8, kopen=4, vcend=10, lowy=6)
s.grav_period = 40                      # Y stays high -> isolate the OPEN stability gate (no crossover)
spawn_pill(s, y=0x0D, x=3, orient=0)
s.mem[SLAM_OK] = 0                       # COLD entry: nothing validated yet this match
publish_live(s, col=3, orient=0)        # perfectly stable + aligned argmax -- but pre-first-DONE
cold_downs = 0
for i in range(60):
    st = s.frame(apply_physics=False)   # Y frozen high: only the OPEN stability gate could fire
    if st["f6"] & 0x04:
        cold_downs += 1
check("G: pre-first-DONE (SLAM_OK=0) the confidence slam does NOT fire (falls back to DONE-wait)",
      cold_downs == 0 and s.mem[SLAM_OK] == 0, f"DOWN frames={cold_downs} SLAM_OK={s.mem[SLAM_OK]}")
publish_done(s, col=3, orient=0)        # P2's first DONE -> handle() arms SLAM_OK; the ceiling slams
g_done_slam = False
for i in range(10):
    st = s.frame(apply_physics=False)
    if st["f6"] & 0x04:
        g_done_slam = True
check("G: P2's first DONE arms SLAM_OK (and the DONE ceiling still slams)",
      s.mem[SLAM_OK] == 1 and g_done_slam, f"SLAM_OK={s.mem[SLAM_OK]} done_slam={g_done_slam}")

# ---------------------------------------------------------------- (h) round-1 dead-round REGRESSION
print("SCENARIO H (regression): cold round-1 first pill -- pre-fix slam commits the pre-DONE window,")
print("  the coldguard waits for the validated DONE. (Field: slam dead-rounds round 1, wins rounds 2-3.)")
def cold_first_pill(coldguard):
    # cold match entry: the $5200 window holds a WRONG move (col1) until the search DONEs the RIGHT
    # move (col6) late (cold search). SLAM_OK=0 = first pill of the match, nothing validated yet.
    s = Sim(rotfix=True, slam=True, coldguard=coldguard, minthink=8, kopen=4, kcross=6, vcend=10, lowy=6)
    s.soft_drop = True; s.grav_period = 16
    spawn_pill(s, y=0x0D, x=3, orient=0)
    s.mem[SLAM_OK] = 0
    for i in range(300):
        if i < 120:
            publish_live(s, col=1, orient=0)      # cold pre-DONE window = a WRONG move
        else:
            publish_done(s, col=6, orient=0)      # the real answer, only now validated (DONE)
        st = s.frame(apply_physics=True)
        if st["y"] == 0:
            break
    return s.mem[P2X]
buggy = cold_first_pill(coldguard=False)   # == the aea9f6e pre-fix slam
fixed = cold_first_pill(coldguard=True)    # DRSLAM_COLDGUARD default
check("H: WITHOUT the coldguard the cold pill commits the WRONG pre-DONE move (col1) = the dead round",
      buggy == 1, f"pre-fix landed col={buggy} (wrong=1, correct=6)")
check("H: WITH the coldguard (default) the cold pill waits for the DONE and lands correct (col6)",
      fixed == 6, f"fixed landed col={fixed}")

# ---------------------------------------------------------------- byte-exactness: DRSLAM=0 == canonical
print("BYTE-EXACT (DRSLAM=0): rebuilds byte-identical to canonical, all three shipped variants")
import hashlib
VARIANTS = {"ab": {}, "human": {"human": True}, "pocket": {"human": True, "pocket": True}}
CANON = "/home/struktured/projects/dr-mario-canonical-wt/patch_cartridge_copro.py"
# canonical golden sha256[:16] of build_main(11,1) at copro-canonical c300acb (DRSLAM did not exist).
GOLDEN = {"ab": "855ca99a2cc3c8aa", "human": "70568fdbb39422cc", "pocket": "d1c7f8165767b4a4"}
for name, kw in VARIANTS.items():
    mine, _ = load_build(rotfix=True, slam=False, **kw)
    if os.path.exists(CANON):                       # strongest: diff against the live canonical patcher
        canon, _ = load_build(rotfix=True, slam=False, patcher=CANON, **kw)
        check(f"BYTE-EXACT {name}: DRSLAM=0 == canonical patcher (live diff)", bytes(mine) == bytes(canon),
              f"len mine={len(mine)} canon={len(canon)}")
    else:                                           # fallback: golden hash of c300acb
        sha = hashlib.sha256(bytes(mine)).hexdigest()[:16]
        check(f"BYTE-EXACT {name}: DRSLAM=0 == canonical golden", sha == GOLDEN[name],
              f"got {sha} want {GOLDEN[name]}")

print()
npass = sum(1 for _, c, _ in results if c)
print(f"==== {npass}/{len(results)} checks passed ====")
sys.exit(0 if npass == len(results) else 1)
