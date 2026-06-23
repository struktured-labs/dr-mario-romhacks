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
from drmario.faithful_game import FaithfulBoard, Pill
from drmario.planner import GreedyPlanner

MODE, BOARD, CAP_X, CAP_Y, ORIENT = 0x0046, 0x0400, 0x0305, 0x0306, 0x00A5
PILL_A, PILL_B, P1_VIR, LEVEL, SPEED = 0x0301, 0x0302, 0x0324, 0x0096, 0x008B
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


def read_board(it):
    pf = it.read_memory(BOARD, 128)
    b = FaithfulBoard(16, 8)
    for i, byte in enumerate(pf):
        c, v = nes_color(byte)
        b.color[i // 8, i % 8] = c
        b.is_virus[i // 8, i % 8] = v
    return b


def fill(it):
    return sum(1 for b in it.read_memory(BOARD, 128) if b not in (0xFF, 0x00))


def tap(it, btn):
    it.set_input(0, [btn]); it.step_frame(1)
    it.set_input(0, []); it.step_frame(1)


def nav(it, rd, level=0, speed=None):
    """Soft-reset to title, set the virus level (and optional speed), start a game.

    Flow (verified): title -> Start -> level-select (mode 1) where RIGHT/LEFT change
    the virus level ($0096) and, on the speed row, the speed cursor ($008B; 0=LOW,
    1=MED, 2=HI) -> Start begins the game (mode 8 intro -> 4 play). Never presses
    Start once in-game (Start = pause)."""
    def start_tap():
        it.set_input(0, ["start"]); it.step_frame(8); it.set_input(0, []); it.step_frame(40)
    def tap(b, n=1):
        for _ in range(n):
            it.set_input(0, [b]); it.step_frame(3); it.set_input(0, []); it.step_frame(3)
    it.reset()
    it.step_frame(150)  # boot: logo -> title
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


def main():
    level = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    speed = int(sys.argv[2]) if len(sys.argv) > 2 else None  # 0=LOW 1=MED 2=HI
    it = MesenInterface(work_dir=RELEASE)
    if not it.connect(timeout=8):
        print("no bridge"); return
    rd = lambda a: it.read_memory(a, 1)[0]
    planner = GreedyPlanner(depth=2)
    if not nav(it, rd, level=level, speed=speed):
        print("nav failed to start a game"); it.release(0); it.disconnect(); return
    it.set_step_mode(True)
    if not wait_falling(it, rd):
        print("never reached gameplay"); it.set_step_mode(False); it.release(0); it.disconnect(); return
    start_v = read_board(it).virus_count()
    spd = {0: "LOW", 1: "MED", 2: "HI"}.get(rd(SPEED), "?")
    print(f"=== level {rd(LEVEL)} start: {start_v} viruses, speed={spd} (base ROM, frame-perfect) ===", flush=True)
    won = False
    try:
        for pill in range(250):
            board = read_board(it)
            vleft = board.virus_count()
            if vleft == 0:
                print(f"*** WON! cleared all {start_v} viruses in {pill} pills ***", flush=True)
                won = True; break
            a = (rd(PILL_A) & 0x0F) + 1
            b = (rd(PILL_B) & 0x0F) + 1
            cur = Pill(a, b)
            action = planner.choose(board, cur)
            if action is None:
                print(f"  no legal move after {pill} pills (topped out), viruses_left={vleft}"); break
            variant, col = action // 8, action % 8
            nes_or = VAR2NES[variant]
            rotate_to(it, rd, nes_or)
            move_to(it, rd, col)
            if rd(ORIENT) != nes_or:  # drifted (rare wall-kick) -- correct once
                rotate_to(it, rd, nes_or); move_to(it, rd, col)
            locked = drop_lock(it)
            nv = read_board(it).virus_count()
            if pill % 2 == 0 or nv != vleft:
                print(f"  pill#{pill+1}: var{variant}->or{nes_or} col{col} "
                      f"locked={locked} viruses {vleft}->{nv}", flush=True)
            if not locked:
                print(f"  pill didn't lock (topped out) after {pill+1} pills"); break
            if not wait_falling(it, rd):
                nv = read_board(it).virus_count()
                if nv == 0:
                    print(f"*** WON! cleared all {start_v} viruses in {pill+1} pills ***", flush=True)
                    won = True
                else:
                    print(f"  no next capsule (game over?) viruses_left={nv}")
                break
    except KeyboardInterrupt:
        pass
    finally:
        it.set_input(0, []); it.set_step_mode(False); it.release(0)
        v = read_board(it).virus_count()
        print(f"\ndone. won={won}  viruses left={v} (started {start_v})", flush=True)
        it.disconnect()


if __name__ == "__main__":
    main()
