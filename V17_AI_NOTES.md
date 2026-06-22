# v17 AI Notes

Dr. Mario VS CPU edition: in-ROM 6502 AI, version 17.

## Algorithm

```
For each tile in P2 playfield $0500-$057F (scan Y = 0..127):
  1. If tile is NOT a virus (0xD0-0xD2), continue.
  2. Extract virus color = tile EOR 0xD0.
  3. If color matches neither left nor right capsule color, continue.
  4. Compute target column:
     - left match  -> target = virus_col
     - right match -> target = virus_col - 1  (skip if virus_col == 0)
  5. FAT TOP CHECK (H1): skip candidate if row 0 OR row 1 of target column
     is occupied. (Combined top-row partition + height-1 penalty.)
  6. Base score = virus row (0-15). Lower row = better candidate. Store in $02.
  7. ADJACENCY BONUS (H3): if the tile DIRECTLY ABOVE or DIRECTLY RIGHT of
     the virus has the same color (same tile byte), DEC $02 (-1 bonus).
     This sets up 3-in-a-row clears (4 same-color tiles in a row clear).
  8. If $02 < $01 (best so far), update best score and target column.

After scan, move toward target column (or drop if already there).
```

## Heuristics introduced in v17

| # | Heuristic                  | Bytes vs v16 | Notes |
|---|----------------------------|--------------|-------|
| H1 | Fat top check (rows 0+1)  | +3           | Folds height-1 penalty into the existing top-row check via `AND $0508,X` |
| H2 | Weighted scoring via $02  | +4           | Adds `STA $02` after base score, `LDA $02` before compare |
| H3 | Adjacency bonus (V or H)  | +18          | Checks tile above + tile right of virus; -1 if either matches |

Plus v16 micro-optimizations (-8 bytes total) that made room for the above:

| # | Optimization                                       | Saved |
|---|----------------------------------------------------|-------|
| 1 | `EOR #$D0` instead of `SEC ; SBC #$D0`             | 1     |
| 2 | Removed redundant `TAX` after color extraction     | 1     |
| 3 | Removed redundant `TXA` before right-side `CMP`    | 1     |
| 4 | Compact movement via shared `STY $F6` tail         | 1     |
| 5 | Loop iter: `INY ; BPL` instead of `INY ; CPY ; BCC`| 2     |
| 6 | VS CPU mode: `LDA $04 ; BEQ` (no CMP #$01)         | 2     |

## ROM layout (v17 reorg)

v16 used 0x7F50-0x7FDF (144 bytes) with toggle+mirror+AI=27+9+107.
v17 expands into the previously-unused 0x7F40-0x7F4F padding region.

| Region          | v16          | v17          | Notes |
|-----------------|--------------|--------------|-------|
| 0x7F40-0x7F5A   | (padding)    | toggle (27)  | moved 0x10 bytes earlier |
| 0x7F5B-0x7F63   | (padding)    | mirror (9)   | moved 0x10 bytes earlier |
| 0x7F64-0x7FDF   | (mostly unused) | AI (124)  | AI window grew from 108 to 124 |
| 0x7FE0-0x7FE8   | JMP table    | JMP table    | unchanged |

CPU addresses (after relocation):
- Toggle: ROM 0x7F40 -> CPU $FF30 (was $FF40)
- Mirror: ROM 0x7F5B -> CPU $FF4B (was $FF5B)
- AI:     ROM 0x7F64 -> CPU $FF54 (was $FF64)

Hook patches updated:
- 0x18E5 JSR target: $FF40 -> $FF30
- 0x10AE JSR target: $FF5B -> $FF4B
- 0x37CF JMP target: $FF64 -> $FF54

The original 0x7F40-0x7FDF range was all padding (0x00/0xFF alternating
blocks) in the unmodified ROM, so this reorg does not displace any game
code or data.

## Byte budget table

| Component                   | Bytes | Notes |
|-----------------------------|-------|-------|
| Toggle routine              | 27    | unchanged |
| Mirror routine              | 9     | unchanged |
| AI routine (v17)            | 124   | exactly fills budget |
| **Total in 0x7F40-0x7FE0**  | **160** | exactly 160 bytes |

v17 AI breakdown (124 bytes):
- Hook plumbing (STA $F6, VS CPU check, gameplay check, P1 mirror): 17 bytes
- Setup (target=3, best=255, Y=0): 10 bytes
- Scan loop body:
  - Virus detect + color extract: 6 bytes
  - Color match left/right: 10 bytes
  - Right-match target compute: 9 bytes
  - Left-match target compute: 4 bytes
  - Fat top check (H1): 10 bytes
  - Base score + STA $02 (H2): 6 bytes
  - Adjacency bonus check (H3): 18 bytes
  - Compare with best + update: 10 bytes
  - Loop iter (INY/BPL): 3 bytes
- Movement decision (left/right/down): 19 bytes
- RTS: 1 byte

## Tradeoffs / known issues

- **Fat top is conservative.** Skipping any column whose rows 0+1 aren't both
  empty can make all candidates unreachable late in the game when the stack
  is tall. When that happens, AI falls back to default target = column 3
  and effectively drops blocks in center. Could relax to "row 0 must be
  empty AND row 1 occupancy adds +N to score" in v18 if room allows.

- **Horizontal adjacency wraps columns.** The right-neighbor check `$0501,Y`
  reads the next byte in memory, which for col 7 is actually col 0 of the
  next row. We accept this false-positive bonus to save ~4-6 bytes that
  a `Y AND #$07` column guard would cost. Edge effect is minor — at most
  one false-positive bonus per row.

- **Vertical adjacency wraps row 0.** For viruses in row 0, the "tile above"
  read at `$04F8,Y` lands in the P1 playfield region. Random P1 tile values
  could falsely trigger or miss the bonus. Same byte-saving tradeoff as
  above; no observed harm during testing because row-0 viruses are rare
  in normal play and would be skipped by the fat top check anyway.

- **Right-match col=1 degeneracy.** When the right capsule matches a virus
  at column 1, the intended target is col 0. The `DEX ; BNE eval`
  always-taken branch is NOT taken when DEX yields zero (Z=1), so flow
  falls into the left-match path which recomputes X=1. This is a
  pre-existing v16 bug, preserved in v17 for size. Could be fixed in v18
  with `BPL` (no byte change) once a v18 reorg lands.

- **No deeper height (row 2+) penalty.** A 3-row fat check (`AND $0510,X`)
  would cost +3 bytes which fits in the spare budget (0 bytes), so it
  would push v17 over. Deferred to v18.

- **No "consecutive-3" clear prediction.** Detecting that a placement would
  actually form a 3-in-a-row clear (vs just having a same-color neighbor)
  would require simulating the drop, which is too expensive in 6502.
  H3 is a cheap proxy: virus adjacency is correlated with chain potential.

## Test coverage

`test_vs_cpu.py` adds 7 v17-specific tests on top of the v16 baseline:

1. `test_v17_skips_column_with_row1_occupied` - H1 fat top in action
2. `test_v17_vertical_adjacency_bonus` - H3 vertical neighbor preference
3. `test_v17_vertical_adjacency_breaks_tie` - H3 tie-break by adj
4. `test_v17_horizontal_adjacency_bonus` - H3 horizontal neighbor preference
5. `test_v17_score_stored_in_temp` - H2 weighted scoring uses $02
6. `test_v17_height_penalty_skips_partition` - H1 fallback to default target
7. `test_v17_ai_fits_in_124_byte_budget` - layout + size assertions

All 30 v16 tests still pass against v17 (backward compatible behavior).
Total: 44 assertions across 36 test functions. Run via:

```
cd /home/struktured/projects/dr-mario-mods
.venv/bin/python test_vs_cpu.py
```

## Future work (v18+)

If more bytes become available (e.g., further v17 optimizations, or moving
toggle/mirror entirely out of 0x7F40-0x7FDF), the following are worth
adding in priority order:

1. Row-2 fat-top extension (`AND $0510,X`, +3 bytes) - deeper height-aware skip.
2. Column wrap guards for adjacency checks (+4-6 bytes) - removes false positives.
3. Fix the right-match col=1 degeneracy (`BPL` instead of `BNE`, 0 bytes if
   we also reorder paths, otherwise +1).
4. Separate H-adj and V-adj bonuses (-2 from -1 each, costs +0 bytes,
   but changes scoring semantics).
5. Block-clearing potential: count how many same-color tiles would be in
   the column after placement and bonus proportionally. Expensive (~20 bytes).
