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
- **Version credit** — `V8.00 STRUK LABS` centered beneath the title menu.
- **Attract demo preserved** — the title nametable is byte-for-byte original and the footer is a
  title-only sprite overlay, so the title→attract-demo handoff and gameplay are untouched.

## Compatibility

- **Base ROM:** Dr. Mario (USA)
- **Base-ROM MD5:** `d3ec44424b5ac1a4dc77709829f721c9`
- **Patched-ROM MD5:** `b435d576857087e9772766d4c693701e`
- **Patch (BPS) MD5:** `731ba68fad5c0d519326de6c74e48d7d`
- **Mapper:** standard MMC1 (mapper 1)

## Implementation notes — how the collision was resolved

The v6 study chain and v7 footer are byte-disjoint *except* for two 6502 dead runs. v8 leaves the
study chain byte-identical and moves only the footer:

| piece | v7 location | v8 location | why |
|-------|-------------|-------------|-----|
| footer routine (23 B) | `$BE56` (study `part3b`) | **`$C0A9`** (file `0x40B9`) | free fixed-bank run; also free in the v28cs / copro carts |
| footer metasprite (33 B) | `$9FF8` (study `part2`) | **`$CF00`** (file `0x4F10`) | free 48-byte fixed-bank run |
| title hook `0x0C34` | `JSR $BE56` | **`JSR $C0A9`** | repointed to the relocated routine |

The footer routine is position-independent apart from the two-byte pointer to its metasprite table,
so relocation is a pure address change: the hook `JSR` target and the routine's data pointer are
both derived from the new offsets. `title_screen.py` was parameterized (`routine_off` / `data_off`
/ `footer_text`) with defaults that still reproduce the exact committed v7 bytes; the v6 study
patcher is unchanged.

Everything else is the union of v6 and v7: the VS-CPU/study internal patches, the DRSTUDY v3.3
5-part chain (`part1 $D2CC` … `part3c $BC26`), the study letter tiles (`0xA0-0xA2`, CHR page 2), the
subtitle tiles (title CHR pages 3/4), and the footer tiles (`0xE8-0xEF`, CHR page 2) — all
byte-disjoint and verified.

### Validation (headless Mesen)

- **Title** — `TRAINING EDITION` subtitle and `V8.00 STRUK LABS` footer both render.
- **1P / 2P / VS-CPU study pause** — capsule(s) frozen, background on (`$2001=$1E`), `STUDY` in OAM
  slots 32-36, P1 preview 37-38, P2 preview 39-40 (2P/VS), clean resume — identical to v6.
- **Attract demo** — title→demo handoff clean; footer sprites clear with OAM, no bleed into the demo.

## Version history

| Version | Changes |
|---------|---------|
| **v8** | **Unified v6 study + v7 branding; relocated the footer off the DRSTUDY dead runs; credit → `V8.00 STRUK LABS`** |
| v7 | `TRAINING EDITION` branding + `V7.00 STRUK LABS` credit on the public v5 title |
| v6 | VS-CPU AI + DRSTUDY v3.3 study-pause (both previews, 2P/VS STUDY lift) |
| v5 | Fixed FEVER menu text corruption |
| v3–v4 | Custom-tile fixes, second-sprite preservation |
| v1–v2 | Visible-playfield pause + `STUDY` text |
