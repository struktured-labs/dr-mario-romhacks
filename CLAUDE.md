# Dr. Mario Mods - Claude Code Notes

## VS CPU Mode Implementation

### Current Version: v16 (Enhanced AI with Heuristics)

**Latest:** Multi-candidate selection with row-based scoring and top row avoidance

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

### AI Evolution

**v15 (First Working AI):**
- Simple greedy algorithm: scan top-to-bottom for FIRST matching virus
- No evaluation, just move to first match and drop
- 59 bytes

**v16 (Current - Enhanced Heuristics):**
- Multi-candidate selection: evaluates ALL matching viruses
- Row-based scoring: prefers lower rows (score = row number, lower = better)
- Top row avoidance: skips columns with occupied top row (partition risk)
- Stores best candidate after scanning entire playfield
- 107 bytes (1 byte spare before JMP table at 0x7FE0)

**v16 Algorithm:**
```
1. Initialize: target=$00 (default center), best_score=$01 (255=unset)
2. For each tile in P2 playfield ($0500-$057F):
   a. If virus (0xD0-0xD2), extract color
   b. If color matches left or right capsule:
      - Calculate target column (col for left, col-1 for right)
      - Check top row of target column (skip if occupied)
      - Calculate score = row number (0-15)
      - If score < best_score: update best_score and target
3. Move toward target column (left/right)
4. Drop when at target
```

**Future (v17+ if needed):**
- Full column height counting
- Consecutive color detection
- Virus adjacency scoring
- Weighted scoring system
- Total: ~120 bytes (requires ROM reorganization)

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

**AI State (v16+):**
- `$00` - AI target column (0-7)
- `$01` - AI best score (255=unset, lower=better)

**Game State:**
- `$04` - VS CPU flag (custom, 0=normal, 1=VS CPU)
- `$46` - Game mode (< 4 = menu/level select, >= 4 = gameplay)
- `$0727` - Player mode (1=1P, 2=2P)

**Controller Input:**
- `$F5/$F7` - P1 controller input (new/held)
- `$F6/$F8` - P2 controller input (new/held)
- `$5B/$5C` - P2 processed input (what game uses)

**P2 Capsule State:**
- `$0385` - P2 capsule X position (0-7 columns)
- `$0386` - P2 capsule Y position (0-15 rows)
- `$0381` - P2 left capsule color (0=yellow, 1=red, 2=blue)
- `$0382` - P2 right capsule color

**Virus Counts:**
- `$0324` - P1 virus count
- `$03A4` - P2 virus count

### Hook Points

- `0x18E5` - Menu toggle (JSR to cycle 1P->2P->VS CPU->1P)
- `0x10AE` - Level select P2 input (JSR, copies $F6 to $5B)
- `0x37CF` - Controller read (JMP to AI routine)

### ROM Layout

Routines at 0x7F50, must end before 0x7FE0 (JMP table):
- Toggle routine: 27 bytes (0x7F50-0x7F6A)
- Mirror routine: 9 bytes (0x7F6B-0x7F73, simplified pass-through)
- AI routine: 107 bytes (0x7F74-0x7FDE)
- **Total: 143 bytes, ends at 0x7FDF (1 byte spare)**

**Version History:**
- v15: 59-byte AI (simple greedy)
- v16: 107-byte AI (multi-candidate with heuristics)
- v17+: ~120 bytes projected (full heuristic system)

### Testing

**Unit Tests:**
- Run: `python3 test_vs_cpu.py`
- v16: 30 tests passing (5 new heuristic tests added)
- Tests cover: toggle routine, mirroring, AI targeting, movement, and heuristics
- **Note:** Unit tests run routines in isolation - they can pass even when real game behavior fails

**Integration Testing:**
- Launch: `python3 patch_vs_cpu.py && mednafen drmario_vs_cpu.nes`
- Select "VS CPU" mode (press Select twice from main menu)
- MCP server for debugging: `mednafen-mcp/mcp_server.py`

### Research Basis (v16)

AI heuristics based on:
- **meatfighter.com Dr. Mario AI**: Industry-standard approach with top row penalty, height management, and consecutive color detection
- **Tetris AI research**: Height penalty, flat stack preference, downstacking strategies
- **PuyoPuyo AI**: Tree search algorithms and tactical heuristics for chain-based puzzle games

Key insight: NES constraints require cheap heuristics. v16 implements the most impactful ones first (top row avoidance, multi-candidate selection) before adding more complex scoring.

---

## Latent Project Goals

### 1. RL Training Infrastructure with Mesen

**Status: Phase 0 Complete** - Mesen integration operational

Switched from Mednafen to **Mesen2** for superior debugger support and RL training:
- Well-documented Lua API (memory read/write, callbacks)
- Most accurate NES emulator (trusted DMA handling)
- Active development, strong community support

**Architecture:**
```
Python RL Trainer ←→ Lua Bridge (TCP socket) ←→ Mesen Core (Lua API)
```

**Components:**
- **Mesen2**: Compiled from source as git submodule (`mesen2/`)
- **Lua Bridge** (`rl-training-new/lua/mesen_bridge.lua`): Socket server running inside Mesen
  - Commands: READ, WRITE, STEP, GET_STATE, QUIT
  - Exposes NES memory and frame control via TCP port 8765
- **Python Client** (`rl-training-new/src/mesen_interface.py`): Interface to Lua bridge
  - `read_memory(addr, size)` - Read NES RAM
  - `write_memory(addr, data)` - Write NES RAM (e.g., controller input)
  - `step_frame(n)` - Advance N frames
  - `get_game_state()` - Full Dr. Mario state (playfield, capsule, virus count)

**Benefits over Mednafen:**
- 1-2 days to implement (vs weeks of reverse engineering)
- Well-documented API (vs undocumented network debugger)
- Lua scripting support (vs none)
- Better accuracy (critical for realistic RL training)

**Next Steps:**
1. Build MCP Python AI (oracle with full heuristics) - Phase 1
2. Train PPO agent on 3090 GPU - Phase 2
3. Distill to decision tree (~500 bytes) - Phase 3
4. Compile to 6502 assembly - Phase 4
5. Expand ROM and embed tree - Phase 5

### 1b. Legacy: Mednafen MCP (Deprecated)

**Note:** Mednafen MCP approach was abandoned in favor of Mesen.

The mednafen-mcp server was designed for deep RL training but had limitations:
- Location: `mednafen-mcp/mcp_server.py`
- Works when Mednafen has a display (real or Xvfb)
- Headless with SDL dummy drivers does NOT work (frame counter stays 0)
- No documented debugger protocol (would require reverse engineering)

### 2. Smart AI Strategy

**Current Implementation (v16):**
- ✅ Row-based scoring: prefer lower rows (safer placements)
- ✅ Top row avoidance: prevent partition risk
- ✅ Multi-candidate evaluation: consider all matching viruses

**Planned Enhancements (v17+):**
- ⏳ Full column height counting
- ⏳ Consecutive color detection (scan for 2-3 color sequences)
- ⏳ Virus adjacency scoring (prefer viruses with adjacent matching colors)
- ⏳ Weighted scoring system (balance multiple factors)

**Future Advanced AI (MCP-based):**

For RL training or complex heuristics beyond ROM constraints:

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
