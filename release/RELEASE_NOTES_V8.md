# Dr. Mario Training Edition v8

**v8 unifies the two prior public builds into one patch and supersedes both:**

- **v6** — VS-CPU AI plus the DRSTUDY v3.3 study-pause apparatus (frozen playfield, `STUDY`
  text, *both* players' next-pill previews, and the 2P/VS `STUDY` lift above the score header).
- **v7** — the `TRAINING EDITION` title subtitle and a `STRUK LABS` version-credit footer
  (title-branding work carried over faithfully from the v7 release).

The two builds were developed on different baselines and **collided**: v7's footer routine
(`$BE56`) and metasprite table (`$9FF8`) are exactly DRSTUDY v3.3's `part3b` / `part2` dead
runs. v8 keeps the entire study chain intact and **relocates the footer** into free fixed-bank
runs, then bumps the credit to `V8.00 STRUK LABS`.

## Download

Apply `release/drmario_te_v8.bps` against an unmodified *Dr. Mario (USA)* ROM with a BPS-capable
patcher (Floating IPS / beat).

## Features

- **Study Mode pause** — the playfield stays rendered on pause; the falling capsule(s) freeze in
  place, `STUDY` is drawn above the board, and each player's real next pill is shown as a preview.
  Works in 1P, 2-player and VS-CPU; in 2P/VS `STUDY` is lifted clear of the score header.
- **VS-CPU mode** — a third title option (`1 PLAYER` → `2 PLAYER` → `VS CPU`) with an AI-controlled
  Player 2.
- **Training Edition title branding** — a two-tone `TRAINING EDITION` subtitle beneath `Dr. MARIO`.
- **Version credit** — `V8.00 SL` centered beneath the title menu.
- **Attract demo preserved** — the title nametable is byte-for-byte original and the footer is a
  title-only sprite overlay, so the title→attract-demo handoff and gameplay are untouched.
- **Coprocessor-cart byte-basis** — every branding byte lives at an address free-and-identical in
  the public ROM *and* the v28cs / copro cart lineage, so the auto-play carts are strictly this
  public build + the AI/driver additions, with zero divergent branding bytes (see below).

## Compatibility

- **Base ROM:** Dr. Mario (USA)
- **Base-ROM MD5:** `d3ec44424b5ac1a4dc77709829f721c9`
- **Patched-ROM MD5:** `2dd25dad2a11d9c9ac7183b73edc57d2`
- **Patch (BPS) MD5:** `2b07da40c74859c1080ccbefaea4e0ef`
- **Mapper:** standard MMC1 (mapper 1)

## Implementation notes — how the collision was resolved

The v6 study chain and v7 footer are byte-disjoint *except* for two 6502 dead runs (v7's footer
routine and metasprite sit exactly on DRSTUDY v3.3's `part3b` / `part2`). v8 leaves the study chain
byte-identical and moves only the footer — into two 24-byte dead runs that are free **and identical**
in the base ROM and the v28cs/copro carts, so the same bytes fold into the carts unchanged:

| piece | v7 location | v8 location | why |
|-------|-------------|-------------|-----|
| footer routine (23 B) | `$BE56` (study `part3b`) | **`$C0A9`** (file `0x40B9`) | 24-byte run free in base v6 + v28cs + copro |
| footer metasprite (17 B) | `$9FF8` (study `part2`) | **`$C0EF`** (file `0x40FF`) | 24-byte run free in base v6 + v28cs + copro |
| title hook `0x0C34` | `JSR $BE56` | **`JSR $C0A9`** | repointed to the relocated routine |

The only always-mapped runs free in *both* the public ROM and a study-v3.3 cart are 24 bytes, so the
credit was shortened to **`V8.00 SL`** — a 4-tile, 17-byte metasprite (the `TRAINING EDITION`
subtitle already carries the brand). The footer routine is position-independent apart from the
two-byte pointer to its metasprite table, so relocation is a pure address change: the hook `JSR`
target, the routine's data pointer, the tile count and the centering X are all derived from the
offsets and text. `title_screen.py` was parameterized (`routine_off` / `data_off` / `footer_text`)
with defaults that still reproduce the exact committed v7 bytes; the v6 study patcher is unchanged.

Everything else is the union of v6 and v7: the VS-CPU/study internal patches, the DRSTUDY v3.3
5-part chain (`part1 $D2CC` … `part3c $BC26`), the study letter tiles (`0xA0-0xA2`, CHR page 2), the
subtitle tiles (title CHR pages 3/4), and the footer tiles (`0xE8-0xEB`, CHR page 2) — all
byte-disjoint and verified.

### Coprocessor-cart basis (acceptance-tested)

`build_te_v8_cart.py` folds this exact branding into a v28cs + DRSTUDY-v3.3 core and asserts that
**every** branding byte — hook, routine, metasprite, and all 24 CHR tiles — is byte-identical (same
file address, same value) to the public v8 ROM, then `expand()`s to the mapper-100 cart. The public
BPS is therefore the literal byte-basis for the carts: `cart == public TE v8 (unit 0) + AI additions`.

### Validation (headless Mesen)

- **Title** — `TRAINING EDITION` subtitle and `V8.00 SL` footer both render.
- **1P / 2P / VS-CPU study pause** — capsule(s) frozen, background on (`$2001=$1E`), `STUDY` in OAM
  slots 32-36, P1 preview 37-38, P2 preview 39-40 (2P/VS), clean resume — identical to v6.
- **Attract demo** — title→demo handoff clean; footer sprites clear with OAM, no bleed into the demo.

## Version history

| Version | Changes |
|---------|---------|
| **v8** | **Unified v6 study + v7 branding; footer relocated off the DRSTUDY dead runs into cart-shared runs; credit → `V8.00 SL`; the public BPS is the byte-basis for the copro carts** |
| v7 | `TRAINING EDITION` branding + `V7.00 STRUK LABS` credit on the public v5 title |
| v6 | VS-CPU AI + DRSTUDY v3.3 study-pause (both previews, 2P/VS STUDY lift) |
| v5 | Fixed FEVER menu text corruption |
| v3–v4 | Custom-tile fixes, second-sprite preservation |
| v1–v2 | Visible-playfield pause + `STUDY` text |
