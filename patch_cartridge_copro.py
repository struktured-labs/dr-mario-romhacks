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
GRAV_P1, GRAV_P2 = 0x0312, 0x0392   # per-player gravity counters
# CPU-vs-CPU: FPGA coprocessor is time-shared between P1 and P2 (~0.3s per pill each);
# ARMED tracks in-flight search, WHICH is 1=serving P1, 2=serving P2, PEND_* records
# player i's pill has locked and needs a search, TGT_C/O_* are that player's target move.
WHICH  = 0x614D
PEND1  = 0x614E
PEND2  = 0x614F
TGT_C1 = 0x6150
TGT_O1 = 0x6151
TGT_C2 = 0x6152
TGT_O2 = 0x6153
LASTY1 = 0x6154
LASTY2 = 0x6155
# copro window (mapper 100)
W_BOARD, W_CA, W_GO, W_DONE, W_COL, W_OR = 0x5000, 0x5080, 0x5084, 0x5084, 0x5085, 0x5086
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

    # ================= play-mode CPU-vs-CPU driver (time-shared FPGA) =================
    a.label("dispatch")
    # ---- pill-lock edge detect (both players) ----
    a.ins16("LDA_abs", 0x0306); a.ins16("CMP_abs", LASTY1)
    a.br("BCC", "no_p1_new"); a.br("BEQ", "no_p1_new")
    a.ins("LDA_imm", 1); a.ins16("STA_abs", PEND1)
    a.label("no_p1_new")
    a.ins16("LDA_abs", 0x0306); a.ins16("STA_abs", LASTY1)
    a.ins16("LDA_abs", 0x0386); a.ins16("CMP_abs", LASTY2)
    a.br("BCC", "no_p2_new"); a.br("BEQ", "no_p2_new")
    a.ins("LDA_imm", 1); a.ins16("STA_abs", PEND2)
    a.label("no_p2_new")
    a.ins16("LDA_abs", 0x0386); a.ins16("STA_abs", LASTY2)

    # ---- FPGA search state machine ----
    a.ins16("LDA_abs", ARMED); a.br("BEQ", "d_start")       # nothing in flight -> maybe start one
    a.ins16("LDA_abs", W_DONE); a.br("BNE", "d_pub")        # got a result -> publish
    a.jmp("d_hold")                                          # still searching -> hold serving player

    a.label("d_pub")
    a.ins16("LDA_abs", W_COL)                                # store best col to WHICH's target
    a.ins16("LDX_abs", WHICH); a.ins("CPX_imm", 2); a.br("BEQ", "pub_c2")
    a.ins16("STA_abs", TGT_C1); a.jmp("pub_o")
    a.label("pub_c2"); a.ins16("STA_abs", TGT_C2)
    a.label("pub_o")
    a.ins16("LDA_abs", W_OR); a.ins("CMP_imm", 0xFF); a.br("BNE", "pub_map")
    a.ins("LDA_imm", 3); a.jmp("pub_st")                    # topout: col 3, orient 3
    a.label("pub_map")                                      # orient4 -> $03A5 {0:3,1:1,2:0,3:2}
    a.ins("CMP_imm", 0); a.br("BNE", "pm1"); a.ins("LDA_imm", 3); a.jmp("pub_st")
    a.label("pm1"); a.ins("CMP_imm", 1); a.br("BNE", "pm2"); a.ins("LDA_imm", 1); a.jmp("pub_st")
    a.label("pm2"); a.ins("CMP_imm", 2); a.br("BNE", "pm3"); a.ins("LDA_imm", 0); a.jmp("pub_st")
    a.label("pm3"); a.ins("LDA_imm", 2)
    a.label("pub_st")
    a.ins16("LDX_abs", WHICH); a.ins("CPX_imm", 2); a.br("BEQ", "pub_o2")
    a.ins16("STA_abs", TGT_O1); a.jmp("pub_done")
    a.label("pub_o2"); a.ins16("STA_abs", TGT_O2)
    a.label("pub_done")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", ARMED)
    a.jmp("d_start_now")                                    # immediately try to start the other

    a.label("d_hold")
    # freeze the served player's gravity + inputs (the other player keeps acting via `act`)
    a.ins16("LDA_abs", WHICH); a.ins("CMP_imm", 2); a.br("BEQ", "hold_p2")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", GRAV_P1)
    a.ins("STA_zp", 0xF5); a.ins("STA_zp", 0xF7); a.jmp("act")
    a.label("hold_p2")
    a.ins("LDA_imm", 0); a.ins16("STA_abs", GRAV_P2)
    a.ins("STA_zp", 0xF6); a.ins("STA_zp", 0xF8); a.jmp("act")

    a.label("d_start")
    a.label("d_start_now")
    # priority: whichever is pending (P2 first if both, matches prior demo behavior)
    a.ins16("LDA_abs", PEND2); a.br("BNE", "start_p2")
    a.ins16("LDA_abs", PEND1); a.br("BNE", "start_p1")
    a.jmp("act")

    a.label("start_p2")
    a.ins("LDX_imm", 0)
    a.label("cp2")
    a.ins16("LDA_absX", 0x0500); a.ins16("STA_absX", W_BOARD)
    a.ins("INX"); a.ins("CPX_imm", 128); a.br("BNE", "cp2")
    for src, dst in [(0x0381, W_CA), (0x0382, W_CA + 1), (0x039A, W_CA + 2), (0x039B, W_CA + 3)]:
        a.ins16("LDA_abs", src); a.ins("AND_imm", 0x0F); a.ins16("STA_abs", dst)
    a.ins16("STA_abs", W_GO)
    a.ins("LDA_imm", 2); a.ins16("STA_abs", WHICH)
    a.ins("LDA_imm", 1); a.ins16("STA_abs", ARMED)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", PEND2)
    a.jmp("act")

    a.label("start_p1")
    a.ins("LDX_imm", 0)
    a.label("cp1")
    a.ins16("LDA_absX", 0x0400); a.ins16("STA_absX", W_BOARD)
    a.ins("INX"); a.ins("CPX_imm", 128); a.br("BNE", "cp1")
    for src, dst in [(0x0301, W_CA), (0x0302, W_CA + 1), (0x031A, W_CA + 2), (0x031B, W_CA + 3)]:
        a.ins16("LDA_abs", src); a.ins("AND_imm", 0x0F); a.ins16("STA_abs", dst)
    a.ins16("STA_abs", W_GO)
    a.ins("LDA_imm", 1); a.ins16("STA_abs", WHICH)
    a.ins("LDA_imm", 1); a.ins16("STA_abs", ARMED)
    a.ins("LDA_imm", 0); a.ins16("STA_abs", PEND1)
    a.jmp("act")

    # ---- act: steer BOTH players toward their published targets ----
    a.label("act")
    # P2 first (only if we're not currently freezing it)
    a.ins16("LDA_abs", ARMED); a.br("BEQ", "act_p2")
    a.ins16("LDA_abs", WHICH); a.ins("CMP_imm", 2); a.br("BEQ", "act_p1")
    a.label("act_p2")
    a.ins16("LDA_abs", 0x03A5); a.ins16("CMP_abs", TGT_O2); a.br("BEQ", "mv_p2")
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", 0xF8)
    a.ins("LDA_imm", 0x80); a.ins("STA_zp", 0xF6); a.jmp("act_p1")
    a.label("mv_p2")
    a.ins16("LDA_abs", 0x0385); a.ins16("CMP_abs", TGT_C2); a.br("BEQ", "dn_p2")
    a.ins("LDY_imm", 0x01); a.br("BCC", "st_p2")
    a.ins("LDY_imm", 0x02); a.jmp("st_p2")
    a.label("dn_p2"); a.ins("LDY_imm", 0x04)
    a.label("st_p2"); a.ins("STY_zp", 0xF6)
    a.label("act_p1")
    # skip P1 acting if we're currently searching for P1
    a.ins16("LDA_abs", ARMED); a.br("BEQ", "act_p1_go")
    a.ins16("LDA_abs", WHICH); a.ins("CMP_imm", 1); a.br("BEQ", "act_done")
    a.label("act_p1_go")
    a.ins16("LDA_abs", 0x0325); a.ins16("CMP_abs", TGT_O1); a.br("BEQ", "mv_p1")
    a.ins("LDA_imm", 0x00); a.ins("STA_zp", 0xF7)
    a.ins("LDA_imm", 0x80); a.ins("STA_zp", 0xF5); a.jmp("act_done")
    a.label("mv_p1")
    a.ins16("LDA_abs", 0x0305); a.ins16("CMP_abs", TGT_C1); a.br("BEQ", "dn_p1")
    a.ins("LDY_imm", 0x01); a.br("BCC", "st_p1")
    a.ins("LDY_imm", 0x02); a.jmp("st_p1")
    a.label("dn_p1"); a.ins("LDY_imm", 0x04)
    a.label("st_p1"); a.ins("STY_zp", 0xF5)
    a.label("act_done")
    a.ins("RTS")
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
