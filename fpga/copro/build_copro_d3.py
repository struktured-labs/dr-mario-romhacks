#!/usr/bin/env python3
"""Build the DEPTH-3 copro firmware (the 91.7% config on hardware): ply1 top-8 +
ply2 top-8 + integer expectimax over 8 pills, TARGETED capped resolve, ext+pollute+vrdy
leaf, WIN=30000. Same host handshake as full-d2 (NO SV/driver changes):
  host -> board@$0500 (LIVE), colors@$6124-27; GO=reset pulse ($BF80); firmware searches,
  writes col@$6134 orient@$6135, DONE($61FF)=1; host polls DONE.
SQ tables are read straight from ROM @$B000 (copro RAM is only $0000-$0FFF + $6100-$61FF);
the stub copies the 8-pill table ROM $B030 -> RAM $09C0. Search logic byte-identical to
tests/test_search_d3.py (30/30 vs decide_d3). Emits copro_rom.hex ($8000-$BFFF slice) and
validates in py65: direct search call + full $BF80 reset->DONE flow vs decide_d3."""
import sys, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tests")); sys.path.insert(0, ROOT)
import patch_vs_cpu
patch_vs_cpu.OPS.setdefault("SEI", 0x78)
patch_vs_cpu.OPS.setdefault("TXS", 0x9A)
from patch_vs_cpu import Asm6502
from py65_harness import Cpu
import test_vrdy, test_readiness_ext
import test_search_d3 as D3
from test_search_d3 import (THIRD, PILLA, PILLB, D_BC, D_BO, make_fewlegal)
from test_depth2 import S_CA, S_CB, S_NA, S_NB, S_BEST_C, S_BEST_O
import primitives as P
import nes_d3_golden as G3

EMPTY = 0xFF
STUB = 0xBF80            # MiSTer mapper hardcodes the copro reset to $BF80 (in-ROM)
DONE = 0x61FF
SQ_ROM, PILL_ROM = 0xB000, 0xB030
MAX_STEPS = 3_000_000_000


def build_image(board, cA, cB, nA, nB):
    assert (D3.NPILLS, D3.SHIFT) == (8, 3), "deploy config is 8 pills / >>3"
    # copro RAM is ONLY $0000-$0FFF + $6100-$61FF (CoproDrMario.sv): the SQ tables must be
    # read straight from ROM @$B000 (there is no RAM at the py65 tests' $7A00 location).
    # test_vrdy/test_readiness_ext capture the addresses at import -> override those too.
    P.SQ_LO_ADDR, P.SQ_HI_ADDR = SQ_ROM, SQ_ROM + 17
    test_vrdy.SQ_LO, test_vrdy.SQ_HI = SQ_ROM, SQ_ROM + 17
    test_readiness_ext.SQ_LO, test_readiness_ext.SQ_HI = SQ_ROM, SQ_ROM + 17
    code, labels = D3.build()
    assert len(code) <= SQ_ROM - 0x8000, f"search overruns ROM tables ({len(code)}B)"
    search_ep = 0x8000 + labels["search"]

    stub = Asm6502(STUB)
    stub.ins("SEI"); stub.ins("CLD")
    stub.ins("LDX_imm", 0xFF); stub.ins("TXS")
    stub.ins("LDX_imm", 15)                     # PILLA[8]+PILLB[8] ROM -> $09C0 RAM
    stub.label("cp2")
    stub.ins16("LDA_absX", PILL_ROM); stub.ins16("STA_absX", PILLA)
    stub.ins("DEX"); stub.br("BPL", "cp2")
    stub.jsr(search_ep)
    stub.ins("LDA_zp", D_BC); stub.ins16("STA_abs", S_BEST_C)
    stub.ins("LDA_zp", D_BO); stub.ins16("STA_abs", S_BEST_O)
    stub.ins("LDA_imm", 1); stub.ins16("STA_abs", DONE)
    stub.label("spin"); stub.jmp("spin")
    stub_code = stub.assemble()
    assert STUB + len(stub_code) <= 0xC000, f"stub overruns ROM ({len(stub_code)}B)"

    img = bytearray(0x10000)
    img[0x8000:0x8000 + len(code)] = code
    for i in range(17):
        img[SQ_ROM + i] = (i * i) & 0xFF
        img[SQ_ROM + 17 + i] = (i * i) >> 8
    for i in range(8):
        img[PILL_ROM + i] = THIRD[i][0]
        img[PILL_ROM + 8 + i] = THIRD[i][1]
    img[STUB:STUB + len(stub_code)] = stub_code
    for i, b in enumerate(board):
        img[0x0500 + i] = b & 0xFF
    img[S_CA] = cA; img[S_CB] = cB; img[S_NA] = nA; img[S_NB] = nB
    img[DONE] = 0
    img[0xFFFC] = STUB & 0xFF; img[0xFFFD] = (STUB >> 8) & 0xFF   # py65 only; mapper hardcodes
    return img, len(code), len(stub_code)


def main():
    sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/src")
    sys.path.insert(0, "/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/tmp")
    from drmario.faithful_game import FaithfulBoard
    from xcheck_terms import faithful_to_nes

    img, clen, slen = build_image([EMPTY] * 128, 0, 0, 0, 0)
    for i in range(128):
        img[0x0500 + i] = EMPTY
    rom = img[0x8000:0xC000]
    with open(os.path.join(HERE, "copro_rom.hex"), "w") as f:
        f.write("\n".join("%02x" % x for x in rom) + "\n")
    print(f"copro_rom.hex written: d3 search={clen}B stub={slen}B rom={len(rom)}B "
          f"(topk1={D3.TOPK1} topk2=8 pills={D3.NPILLS} resolve={D3.RESOLVE_LBL} WIN={D3.WIN})")

    _code, labels = D3.build()
    search_ep = 0x8000 + labels["search"]
    rng = random.Random(2026)

    def problem():
        fb = make_fewlegal(rng, FaithfulBoard)
        ca, cb = rng.randint(1, 3), rng.randint(1, 3)
        na, nb_ = rng.randint(1, 3), rng.randint(1, 3)
        return list(faithful_to_nes(fb)), ca - 1, cb - 1, na - 1, nb_ - 1

    fails = 0

    # ---- (1) direct search-entry call vs decide_d3 ----
    b, cA, cB, nA, nB = problem()
    cpu = Cpu()
    for a, v in enumerate(img):
        cpu.mem[a] = v
    for i in range(16):                          # direct call skips the stub: load pill table
        cpu.mem[PILLA + i] = img[PILL_ROM + i]
    cpu.set_board(b)
    cpu.mem[S_CA] = cA; cpu.mem[S_CB] = cB; cpu.mem[S_NA] = nA; cpu.mem[S_NB] = nB
    cpu.call(search_ep, max_steps=MAX_STEPS)
    got = (cpu.mem[D_BC], cpu.mem[D_BO]) if cpu.mem[D_BO] != 0xFF else None
    exp = G3.decide_d3(b, cA, cB, nA, nB, topk1=D3.TOPK1, topk2=8, third=THIRD)
    ok = got == exp
    fails += 0 if ok else 1
    print(f"  direct-call: got={got} exp={exp}  {'OK' if ok else 'FAIL'}")

    # ---- (2) hardware path: reset @$BF80 -> stub copies tables -> search -> DONE ----
    b, cA, cB, nA, nB = problem()
    cpu2 = Cpu()
    for a, v in enumerate(img):
        cpu2.mem[a] = v
    cpu2.set_board(b)
    cpu2.mem[S_CA] = cA; cpu2.mem[S_CB] = cB; cpu2.mem[S_NA] = nA; cpu2.mem[S_NB] = nB
    cpu2.mem[DONE] = 0
    m = cpu2.mpu
    m.pc = STUB; m.sp = 0xFF
    steps = 0; reached = False
    while steps < MAX_STEPS:
        m.step(); steps += 1
        if cpu2.mem[DONE] == 1:
            reached = True; break
    got2 = (cpu2.mem[S_BEST_C], cpu2.mem[S_BEST_O])
    exp2 = G3.decide_d3(b, cA, cB, nA, nB, topk1=D3.TOPK1, topk2=8, third=THIRD)
    tables_ok = all(cpu2.mem[PILLA + i] == img[PILL_ROM + i] for i in range(16))
    ok2 = reached and tables_ok and exp2 is not None and got2 == exp2
    fails += 0 if ok2 else 1
    est = steps * 3 / 85_900_000
    print(f"  stub-flow: DONE={reached} tables={tables_ok} got={got2} exp={exp2} "
          f"steps={steps/1e6:.0f}M (~{est:.1f}s @85.9MHz)  {'OK' if ok2 else 'FAIL'}")

    print(f"build_copro_d3 validation: {'PASS' if not fails else 'FAIL'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
