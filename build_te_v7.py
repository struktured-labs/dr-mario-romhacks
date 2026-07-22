#!/usr/bin/env python3
"""Reproducible title-branded build of Dr. Mario Training Edition.

The build applies the public v5 IPS from ROMhacking.net to a clean USA ROM,
then adds a ``TRAINING EDITION`` subtitle and ``V7.00 STRUK LABS`` title footer.

  usage: build_te_v7.py [rom_out=tmp/drmario_te_v7.nes] [bps_out=release/drmario_te_v7.bps]
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "tests")

from make_bps import apply_bps, make_bps
from title_screen import (
    FOOTER_HOOK_OFFSET,
    FOOTER_HOOK_PATCHED,
    TITLE_BOTTOM_BASE_TILE_IDS,
    TITLE_TILEMAP_OFFSET,
    apply_training_edition_title,
)

BASE = "drmario.nes"
BASE_MD5 = "d3ec44424b5ac1a4dc77709829f721c9"
PUBLIC_V5_IPS = "release/drmario_training_v5.ips"
PUBLIC_V5_MD5 = "ce4d7319d66a5bbf3d2e942201a2347e"
rom_out = sys.argv[1] if len(sys.argv) > 1 else "tmp/drmario_te_v7.nes"
bps_out = sys.argv[2] if len(sys.argv) > 2 else "release/drmario_te_v7.bps"

src = open(BASE, "rb").read()
assert hashlib.md5(src).hexdigest() == BASE_MD5, f"{BASE} is not the expected clean USA ROM"
os.makedirs(os.path.dirname(rom_out) or ".", exist_ok=True)

def apply_ips(source, patch):
    """Apply a standard IPS patch and return the patched bytes."""
    if patch[:5] != b"PATCH":
        raise ValueError("invalid IPS header")
    out = bytearray(source)
    cursor = 5
    while patch[cursor:cursor + 3] != b"EOF":
        offset = int.from_bytes(patch[cursor:cursor + 3], "big")
        size = int.from_bytes(patch[cursor + 3:cursor + 5], "big")
        cursor += 5
        if size:
            data = patch[cursor:cursor + size]
            cursor += size
        else:
            run_size = int.from_bytes(patch[cursor:cursor + 2], "big")
            data = bytes((patch[cursor + 2],)) * run_size
            cursor += 3
        if offset + len(data) > len(out):
            out.extend(bytes(offset + len(data) - len(out)))
        out[offset:offset + len(data)] = data
    return out


# 1) Exact public v5 Training Edition patch from ROMhacking.net entry 9292.
d = apply_ips(src, open(PUBLIC_V5_IPS, "rb").read())
assert hashlib.md5(d).hexdigest() == PUBLIC_V5_MD5, "public v5 baseline mismatch"

# 2) Title branding only.
title_tiles = apply_training_edition_title(d)
open(rom_out, "wb").write(d)
tgt = bytes(d)

assert tgt[TITLE_TILEMAP_OFFSET:TITLE_TILEMAP_OFFSET + 10] == bytes(TITLE_BOTTOM_BASE_TILE_IDS)
assert tgt[FOOTER_HOOK_OFFSET:FOOTER_HOOK_OFFSET + 3] == FOOTER_HOOK_PATCHED

# 3) Release patch, verified by applying it back to the clean base.
patch = make_bps(src, tgt)
assert apply_bps(patch, src) == tgt, "BPS self-verify failed"
os.makedirs(os.path.dirname(bps_out) or ".", exist_ok=True)
open(bps_out, "wb").write(patch)

print(
    f"\nTE title ROM -> {rom_out} ({len(tgt)} B, md5 {hashlib.md5(tgt).hexdigest()}, "
    f"public v5 + {title_tiles} title tiles)"
)
print(f"BPS patch -> {bps_out} ({len(patch)} B, verified: drmario.nes + patch == ROM)")
