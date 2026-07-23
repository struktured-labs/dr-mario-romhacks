#!/usr/bin/env python3
"""Ground-truth byte-overlap: which community patches collide with OUR TE footprint.

Feed the built TE ROM (.nes) + the community IPS patches. Each target is reduced to the
SET of base-file offsets it changes; we then intersect TE's set with each community set
and print the exact colliding runs (file offset, CPU addr, base bytes).
"""
import os, sys

BASE = os.environ.get("DRMARIO_BASE", "/home/struktured/projects/dr-mario-mods/drmario.nes")
base = bytearray(open(BASE, "rb").read())

def apply_ips(src, patch):
    out = bytearray(src); p = 5
    while patch[p:p+3] != b"EOF":
        off = int.from_bytes(patch[p:p+3], "big"); size = int.from_bytes(patch[p+3:p+5], "big"); p += 5
        if size:
            data = patch[p:p+size]; p += size
        else:
            rle = int.from_bytes(patch[p:p+2], "big"); data = bytes((patch[p+2],))*rle; p += 3
        if off+len(data) > len(out): out.extend(b"\x00"*(off+len(data)-len(out)))
        out[off:off+len(data)] = data
    return out

def changed_offsets(target):
    if target.endswith(".ips"):
        patched = apply_ips(base, open(target, "rb").read())
    else:
        patched = bytearray(open(target, "rb").read())
    s = set()
    for i in range(min(len(base), len(patched))):
        if base[i] != patched[i]:
            s.add(i)
    for i in range(len(base), len(patched)):  # appended
        s.add(i)
    return s

def cpu(off):
    if off < 0x10: return "hdr"
    if off < 0x8010:
        prg = off-0x10
        return f"${0x8000+prg:04X}" if prg < 0x4000 else f"${0xC000+prg-0x4000:04X}"
    if off < 0x10010: return "CHR"
    return "APPEND"

def runs(offs):
    out=[]; offs=sorted(offs); i=0
    while i < len(offs):
        j=i
        while j+1 < len(offs) and offs[j+1]==offs[j]+1: j+=1
        out.append((offs[i], offs[j]-offs[i]+1)); i=j+1
    return out

te = sys.argv[1]
te_set = changed_offsets(te)
print(f"TE ({os.path.basename(te)}): {len(te_set)} changed bytes, {len(runs(te_set))} runs")
print("TE runs:", [f"0x{o:04X}/{cpu(o)}({l})" for o,l in runs(te_set)])
print()
for patch in sys.argv[2:]:
    cs = changed_offsets(patch)
    inter = te_set & cs
    tag = "*** COLLISION ***" if inter else "clean"
    print(f"{os.path.basename(patch):16s} {len(cs):6d} changed  |  TE∩ = {len(inter)}  {tag}")
    for o,l in runs(inter):
        print(f"      collide 0x{o:05X} {cpu(o)} len {l}  base={bytes(base[o:o+min(l,12)]).hex()}")
