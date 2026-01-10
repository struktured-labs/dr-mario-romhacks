# Dr. Mario Mods - Claude Code Notes

## VS CPU Mode Implementation

### Working Approach (v13+)

The key insight for level select mirroring + gameplay AI:

**Handle BOTH in a single hook at 0x37CF (controller read):**

```
1. Store original P2 input to $F6
2. If VS CPU mode ($04 == 1):
   a. Copy P1 input ($F5) to $F6 (mirroring for level select)
   b. If gameplay (mode $46 >= 4):
      - Override $F6 with AI input
3. Return
```

The 0x10AE routine then copies $F6 to $5B normally.

### Failed Approaches (DO NOT USE)

These approaches did NOT work despite passing unit tests:

1. **Virus count check** ($03A4 or $0324)
   - Theory: virus count > 0 means gameplay
   - Reality: Didn't reliably detect gameplay state

2. **Separate mirror routine at 0x10AE with mode check**
   - Theory: Check mode in mirror routine, skip if gameplay
   - Reality: Timing/race conditions with AI routine

3. **Flag-based coordination** ($02 flag)
   - Theory: AI sets flag, mirror checks flag
   - Reality: Execution order unpredictable, race conditions

### Key Memory Addresses

- `$04` - VS CPU flag (custom, 0=normal, 1=VS CPU)
- `$46` - Game mode (< 4 = menu/level select, >= 4 = gameplay)
- `$F5/$F7` - P1 controller input (new/held)
- `$F6/$F8` - P2 controller input (new/held)
- `$5B/$5C` - P2 processed input (what game uses)
- `$0385` - P2 capsule X position
- `$0386` - P2 capsule Y position
- `$0324` - P1 virus count
- `$03A4` - P2 virus count
- `$0727` - Player mode (1=1P, 2=2P)

### Hook Points

- `0x18E5` - Menu toggle (JSR to cycle 1P->2P->VS CPU->1P)
- `0x10AE` - Level select P2 input (JSR, copies $F6 to $5B)
- `0x37CF` - Controller read (JMP to AI routine)

### ROM Layout

Routines at 0x7F50, must end before 0x7FE0 (JMP table):
- Toggle routine: ~27 bytes
- Mirror routine: ~9 bytes (simplified pass-through)
- AI routine: ~59 bytes

### Testing

- Unit tests: `python3 test_vs_cpu.py`
- MCP server for headless debugging: `mednafen-mcp/mcp_server.py`
- The unit tests run routines in isolation - they can pass even when real game behavior fails

---

## Latent Project Goals

### 1. MCP Tooling for Deep RL Training

The mednafen-mcp server is designed to support **deep reinforcement learning** agents:
- Provides game state observation (playfield, capsule position, virus counts)
- Allows action injection (controller input)
- Goal: Enable RL agents to learn Dr. Mario without ROM hacking

**MCP Server Status:**
- Location: `mednafen-mcp/mcp_server.py`
- Works when Mednafen has a display (real or Xvfb)
- Headless with SDL dummy drivers does NOT work (frame counter stays 0)
- Use `xvfb-run mednafen <rom>` for headless training

**Design Philosophy:**
- Mednafen MCP is the base (generic emulator control)
- Dr. Mario specific tools are specializations
- Future: Add other game specializations (enable/disable at will)

### 2. Smart AI Strategy

**Scoring-based capsule placement:**

1. **Enumerate all valid drop positions** (column + rotation)
2. **Score each position** based on:
   - Virus matches: +points for each virus that would be cleared
   - Consecutive bonus: 2-match < 3-match < 4-match (exponential)
   - Chain potential: bonus if placement enables future clears
   - Height penalty: prefer lower placements (safer)
   - Blocking penalty: avoid blocking access to viruses

3. **Pathfinding:** Navigate around obstacles to reach target column
   - May need to rotate to fit through gaps
   - Consider that capsule is 2 tiles wide (or 1 tall when vertical)

4. **Dynamic recomputation:**
   - Recompute scores when opponent clears (garbage may drop)
   - Or simply recompute every N frames
   - Balance computation cost vs responsiveness

**Dr. Mario Mechanics:**
- 4 consecutive same-color tiles clears them (horizontal OR vertical)
- Colors: Yellow, Red, Blue
- Capsule has 2 halves, each with a color
- Rotation cycles through 4 orientations
- Playfield: 8 columns x 16 rows

### 3. Key Memory for AI

Playfield scanning:
- P1 playfield: `$0400-$047F` (8x16 = 128 bytes)
- P2 playfield: `$0500-$057F`
- Tile values: `$FF` = empty, `$D0` = yellow virus, `$D1` = red virus, `$D2` = blue virus
- Capsule halves: `$4C-$5B` range

Current capsule:
- P2 X: `$0385`, Y: `$0386`
- P2 left color: `$0381`, right color: `$0382`
- Orientation: `$00A5` (0=horiz, 1=vert CCW, 2=reverse, 3=vert CW)

Drop timer: `$0392` (P2) - frames until capsule drops one row
