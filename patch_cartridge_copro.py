#!/usr/bin/env python3
"""Build drmario_copro.nes — the COPROCESSOR cartridge for the custom MiSTer NES core
(mapper 100 = MMC1 + Dr.Mario coprocessor at $5000-$51FF), with AUTO-NAV: the cart boots
itself into a VS-CPU L11 match and re-arms after every match. No controller needed (built
for a MiSTer whose physical controls are broken; also makes it a self-running demo).

How: the v28cs blob head at $FB00 (reached from the 0x37CF controller hook EVERY frame,
all modes) is repointed to the $FF54 trampoline, which bank-switches to unit-1 and runs
`main` each frame:
  menu modes  -> autonav state machine injecting P1 presses into $F5 (SELECT,SELECT,START,
                 LEFT x15, RIGHT x11, START) so the hack's own menu toggle sets VS-CPU
                 state properly; mirrors $F5->$F6 when $04=1 (P2 level cursor).
  intro (8)   -> hands off (no stray START).
  play (4)    -> the copro driver: on new pill upload board+colors to the FPGA window,
                 GO, hold pill while DONE=0, then publish best move to $DD/$DA and act.
The heavy depth-2 search runs on the SECOND 6502 inside the FPGA (~0.2-0.3s/pill vs 78s).
NOT Mesen-compatible (mapper 100) — MiSTer custom core only.
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
BLOB_FILE = 0x7B10                       # CPU $FB00
PRG_REG = 0xFFF0
ARMED = 0x6143             # PRG-RAM: !=0 searching (hold), ==0 act
NAV_T, NAV_MAGIC = 0x6147, 0x6149   # autonav frame counter + PRG-RAM power-on magic
GRAV = 0x0392
# copro window (mapper 100)
W_BOARD, W_CA, W_GO, W_DONE, W_COL, W_OR = 0x5000, 0x5080, 0x5084, 0x5085 - 1, 0x5085, 0x5086
# NES pad bits on $F5 (pressed-this-frame): A=$80 B=$40 Sel=$20 Start=$10 U=$08 D=$04 L=$02 R=$01
B_SEL, B_START, B_LEFT, B_RIGHT = 0x20, 0x10, 0x02, 0x01


def build_main():
    a = Asm6502(UNIT1_CPU)

    # ================= per-frame entry =================
    a.label("main")
    # PRG-RAM power-on init (SDRAM boots as garbage): magic byte at NAV_MAGIC
    a.ins16("LDA_abs", NAV_MAGIC); a.ins("CMP_imm", 0xA5); a.br("BEQ", "inited")
    a.ins("LDA_imm", 0xA5); a.ins16("STA_abs", NAV_MAGIC)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", ARMED); a.ins16("STA_abs", NAV_T)
    a.label("inited")
    a.ins16("LDA_abs", 0x0046); a.ins("CMP_imm", 0x04); a.br("BNE", "not_play")
    a.ins("LDA_zp", 0x04); a.br("BNE", "go_ai"); a.ins("RTS")
    a.label("go_ai"); a.jmp("dispatch")
    a.label("not_play")
    a.ins("CMP_imm", 0x08); a.br("BNE", "menus")
    a.ins("RTS")                                            # intro/init: hands off
    a.label("menus")
    a.jsr("autonav")
    a.ins("LDA_zp", 0x04); a.br("BEQ", "m_done")
    a.ins("LDA_zp", 0xF5); a.ins("STA_zp", 0xF6)            # VS: mirror P1->P2 (level cursor)
    a.label("m_done"); a.ins("RTS")

    # ============ autonav: direct state + $F5-only START injection (ZERO input) ============
    # SELECT-equivalent: JSR $FF30 (hack's own toggle; touches only $0727/$04/$06F1) until
    # $04==1. Levels: force $0316/$0396/$96=11 in mode 1. STARTs: inject $F5=$10 in a press
    # window. KEY: inject $F5 ONLY -- the read routine ANDs two raw passes (hook fires in
    # both, value survives) then computes newly-pressed = raw & ~held($F7); writing $F7 too
    # marks the button already-held and zeroes the edge (the original injection bug).
    # Window (NAV_T & $1F) < 4: pressed ~1 frame in ~6 (hook ~5 calls/frame), then released.
    def inject(bits):
        a.ins("LDA_imm", bits); a.ins("STA_zp", 0xF5)
        a.ins16("STA_abs", 0x6148)                          # DBG: last injected
        a.ins16("INC_abs", 0x614B)                          # DBG: inject count
    a.label("autonav")
    a.ins16("INC_abs", NAV_T)
    a.ins16("LDA_abs", 0x0046)
    a.ins("CMP_imm", 0x00); a.br("BEQ", "an_title")
    a.ins("CMP_imm", 0x01); a.br("BEQ", "an_lvl")
    a.ins("CMP_imm", 0x07); a.br("BEQ", "an_start")         # post-match: START -> rematch
    a.ins("RTS")
    a.label("an_title")
    a.ins("LDA_zp", 0x04); a.br("BEQ", "an_tog")
    a.jmp("an_start")                                       # VS armed -> START off the title
    a.label("an_tog")
    a.ins16("LDA_abs", NAV_T); a.ins("AND_imm", 0x1F); a.ins("CMP_imm", 1); a.br("BEQ", "an_tog_go")
    a.ins("RTS")
    a.label("an_tog_go")
    a.jsr(0xFF30)                                           # hack's toggle: 1P->2P->VS-CPU
    a.ins("RTS")
    a.label("an_lvl")
    a.ins("LDA_imm", 11)
    a.ins16("STA_abs", 0x0316)                              # P1 level
    a.ins16("STA_abs", 0x0396)                              # P2 level (+$80 struct offset)
    a.ins("STA_zp", 0x96)                                   # live cursor (cosmetic)
    a.label("an_start")
    a.ins16("LDA_abs", NAV_T); a.ins("AND_imm", 0x1F); a.ins("CMP_imm", 4); a.br("BCC", "an_st_go")
    a.ins("RTS")
    a.label("an_st_go")
    inject(B_START)
    a.ins("RTS")

    # ================= play-mode copro driver =================
    a.label("dispatch")
    a.ins16("LDA_abs", 0x0386); a.ins("CMP_zp", 0xDF)       # new-pill edge (same as d2 cart)
    a.br("BCC", "no_new"); a.br("BEQ", "no_new")
    a.ins("LDX_imm", 0)                                     # upload board $0500-7F -> $5000-7F
    a.label("cp")
    a.ins16("LDA_absX", 0x0500); a.ins16("STA_absX", W_BOARD)
    a.ins("INX"); a.ins("CPX_imm", 128); a.br("BNE", "cp")
    for src, dst in [(0x0381, W_CA), (0x0382, W_CA + 1), (0x039A, W_CA + 2), (0x039B, W_CA + 3)]:
        a.ins16("LDA_abs", src); a.ins("AND_imm", 0x0F); a.ins16("STA_abs", dst)
    a.ins16("STA_abs", W_GO)                                # GO (value irrelevant)
    a.ins("LDA_imm", 1); a.ins16("STA_abs", ARMED)
    a.label("no_new")
    a.ins16("LDA_abs", 0x0386); a.ins("STA_zp", 0xDF)       # $DF = P2y (edge memory)
    a.ins16("LDA_abs", ARMED); a.br("BNE", "chk")
    a.jmp("act")                                            # idle: keep steering to target
    a.label("chk")
    a.ins16("LDA_abs", W_DONE); a.br("BNE", "pub")
    # searching: hold (freeze gravity + clear P2 input)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", GRAV)
    a.ins("STA_zp", 0xF6); a.ins("STA_zp", 0xF8); a.ins("RTS")
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
    # ---- act: rotate $03A5 toward $DA (A edge), move toward $DD, drop when aligned ----
    a.label("act")
    a.ins16("LDA_abs", 0x03A5); a.ins("CMP_zp", 0xDA); a.br("BEQ", "mv")
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", 0xF8)
    a.ins("LDA_imm", 0x80); a.ins("STA_zp", 0xF6); a.ins("RTS")
    a.label("mv")
    a.ins16("LDA_abs", 0x0385); a.ins("CMP_zp", 0xDD); a.br("BEQ", "dn")
    a.ins("LDY_imm", 0x01); a.br("BCC", "st")
    a.ins("LDY_imm", 0x02); a.jmp("st")
    a.label("dn"); a.ins("LDY_imm", 0x04)
    a.label("st"); a.ins("STY_zp", 0xF6); a.ins("RTS")
    return a.assemble(), a.labels


def _sel(w, value):
    w.ins("LDA_imm", value)
    for i in range(5):
        w.ins("STA_abs", PRG_REG & 0xFF, (PRG_REG >> 8) & 0xFF)
        if i < 4:
            w.ins("LSR_A")


def build_wrapper(main_cpu):
    """Trampoline (every frame, all modes): bank2 -> JSR main -> bank0 -> RTS."""
    w = Asm6502(WRAP_CPU)
    _sel(w, 2)
    w.jsr(main_cpu)
    _sel(w, 0)
    w.ins("RTS")
    return w.assemble()


def main():
    unit1, labels = build_main()
    main_cpu = UNIT1_CPU + labels["main"]
    print(f"unit-1 main: {len(unit1)} B at ${UNIT1_CPU:04X}; main=${main_cpu:04X}")
    bank = bytearray(b"\x00" * 0x4000)
    bank[0:len(unit1)] = unit1

    wrap = build_wrapper(main_cpu)
    print(f"trampoline: {len(wrap)} B at ${WRAP_CPU:04X}")
    assert WRAP_CPU + len(wrap) <= 0xFFD2, "wrapper overflows the dead-v17 window"

    rom = bytearray(open(V28CS, "rb").read())
    assert rom[4] == 2
    rom[WRAP_FILE:WRAP_FILE + len(wrap)] = wrap
    HOOK_FILE = 0x37CF
    assert rom[HOOK_FILE] == 0x4C and rom[HOOK_FILE + 1] == 0x00 and rom[HOOK_FILE + 2] == 0xFB, \
        "expected v28cs hook JMP $FB00 at 0x37CF"
    # blob head: STA $F6; LDA $04; BNE... -> STA $F6; JMP $FF54  (trampoline runs every frame)
    assert rom[BLOB_FILE:BLOB_FILE + 6] == bytes.fromhex("85f6a504d003"), \
        "unexpected v28cs blob head"
    rom[BLOB_FILE:BLOB_FILE + 5] = bytes([0x85, 0xF6, 0x4C, 0x54, 0xFF])
    print("blob head repointed: STA $F6; JMP $FF54 (every frame, all modes)")

    tmp = OUT + ".2bank"
    open(tmp, "wb").write(rom)
    expand(tmp, OUT, new_bank_bytes=bytes(bank))
    import os
    os.remove(tmp)
    out = bytearray(open(OUT, "rb").read())
    out[6] = (out[6] & 0x0F) | 0x40      # mapper 100 = 0x64
    out[7] = (out[7] & 0x0F) | 0x60
    open(OUT, "wb").write(out)
    print(f"wrote {OUT} (mapper 100, AUTO-NAV VS-CPU L11, FPGA coprocessor)")


if __name__ == "__main__":
    main()
