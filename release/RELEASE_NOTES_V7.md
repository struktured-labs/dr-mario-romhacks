# Dr. Mario Training Edition v7

This build carries the published **Dr. Mario Training Edition v5** patch forward unchanged
and adds an identifying **TRAINING EDITION** subtitle to the original title screen.

## Download

**[Download BPS Patch (v7)](https://github.com/struktured-labs/dr-mario-te/raw/main/release/drmario_te_v7.bps)**

Apply it against an unmodified *Dr. Mario (USA)* ROM with a BPS-capable patcher such as
Floating IPS / beat.

## Features

- **Study Mode pause** — keeps the playfield visible for position analysis
- **Training Edition title branding** — a two-tone subtitle beneath `Dr. MARIO`
- **Clean title menu** — the public v5 `1 PLAYER` / `2 PLAYER` art remains untouched

## Compatibility

- **Base ROM:** Dr. Mario (USA)
- **Base-ROM MD5:** `d3ec44424b5ac1a4dc77709829f721c9`
- **Patched-ROM MD5:** `6ed3cec9735141ce72be18440cd629d3`
- **Mapper:** standard MMC1 (mapper 1)

## Title-screen implementation

The subtitle occupies the same pocket used by Dr. Mario Turbo, so no menu or logo geometry
moves. Its graphics are installed in the ten existing upper-row tiles on both title CHR pages.
The encoded title nametable at `0x3B06–0x3B0F` remains byte-for-byte original; this preserves
the `1 PLAYER` / `2 PLAYER` menu and the complete title-to-attract-demo transition.

## Version history

| Version | Changes |
|---------|---------|
| v7 | Added `TRAINING EDITION` branding to the public v5 title screen |
| v5 | Fixed FEVER menu text corruption |
| v4 | Fixed title-screen Mario eyes and added second sprite preservation |
| v3 | Moved custom tiles to avoid conflicts |
| v2 | Added STUDY text with custom tiles |
| v1 | Initial visible-playfield pause release |
