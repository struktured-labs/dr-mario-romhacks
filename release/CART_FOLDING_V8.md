# TE v8 branding — copro-cart folding spec

How the TE v8 title branding (`TRAINING EDITION` subtitle + `V8.00 SL` footer) folds into the
**coprocessor carts** (v28cs depth-2 core + DRSTUDY v3.3, mapper 100, 64 KB PRG).

**The public v8 BPS is the exact byte-basis for the carts.** Every branding byte lives at an
address that is free-and-identical in both the public ROM and a study-v3.3 cart core, so the fold
is a pure overlay: `cart == public TE v8 (unit 0) + AI / coprocessor additions`, with zero
divergent branding bytes. `build_te_v8_cart.py` builds the folded core and asserts that identity.

## 1. Cart PRG layout (authoritative: `expand_prg.py`)

The game runs MMC1 in 32 KB PRG-switch mode. `expand()` turns the 32 KB core into 4×16 KB banks:

| index | file range | mapping | contents |
|-------|-----------|---------|----------|
| 0 | `0x00010-0x0400F` | unit0 `$8000-$BFFF` | original low half |
| 1 | `0x04010-0x0800F` | unit0 `$C000-$FFFF` | original high half (vectors, fixed AI, study `part1`) |
| 2 | `0x08010-0x0C00F` | unit1 `$8000-$BFFF` | coprocessor / search code (mapped only when PRG-bank=2) |
| 3 | `0x0C010-0x1000F` | unit1 `$C000-$FFFF` | duplicate of index 1 (high half is always mapped) |

At reset PRG-bank=0 → **unit0 = the original 32 KB runs the title, menus, gameplay and study
pause.** All of the branding lives in unit0, so **fold it into the 32 KB v28cs core BEFORE
`expand()`** — `expand()` duplicates the high-half edits into index 3 and carries the CHR through.

## 2. The fold — identical offsets/bytes to the public v8 ROM

Apply to the 32 KB core (`drmario_v28cs.nes` + `apply_study_pause` = the study-v3.3 core). Every
precondition below is asserted; every write equals the public v8 ROM byte-for-byte at the same
file offset.

| piece | file offset | CPU / PPU | precondition | write (== public v8) |
|-------|-------------|-----------|--------------|----------------------|
| title hook | `0x0C34` | `$8C24` | `== 20 F6 88` (JSR $88F6) | `20 A9 C0` (JSR `$C0A9`) |
| footer routine (23 B) | `0x40B9` | `$C0A9` | 24-byte run filler | `footer_routine($C0EF, base_x=0x70)` |
| footer metasprite (17 B) | `0x40FF` | `$C0EF` | 24-byte run filler | 4-tile `V8.00 SL` table + `$80` |
| footer CHR tiles `0xE8-0xEB` | pg 2 | PPU `$2E80` | filler | 4 footer tiles |
| subtitle CHR (10 tiles ×2) | pages 3/4 | — | `== base title art` | subtitle overlay |
| `™`→`TE` mark tile `$0F` | pages 3/4 | — | `== base "™" M-half` | repaint M-half to `E` |
| title tilemap | `0x3B06-0x3B0F` | — | `== 42 FC×9` (untouched) | *(no write)* |

Both dead runs (`$C0A9`, `$C0EF`) are in the always-mapped high half and are confirmed filler in
base v6, plain v28cs, the copro carts, **and** the study-v3.3 core. Because the credit is only 17 B
(4 tiles), it fits the 24-byte runs that survive in a study-v3.3 cart — which is why the footer text
is `V8.00 SL` rather than the longer v7 string. Nothing in the cart's depth-2 AI, the study chain,
or the coprocessor bank overlaps these bytes.

## 3. Build + acceptance test

```
$ python build_te_v8_cart.py [core=tmp/drmario_v28cs.nes] [base_v8=tmp/drmario_te_v8.nes] [out]
```

It: (1) applies DRSTUDY v3.3; (2) asserts the hook/routine/data runs are filler; (3) applies the
identical v8 branding; (4) asserts DRSTUDY `part2`/`part3b` are intact; (5) **asserts every branding
region equals the public v8 ROM at the same file offset** (hook, routine, metasprite, all 26 CHR
tiles); (6) `expand()`s to the mapper-100 cart and asserts unit0 is unchanged. A green run is the
acceptance proof that the public BPS is the cart byte-basis.

For a *shipping* copro cart, drive `patch_cartridge_copro.main()` as today but apply this branding to
the core before its `expand()` (or fold the same three PRG writes + CHR tiles into the existing 2-bank
image and re-`expand`). The coprocessor search code occupies unit1 (bank 2) and never touches these
unit0 branding bytes.

## 4. Validation status

Base-ROM v8 is fully Mesen-validated (title branding, 1P/2P/VS study pause, attract demo). The
branding byte-identity into the cart core is asserted by `build_te_v8_cart.py`. Mapper-100 carts are
not Mesen-emulable, so the assembled cart still needs a MiSTer/Pocket check that the title shows the
subtitle + `V8.00 SL` and that VS-CPU auto-play + study pause are unaffected — but since the branding
bytes are provably identical to the validated public ROM, only the title's brief on-cart appearance
is unverified, not its content.
