# Dr. Mario Training Edition v6

A ROM hack that combines a **VS CPU** mode (play against an AI-controlled Player 2) with an
enhanced **Study Mode** pause — freeze the game mid-play and study the board, the falling
capsule, and the upcoming pill.

## Download

**[Download BPS Patch (v6)](https://github.com/struktured-labs/dr-mario-romhacks/raw/main/release/drmario_te_v6.bps)**

Apply against an unmodified *Dr. Mario (USA)* ROM with any BPS-capable patcher
(e.g. [Floating IPS / beat](https://www.romhacking.net/utilities/1040/)).

## Features

- **VS CPU mode** — a 3rd menu option (1 PLAYER → 2 PLAYER → VS CPU) where Player 2 is
  driven by a heuristic AI, with a human-like move cadence.
- **Study Mode pause** — pressing START during play freezes the game while keeping the
  screen rendered, so positions can be studied:
  - "STUDY" text shown at the top of the screen instead of "PAUSE"
  - The full bottle, all viruses, and the **falling capsule** stay visible and frozen
  - The **next-pill preview** stays visible while paused *(new in v6)*
  - Pressing START again resumes cleanly with no corruption

## Changes from Original

- New VS CPU game mode with an AI-controlled Player 2
- Pause reworked into a "study" freeze: background rendering stays on, the last gameplay
  frame is held in place, and the falling capsule + next-pill preview are preserved
- "PAUSE" text replaced by "STUDY" using new tile graphics, moved to the top of the screen

## Known Limitations

- The Dr. Mario throwing figure and the magnifier viruses are not shown while paused (these
  decorative sprites are built by a game phase the freeze skips). The study-relevant content —
  bottle, viruses, falling capsule, and next-pill preview — is all shown.
- In VS CPU / 2-player mode the "STUDY" text sits at the very top and slightly overlaps the
  two-player score header; the freeze/capsule/preview behavior is otherwise identical to
  1-player.

## Compatibility

- **Base ROM:** Dr. Mario (USA) — MD5: `d3ec44424b5ac1a4dc77709829f721c9`
- **Study Mode validated on:** Mesen (headless) — both 1-player and VS CPU pause paths
- **Mapper:** standard MMC1 (mapper 1) — runs on accurate NES emulators and the MiSTer NES core

## Technical Details

| ROM Offset | Change | Description |
|------------|--------|-------------|
| 0x17CA | `$16` → `$1E` | PPU_MASK: keep background on during pause |
| 0x17C7 | `$54` → `$70` | pause entry frame-wait `$B654` → `$B670` (no OAM clear) |
| 0x17D4 | `JSR $B894` → `NOP×3` | drop the pause-entry OAM clear |
| 0x17DC | `$77` → `$0F` | move "STUDY" text to the top of the screen |
| 0x17E3 | `JSR $88F6` → `JSR $D2CC` | pause draw calls the study routine (STUDY text + preview) |
| 0x17F3 | `$54` → `$70` | pause loop frame-wait `$B654` → `$B670` (no OAM clear) |
| 0x2968 | Sprite data | "PAUSE" letter quads changed to "STUDY" |
| CHR Bank 1 | Tiles 0xA0-0xA2 | custom T, D, Y letter graphics |
| 0x52DC ($D2CC) | New routine | 50-byte study-draw: STUDY letters (slots 2-6) + next-pill preview (slots 7-8), sparing the frozen capsule (slots 0-1) |

## Credits

Patch created with assistance from [Claude Code](https://claude.com/claude-code) (Anthropic).

Publishing target: [romhacking.net](https://www.romhacking.net/) (Struktured account).

## Version History

| Version | Changes |
|---------|---------|
| v6 | VS CPU + Study Mode combined; next-pill preview + falling capsule now visible while paused |
| v5 | Fixed FEVER menu text corruption |
| v4 | Fixed title screen Mario eyes, added second sprite preservation |
| v3 | Moved custom tiles to avoid conflicts |
| v2 | Added STUDY text with custom tiles |
| v1 | Initial release (visible playfield during pause) |
