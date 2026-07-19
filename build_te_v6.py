#!/usr/bin/env python3
"""Reproducible build of the public Dr. Mario Training Edition v6 re-release.

  clean drmario.nes
  + patch_vs_cpu.apply_patches   -> internal v6 = VS-CPU AI (P2) + STUDY apparatus
                                    (bg-on, OAM-keep, Y-pos top, STUDY quads, CHR tiles 0xA0-0xA2)
  + apply_study_pause (v3)       -> study-pause freeze + the $D2CC blob that reconnects the STUDY
                                    text (slots 2-6) AND draws the next-pill preview (slots 7-8),
                                    sparing the frozen falling capsule (slots 0-1).

Outputs the ROM (gitignored) and the release BPS patch against clean drmario.nes.

  usage: build_te_v6.py [rom_out=tmp/drmario_te_v6.nes] [bps_out=release/drmario_te_v6.bps]
"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "tests")
import patch_vs_cpu
from patch_cartridge_copro import apply_study_pause, STUDY_BLOB, STUDY_BLOB_CPU
from make_bps import make_bps, apply_bps

BASE = "drmario.nes"
BASE_MD5 = "d3ec44424b5ac1a4dc77709829f721c9"
rom_out = sys.argv[1] if len(sys.argv) > 1 else "tmp/drmario_te_v6.nes"
bps_out = sys.argv[2] if len(sys.argv) > 2 else "release/drmario_te_v6.bps"

src = open(BASE, "rb").read()
assert hashlib.md5(src).hexdigest() == BASE_MD5, f"{BASE} is not the expected clean USA ROM"
os.makedirs(os.path.dirname(rom_out) or ".", exist_ok=True)

# 1) internal v6 (VS-CPU + STUDY apparatus)
patch_vs_cpu.apply_patches(BASE, rom_out)
# 2) v3 study-pause (freeze + reconnect STUDY + preview)
d = bytearray(open(rom_out, "rb").read())
n = apply_study_pause(d)
open(rom_out, "wb").write(d)
tgt = bytes(d)

bf = 16 + (STUDY_BLOB_CPU - 0x8000)
assert tgt[bf:bf + len(STUDY_BLOB)] == STUDY_BLOB, "v3 blob not present at $D2CC"

# 3) release BPS (self-verifying)
patch = make_bps(src, tgt)
assert apply_bps(patch, src) == tgt, "BPS self-verify failed"
os.makedirs(os.path.dirname(bps_out) or ".", exist_ok=True)
open(bps_out, "wb").write(patch)

print(f"\nTE v6 ROM -> {rom_out} ({len(tgt)} B, md5 {hashlib.md5(tgt).hexdigest()}, study edits {n})")
print(f"BPS patch -> {bps_out} ({len(patch)} B, verified: drmario.nes + patch == ROM)")
