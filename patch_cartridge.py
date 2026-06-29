#!/usr/bin/env python3
"""Build the depth-1-search cartridge AI (drmario_cart.nes).

Layout (all pieces validated/measured separately; see ROM_WIRING_PLAN.md + memory):
  - PRG unit-1 ($8000-$BFFF): the cap=1 working-copy SLICER (arm/slice/eval/kernel/
    primitives, ~1.2KB), BOARD=$0100 (WORK), MARK=$0180, driver RAM $0190-$0199,
    reads LIVE settled board $0500. Validated 400/400 vs golden_capped.
  - FIXED bank ($C000-$FFFF, always mapped): sel_unit1/sel_unit0 MMC1 serial-write
    helpers at $D2CC; the NEW wrapper at $FF54 (replaces v28cs's rotation wrapper).
  - The v28cs blob ($FB00) plumbing + its `JMP $FF54` stay; the new wrapper is the
    target. Bank-switch is safe because it happens entirely inside the NMI hook
    (no nested NMI) -- validated by the $D2CC bank-test.

Start ROM: drmario_v28cs.nes (2-bank). Output: drmario_cart.nes (4-bank).
"""
import sys
sys.path.insert(0, "tests")
import primitives
# ROM working-copy config: WORK board $0100, bit-packed mark $0180 (LIVE stays $0500)
primitives.BOARD = 0x0600
primitives.MARK = 0x068C
import importlib, test_slicer
importlib.reload(test_slicer)
from patch_vs_cpu import Asm6502
from expand_prg import expand

V28CS = "drmario_v28cs.nes"
OUT = "drmario_cart.nes"
UNIT1_CPU = 0x8000          # slicer lives here in unit-1
SEL_CPU = 0xD2CC            # sel_unit1/sel_unit0 (fixed bank, 52B free run)
WRAP_CPU = 0xFF54           # new wrapper (fixed bank, dead-v17 window ~126B)
WRAP_FILE = 0x4010 + (WRAP_CPU - 0xC000)
SEL_FILE = 0x4010 + (SEL_CPU - 0xC000)
PRG_REG = 0xFFF0            # MMC1 PRG-bank register
# slicer RAM interface
ST_MODE, SE_PCA, SE_PCB = 0x01C0, 0x01C7, 0x01C8
GRAV = 0x0392              # P2 gravity drop-counter (pin to freeze)


def _sel(a, value):
    """Emit an INLINE MMC1 5-bit serial write of `value` to PRG_REG (LSB first).
    Matches the VALIDATED banktest trampoline exactly (inline, not a subroutine)."""
    a.ins("LDA_imm", value)
    for i in range(5):
        a.ins("STA_abs", PRG_REG & 0xFF, (PRG_REG >> 8) & 0xFF)
        if i < 4: a.ins("LSR_A")


def build_trampoline(dispatch_cpu):
    """ONE bank-switch per frame (inline sel, like the validated banktest):
    select unit-1 -> JSR dispatch (unit-1 does edge+arm+slice) -> select unit-0 ->
    RTS. Lives in the fixed bank at $D2CC."""
    a = Asm6502(SEL_CPU)
    a.label("tramp")
    _sel(a, 2)                  # -> unit-1
    a.jsr(dispatch_cpu)         # edge-check + arm + slice (all in unit-1)
    _sel(a, 0)                  # -> unit-0
    a.ins("RTS")
    return a.assemble(), SEL_CPU + a.labels["tramp"]


def build_wrapper(dispatch_cpu):
    """SELF-CONTAINED hook routine at $FF54, reached DIRECTLY from the controller
    hook (0x37CF re-pointed here, exactly like the validated banktest -- NOT via the
    v28cs blob, which path broke the bank-switch). Does: VS-CPU/play gate, INLINE
    bank-switch around dispatch (edge+arm+slice in unit-1), $DF update, then the
    ST_MODE gate (hold+freeze gravity until DONE, else rotate->$DA / move->$DD)."""
    w = Asm6502(WRAP_CPU)
    # --- gate: only run in VS-CPU ($04!=0) play mode ($46==4) (replicates the blob) ---
    w.ins("LDA_abs", 0x46, 0x00); w.ins("CMP_imm", 0x04); w.br("BNE", "nw_skip")
    w.ins("LDA_zp", 0x04); w.br("BEQ", "nw_skip")
    # --- bank-switch (INLINE sel, like the banktest) around dispatch ---
    _sel(w, 2)                          # -> unit-1
    w.jsr(dispatch_cpu)                 # edge + arm + slice (all in unit-1)
    _sel(w, 0)                          # -> unit-0
    # --- update last-y AFTER dispatch (dispatch read the old $DF for its edge) ---
    w.ins("LDA_abs", 0x86, 0x03); w.ins("STA_zp", 0xDF)
    # --- ST_MODE gate: hold (freeze gravity + clear input) until DONE ---
    w.ins16("LDA_abs", ST_MODE); w.ins("CMP_imm", 0x02); w.br("BEQ", "nw_act")
    w.ins("LDA_imm", 0x00); w.ins16("STA_abs", GRAV)          # pin P2 gravity counter = 0
    w.ins("STA_zp", 0xF6); w.ins("STA_zp", 0xF8)              # clear move/rotate + prev (no drop)
    w.label("nw_skip")
    w.ins("RTS")
    w.label("nw_act")
    # --- rotate to the chosen orientation $DA (edge-triggered A=CCW) ---
    w.ins("LDA_abs", 0xA5, 0x03); w.ins("CMP_zp", 0xDA); w.br("BEQ", "nw_mv")
    w.ins("LDA_imm", 0x00); w.ins("STA_zp", 0xF8)
    w.ins("LDA_imm", 0x80); w.ins("STA_zp", 0xF6); w.ins("RTS")
    # --- move toward target column $DD, drop when aligned ---
    w.label("nw_mv")
    w.ins("LDA_abs", 0x85, 0x03); w.ins("CMP_zp", 0xDD); w.br("BEQ", "nw_dn")
    w.ins("LDY_imm", 0x01); w.br("BCC", "nw_st")
    w.ins("LDY_imm", 0x02); w.jmp("nw_st")
    w.label("nw_dn"); w.ins("LDY_imm", 0x04)
    w.label("nw_st"); w.ins("STY_zp", 0xF6); w.ins("RTS")
    return w.assemble()


def main():
    # 1) slicer for unit-1 ($8000), working-copy + cap=1
    slicer, labels = test_slicer.build_slicer(wc=True, base=UNIT1_CPU)
    dispatch_cpu = UNIT1_CPU + labels["dispatch"]
    print(f"slicer: {len(slicer)} B at unit-1 ${UNIT1_CPU:04X}; dispatch=${dispatch_cpu:04X}")
    assert len(slicer) <= 0x4000, "slicer overflows the 16KB unit-1 bank"

    # 2) self-contained hook routine (fixed bank, INLINE sel, reached DIRECTLY from
    #    the controller hook like the validated banktest)
    wrap = build_wrapper(dispatch_cpu)
    print(f"hook routine: {len(wrap)} B at ${WRAP_CPU:04X}")
    assert WRAP_CPU + len(wrap) <= 0xFFD2, "hook routine overflows the dead-v17 window"

    # 3) patch the 2-bank v28cs ROM, then expand to 4 banks with the slicer in unit-1
    rom = bytearray(open(V28CS, "rb").read())
    assert rom[4] == 2
    rom[WRAP_FILE:WRAP_FILE + len(wrap)] = wrap
    # RE-POINT the controller hook (0x37CF) DIRECTLY to $FF54 (was -> $FB00 blob)
    HOOK_FILE = 0x37CF
    assert rom[HOOK_FILE] == 0x4C, "hook is not a JMP"
    rom[HOOK_FILE + 1] = WRAP_CPU & 0xFF
    rom[HOOK_FILE + 2] = (WRAP_CPU >> 8) & 0xFF
    print(f"hook 0x{HOOK_FILE:04X}: JMP ${WRAP_CPU:04X} (direct, bypassing blob)")
    tmp = OUT + ".2bank"; open(tmp, "wb").write(rom)
    expand(tmp, OUT, new_bank_bytes=slicer)
    import os; os.remove(tmp)
    print(f"wrote {OUT} (4-bank cartridge AI)")


if __name__ == "__main__":
    main()
