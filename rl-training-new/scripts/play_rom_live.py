"""Drive the NES Dr. Mario P1 capsule with the faithful planner (live, autonomous).

Horizontal-only v3: capsules spawn horizontal, so we steer the chosen column and
drop (no rotation -- the rotation RAM address isn't pinned down yet). Replans on
every lock (board-fill change) and auto-reloads the save state when a round ends,
so it runs unattended.

Verified live addresses (VS CPU, save slot 1, level 5):
  P1 board=$0400 (virus=$Dx, pill=$4x-8x, color=low nibble, empty=$FF)
  P1 cap X=$0090 (0-7 col, verified)   P1 pill=$0301/$0302   next=$031A/$031B
"""
import sys, time
from pathlib import Path
sys.path.insert(0, "/home/struktured/projects/dr-mario-mods/rl-training-new/src")
sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/src")
RELEASE = Path("/home/struktured/projects/dr-mario-mods/mesen2/bin/linux-x64/Release")
from mesen_interface_file import MesenInterface
from drmario.faithful_game import FaithfulBoard, Pill, ORIENT_H
from drmario.planner import GreedyPlanner

BOARD, CAP_X = 0x0400, 0x0090
PILL_L, PILL_R, NEXT_L, NEXT_R = 0x0301, 0x0302, 0x031A, 0x031B
STATE = str(RELEASE / "SaveStates/drmario_vs_cpu_1.mss")


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


def best_horizontal_col(planner, board, cur, nxt):
    best, bestv = None, -1e9
    for action, orient, col, pill in planner.enumerate_placements(board, cur):
        if orient != ORIENT_H:
            continue
        sim = planner._simulate(board, orient, col, pill)
        if sim is None:
            continue
        imm, bs = planner._move_value(sim)
        if imm + bs > bestv:
            bestv, best = imm + bs, col
    return best


def start_round(it):
    it.load_state(STATE)
    for _ in range(6): it.step_frame(1)
    it.set_input(0, ["start"])
    for _ in range(8): it.step_frame(1)
    it.set_input(0, [])
    for _ in range(18): it.step_frame(1)


def main():
    it = MesenInterface(work_dir=RELEASE)
    if not it.connect(timeout=8):
        print("no bridge"); return
    rd = lambda a: it.read_memory(a, 1)[0]
    planner = GreedyPlanner(depth=1)
    rounds_won = 0
    try:
        for attempt in range(6):
            start_round(it)
            board = read_board(it)
            start_v = board.virus_count()
            print(f"\n=== attempt {attempt+1}: round start, {start_v} viruses ===", flush=True)
            last_fill = int((board.color != 0).sum())
            target = None
            idle = 0
            pills = 0
            for step in range(1500):
                x = rd(CAP_X)
                board = read_board(it)
                fill = int((board.color != 0).sum())
                vleft = board.virus_count()
                if vleft == 0:
                    print(f"*** ROUND WON! cleared all {start_v} viruses in {pills} pills ***", flush=True)
                    rounds_won += 1
                    break
                if fill != last_fill or target is None:   # pill locked/cleared -> replan
                    last_fill = fill
                    idle = 0
                    cur = Pill((rd(PILL_L) & 0x0F) + 1, (rd(PILL_R) & 0x0F) + 1)
                    nxt = Pill((rd(NEXT_L) & 0x0F) + 1, (rd(NEXT_R) & 0x0F) + 1)
                    target = best_horizontal_col(planner, board, cur, nxt)
                    pills += 1
                    if pills % 8 == 1:
                        print(f"  pill#{pills}: col{target}  viruses_left={vleft}", flush=True)
                else:
                    idle += 1
                btns = []
                if target is not None:
                    if x > target: btns = ["left"]
                    elif x < target: btns = ["right"]
                    else: btns = ["down"]
                it.set_input(0, btns); it.step_frame(1)
                it.set_input(0, []); it.step_frame(1)
                if idle > 120:   # no lock for ~4s -> round likely ended (lost)
                    print(f"  round ended (lost or stalled) after {pills} pills, viruses_left={vleft}", flush=True)
                    break
    except KeyboardInterrupt:
        pass
    finally:
        it.set_input(0, []); it.release(0)
        print(f"\ndone. rounds won={rounds_won}", flush=True)
        it.disconnect()


if __name__ == "__main__":
    main()
