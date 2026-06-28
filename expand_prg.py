#!/usr/bin/env python3
"""Expand a Dr. Mario (MMC1) ROM's PRG from 2 banks (32KB) to 4 banks (64KB),
WITHOUT changing how the game runs, so depth-2 search code can live in new space.

CRITICAL: this game runs MMC1 in **32KB PRG-switch mode** (reset writes control
reg = $10, PRG mode 0). The whole $8000-$FFFF is ONE 32KB unit selected by the
PRG-bank register (low bit ignored). So you canNOT insert a single 16KB bank in
the middle -- that splits the 32KB pair and the game breaks (boots to title but
input/nav dies; verified empirically).

Correct layout keeps the original 32KB pair intact as **unit 0** and appends our
code as **unit 1**, duplicating orig bank 1 so $C000-$FFFF (vectors/NMI/fixed AI
+ bank-switch trampoline) stays mapped in BOTH units:

  index 0: orig bank 0     unit 0 ($8000-$BFFF)  = original low half
  index 1: orig bank 1     unit 0 ($C000-$FFFF)  = original high half (vectors)
  index 2: NEW 16KB        unit 1 ($8000-$BFFF)  = our search code
  index 3: orig bank 1     unit 1 ($C000-$FFFF)  = SAME high half (vectors/NMI)

- Power-on (MMC1 default fixes last bank @ $C000): last = index 3 = orig bank 1
  -> reset vector $FF00 valid -> boots.
- Reset sets 32KB mode, PRG-bank=0 -> unit 0 = original 32KB -> game runs
  byte-for-byte as the unmodified ROM.
- $C000-$FFFF is orig bank 1 in BOTH units -> the high half (and any trampoline
  we add there) is always mapped, regardless of selected unit.
- To run our code: write PRG-bank-reg = 2 (serial to $E000/$FFF0) -> unit 1 ->
  $8000 = NEW. Switch back to 0 when done. The switch routine must live in the
  always-mapped $C000-$FFFF half (orig bank 1).
"""
import sys

BANK = 0x4000  # 16KB


def expand(in_path, out_path, new_bank_bytes=None):
    rom = bytearray(open(in_path, "rb").read())
    assert rom[:4] == b"NES\x1a", "not an iNES ROM"
    nprg = rom[4]
    nchr = rom[5]
    assert nprg == 2, f"expected 2 PRG banks, got {nprg}"
    prg = rom[16:16 + nprg * BANK]
    chr_ = rom[16 + nprg * BANK:]
    bank0 = prg[:BANK]
    bank1 = prg[BANK:2 * BANK]

    new_bank = bytearray(b"\xff" * BANK)
    if new_bank_bytes:
        new_bank[:len(new_bank_bytes)] = new_bank_bytes

    # unit 0 = [bank0, bank1] (original 32KB, untouched); unit 1 = [NEW, bank1]
    new_prg = bytes(bank0) + bytes(bank1) + bytes(new_bank) + bytes(bank1)
    assert len(new_prg) == 4 * BANK

    out = bytearray(rom[:16])
    out[4] = 4                      # 4 PRG banks now
    out += new_prg
    out += chr_                     # CHR unchanged
    open(out_path, "wb").write(out)
    print(f"wrote {out_path}: PRG {nprg}->4 banks ({len(new_prg)} B), "
          f"CHR {nchr} banks unchanged, total {len(out)} B")
    # sanity: original 32KB (unit 0) byte-identical; vectors present in high half
    assert new_prg[:2 * BANK] == bytes(prg), "unit 0 must equal the original 32KB"
    fixed = new_prg[BANK:2 * BANK]   # bank1 = high half
    rst = fixed[0x3FFC] | (fixed[0x3FFD] << 8)
    nmi = fixed[0x3FFA] | (fixed[0x3FFB] << 8)
    print(f"  unit 0 == original 32KB ✓ ; high-half vectors RESET=${rst:04X} NMI=${nmi:04X}")
    return out_path


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "drmario.nes"
    outp = sys.argv[2] if len(sys.argv) > 2 else "tmp/drmario_exp.nes"
    import os
    os.makedirs(os.path.dirname(outp) or ".", exist_ok=True)
    expand(inp, outp)
