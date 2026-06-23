"""Drive NES Dr. Mario with the faithful depth-2 planner via FRAME-PERFECT stepping.

Uses the BASE drmario.nes (no in-ROM AI hook -- the VS-CPU hook intercepts the
controller read, so external input only works on the un-hooked base ROM). The
bridge's step mode advances one frame per STEP and blocks between, so each pill:
read board -> plan (depth-2, unlimited time) -> rotate -> steer X to the exact
column one frame at a time -> drop until it locks. Deterministic placement.

Verified live addresses (base drmario.nes, 2P level 0 via Start x3):
  board=$0400  capsule X(col 0-7)=$004B  pill=$0301/$0302  next=$031A/$031B
  cell: virus=$Dx, pill=$4x-8x, color=low nibble, empty=$FF; port-0 input, DOWN locks.
"""
import sys
from pathlib import Path
sys.path.insert(0, "/home/struktured/projects/dr-mario-mods/rl-training-new/src")
sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/src")
RELEASE = Path("/home/struktured/projects/dr-mario-mods/mesen2/bin/linux-x64/Release")
from mesen_interface_file import MesenInterface
from drmario.faithful_game import FaithfulBoard, Pill
from drmario.planner import GreedyPlanner

BOARD, CAP_X = 0x0400, 0x004B
PILL_L, PILL_R, NEXT_L, NEXT_R = 0x0301, 0x0302, 0x031A, 0x031B
ROT_PRESSES = {0: 0, 1: 2, 2: 1, 3: 3}


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


def fill_count(it):
    return sum(1 for b in it.read_memory(BOARD, 128) if b not in (0xFF, 0x00))


def tap(it, btn):
    it.set_input(0, [btn]); it.step_frame(1)
    it.set_input(0, []); it.step_frame(1)


def nav_new_game(it):
    """Boot/menu nav to a fresh game (free-run)."""
    it.step_frame(40)
    for _ in range(3):
        it.set_input(0, ["start"])
        for _ in range(8): it.step_frame(1)
        it.set_input(0, [])
        for _ in range(40): it.step_frame(1)


def main():
    it = MesenInterface(work_dir=RELEASE)
    if not it.connect(timeout=8):
        print("no bridge"); return
    rd = lambda a: it.read_memory(a, 1)[0]
    planner = GreedyPlanner(depth=2)
    nav_new_game(it)
    it.set_step_mode(True)
    start_v = read_board(it).virus_count()
    print(f"=== round start: {start_v} viruses (frame-perfect, base ROM) ===", flush=True)
    won = False
    try:
        for pill in range(150):
            board = read_board(it)
            vleft = board.virus_count()
            if vleft == 0:
                print(f"*** WON! cleared all {start_v} viruses in {pill} pills ***", flush=True)
                won = True; break
            # color-order verified: board-left=$0302, board-right=$0301 (swapped vs naming)
            cur = Pill((rd(PILL_R) & 0x0F) + 1, (rd(PILL_L) & 0x0F) + 1)
            # rotation-0 horizontal only (variant 0 = a-left,b-right) -- isolate color fix
            col, bestv = None, -1e9
            for action, orient, c2, p in planner.enumerate_placements(board, cur):
                if action // 8 != 0:
                    continue
                sim = planner._simulate(board, orient, c2, p)
                if sim:
                    imm, bs = planner._move_value(sim)
                    if imm + bs > bestv:
                        bestv, col = imm + bs, c2
            if col is None:
                print(f"  no legal move after {pill} pills (topped out)"); break
            var = 0
            for _ in range(12):
                x = rd(CAP_X)
                if x == col:
                    break
                tap(it, "left" if x > col else "right")
            fill0 = fill_count(it)
            it.set_input(0, ["down"])
            locked = False
            for _ in range(120):
                it.step_frame(1)
                if fill_count(it) != fill0:
                    locked = True; break
            it.set_input(0, [])
            for _ in range(4): it.step_frame(1)
            if pill % 3 == 0 or vleft <= 4:
                print(f"  pill#{pill+1}: col{col} rot{ROT_PRESSES.get(var,0)} locked={locked} viruses_left={vleft}", flush=True)
            if not locked:
                print(f"  pill didn't lock after {pill+1} pills (topped out), viruses_left={vleft}", flush=True)
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
