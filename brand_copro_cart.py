#!/usr/bin/env python3
"""Overlay the TE v8 title branding onto a FINISHED mapper-100 copro cart (driver-agnostic).

The branding is cart-side (rendered by the ROM's own title code) and byte-disjoint from the
depth-2 AI, the DRSTUDY chain and the coprocessor driver, so it can be applied as a pure overlay
to any built cart — the current slam-maturity carts, combo-port's freeze-fixed Pocket cart, or a
future DRNAVFIX cart. This script:

  1. asserts the branding runs are filler in the cart's unit0 (and its index-3 high-half copy),
  2. applies the IDENTICAL TE v8 branding used by build_te_v8.py ($C0A9 routine / $C0EF metasprite
     / "V8.00 SL"), with CHR_START adjusted for the cart's 64 KB PRG, and duplicates the high-half
     branding into index 3 (as `expand()` would have),
  3. proves the only bytes that changed are the branding bytes (=> study + driver are intact),
  4. proves every branding byte equals the public TE v8 ROM (=> the public BPS is the cart basis).

  usage: brand_copro_cart.py <cart_in.nes> <cart_out.nes> [base_v8=tmp/drmario_te_v8.nes]
"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import title_screen as ts
from title_screen import (apply_training_edition_title, footer_routine, footer_metasprite,
                          footer_layout, FOOTER_HOOK_OFFSET, FOOTER_CHR_PAGE, FOOTER_TILE_IDS,
                          TITLE_TOP_TILE_IDS, TITLE_CHR_PAGES, CHR_PAGE_SIZE)

# Identical relocation to build_te_v8.py.
V8_ROUTINE_OFF, V8_DATA_OFF, V8_FOOTER_TEXT = 0x40B9, 0x40FF, "V8.00 SL"
HIGH_DUP = 0x8000            # index1 (file 0x4010-0x800F) -> index3 (file 0xC010-0x1000F) delta

cart_in  = sys.argv[1]
cart_out = sys.argv[2]
base_v8  = sys.argv[3] if len(sys.argv) > 3 else "tmp/drmario_te_v8.nes"

before = bytearray(open(cart_in, "rb").read())
assert before[4] == 4 and len(before) == 98320, "expected a 64 KB-PRG (4-bank) mapper-100 copro cart"
n_tiles, base_x = footer_layout(V8_FOOTER_TEXT)
routine = footer_routine(V8_DATA_OFF, base_x)
meta    = footer_metasprite(n_tiles)

# 1) preconditions — branding runs must be filler in unit0 AND the index-3 duplicate
assert bytes(before[FOOTER_HOOK_OFFSET:FOOTER_HOOK_OFFSET + 3]) == b"\x20\xF6\x88", "hook not original (20 F6 88)"
for off in (V8_ROUTINE_OFF, V8_ROUTINE_OFF + HIGH_DUP):
    assert set(before[off:off + len(routine)]) <= {0x00, 0xFF}, f"routine run 0x{off:05X} not free"
for off in (V8_DATA_OFF, V8_DATA_OFF + HIGH_DUP):
    assert set(before[off:off + len(meta)]) <= {0x00, 0xFF}, f"metasprite run 0x{off:05X} not free"

# 2) apply the branding; title_screen uses CHR_START, so point it at the cart's 64 KB-PRG CHR
cart = bytearray(before)
CHR_BASE = 16 + cart[4] * 16384          # 0x10010 for a 4-bank cart
orig = ts.CHR_START
ts.CHR_START = CHR_BASE
try:
    apply_training_edition_title(cart, routine_off=V8_ROUTINE_OFF, data_off=V8_DATA_OFF, footer_text=V8_FOOTER_TEXT)
finally:
    ts.CHR_START = orig
# duplicate the high-half branding into index 3 (expand() would have; keep index1 == index3)
cart[V8_ROUTINE_OFF + HIGH_DUP:V8_ROUTINE_OFF + HIGH_DUP + len(routine)] = cart[V8_ROUTINE_OFF:V8_ROUTINE_OFF + len(routine)]
cart[V8_DATA_OFF + HIGH_DUP:V8_DATA_OFF + HIGH_DUP + len(meta)] = cart[V8_DATA_OFF:V8_DATA_OFF + len(meta)]

# 3) prove ONLY branding bytes changed (=> DRSTUDY chain + driver/AI are byte-intact)
def cchr(page, tile): return CHR_BASE + page * CHR_PAGE_SIZE + tile * 16
allowed = set(range(FOOTER_HOOK_OFFSET, FOOTER_HOOK_OFFSET + 3))
for off in (V8_ROUTINE_OFF, V8_ROUTINE_OFF + HIGH_DUP):
    allowed |= set(range(off, off + len(routine)))
for off in (V8_DATA_OFF, V8_DATA_OFF + HIGH_DUP):
    allowed |= set(range(off, off + len(meta)))
for page in TITLE_CHR_PAGES:
    for t in TITLE_TOP_TILE_IDS:
        allowed |= set(range(cchr(page, t), cchr(page, t) + 16))
for i in range(n_tiles):
    allowed |= set(range(cchr(FOOTER_CHR_PAGE, FOOTER_TILE_IDS[0] + i), cchr(FOOTER_CHR_PAGE, FOOTER_TILE_IDS[0] + i) + 16))
changed = {i for i in range(len(cart)) if cart[i] != before[i]}
stray = changed - allowed
print(f"changed {len(changed)} bytes; confined to branding set: {not stray} (stray {len(stray)})")
assert not stray, "branding overlay touched non-branding bytes (study/driver collision!)"

# 4) prove every branding byte == public TE v8 (PRG at same file offset; CHR by content)
base = open(base_v8, "rb").read()
assert base[4] == 2, "base_v8 must be the 32 KB-PRG public ROM"
def bchr(page, tile): return 16 + 2 * 16384 + page * CHR_PAGE_SIZE + tile * 16
ident = True
for name, off, ln in [("hook 0x0C34", FOOTER_HOOK_OFFSET, 3),
                      ("routine $C0A9", V8_ROUTINE_OFF, len(routine)),
                      ("metasprite $C0EF", V8_DATA_OFF, len(meta))]:
    g = base[off:off + ln] == bytes(cart[off:off + ln]); ident &= g
    print(f"  {'OK ' if g else 'FAIL'} PRG {name}")
for page in TITLE_CHR_PAGES:
    for t in TITLE_TOP_TILE_IDS:
        ident &= base[bchr(page, t):bchr(page, t) + 16] == bytes(cart[cchr(page, t):cchr(page, t) + 16])
for i in range(n_tiles):
    t = FOOTER_TILE_IDS[0] + i
    ident &= base[bchr(FOOTER_CHR_PAGE, t):bchr(FOOTER_CHR_PAGE, t) + 16] == bytes(cart[cchr(FOOTER_CHR_PAGE, t):cchr(FOOTER_CHR_PAGE, t) + 16])
print(f"  {'OK ' if ident else 'FAIL'} all 24 CHR tiles (subtitle + footer) == public v8")
assert ident, "branding bytes DIVERGE from public TE v8"

open(cart_out, "wb").write(cart)
print(f"\nbranded {os.path.basename(cart_in)} -> {cart_out}")
print(f"  ({len(cart)}B, mapper 100, md5 {hashlib.md5(bytes(cart)).hexdigest()})")
print("RESULT: PASS — TRAINING EDITION + V8.00 SL overlaid; study/driver intact; branding == public v8.")
