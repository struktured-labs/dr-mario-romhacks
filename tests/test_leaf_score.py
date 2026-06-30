#!/usr/bin/env python3
"""Validate the consolidated 6502 `leaf_score` (shape+buried+readiness+setup+
combine -> EV_WIN + EV_SCO 16-bit) cell-exact vs the Python golden."""
import sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import primitives
primitives.BOARD = 0x0500
from py65_harness import Cpu
from patch_vs_cpu import Asm6502
from test_eval_terms import g_buried, g_readiness, g_setup, rand_board
from test_shape_eval import golden_shape

BASE = 0x4000


def golden_leaf(b):
    if not any(t != 0xFF and (t & 0xF0) == 0xD0 for t in b):
        return 1, 0                      # virus-free -> WIN
    mh, ho, tr = golden_shape(b)
    s = 5000 - 12*mh - 25*ho - 45*tr + 40*g_setup(b) - 30*g_buried(b) + 4*g_readiness(b)
    return 0, s & 0xFFFF


def main():
    a = Asm6502(BASE)
    primitives.emit_shape(a)
    primitives.emit_eval(a)
    code = a.assemble()
    cpu = Cpu(); cpu.load(BASE, code)
    for i in range(17):
        cpu.mem[primitives.SQ_LO_ADDR + i] = (i*i) & 0xFF
        cpu.mem[primitives.SQ_HI_ADDR + i] = (i*i) >> 8
    addr = BASE + a.labels["leaf_score"]
    rng = random.Random(123)
    fails = 0; n = 500; cmax = 0
    for t in range(n):
        b = rand_board(rng)
        cpu.set_board(b)
        c = cpu.call(addr); cmax = max(cmax, c)
        win = cpu.mem[primitives.EV_WIN]
        sco = cpu.mem[primitives.EV_SCO_LO] | (cpu.mem[primitives.EV_SCO_HI] << 8)
        ew, es = golden_leaf(b)
        if (win, sco) != (ew, es):
            fails += 1
            if fails <= 5:
                print(f"  MISMATCH t={t}: got=({win},{sco}) exp=({ew},{es})")
    print(f"leaf_score: {n-fails}/{n} match  size={len(code)}B  cyc_max={cmax}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
