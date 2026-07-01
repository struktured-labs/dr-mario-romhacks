#!/usr/bin/env python3
"""Assemble the depth-2 search as standalone coprocessor firmware for a bare 6502 (Arlet core
in sim; T65 in the MiSTer mapper / cart FPGA later). Memory map:
  $0000-$7FFF RAM  (board LIVE=$0500, search state $6120+, work boards; zp scratch/stack)
  $8000-$AFFF ROM  search code (build_search, base $8000)
  $B000       ROM  SQ_LO[17], $B011 SQ_HI[17]  (readiness square table)
  $C000       ROM  reset stub: init SP -> JSR search -> set DONE($6140)=1 -> spin
  $FFFC/D     reset vector -> $C000
The "host" (game CPU / testbench) preloads the board ($0500) + colors ($6124-$6127), releases
reset, waits for DONE, reads best_col($6134)/best_orient($6135). Emits firmware.hex ($readmemh,
one byte/line, 65536 lines) with a chosen test board preloaded, + expected.txt from the oracle.
"""
import sys, os, random
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # dr-mario-mods
sys.path.insert(0, os.path.join(ROOT, "tests")); sys.path.insert(0, ROOT)
import primitives as P
import patch_vs_cpu
from patch_vs_cpu import Asm6502
# minimal assembler lacks these implied-mode ops; register them (needed for a clean bare-metal reset)
patch_vs_cpu.OPS.setdefault("SEI", 0x78)
patch_vs_cpu.OPS.setdefault("CLD", 0xD8)
patch_vs_cpu.OPS.setdefault("TXS", 0x9A)
import test_depth2 as D2
from test_depth2 import S_CA, S_CB, S_NA, S_NB, S_BEST_C, S_BEST_O, decide_d2_4, _rand_board

SQ_LO_ROM, SQ_HI_ROM = 0xB000, 0xB011
STUB = 0xC000
DONE = 0x6140            # firmware sets =1 when the search has written the result


def build_image(board, cA, cB, nA, nB):
    P.SQ_LO_ADDR, P.SQ_HI_ADDR = SQ_LO_ROM, SQ_HI_ROM
    code, labels = D2.build_search(resolve="full")          # atomic depth-2, entry = "search"
    search_ep = 0x8000 + labels["search"]

    stub = Asm6502(STUB)
    stub.ins("SEI"); stub.ins("CLD")
    stub.ins("LDX_imm", 0xFF); stub.ins("TXS")
    stub.jsr(search_ep)
    stub.ins("LDA_imm", 1); stub.ins16("STA_abs", DONE)
    stub.label("spin"); stub.jmp("spin")
    stub_code = stub.assemble()

    img = bytearray(0x10000)
    img[0x8000:0x8000 + len(code)] = code
    for i in range(17):
        img[SQ_LO_ROM + i] = (i * i) & 0xFF
        img[SQ_HI_ROM + i] = (i * i) >> 8
    img[STUB:STUB + len(stub_code)] = stub_code
    # preload the test problem into RAM
    for i, b in enumerate(board):
        img[0x0500 + i] = b & 0xFF
    img[S_CA] = cA; img[S_CB] = cB; img[S_NA] = nA; img[S_NB] = nB
    img[DONE] = 0
    img[0xFFFC] = STUB & 0xFF; img[0xFFFD] = (STUB >> 8) & 0xFF
    return img, len(code), len(stub_code)


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 321
    rng = random.Random(seed)
    b = _rand_board(rng); cA, cB, nA, nB = (rng.randint(0, 2) for _ in range(4))
    img, clen, slen = build_image(b, cA, cB, nA, nB)
    gc, go = decide_d2_4(b, cA, cB, nA, nB)

    outdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(outdir, "firmware.hex"), "w") as f:
        f.write("\n".join("%02x" % x for x in img) + "\n")
    with open(os.path.join(outdir, "expected.txt"), "w") as f:
        f.write("seed %d\nsearch_bytes %d stub_bytes %d\ncolors cA=%d cB=%d nA=%d nB=%d\n"
                "EXPECT best_col=%d best_orient=%d\nDONE_ADDR=0x%04X RESULT_C=0x%04X RESULT_O=0x%04X\n"
                % (seed, clen, slen, cA, cB, nA, nB, gc, go, DONE, S_BEST_C, S_BEST_O))
    print("firmware.hex written (64KB). search=%dB stub=%dB. oracle best=(col %d, orient %d)"
          % (clen, slen, gc, go))
    print("DONE=0x%04X result_col=0x%04X result_orient=0x%04X" % (DONE, S_BEST_C, S_BEST_O))


if __name__ == "__main__":
    main()
