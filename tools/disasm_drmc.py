#!/usr/bin/env python3
"""Disassemble the DrMC hook sites + new-code blocks to locate seed-select, seed
storage, SPD render, and the ULT speed tier. Applies the IPS to the clean base first."""
import os, sys
# Needs the repo-root disasm_6502.py (its OPCODES table). Run from the repo root, or set
# DRMARIO_REPO. Importing it also opens ./drmario.nes, so cwd must contain a copy.
sys.path.insert(0, os.environ.get("DRMARIO_REPO", os.path.expanduser("~/projects/dr-mario-mods")))
from disasm_6502 import OPCODES

BASE = os.environ.get("DRMARIO_BASE", "/home/struktured/projects/dr-mario-mods/drmario.nes")
base = bytearray(open(BASE, "rb").read())

def apply_ips(src, patch):
    out = bytearray(src); p = 5
    while patch[p:p+3] != b"EOF":
        off = int.from_bytes(patch[p:p+3], "big"); size = int.from_bytes(patch[p+3:p+5], "big"); p += 5
        if size: data = patch[p:p+size]; p += size
        else:
            rle = int.from_bytes(patch[p:p+2], "big"); data = bytes((patch[p+2],))*rle; p += 3
        if off+len(data) > len(out): out.extend(b"\x00"*(off+len(data)-len(out)))
        out[off:off+len(data)] = data
    return out

rom = apply_ips(base, open(sys.argv[1], "rb").read())

# Known RAM / register labels for operand annotation.
LBL = {
    0x0089:"rngSeed", 0x008A:"rngSeed+1", 0x0065:"optCursor", 0x0046:"mode",
    0x00F5:"p1_btnPressed", 0x00F7:"p1_btnHeld", 0x0731:"musicType", 0x0727:"numPlayers",
    0x030A:"p1_speedUps", 0x030B:"p1_speedSetting", 0x0312:"p1_speedCounter",
    0x0320:"p1_speedIndex", 0x0324:"p1_virusLeft", 0x031A:"p1_nextPill1", 0x031B:"p1_nextPill2",
    0x0316:"p1_level", 0x0200:"OAM", 0x2006:"PPUADDR", 0x2007:"PPUDATA", 0x2001:"PPUMASK",
    0xA795:"gravityTable", 0x0720:"UNK720", 0x0722:"UNK722",
}
def cpu_of(off):
    prg=off-0x10; return 0x8000+prg if prg<0x4000 else 0xC000+prg-0x4000
def off_of(cpu):
    return (cpu-0x8000 if cpu<0xC000 else cpu-0xC000+0x4000)+0x10

def dis(cpu_start, length, title):
    print(f"\n----- {title}  (CPU ${cpu_start:04X}) -----")
    off = off_of(cpu_start); end = off+length; pc = cpu_start
    while off < end:
        op = rom[off]
        if op not in OPCODES:
            print(f"  ${pc:04X}: .db ${op:02X}"); off+=1; pc+=1; continue
        mn, ln, mode = OPCODES[op]
        ops = rom[off:off+ln]
        txt = mn
        if ln == 2:
            v = rom[off+1]
            if mode == "imm": txt += f" #${v:02X}"
            elif mode == "rel":
                tgt = pc+2 + (v-256 if v>127 else v); txt += f" ${tgt:04X}"
            else:
                lab = LBL.get(v, ""); txt += f" ${v:02X}"+(f"({lab})" if lab else "")+("," + mode[-1].upper() if mode.endswith(("x","y")) and mode!="imm" else "")
        elif ln == 3:
            v = rom[off+1] | (rom[off+2]<<8); lab = LBL.get(v, "")
            suf = ",X" if mode.endswith("x") else (",Y" if mode.endswith("y") else "")
            txt += f" ${v:04X}"+(f"({lab})" if lab else "")+suf
        print(f"  ${pc:04X}: {ops.hex():10s} {txt}")
        off += ln; pc += ln

# Hook sites (what the game now calls)
dis(0x80B4, 0x1A, "hook: music/speed-cursor store repurpose")
dis(0x8D87, 0x12, "hook: gravity-table read -> SPD")
dis(0x9A39, 0x10, "hook: pill/RNG path")
dis(0x9AA8, 0x06, "hook: music LDX -> JMP $FB90")
# New-code blocks in the fixed-bank tail
dis(0xFB00, 0x60, "newcode $FB00 (RNG/seed core)")
dis(0xFB60, 0x40, "newcode $FB60")
dis(0xFC00, 0x40, "newcode $FC00")
dis(0xFC60, 0x5D, "newcode $FC60 (called from gravity hook = SPD render)")
dis(0xFF40, 0x40, "newcode $FF40")
dis(0xFF80, 0x30, "newcode $FF80 (called from $8F38)")
