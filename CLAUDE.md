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
