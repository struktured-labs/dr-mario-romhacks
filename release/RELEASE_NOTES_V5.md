# Dr. Mario Training Edition v5

A ROM hack that transforms the pause screen into a study mode for practicing Dr. Mario strategies and analyzing virus/capsule positions.

## Download

**[Download IPS Patch (v5)](https://github.com/struktured-labs/dr-mario-romhacks/raw/main/release/drmario_training_v5.ips)**

## Features

- Playfield remains fully visible when paused (no blackout)
- "STUDY" text displayed at the top of the screen instead of "PAUSE"
- All game elements (viruses, capsules, bottle) stay visible for analysis

## Changes from Original

- PPU rendering enabled during pause state
- Pause text repositioned to top of screen
- Custom "STUDY" text replaces "PAUSE" using new tile graphics

## Known Limitations

- Dr. Mario throwing animation sprite disappears during pause
- Dancing virus sprites (level intro) disappear during pause
- Falling capsule not visible during pause (frozen in place)

These limitations exist because certain sprite routines are shared between the pause system and menu screens. Disabling them would break the game selection menu.

## Compatibility

- **Base ROM:** Dr. Mario (USA) - MD5: `d3ec44424b5ac1a4dc77709829f721c9`
- **Tested on:** Nestopia, MiSTer FPGA NES core
- **Mapper:** MMC1 (no compatibility issues expected)

## Technical Details

| ROM Offset | Change | Description |
|------------|--------|-------------|
| 0x17CA | `$16` → `$1E` | PPU_MASK: enable background+sprites |
| 0x17D4 | `JSR` → `NOP NOP NOP` | Disable sprite clear on pause entry |
| 0x17DC | `$77` → `$0F` | Y position: move text to top |
| 0x2968 | Sprite data | Modified for "STUDY" text |
| CHR Bank 1 | Tiles 0xA0-0xA2 | Custom T, D, Y letter graphics |

## Credits

Patch created with assistance from [Claude Code](https://claude.com/claude-code) (Anthropic)

## Version History

| Version | Changes |
|---------|---------|
| v5 | Fixed FEVER menu text corruption |
| v4 | Fixed title screen Mario eyes, added second sprite preservation |
| v3 | Moved custom tiles to avoid conflicts |
| v2 | Added STUDY text with custom tiles |
| v1 | Initial release (visible playfield during pause) |
