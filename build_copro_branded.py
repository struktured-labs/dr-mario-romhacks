#!/usr/bin/env python3
"""Compose a BRANDED copro cart the direct way: v28cs -> TE v8 branding -> driver -> expand.

This bakes the branding into the 32 KB v28cs core BEFORE the coprocessor driver runs, so the
driver's `expand()` duplicates the branded high half into index 3 for free.  It produces the same
bytes as post-processing a finished cart with brand_copro_cart.py (proven by --verify).

Run FROM the canonical driver worktree (its patch_cartridge_copro.py is picked up via cwd); point
TE_DIR at this te-v8 worktree for title_screen.  Driver flags are the usual env vars (DRHUMAN,
DRPOCKET, DRNOFREEZE, DRLEVEL, ...), read by the driver at import.

  usage: TE_DIR=~/projects/dr-mario-te-v8 [DRHUMAN=1 DRPOCKET=1] \
             python $TE_DIR/build_copro_branded.py <clean_v28cs.nes> <cart_out.nes>
"""
import os, sys

TE_DIR = os.environ.get("TE_DIR", os.path.dirname(os.path.abspath(__file__)))
# Order matters: the CANONICAL driver (cwd) must win for patch_cartridge_copro; te-v8 only
# supplies title_screen (the canonical worktree has no title_screen.py).
sys.path.insert(0, TE_DIR)           # te-v8 title_screen (parameterized)
sys.path.insert(0, os.getcwd())      # canonical patch_cartridge_copro (run from its worktree) -> FIRST

from title_screen import apply_training_edition_title

V28CS_CLEAN = sys.argv[1]
CART_OUT    = sys.argv[2]
V8_ROUTINE_OFF, V8_DATA_OFF, V8_FOOTER_TEXT = 0x40B9, 0x40FF, "V8.00 SL"

# 1) brand the clean 32 KB core (title_screen's default CHR_START is correct for 32 KB PRG)
core = bytearray(open(V28CS_CLEAN, "rb").read())
assert core[4] == 2, "expected a clean 32 KB-PRG v28cs core"
apply_training_edition_title(core, routine_off=V8_ROUTINE_OFF, data_off=V8_DATA_OFF, footer_text=V8_FOOTER_TEXT)
os.makedirs("tmp", exist_ok=True)
branded_core = "tmp/_v28cs_te_core.nes"
open(branded_core, "wb").write(core)

# 2) run the canonical driver on the BRANDED core (adds AI/study/wrapper, then expand()s)
import patch_cartridge_copro as drv     # from cwd = canonical worktree
drv.V28CS = branded_core
drv.OUT = CART_OUT
drv.main()

print(f"\nbranded copro cart -> {CART_OUT}  (v28cs -> TE v8 branding -> driver -> expand)")
