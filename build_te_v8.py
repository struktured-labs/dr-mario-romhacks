#!/usr/bin/env python3
"""Reproducible build of Dr. Mario Training Edition v8 = v6 study + v7 branding, unified.

v8 supersedes both prior public builds:
  * v6 (release/drmario_te_v6.bps): VS-CPU AI + the DRSTUDY v3.3 study-pause apparatus
    (frozen capsules, "STUDY" text, BOTH next-pill previews, 2P/VS STUDY lift).
  * v7 (release/drmario_te_v7.bps): "TRAINING EDITION" title subtitle + a title footer.

The two lineages collide: v7's footer routine ($BE56) and metasprite table ($9FF8) are
exactly DRSTUDY v3.3's part3b / part2 dead runs.  v8 keeps the study intact and RELOCATES
the footer into free fixed-bank runs ($C0A9 routine, $CF00 metasprite), and bumps the
footer text to "V8.00 STRUK LABS".

Pipeline:
  clean drmario.nes
  + patch_vs_cpu.apply_patches        -> internal v6 (VS-CPU AI + STUDY apparatus, CHR A0-A2)
  + apply_study_pause (v3.3)          -> 5-part study chain (part1 $D2CC .. part3c $BC26)
  + apply_training_edition_title(...)  -> subtitle + relocated "V8.00 STRUK LABS" footer

Outputs the ROM (gitignored) and the release BPS patch against clean drmario.nes.

  usage: build_te_v8.py [rom_out=tmp/drmario_te_v8.nes] [bps_out=release/drmario_te_v8.bps]
"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "tests")
import patch_vs_cpu
from patch_cartridge_copro import (apply_study_pause,
                                   STUDY_BLOB, STUDY_BLOB_CPU,
                                   STUDY_BLOB2, STUDY_BLOB2_CPU,
                                   STUDY_BLOB4, STUDY_BLOB4_CPU)
from title_screen import (apply_training_edition_title, footer_routine, footer_hook_patched,
                          footer_metasprite, footer_layout, _tile_offset,
                          FOOTER_HOOK_OFFSET, TITLE_TILEMAP_OFFSET, TITLE_BOTTOM_BASE_TILE_IDS,
                          TITLE_CHR_PAGES, TM_TILE_ID, TE_E_HALF)
from make_bps import make_bps, apply_bps

BASE = "drmario.nes"
BASE_MD5 = "d3ec44424b5ac1a4dc77709829f721c9"

# TE v8 footer relocation.  The v7 footer sat on DRSTUDY's part2 ($9FF8, file 0x2008) and
# part3b ($BE56, file 0x3E66).  v8 is the byte-basis for the copro carts, so BOTH the routine
# and its metasprite must land in runs free-and-identical in base v6, v28cs AND the copro carts.
# The only such runs are 24 bytes, so the footer credit is shortened to "V8.00 SL" -> a 4-tile,
# 17-byte metasprite (see footer_layout); routine (23 B) and table (17 B) each take a common run:
V8_ROUTINE_OFF = 0x40B9   # CPU $C0A9  (24-byte run free in base v6 + v28cs + copro)
V8_DATA_OFF    = 0x40FF   # CPU $C0EF  (24-byte run free in base v6 + v28cs + copro)
V8_FOOTER_TEXT = "V8.00 SL"

rom_out = sys.argv[1] if len(sys.argv) > 1 else "tmp/drmario_te_v8.nes"
bps_out = sys.argv[2] if len(sys.argv) > 2 else "release/drmario_te_v8.bps"

src = open(BASE, "rb").read()
assert hashlib.md5(src).hexdigest() == BASE_MD5, f"{BASE} is not the expected clean USA ROM"
os.makedirs(os.path.dirname(rom_out) or ".", exist_ok=True)

# 1) internal v6 (VS-CPU + STUDY apparatus)
patch_vs_cpu.apply_patches(BASE, rom_out)
# 2) v3.3 study-pause (freeze + reconnect STUDY + both previews)
d = bytearray(open(rom_out, "rb").read())
n_study = apply_study_pause(d)
# 3) title branding: relocated footer + "™"->"TE" mark (Training Edition)
tiles_written = apply_training_edition_title(
    d, routine_off=V8_ROUTINE_OFF, data_off=V8_DATA_OFF, footer_text=V8_FOOTER_TEXT, mark_te=True)
open(rom_out, "wb").write(d)
tgt = bytes(d)

v8_n_tiles, v8_base_x = footer_layout(V8_FOOTER_TEXT)
exp_routine = footer_routine(V8_DATA_OFF, v8_base_x)
exp_meta = footer_metasprite(v8_n_tiles)

# --- self-verify: study intact (incl. the two ex-collision runs), footer relocated, subtitle intact ---
for blob, cpu, name in [(STUDY_BLOB,  STUDY_BLOB_CPU,  "part1 $D2CC"),
                        (STUDY_BLOB2, STUDY_BLOB2_CPU, "part2 $9FF8 (ex-footer-data)"),
                        (STUDY_BLOB4, STUDY_BLOB4_CPU, "part3b $BE56 (ex-footer-routine)")]:
    off = 16 + (cpu - 0x8000)
    assert tgt[off:off + len(blob)] == blob, f"DRSTUDY {name} clobbered by branding"
assert tgt[FOOTER_HOOK_OFFSET:FOOTER_HOOK_OFFSET + 3] == footer_hook_patched(V8_ROUTINE_OFF), \
    "title hook not repointed to $C0A9"
assert tgt[V8_ROUTINE_OFF:V8_ROUTINE_OFF + len(exp_routine)] == exp_routine, "footer routine not at $C0A9"
assert tgt[V8_DATA_OFF:V8_DATA_OFF + len(exp_meta)] == exp_meta, "footer metasprite not at $C0EF"
assert len(exp_meta) <= 24, "footer metasprite must fit a 24-byte common run for the cart basis"
for page in TITLE_CHR_PAGES:                                    # "™" -> "TE" on both title CHR pages
    off = _tile_offset(page, TM_TILE_ID)
    assert tgt[off:off + 16] == TE_E_HALF, f"TM->TE mark not applied on CHR page {page}"
assert tgt[TITLE_TILEMAP_OFFSET:TITLE_TILEMAP_OFFSET + 10] == bytes(TITLE_BOTTOM_BASE_TILE_IDS), \
    "crash-sensitive title tilemap disturbed"

# 4) release BPS (self-verifying)
patch = make_bps(src, tgt)
assert apply_bps(patch, src) == tgt, "BPS self-verify failed"
os.makedirs(os.path.dirname(bps_out) or ".", exist_ok=True)
open(bps_out, "wb").write(patch)

print(f"\nTE v8 ROM -> {rom_out} ({len(tgt)} B, md5 {hashlib.md5(tgt).hexdigest()})")
print(f"  study edits {n_study}, title tiles {tiles_written}; footer routine $C0A9 / "
      f"data $C0EF ({len(exp_meta)}B) / text {V8_FOOTER_TEXT!r}")
print(f"  study runs part2 $9FF8 + part3b $BE56 intact (footer no longer collides)")
print(f"BPS patch -> {bps_out} ({len(patch)} B, verified: drmario.nes + patch == ROM)")
