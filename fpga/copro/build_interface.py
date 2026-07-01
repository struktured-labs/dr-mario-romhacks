#!/usr/bin/env python3
"""Task 2 assets: prove the HOST<->COPROCESSOR handshake (not a one-shot preloaded board).
Emits:
  firmware_rom.hex  -- the incremental-search ROM/stub/SQ/vector with the board region EMPTY
                       (the host must supply the board, exactly like the real mapper).
  hostdata.txt      -- N independent problems the sim host streams in: per line
                       "cA cB nA nB expCol expOrient <128 board bytes hex>".
The handshake modelled: mapper holds the coprocessor in reset, host writes board+colors into
shared RAM ($0500 board, $6124-27 colors) + clears DONE, then releases reset (= GO). Coprocessor
reboots -> arm -> search -> writes result + DONE. Host polls DONE, reads move. Re-runnable: each
new GO re-pulses reset, so one coprocessor services pill after pill.
"""
import sys, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tests")); sys.path.insert(0, ROOT)
import build_firmware_incr as BF
import primitives as P
import test_resumable_incr as R
import py65_harness as _ph
from py65_harness import Cpu
from test_depth2 import S_CA, S_CB, S_NA, S_NB, S_BEST_C, S_BEST_O, _rand_board
from test_resumable import ARMED

EMPTY = 0xFF


def machine_oracle(drop_setup, cases):
    """Run the SAME resumable-incremental machine in py65 for each case — the correct
    expectation for an interface test (isolates handshake bugs from the machine's known
    approximation vs decide_d2_4)."""
    R.DROP_SETUP = drop_setup
    code, labels = R.build_resumable_incr()
    _ph.HALT = 0x8000 + len(code) + 0x100
    cpu = Cpu(); cpu.load(0x8000, code)
    for i in range(17):
        cpu.mem[P.SQ_LO_ADDR + i] = (i * i) & 0xFF
        cpu.mem[P.SQ_HI_ADDR + i] = (i * i) >> 8
    arm = 0x8000 + labels["arm"]; step = 0x8000 + labels["step"]
    out = []
    for (b, cA, cB, nA, nB) in cases:
        cpu.set_board(b)
        for ad, v in [(S_CA, cA), (S_CB, cB), (S_NA, nA), (S_NB, nB)]:
            cpu.mem[ad] = v
        cpu.call(arm)
        n = 0
        while cpu.mem[ARMED] != 0 and n < 400000:
            cpu.call(step, max_steps=400000); n += 1
        out.append((cpu.mem[S_BEST_C], cpu.mem[S_BEST_O]))
    return out


def main():
    drop = bool(int(sys.argv[1])) if len(sys.argv) > 1 else 0
    ncases = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    # ROM image with an EMPTY board (host provides the real one at runtime)
    img, clen, slen = BF.build_image([EMPTY] * 128, 0, 0, 0, 0, drop)
    for i in range(128):
        img[0x0500 + i] = EMPTY
    with open(os.path.join(HERE, "firmware_rom.hex"), "w") as f:
        f.write("\n".join("%02x" % x for x in img) + "\n")
    # host problems; expectations from the SAME machine in py65 (see machine_oracle)
    rng = random.Random(2026)
    cases = []
    for _ in range(ncases):
        b = _rand_board(rng); cA, cB, nA, nB = (rng.randint(0, 2) for _ in range(4))
        cases.append((b, cA, cB, nA, nB))
    expects = machine_oracle(drop, cases)
    lines = []
    for (b, cA, cB, nA, nB), (gc, go) in zip(cases, expects):
        lines.append("%d %d %d %d %d %d %s" % (cA, cB, nA, nB, gc, go,
                                               " ".join("%02x" % (x & 0xFF) for x in b)))
    with open(os.path.join(HERE, "hostdata.txt"), "w") as f:
        f.write(("%d\n" % ncases) + "\n".join(lines) + "\n")
    print("firmware_rom.hex (board EMPTY) + hostdata.txt (%d cases, drop_setup=%d). "
          "board->$0500, colors->$%04X.., DONE=$61FF, result $6134/$6135" % (ncases, drop, S_CA))


if __name__ == "__main__":
    main()
