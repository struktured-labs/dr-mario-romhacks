#!/usr/bin/env python3
"""Fold the TE v8 branding into a v28cs + DRSTUDY-v3.3 copro-cart core and PROVE the branding
bytes are byte-identical (same file address, same value) to the public base-ROM v8.

This is the acceptance test for "the public v8 BPS is the exact byte-basis for the copro carts":
the branding occupies runs free-and-identical in both artifacts, so the cart is strictly
base-v8 branding + the depth-2 AI / coprocessor additions, with zero divergent branding bytes.

Pipeline:
  drmario_v28cs.nes (32KB depth-2 core)
  + apply_study_pause (v3.3)
  + apply_training_edition_title(routine=$C0A9, data=$C0EF, "V8.00 SL")   [SAME params as base v8]
  -> branded 32KB core; then expand()+mapper-100 = the copro cart (unit0 = this core).

  usage: build_te_v8_cart.py [v28cs_core=tmp/drmario_v28cs.nes] [base_v8=tmp/drmario_te_v8.nes]
                             [cart_out=tmp/drmario_te_v8_copro.nes]
"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_cartridge_copro import apply_study_pause, STUDY_BLOB2, STUDY_BLOB2_CPU, STUDY_BLOB4, STUDY_BLOB4_CPU
from title_screen import (apply_training_edition_title, footer_routine, footer_hook_patched,
                          footer_metasprite, footer_layout, FOOTER_HOOK_OFFSET, FOOTER_CHR_PAGE,
                          FOOTER_TILE_IDS, TITLE_TOP_TILE_IDS, TITLE_CHR_PAGES, CHR_PAGE_SIZE,
                          TM_TILE_ID)
from expand_prg import expand

# Identical relocation to build_te_v8.py (this identity is the whole point):
V8_ROUTINE_OFF, V8_DATA_OFF, V8_FOOTER_TEXT = 0x40B9, 0x40FF, "V8.00 SL"

core_path   = sys.argv[1] if len(sys.argv) > 1 else "tmp/drmario_v28cs.nes"
base_v8_path = sys.argv[2] if len(sys.argv) > 2 else "tmp/drmario_te_v8.nes"
cart_out    = sys.argv[3] if len(sys.argv) > 3 else "tmp/drmario_te_v8_copro.nes"

core = bytearray(open(core_path, "rb").read())
assert core[4] == 2, "v28cs core must be a 32KB-PRG image (2 banks)"
n_tiles, base_x = footer_layout(V8_FOOTER_TEXT)
routine_len = len(footer_routine(V8_DATA_OFF, base_x))
data_len    = len(footer_metasprite(n_tiles))

# 1) DRSTUDY v3.3
n_study = apply_study_pause(core)
# 2) branding preconditions — the runs the base ROM used must ALSO be free in the study-v3.3 core
assert bytes(core[FOOTER_HOOK_OFFSET:FOOTER_HOOK_OFFSET + 3]) == b"\x20\xF6\x88", "hook not original in core"
assert set(core[V8_ROUTINE_OFF:V8_ROUTINE_OFF + routine_len]) <= {0x00, 0xFF}, "routine run $C0A9 not free in core"
assert set(core[V8_DATA_OFF:V8_DATA_OFF + data_len]) <= {0x00, 0xFF}, "data run $C0EF not free in core"
# 3) apply the IDENTICAL v8 branding (footer + "™"->"TE")
apply_training_edition_title(core, routine_off=V8_ROUTINE_OFF, data_off=V8_DATA_OFF,
                             footer_text=V8_FOOTER_TEXT, mark_te=True)
# study intact after branding
p2, p4 = 16 + (STUDY_BLOB2_CPU - 0x8000), 16 + (STUDY_BLOB4_CPU - 0x8000)
assert bytes(core[p2:p2 + len(STUDY_BLOB2)]) == STUDY_BLOB2, "study part2 clobbered"
assert bytes(core[p4:p4 + len(STUDY_BLOB4)]) == STUDY_BLOB4, "study part3b clobbered"

# ---- PRIMARY PROOF: branding is byte-identical to base v8 at the SAME file offsets ----
# base v8 and the branded core are both 2-bank/32KB, so PRG *and* CHR live at identical offsets.
base = open(base_v8_path, "rb").read()
assert base[4] == 2
def chr_off(page, tile): return 16 + 2 * 16384 + page * CHR_PAGE_SIZE + tile * 16
regions = [("hook 0x0C34 ($8C24)", FOOTER_HOOK_OFFSET, 3),
           ("routine $C0A9 (0x40B9)", V8_ROUTINE_OFF, routine_len),
           ("data $C0EF (0x40FF)", V8_DATA_OFF, data_len)]
for page in TITLE_CHR_PAGES:
    for t in TITLE_TOP_TILE_IDS:
        regions.append((f"subtitle CHR pg{page} 0x{t:02X}", chr_off(page, t), 16))
for i in range(n_tiles):
    t = FOOTER_TILE_IDS[0] + i
    regions.append((f"footer CHR pg2 0x{t:02X}", chr_off(FOOTER_CHR_PAGE, t), 16))
for page in TITLE_CHR_PAGES:
    regions.append((f"TE mark CHR pg{page} 0x{TM_TILE_ID:02X}", chr_off(page, TM_TILE_ID), 16))

ok = True
print("BRANDING BYTE-IDENTITY  base-v8  vs  v28cs+study-v3.3+branding core (same file offsets):")
for name, off, ln in regions:
    good = base[off:off + ln] == bytes(core[off:off + ln])
    ok = ok and good
    print(f"  {'OK  ' if good else 'FAIL'} 0x{off:05X} {name}: {bytes(core[off:off+ln]).hex()}")
assert ok, "branding bytes DIVERGE between base v8 and the cart core"

# 4) expand 32KB -> 64KB copro cart (unit0 = this branded core; ship fills unit1 with the search AI)
tmp2 = cart_out + ".2bank"
open(tmp2, "wb").write(core)
expand(tmp2, cart_out)
os.remove(tmp2)
cart = bytearray(open(cart_out, "rb").read())
cart[6] = (cart[6] & 0x0F) | 0x40      # mapper 100 (0x64)
cart[7] = (cart[7] & 0x0F) | 0x60
open(cart_out, "wb").write(cart)
# cart unit0 (first 32KB PRG) is byte-identical to the branded core -> branding preserved
assert bytes(cart[16:16 + 32768]) == bytes(core[16:16 + 32768]), "expand altered unit0"

print(f"\nbranded core: study edits {n_study}, footer 'V8.00 SL' ({n_tiles} tiles/{data_len}B) @ $C0EF, routine @ $C0A9")
print(f"copro cart -> {cart_out} ({len(cart)}B, PRG {cart[4]} banks, mapper 100, md5 {hashlib.md5(bytes(cart)).hexdigest()})")
print("RESULT: PASS — every branding byte is identical (address + value) in base v8 and the cart core.")
