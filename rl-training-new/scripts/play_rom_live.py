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
import sys
from pathlib import Path

sys.path.insert(0, "/home/struktured/projects/dr-mario-mods/rl-training-new/src")
sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/src")
RELEASE = Path("/home/struktured/projects/dr-mario-mods/mesen2/bin/linux-x64/Release")
from mesen_interface_file import MesenInterface
from drmario.faithful_game import (
    FaithfulBoard, Pill, LINK_NONE, LINK_UP, LINK_DOWN, LINK_LEFT, LINK_RIGHT,
)
from drmario.planner import GreedyPlanner

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
    for pill in range(300):
        board = read_board(it)
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
        nv = read_board(it).virus_count()
        if pred_v != (vleft - nv):
            diverge_ct += 1
        if verbose and (pill % 5 == 0 or nv != vleft or pred_v != (vleft - nv)):
            tag = "  <-- DIVERGE" if pred_v != (vleft - nv) else ""
            print(f"  pill#{pill+1}: var{variant}->or{nes_or} col{col} "
                  f"viruses {vleft}->{nv} (pred -{pred_v}/act -{vleft-nv}){tag}", flush=True)
        if nv == 0:  # cleared the level THIS drop -- win before the game advances levels
            won = True; vleft = 0; break
        if not locked:
            if verbose:
                print(f"  pill didn't lock (topped out) after {pill+1}", flush=True)
            break
        if not wait_falling(it, rd):
            if read_board(it).virus_count() == 0:
                won = True; vleft = 0
            break
    return {"won": won, "start_v": start_v, "end_v": vleft, "pills": pill + 1, "diverge": diverge_ct}


def main():
    level = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    speed = int(sys.argv[2]) if len(sys.argv) > 2 else None  # 0=LOW 1=MED 2=HI
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    it = MesenInterface(work_dir=RELEASE)
    if not it.connect(timeout=8):
        print("no bridge"); return
    rd = lambda a: it.read_memory(a, 1)[0]
    planner = GreedyPlanner(depth=2)
    it.set_step_mode(True)  # frame-perfect -> nav + play deterministic at any emu speed
    results = []
    try:
        for t in range(trials):
            # vary RNG per trial (soft reset alone is deterministic -> identical games)
            r = play_one_game(it, rd, planner, level, speed,
                              verbose=(trials == 1), seed=(t * 37 + 11) & 0xFF)
            results.append(r)
            print(f"game {t+1}/{trials}: won={r['won']} viruses {r['start_v']}->{r['end_v']} "
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
