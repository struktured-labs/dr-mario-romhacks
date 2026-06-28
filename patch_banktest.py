#!/usr/bin/env python3
"""Bank-switch trampoline smoke test. Proves we can round-trip into the new
PRG unit (unit 1) from the per-frame AI hook and back, WITHOUT disturbing the
running game, before dropping in the real search.

Plan (built on drmario_v28cs.nes, which still plays L11 ~4 clears):
  - NEW bank (unit 1, $8000): a trivial routine that bumps a RAM counter+sentinel.
  - Trampoline in the ALWAYS-MAPPED high half (orig bank1, $FF30): switch PRG-bank
    reg -> 2 (unit 1, serial write to $FFF0), JSR $8000 (new-bank routine), switch
    back -> 0 (unit 0), then JMP $FB00 (continue into the intact v28cs AI).
  - Re-point the AI hook (file 0x37CF) from `JMP $FB00` to `JMP $FF30` (trampoline).

Expected on Mesen: game still navigates + clears ~4 (round-trip is safe) AND
$0780 (counter) is nonzero / $0781 == $42 (the unit-1 routine executed).
"""
import sys
from patch_vs_cpu import Asm6502
from expand_prg import expand, BANK

V28CS = "drmario_v28cs.nes"
OUT = "drmario_banktest.nes"
TRAMPO_CPU = 0xD2CC          # 52 B free in orig bank1 (high half), always mapped
HOOK_FILE = 0x37CF           # AI controller hook (bank0): currently JMP $FB00
PRG_REG = 0xFFF0             # MMC1 PRG-bank register (any addr in $E000-$FFFF)
CTR, SENT = 0x0780, 0x0781   # RAM counter + sentinel the new-bank routine writes


def build_trampoline():
    """Returns (code, entry_cpu). Compact: a shared 5-bit serial-write sub (A=value
    -> PRG_REG) called twice, so the whole thing fits the 36 B free gap before the
    v28cs wrapper at $FF54."""
    a = Asm6502(TRAMPO_CPU)
    a.label("swsub")                         # A = bank value -> MMC1 PRG-bank reg
    for i in range(5):
        a.ins("STA_abs", PRG_REG & 0xFF, (PRG_REG >> 8) & 0xFF)
        if i < 4:
            a.ins("LSR_A")
    a.ins("RTS")
    a.label("tramp")
    # PRESERVE A/X/Y: the AI hook enters $FB00 with the merged controller byte in
    # A (blob does STA $F6). The bank-switch clobbers A -> must save/restore.
    a.ins("PHA"); a.ins("TXA"); a.ins("PHA"); a.ins("TYA"); a.ins("PHA")
    a.ins("LDA_imm", 2); a.jsr("swsub")      # -> unit 1 ($8000 = NEW bank)
    a.jsr(0x8000)                            # run new-bank routine
    a.ins("LDA_imm", 0); a.jsr("swsub")      # -> unit 0 (restore bank0)
    a.ins("PLA"); a.ins("TAY"); a.ins("PLA"); a.ins("TAX"); a.ins("PLA")
    a.jmp(0xFB00)                            # continue into the intact v28cs AI
    code = a.assemble()
    entry = TRAMPO_CPU + a.labels["tramp"]
    return code, entry


def build_newbank_routine():
    # Canonical artifact = NO-OP round-trip (proves the bank-switch is safe).
    #
    # Free-RAM hunt results (Mesen, new-bank routine gated on mode==4, fill $AA,
    # then check L11 still clears ~4 without crashing):
    #   $0700-$07FF : NOT free  - read by AI during play (clearing broke, 0 cleared)
    #   $0580-$05FF : NOT free  - crashed (mode 255) after a few clears
    #   $0100-$017F : FREE      - cleared 4 normally, clean exit (low stack; the
    #                             game only uses ~17 B of stack, stays above $01EF)
    # => use $0100-$017F for the search's board buffer; bit-pack the mark to 16 B.
    a = Asm6502(0x8000)
    a.ins("RTS")
    return a.assemble()


def main():
    rom = bytearray(open(V28CS, "rb").read())
    assert rom[4] == 2, "expected 2 PRG banks"

    # 1) trampoline into bank1's high half (file 0x4010 + (CPU-$C000))
    tramp, entry = build_trampoline()
    assert TRAMPO_CPU + len(tramp) <= 0xD300, \
        f"trampoline ({len(tramp)} B) overruns the free region at $D300"
    toff = 0x4010 + (TRAMPO_CPU - 0xC000)
    rom[toff:toff + len(tramp)] = tramp
    print(f"trampoline @ ${TRAMPO_CPU:04X} (file 0x{toff:04X}, {len(tramp)} B), "
          f"entry ${entry:04X}")

    # 2) re-point the AI hook to the trampoline entry
    assert rom[HOOK_FILE] == 0x4C, "hook is not a JMP"
    rom[HOOK_FILE + 1] = entry & 0xFF
    rom[HOOK_FILE + 2] = (entry >> 8) & 0xFF
    print(f"hook 0x{HOOK_FILE:04X}: JMP ${entry:04X} (was $FB00)")

    # 3) write the patched 2-bank ROM, then expand with the new-bank routine
    tmp = OUT + ".2bank"
    open(tmp, "wb").write(rom)
    newrt = build_newbank_routine()
    expand(tmp, OUT, new_bank_bytes=newrt)
    import os; os.remove(tmp)
    print(f"new-bank routine: {len(newrt)} B at unit1 $8000; wrote {OUT}")


if __name__ == "__main__":
    main()
