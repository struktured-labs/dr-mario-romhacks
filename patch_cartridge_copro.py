#!/usr/bin/env python3
"""Build drmario_copro.nes — the COPROCESSOR cartridge for the custom MiSTer NES core
(mapper 100 = MMC1 + Dr.Mario coprocessor at $5000-$51FF).

Game side is tiny: per new pill, copy the P2 board ($0500-$057F) into the copro window
($5000-$507F), write colors ($5080-3), pulse GO ($5084), then hold the pill while DONE
($5084)==0; when DONE, read best_col($5085)/best_orient($5086), publish to $DD/$DA and act.
The heavy depth-2 search runs on the SECOND 6502 inside the FPGA (~0.2-0.5s/pill vs 78s).

Reuses the proven d2-cart infra verbatim: v28cs base (blob 0x37CF->$FB00 preserved: P2
leveling + play-mode JMP $FF54), $FF54 wrapper (gate + inline MMC1 bank-switch + JSR driver
+ ARMED hold/act), 2->4 bank expansion with the driver in unit-1 at $8000. Only differences:
the unit-1 payload is ~130B instead of 4.9KB, and the iNES header mapper becomes 100.
NOT Mesen-compatible (Mesen has no copro mapper) -- MiSTer custom core only.
"""
import sys
sys.path.insert(0, "tests")
from patch_vs_cpu import Asm6502
from expand_prg import expand

V28CS = "drmario_v28cs.nes"
OUT = "drmario_copro.nes"
UNIT1_CPU = 0x8000
WRAP_CPU = 0xFF54
WRAP_FILE = 0x4010 + (WRAP_CPU - 0xC000)
PRG_REG = 0xFFF0
ARMED = 0x6143             # PRG-RAM flag: !=0 searching (wrapper holds), ==0 act
GRAV = 0x0392
# copro window (mapper 100)
W_BOARD, W_CA, W_GO, W_DONE, W_COL, W_OR = 0x5000, 0x5080, 0x5084, 0x5084, 0x5085, 0x5086


def build_driver():
    """Unit-1 payload at $8000: per-NMI dispatch. Edge -> upload board+colors+GO, ARMED=1;
    while ARMED: poll DONE; when set -> publish $DD/$DA (orient map {0:3,1:1,2:0,3:2},
    $FF topout fallback col3/or3), ARMED=0."""
    a = Asm6502(UNIT1_CPU)
    a.label("dispatch")
    a.ins16("LDA_abs", 0x0386); a.ins("CMP_zp", 0xDF)      # new-pill edge (same as d2 cart)
    a.br("BCC", "no_new"); a.br("BEQ", "no_new")
    # upload board: $0500-$057F -> $5000-$507F
    a.ins("LDX_imm", 0)
    a.label("cp")
    a.ins16("LDA_absX", 0x0500); a.ins16("STA_absX", W_BOARD)
    a.ins("INX"); a.ins("CPX_imm", 128); a.br("BNE", "cp")
    # colors: current $0381/$0382, P2 next preview $039A/$039B (low nibbles)
    for src, dst in [(0x0381, W_CA), (0x0382, W_CA + 1), (0x039A, W_CA + 2), (0x039B, W_CA + 3)]:
        a.ins16("LDA_abs", src); a.ins("AND_imm", 0x0F); a.ins16("STA_abs", dst)
    a.ins16("STA_abs", W_GO)                               # GO (value irrelevant)
    a.ins("LDA_imm", 1); a.ins16("STA_abs", ARMED)
    a.label("no_new")
    a.ins16("LDA_abs", ARMED); a.br("BNE", "chk"); a.ins("RTS")
    a.label("chk")
    a.ins16("LDA_abs", W_DONE); a.br("BNE", "pub"); a.ins("RTS")   # still searching
    a.label("pub")
    a.ins16("LDA_abs", W_COL); a.ins("STA_zp", 0xDD)
    a.ins16("LDA_abs", W_OR); a.ins("CMP_imm", 0xFF); a.br("BNE", "map")
    a.ins("LDA_imm", 3); a.ins("STA_zp", 0xDD); a.ins("STA_zp", 0xDA); a.jmp("fin")
    a.label("map")                                          # orient4 -> $03A5 {0:3,1:1,2:0,3:2}
    a.ins("CMP_imm", 0); a.br("BNE", "m1"); a.ins("LDA_imm", 3); a.jmp("mst")
    a.label("m1"); a.ins("CMP_imm", 1); a.br("BNE", "m2"); a.ins("LDA_imm", 1); a.jmp("mst")
    a.label("m2"); a.ins("CMP_imm", 2); a.br("BNE", "m3"); a.ins("LDA_imm", 0); a.jmp("mst")
    a.label("m3"); a.ins("LDA_imm", 2)
    a.label("mst"); a.ins("STA_zp", 0xDA)
    a.label("fin"); a.ins("LDA_imm", 0); a.ins16("STA_abs", ARMED)
    a.ins("RTS")
    return a.assemble(), a.labels


def _sel(w, value):
    w.ins("LDA_imm", value)
    for i in range(5):
        w.ins("STA_abs", PRG_REG & 0xFF, (PRG_REG >> 8) & 0xFF)
        if i < 4:
            w.ins("LSR_A")


def build_wrapper(dispatch_cpu):
    """Identical shape to the proven d2 wrapper: gate -> bank2 -> JSR dispatch -> bank0 ->
    $DF=P2y -> ARMED? hold (freeze grav + clear input) : act (rotate $03A5->$DA, move->$DD)."""
    w = Asm6502(WRAP_CPU)
    w.ins("LDA_abs", 0x46, 0x00); w.ins("CMP_imm", 0x04); w.br("BNE", "nw_skip")
    w.ins("LDA_zp", 0x04); w.br("BEQ", "nw_skip")
    _sel(w, 2)
    w.jsr(dispatch_cpu)
    _sel(w, 0)
    w.ins("LDA_abs", 0x86, 0x03); w.ins("STA_zp", 0xDF)
    w.ins("LDA_abs", ARMED & 0xFF, (ARMED >> 8) & 0xFF); w.br("BEQ", "nw_act")
    w.ins("LDA_imm", 0x00); w.ins("STA_abs", GRAV & 0xFF, (GRAV >> 8) & 0xFF)
    w.ins("STA_zp", 0xF6); w.ins("STA_zp", 0xF8)
    w.label("nw_skip")
    w.ins("RTS")
    w.label("nw_act")
    w.ins("LDA_abs", 0xA5, 0x03); w.ins("CMP_zp", 0xDA); w.br("BEQ", "nw_mv")
    w.ins("LDA_imm", 0x00); w.ins("STA_zp", 0xF8)
    w.ins("LDA_imm", 0x80); w.ins("STA_zp", 0xF6); w.ins("RTS")
    w.label("nw_mv")
    w.ins("LDA_abs", 0x85, 0x03); w.ins("CMP_zp", 0xDD); w.br("BEQ", "nw_dn")
    w.ins("LDY_imm", 0x01); w.br("BCC", "nw_st")
    w.ins("LDY_imm", 0x02); w.jmp("nw_st")
    w.label("nw_dn"); w.ins("LDY_imm", 0x04)
    w.label("nw_st"); w.ins("STY_zp", 0xF6); w.ins("RTS")
    return w.assemble()


def main():
    driver, labels = build_driver()
    dispatch_cpu = UNIT1_CPU + labels["dispatch"]
    print(f"driver: {len(driver)} B at ${UNIT1_CPU:04X}; dispatch=${dispatch_cpu:04X}")
    bank = bytearray(b"\x00" * 0x4000)
    bank[0:len(driver)] = driver

    wrap = build_wrapper(dispatch_cpu)
    print(f"wrapper: {len(wrap)} B at ${WRAP_CPU:04X}")
    assert WRAP_CPU + len(wrap) <= 0xFFD2, "wrapper overflows the dead-v17 window"

    rom = bytearray(open(V28CS, "rb").read())
    assert rom[4] == 2
    rom[WRAP_FILE:WRAP_FILE + len(wrap)] = wrap
    HOOK_FILE = 0x37CF
    assert rom[HOOK_FILE] == 0x4C and rom[HOOK_FILE + 1] == 0x00 and rom[HOOK_FILE + 2] == 0xFB, \
        "expected v28cs hook JMP $FB00 at 0x37CF"
    tmp = OUT + ".2bank"
    open(tmp, "wb").write(rom)
    expand(tmp, OUT, new_bank_bytes=bytes(bank))
    import os
    os.remove(tmp)
    # set iNES mapper = 100 (0x64): byte6[7:4]=4, byte7[7:4]=6
    out = bytearray(open(OUT, "rb").read())
    out[6] = (out[6] & 0x0F) | 0x40
    out[7] = (out[7] & 0x0F) | 0x60
    open(OUT, "wb").write(out)
    print(f"wrote {OUT} (mapper 100 = MMC1 + FPGA coprocessor; MiSTer custom core only)")


if __name__ == "__main__":
    main()
