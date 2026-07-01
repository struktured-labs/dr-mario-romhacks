#!/usr/bin/env python3
"""Coprocessor firmware for the INCREMENTAL depth-2 search (base-once + delta-per-leaf),
driven to completion on a bare 6502. Same memory map as build_firmware.py, but the stub runs
the resumable machine atomically:  JSR arm ; loop { JSR step } while ARMED!=0 ; DONE=1.
Usage: build_firmware_incr.py [seed] [dropsetup 0|1]
"""
import sys, os, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tests")); sys.path.insert(0, ROOT)
import primitives as P
import patch_vs_cpu
from patch_vs_cpu import Asm6502
patch_vs_cpu.OPS.setdefault("CLD", 0xD8)
patch_vs_cpu.OPS.setdefault("TXS", 0x9A)
import test_resumable_incr as R
from test_depth2 import (S_CA, S_CB, S_NA, S_NB, S_BEST_C, S_BEST_O, CUR, WORK1, LIVE,
                         decide_d2_4, _rand_board)
from test_resumable import ARMED

SQ_LO_ROM, SQ_HI_ROM = 0xB000, 0xB011
STUB = 0xC000
DONE = 0x61FF


def build_image(board, cA, cB, nA, nB, drop_setup):
    R.DROP_SETUP = drop_setup
    code, labels = R.build_resumable_incr(base=0x8000, cur=CUR, work1=WORK1, live=LIVE,
                                          mark=0x0780, sq_lo=SQ_LO_ROM, sq_hi=SQ_HI_ROM)
    arm_ep = 0x8000 + labels["arm"]
    step_ep = 0x8000 + labels["step"]

    s = Asm6502(STUB)
    s.ins("CLD"); s.ins("LDX_imm", 0xFF); s.ins("TXS")
    s.jsr(arm_ep)
    s.label("loop")
    s.jsr(step_ep)
    s.ins16("LDA_abs", ARMED); s.br("BNE", "loop")          # while ARMED != 0
    s.ins("LDA_imm", 1); s.ins16("STA_abs", DONE)
    s.label("spin"); s.jmp("spin")
    stub = s.assemble()

    img = bytearray(0x10000)
    img[0x8000:0x8000 + len(code)] = code
    for i in range(17):
        img[SQ_LO_ROM + i] = (i * i) & 0xFF
        img[SQ_HI_ROM + i] = (i * i) >> 8
    img[STUB:STUB + len(stub)] = stub
    for i, b in enumerate(board):
        img[LIVE + i] = b & 0xFF
    img[S_CA] = cA; img[S_CB] = cB; img[S_NA] = nA; img[S_NB] = nB
    img[DONE] = 0
    img[0xFFFC] = STUB & 0xFF; img[0xFFFD] = (STUB >> 8) & 0xFF
    return img, len(code), len(stub)


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 321
    drop = bool(int(sys.argv[2])) if len(sys.argv) > 2 else False
    rng = random.Random(seed)
    b = _rand_board(rng); cA, cB, nA, nB = (rng.randint(0, 2) for _ in range(4))
    img, clen, slen = build_image(b, cA, cB, nA, nB, drop)
    gc, go = decide_d2_4(b, cA, cB, nA, nB)
    out = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(out, "firmware.hex"), "w") as f:
        f.write("\n".join("%02x" % x for x in img) + "\n")
    with open(os.path.join(out, "expected.txt"), "w") as f:
        f.write("seed %d drop_setup %d\ncode_bytes %d stub_bytes %d\n"
                "EXPECT_oracle best_col=%d best_orient=%d  (drop_setup differs from oracle by design)\n"
                "DONE_ADDR=0x%04X RESULT_C=0x%04X RESULT_O=0x%04X\n"
                % (seed, drop, clen, slen, gc, go, DONE, S_BEST_C, S_BEST_O))
    print("incr firmware: code=%dB stub=%dB drop_setup=%d oracle=(%d,%d) DONE=0x%04X"
          % (clen, slen, drop, gc, go, DONE))


if __name__ == "__main__":
    main()
