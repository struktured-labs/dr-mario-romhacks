"""Drive NES Dr. Mario (base drmario.nes) with the faithful depth-2 planner via
the frame-perfect bridge. Movement + rotation are fully verified live.

Canonical RAM (Data Crystal; verified live, see LIVE_CONTROL_NOTES UPDATE 3):
  mode=$0046 (active play=4)   board=$0400 (virus=$Dx, color=low nibble, empty=$FF)
  capsule X(col 0-7)=$0305     Y(row,15=spawn top)=$0306     orientation=$00A5
  pill colors=$0301/$0302      P1 viruses=$0324

Control: rotate = tap A until $00A5==target (A decrements orient mod 4);
move = tap LEFT/RIGHT until $0305==target; drop = hold DOWN until the board
changes (lock). The capsule is ONLY controllable while falling (mode==4, Y<=13);
at Y=15 it is in the ~20-frame spawn animation and ignores input.

Planner action = variant*8 + col, variant {0:H(a,b),1:H(b,a),2:V(a-top,b-bot),
3:V(b-top,a-bot)} with pill a=$0301, b=$0302. Verified variant->$00A5 orientation
map and col==X below.
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, "/home/struktured/projects/dr-mario-mods/rl-training-new/src")
sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/src")
RELEASE = Path("/home/struktured/projects/dr-mario-mods/mesen2/bin/linux-x64/Release")
from mesen_interface_file import MesenInterface
from drmario.faithful_game import (
    FaithfulBoard, Pill, LINK_NONE, LINK_UP, LINK_DOWN, LINK_LEFT, LINK_RIGHT,
)
from drmario.planner import GreedyPlanner, PlannerWeights

# Tuned weights: vertical-clear pursuit (lifts the buried-virus endgame) + a
# spawn-column penalty (cols 3-4) to stop the greedy clustering -> fast top-out
# seen live at high levels (viruses near the top tempt it to stack the spawn lane).
# Every knob exposed via env for quick live A/B (preserves PlannerWeights defaults).
import os as _os
def _wf(name, default):
    return float(_os.environ.get("DRM_" + name, default))
TUNED_WEIGHTS = PlannerWeights(
    virus=_wf("VIRUS", 18.0),
    clear_cell=_wf("CLEAR_CELL", 0.6),
    combo=_wf("COMBO", 6.0),
    height_pen=_wf("HEIGHT_PEN", 1.2),
    holes_pen=_wf("HOLES_PEN", 2.5),
    top_risk_pen=_wf("TOP_RISK_PEN", 4.5),
    setup_bonus=_wf("SETUP_BONUS", 4.0),
    buried_pen=_wf("BURIED_PEN", 3.0),
    readiness_bonus=_wf("READINESS", 0.4),
    v_readiness_bonus=_wf("V_READY", 1.5),
    spawn_pen=_wf("SPAWN_PEN", 0.0),
    spawn_col_pen=_wf("SPAWN_COL_PEN", 0.0),
    junk_bonus=_wf("JUNK_BONUS", 0.0),
    pollution_pen=_wf("POLLUTION_PEN", 0.0),
    dual_end_bonus=_wf("DUAL_END_BONUS", 0.0),
)

# Endgame-only profile, activated by GreedyPlanner when virus_count <= threshold.
# Defaults are "dig mode": heavy buried_pen + clear_cell + push verticals to dig
# debris off the last few viruses. Off by default (threshold=0 -> never fires);
# set DRM_ENDGAME_THRESHOLD>0 to enable. Each knob takes DRM_END_<NAME>.
_ENDGAME_THRESHOLD = int(_os.environ.get("DRM_ENDGAME_THRESHOLD", "0"))
def _ef(name, default):
    return float(_os.environ.get("DRM_END_" + name, default))
ENDGAME_WEIGHTS = PlannerWeights(
    virus=_ef("VIRUS", 18.0),
    clear_cell=_ef("CLEAR_CELL", 2.5),
    combo=_ef("COMBO", 6.0),
    height_pen=_ef("HEIGHT_PEN", 0.9),
    holes_pen=_ef("HOLES_PEN", 2.5),
    top_risk_pen=_ef("TOP_RISK_PEN", 4.5),
    setup_bonus=_ef("SETUP_BONUS", 4.0),
    buried_pen=_ef("BURIED_PEN", 6.0),
    readiness_bonus=_ef("READINESS", 0.4),
    v_readiness_bonus=_ef("V_READY", 2.5),
    spawn_pen=_ef("SPAWN_PEN", 0.0),
    spawn_col_pen=_ef("SPAWN_COL_PEN", 0.0),
    junk_bonus=_ef("JUNK_BONUS", 0.0),
    pollution_pen=_ef("POLLUTION_PEN", 0.0),
    dual_end_bonus=_ef("DUAL_END_BONUS", 0.0),
)

MODE, BOARD, CAP_X, CAP_Y, ORIENT = 0x0046, 0x0400, 0x0305, 0x0306, 0x00A5
PILL_A, PILL_B, P1_VIR, LEVEL, SPEED = 0x0301, 0x0302, 0x0324, 0x0096, 0x008B
NEXT_A, NEXT_B = 0x031A, 0x031B  # next-pill preview (verified: becomes current next lock)
RNG_LO, RNG_HI = 0x0017, 0x0018  # RNG state; writing at level-select varies the game
# planner variant -> NES $00A5 orientation (verified by geometry.py drop test)
VAR2NES = {0: 0, 1: 2, 2: 3, 3: 1}


def nes_color(b):
    if b in (0xFF, 0x00):
        return 0, False
    if (b & 0xF0) == 0xD0:
        return (b & 0x0F) + 1, True
    if 0x40 <= b <= 0x8F:
        return (b & 0x0F) + 1, False
    return 0, False


def nes_link(b):
    """Decode the capsule connection from a board tile (verified live):
    0x4x=top half (links down), 0x5x=bottom (links up), 0x6x=left (links right),
    0x7x=right (links left), else single/virus/empty. Correct links are essential
    so the planner's cascade gravity matches the ROM (pairs fall rigidly)."""
    hi = b & 0xF0
    if hi == 0x40:
        return LINK_DOWN
    if hi == 0x50:
        return LINK_UP
    if hi == 0x60:
        return LINK_RIGHT
    if hi == 0x70:
        return LINK_LEFT
    return LINK_NONE


def read_board(it):
    pf = it.read_memory(BOARD, 128)
    b = FaithfulBoard(16, 8)
    for i, byte in enumerate(pf):
        c, v = nes_color(byte)
        b.color[i // 8, i % 8] = c
        b.is_virus[i // 8, i % 8] = v
        b.link[i // 8, i % 8] = nes_link(byte) if not v else LINK_NONE
    return b


def fill(it):
    return sum(1 for b in it.read_memory(BOARD, 128) if b not in (0xFF, 0x00))


def tap(it, btn):
    it.set_input(0, [btn]); it.step_frame(1)
    it.set_input(0, []); it.step_frame(1)


def nav(it, rd, level=0, speed=None, seed=None):
    """Soft-reset to title, set the virus level (and optional speed), start a game.

    Flow (verified): title -> Start -> level-select (mode 1) where RIGHT/LEFT change
    the virus level ($0096) and, on the speed row, the speed cursor ($008B; 0=LOW,
    1=MED, 2=HI) -> Start begins the game (mode 8 intro -> 4 play). Never presses
    Start once in-game (Start = pause).

    ``seed`` (0-255) writes the RNG state ($0017/$0018) at level-select before
    starting, which changes the virus layout AND pill sequence -- verified live.
    A soft reset alone replays the identical game, so this is required to get
    distinct trials / to retry for a win."""
    def start_tap():
        it.set_input(0, ["start"]); it.step_frame(8); it.set_input(0, []); it.step_frame(40)
    def tap(b, n=1):
        for _ in range(n):
            it.set_input(0, [b]); it.step_frame(3); it.set_input(0, []); it.step_frame(3)
    it.reset()
    it.step_frame(150)  # boot to title
    # reach the level-select screen
    for _ in range(5):
        if rd(MODE) in (1, 4, 8):
            break
        start_tap()
    # set virus level via RIGHT/LEFT (cursor defaults to the level row)
    if rd(MODE) == 1:
        for _ in range(40):
            cur = rd(LEVEL)
            if cur == level:
                break
            tap("right" if cur < level else "left")
        # optional speed: move cursor down to the speed row, then set $008B
        if speed is not None:
            tap("down")
            for _ in range(6):
                cur = rd(SPEED)
                if cur == speed:
                    break
                tap("right" if cur < speed else "left")
        # inject RNG seed so each trial gets a distinct game (verified $0017/$0018)
        if seed is not None:
            it.write_memory(RNG_LO, [seed & 0xFF])
            it.write_memory(RNG_HI, [(seed ^ 0x5A) & 0xFF])
    # begin the game
    for _ in range(5):
        if rd(MODE) in (4, 8):
            return True
        start_tap()
    return rd(MODE) in (4, 8)


def wait_falling(it, rd):
    """Step until a freshly-spawned capsule is controllable (mode==4, fell past spawn).
    Unpauses once if it looks frozen. Returns False if no capsule appears (win/lose)."""
    for attempt in range(2):
        seen_spawn = False
        for _ in range(600):
            it.step_frame(1)
            m, y = rd(MODE), rd(CAP_Y)
            if m == 4 and y >= 14:
                seen_spawn = True
            if m == 4 and seen_spawn and y <= 13:
                return True
        # frozen? unpause with a single Start and retry once
        it.set_step_mode(False)
        it.set_input(0, ["start"]); it.step_frame(8); it.set_input(0, [])
        it.step_frame(20); it.set_step_mode(True)
    return False


def rotate_to(it, rd, target):
    for _ in range(6):
        if rd(ORIENT) == target:
            return True
        tap(it, "a")
    return rd(ORIENT) == target


def move_to(it, rd, target):
    """Set the capsule column INSTANTLY via direct RAM write ($0305 is writable and
    the capsule lands at the written column -- verified). This avoids spending
    game-frames tapping LEFT/RIGHT, so the capsule barely falls during maneuver --
    critical at tall stacks / high fall speed. Falls back to tapping if needed."""
    it.write_memory(CAP_X, [target]); it.step_frame(1)
    if rd(CAP_X) == target:
        return True
    for _ in range(10):
        x = rd(CAP_X)
        if x == target:
            return True
        tap(it, "left" if x > target else "right")
    return rd(CAP_X) == target


def drop_lock(it):
    f0 = fill(it)
    it.set_input(0, ["down"])
    locked = False
    for _ in range(240):
        it.step_frame(1)
        if fill(it) != f0:
            locked = True
            break
    it.set_input(0, [])
    for _ in range(30):  # settle clears / cascades
        it.step_frame(1)
    return locked


def play_one_game(it, rd, planner, level, speed, verbose=True, seed=None):
    """Play one game from a fresh reset at ``level``/``speed`` (frame-perfect).
    ``seed`` varies the RNG so trials differ. Returns
    {won, start_v, end_v, pills, diverge}."""
    if not nav(it, rd, level=level, speed=speed, seed=seed):
        return {"won": False, "start_v": 0, "end_v": -1, "pills": 0, "diverge": 0, "err": "nav"}
    if not wait_falling(it, rd):
        return {"won": False, "start_v": 0, "end_v": -1, "pills": 0, "diverge": 0, "err": "no-gameplay"}
    start_v = read_board(it).virus_count()
    if verbose:
        spd = {0: "LOW", 1: "MED", 2: "HI"}.get(rd(SPEED), "?")
        print(f"=== level {rd(LEVEL)} start: {start_v} viruses, speed={spd} ===", flush=True)
    won, diverge_ct, vleft, pill = False, 0, start_v, 0
    last_live_board = None  # snapshot to log on failure (post-game reads unreliable)
    last_live_pill = 0
    max_pills = int(_os.environ.get("DRM_MAX_PILLS", "200"))
    # Track auto-level-advance wins. The game increments $0096 only when the
    # player clears all viruses on the current level — even though our nv read
    # afterwards sees the next level's freshly-spawned viruses. Watching the
    # level register catches these wins reliably.
    start_level = rd(LEVEL)
    level_wins = 0
    pills_at_first_win = -1
    for pill in range(max_pills):  # match sim MAX_PILLS; thrashing past this is a loss
        board = read_board(it)
        last_live_board = board       # snapshot the in-game state (post-game reads are unreliable)
        last_live_pill = pill
        vleft = board.virus_count()
        if vleft == 0:
            won = True; break
        cur = Pill((rd(PILL_A) & 0x0F) + 1, (rd(PILL_B) & 0x0F) + 1)
        nxt = Pill((rd(NEXT_A) & 0x0F) + 1, (rd(NEXT_B) & 0x0F) + 1)
        action = planner.choose(board, cur, nxt)  # exact 2-ply (real next pill)
        if action is None:
            if verbose:
                print(f"  no legal move (topped out), viruses_left={vleft}", flush=True)
            break
        sim = planner.simulate(board, action, cur)
        pred_v = sim[1] if sim else 0
        variant, col = action // 8, action % 8
        nes_or = VAR2NES[variant]
        rotate_to(it, rd, nes_or)
        move_to(it, rd, col)
        if rd(ORIENT) != nes_or:  # drifted (rare wall-kick) -- correct once
            rotate_to(it, rd, nes_or); move_to(it, rd, col)
        locked = drop_lock(it)
        # Check level register IMMEDIATELY after lock — catches a level-clear before
        # the next-level board (with its freshly-spawned viruses) overwrites our nv read.
        post_lock_level = rd(LEVEL)
        if post_lock_level > start_level + level_wins:
            level_wins += 1
            if pills_at_first_win < 0:
                pills_at_first_win = pill + 1
            won = True
            if verbose:
                print(f"  pill#{pill+1}: *** LEVEL CLEARED *** (L{post_lock_level - 1} -> L{post_lock_level}; total wins={level_wins})", flush=True)
        got_next = wait_falling(it, rd)  # wait out the full cascade + next capsule spawn
        nv = read_board(it).virus_count()  # fully-settled board (accurate clear count)
        if pred_v != (vleft - nv):
            diverge_ct += 1
        if verbose and (pill % 5 == 0 or nv != vleft or pred_v != (vleft - nv)):
            tag = "  <-- DIVERGE" if pred_v != (vleft - nv) else ""
            print(f"  pill#{pill+1}: var{variant}->or{nes_or} col{col} "
                  f"viruses {vleft}->{nv} (pred -{pred_v}/act -{vleft-nv}){tag}", flush=True)
        if nv == 0:  # level cleared (fallback when level didn't auto-advance)
            won = True; vleft = 0; break
        if not locked or not got_next:  # topped out / no next capsule
            break
    if not won:
        try:
            # Use the in-game snapshot, NOT a fresh read_board: after a game ends
            # the NES may show a game-over screen / next-game state whose playfield
            # bytes look like a different board, so post-game reads are unreliable.
            final_b = last_live_board if last_live_board is not None else read_board(it)
            remaining = []
            for r in range(final_b.rows):
                for c in range(final_b.cols):
                    if final_b.is_virus[r, c]:
                        remaining.append({"r": int(r), "c": int(c), "color": int(final_b.color[r, c])})
            buried = 0
            for c in range(final_b.cols):
                seen_v = False
                for r in range(final_b.rows - 1, -1, -1):
                    if final_b.is_virus[r, c]:
                        seen_v = True
                    elif seen_v and final_b.color[r, c] != 0:
                        buried += 1
            os.makedirs("/home/struktured/projects/dr-mario-mods/tmp", exist_ok=True)
            rec = {
                "level": int(level),
                "seed": int(seed) if seed is not None else -1,
                "start_v": int(start_v),
                "end_v": int(vleft),
                "pills": int(pill + 1),
                "diverge": int(diverge_ct),
                "board_ascii": final_b.ascii(),
                "remaining_viruses": remaining,
                "buried_count": int(buried),
            }
            with open("/home/struktured/projects/dr-mario-mods/tmp/endgame_failures.jsonl", "a") as _f:
                _f.write(json.dumps(rec) + "\n")
        except Exception:
            pass
    return {"won": won, "start_v": start_v, "end_v": vleft, "pills": pill + 1,
            "diverge": diverge_ct, "level_wins": level_wins,
            "pills_to_first_win": pills_at_first_win}


def main():
    level = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    speed = int(sys.argv[2]) if len(sys.argv) > 2 else None  # 0=LOW 1=MED 2=HI
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    it = MesenInterface(work_dir=RELEASE)
    if not it.connect(timeout=8):
        print("no bridge"); return
    rd = lambda a: it.read_memory(a, 1)[0]
    depth = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    # Enable endgame weight switching only if DRM_ENDGAME_THRESHOLD > 0 (default off).
    eg_weights = ENDGAME_WEIGHTS if _ENDGAME_THRESHOLD > 0 else None
    # Optional pruned-depth endgame: set DRM_ENDGAME_DEPTH > 0 to use deeper
    # search (with top-K pruning) once virus_count <= ENDGAME_THRESHOLD.
    endgame_depth = int(_os.environ.get("DRM_ENDGAME_DEPTH", "0"))
    endgame_top_k = int(_os.environ.get("DRM_ENDGAME_TOP_K", "8"))
    planner = GreedyPlanner(TUNED_WEIGHTS, depth=depth,
                            endgame_weights=eg_weights,
                            endgame_virus_threshold=_ENDGAME_THRESHOLD,
                            endgame_depth=endgame_depth,
                            endgame_top_k=endgame_top_k)
    if endgame_depth > 0:
        print(f"endgame depth-{endgame_depth} with top-{endgame_top_k} pruning, threshold={_ENDGAME_THRESHOLD}", flush=True)
    if eg_weights is not None:
        print(f"endgame profile active when virus_count <= {_ENDGAME_THRESHOLD}", flush=True)
    it.set_step_mode(True)  # frame-perfect -> nav + play deterministic at any emu speed
    results = []
    try:
        seed0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        for t in range(trials):
            # vary RNG per trial via the $0017/$0018 seed write (sequential from seed0
            # so trials line up with harvested/replayed layouts for apples-to-apples).
            r = play_one_game(it, rd, planner, level, speed,
                              verbose=(trials == 1), seed=(seed0 + t) & 0xFF)
            results.append(r)
            print(f"game {t+1}/{trials}: won={r['won']} levels_cleared={r.get('level_wins', 0)} "
                  f"pills_to_1st_win={r.get('pills_to_first_win', -1)} "
                  f"viruses {r['start_v']}->{r['end_v']} "
                  f"pills={r['pills']} diverge={r['diverge']}", flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        it.set_input(0, []); it.set_step_mode(False); it.release(0); it.disconnect()
    wins = sum(1 for r in results if r["won"])
    if results:
        print(f"\n=== WIN RATE: {wins}/{len(results)} at level {level} speed={speed} ===", flush=True)


if __name__ == "__main__":
    main()
