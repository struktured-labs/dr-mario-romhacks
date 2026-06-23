"""Drive the NES Dr. Mario P1 capsule with the faithful planner (live, autonomous).

v5: minimal-command state machine for precise real-time placement. Earlier loops
sent ~6 bridge commands per iteration (board+X reads + press/step/release/step),
so they only steered once every ~6 game-frames -- too coarse, pills never reached
their target. v5 reads only X each frame and sends one input/frame (board only on
replan), ~3x the control rate, alternating press/release for distinct inputs.

Phases per pill: ROTATE (A x N for color-correct orientation) -> MOVE (L/R to the
planned column) -> DROP (hold down). Replans per pill; auto-reloads on round loss.

Verified addresses (VS CPU save slot 1, level 5): board $0400, cap X $0090,
pill $0301/$0302, next $031A/$031B; virus=$Dx, color=low nibble, empty=$FF.
"""
import sys
from pathlib import Path
sys.path.insert(0, "/home/struktured/projects/dr-mario-mods/rl-training-new/src")
sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/src")
RELEASE = Path("/home/struktured/projects/dr-mario-mods/mesen2/bin/linux-x64/Release")
from mesen_interface_file import MesenInterface
from drmario.faithful_game import FaithfulBoard, Pill
from drmario.planner import GreedyPlanner

BOARD, CAP_X = 0x0400, 0x0090
PILL_L, PILL_R, NEXT_L, NEXT_R = 0x0301, 0x0302, 0x031A, 0x031B
SPAWN = 3
STATE = str(RELEASE / "SaveStates/drmario_vs_cpu_1.mss")
ROT_PRESSES = {0: 0, 1: 2, 2: 1, 3: 3}   # variant -> A presses (color-correct orientation)


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
        col, vir = nes_color(byte)
        b.color[i // 8, i % 8] = col
        b.is_virus[i // 8, i % 8] = vir
    return b


def start_round(it):
    it.load_state(STATE)
    for _ in range(6): it.step_frame(1)
    it.set_input(0, ["start"])
    for _ in range(8): it.step_frame(1)
    it.set_input(0, [])
    for _ in range(16): it.step_frame(1)


def main():
    it = MesenInterface(work_dir=RELEASE)
    if not it.connect(timeout=8):
        print("no bridge"); return
    rd = lambda a: it.read_memory(a, 1)[0]
    planner = GreedyPlanner(depth=2)
    rounds_won = 0
    try:
        for attempt in range(6):
            start_round(it)
            start_v = read_board(it).virus_count()
            print(f"\n=== attempt {attempt+1}: {start_v} viruses ===", flush=True)
            phase = "plan"
            target_col = SPAWN
            rot_left = 0
            press = True       # alternate press/release for distinct inputs
            last_x = SPAWN
            pills = 0
            idle = 0
            best_v = start_v
            for step in range(2000):
                x = rd(CAP_X)
                # detect new pill: X back at spawn after having moved away
                if phase == "plan" or (x in (SPAWN, SPAWN + 1) and last_x not in (SPAWN, SPAWN + 1)):
                    board = read_board(it)
                    vleft = board.virus_count()
                    if vleft == 0:
                        print(f"*** ROUND WON in {pills} pills! ***", flush=True)
                        rounds_won += 1; break
                    if vleft < best_v:
                        best_v = vleft; idle = 0
                    cur = Pill((rd(PILL_L) & 0x0F) + 1, (rd(PILL_R) & 0x0F) + 1)
                    nxt = Pill((rd(NEXT_L) & 0x0F) + 1, (rd(NEXT_R) & 0x0F) + 1)
                    a = planner.choose(board, cur, nxt)
                    if a is not None:
                        var, target_col = a // 8, a % 8
                        rot_left = ROT_PRESSES.get(var, 0)
                        phase = "rotate" if rot_left else "move"
                        pills += 1
                        if pills % 5 == 1:
                            print(f"  pill#{pills}: col{target_col} rot{rot_left}  viruses_left={vleft}", flush=True)
                # choose the desired action for this phase
                want = None
                if phase == "rotate":
                    want = "a" if rot_left > 0 else None
                    if rot_left == 0:
                        phase = "move"
                if phase == "move":
                    if x > target_col: want = "left"
                    elif x < target_col: want = "right"
                    else: phase = "drop"
                if phase == "drop":
                    it.set_input(0, ["down"]); last_x = x; idle += 1
                    continue
                # alternate press / release so each input registers distinctly
                if press and want:
                    it.set_input(0, [want]); press = False
                else:
                    it.set_input(0, [])
                    if not press and want == "a":
                        rot_left -= 1            # count a rotation per press+release cycle
                    press = True
                last_x = x
                idle += 1
                if idle > 200:
                    print(f"  round ended after {pills} pills, best viruses_left={best_v}", flush=True)
                    break
    except KeyboardInterrupt:
        pass
    finally:
        it.set_input(0, []); it.release(0)
        print(f"\ndone. rounds won={rounds_won}", flush=True)
        it.disconnect()


if __name__ == "__main__":
    main()
