"""Drive the NES Dr. Mario CPU live with the depth-2 faithful planner.

Reads the settled board + active capsule from the running ROM via the bridge,
asks the planner for the best placement, and drives P1's controller (emu.setInput)
to rotate + slide + drop the capsule there. Run while a game is active.

  cd mesen2/bin/linux-x64/Release
  ../../../../.venv/bin/python ../../../../rl-training-new/scripts/play_rom_live.py
"""
import sys, time
from pathlib import Path
sys.path.insert(0, "/home/struktured/projects/dr-mario-mods/rl-training-new/src")
sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/src")
RELEASE = Path("/home/struktured/projects/dr-mario-mods/mesen2/bin/linux-x64/Release")
from mesen_interface_file import MesenInterface
from drmario.faithful_game import FaithfulBoard, Pill, ORIENT_H, ORIENT_V
from drmario.planner import GreedyPlanner

# P1 addresses
BOARD = 0x0400
CAP_X, CAP_Y, CAP_ROT = 0x0305, 0x0306, 0x00A5
CAP_L, CAP_R = 0x0301, 0x0302
NEXT_L, NEXT_R = 0x031A, 0x031B
MODE = 0x0046
# NES rotation ($00A5): 0=horiz(a-left), 1=vert, 2=horiz flipped, 3=vert flipped
# faithful variant: 0=H(a,b) 1=H(b,a) 2=V(a-top) 3=V(b-top)
VARIANT_TO_ROT = {0: 0, 1: 2, 2: 3, 3: 1}


def nes_color(b):
    if b == 0xFF or b == 0x00:
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
        r, c = divmod(i, 8)
        col, vir = nes_color(byte)
        b.color[r, c] = col
        b.is_virus[r, c] = vir
    return b


def main():
    it = MesenInterface(work_dir=RELEASE)
    if not it.connect(timeout=8):
        print("no bridge"); return
    rd = lambda a: it.read_memory(a, 1)[0]
    planner = GreedyPlanner(depth=2)
    print("driving P1 with depth-2 planner. Ctrl-C to stop.")
    last_target = None
    last_y = -1
    pills = 0
    try:
        for step in range(4000):
            x, y, rot = rd(CAP_X), rd(CAP_Y), rd(CAP_ROT)
            la, ra = rd(CAP_L), rd(CAP_R)
            board = read_board(it)
            vleft = board.virus_count()
            # new pill detected: Y reset to a low row
            if y <= 2 and last_y > 2:
                cur = Pill((la & 0x0F) + 1, (ra & 0x0F) + 1)
                nxt = Pill((rd(NEXT_L) & 0x0F) + 1, (rd(NEXT_R) & 0x0F) + 1)
                a = planner.choose(board, cur, nxt)
                if a is not None:
                    last_target = (a // 8, a % 8)  # (variant, col)
                    pills += 1
                    print(f"pill#{pills} y={y} cur={la},{ra} -> variant{last_target[0]} col{last_target[1]} | viruses_left={vleft}", flush=True)
            # drive toward target
            btns = []
            if last_target is not None:
                tvar, tcol = last_target
                trot = VARIANT_TO_ROT[tvar]
                if rot != trot:
                    btns = ["a"]            # rotate toward target orientation
                elif x > tcol:
                    btns = ["left"]
                elif x < tcol:
                    btns = ["right"]
                else:
                    btns = ["down"]         # aligned -> drop
            it.set_input(0, btns)
            it.step_frame(2)
            it.set_input(0, [])
            it.step_frame(1)
            last_y = y
            if vleft == 0:
                print("*** board cleared! ***", flush=True); break
    except KeyboardInterrupt:
        pass
    finally:
        it.set_input(0, [])
        it.disconnect()
    print(f"done. pills placed={pills}")


if __name__ == "__main__":
    main()
