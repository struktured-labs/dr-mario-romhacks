# v18 AI Notes — Depth-1 Simulation AI

Dr. Mario VS CPU edition: in-ROM 6502 AI, version 18.

v18 is the first version that **actually simulates** each candidate placement and
**detects real line-of-4 clears** at the resting position, instead of *guessing*
at clears via color-adjacency the way v17 did. It is a depth-1 search:

```
enumerate placements  ->  drop  ->  detect clears  ->  score  ->  pick best
```

v17 is kept 100% intact: `drmario_vs_cpu.nes` is still the v17 ROM, all 44 v17
tests still pass, and the v17 toggle/mirror/AI bytes are byte-for-byte unchanged
inside the v18 ROM. v18 ships as a **separate** ROM, `drmario_v18.nes`.

## Build

```
cd /home/struktured/projects/dr-mario-mods
.venv/bin/python patch_vs_cpu.py        # writes drmario_vs_cpu.nes (v17) + drmario_v18.nes (v18)
.venv/bin/python test_vs_cpu.py         # 76 assertions, all pass (44 v17 + 32 v18)
```

`apply_patches_v18()` in `patch_vs_cpu.py` builds v18 on top of a fresh v17 ROM,
installs the v18 routine, and re-points the controller hook to it.

## Algorithm (depth-1, real clear detection)

```
plumbing: store P2 input; if not VS CPU -> return; mirror P1 in level select;
          if game mode < 4 (menu) -> return.

best_score = 0 ; best_col = 3 (center default)
build placement tiles: tileA = $4C | $0381 (left/top color),
                       tileB = $4C | $0382 (right/bottom color)

VERTICAL pass, col = 0..7:        (A on top, B on bottom)
  land_col(col): scan column top->down for first occupied; landing = row above.
                 skip if top row occupied; an empty column lands at row 15.
  require >= 2 empty rows (landing row >= 1) so the pair fits vertically.
  place A at (row-1,col), B at (row,col) in the live $0500 board.
  eval_pair (vertical): clears = colrun(A) [spans A&B] + rowrun(A) + rowrun(B).
  undo (restore both cells to $FF).
  score; keep if strictly better.

HORIZONTAL pass, col = 0..6:      (A on left, B on right)
  landing row = min(top_occupied(col), top_occupied(col+1)) - 1.
  place A at (row,col), B at (row,col+1).
  eval_pair (horizontal): clears = rowrun(A) [spans A&B] + colrun(A) + colrun(B).
  undo.
  score; keep if strictly better.

move the real capsule toward best_col: capsule X < target -> Right ($01),
  > target -> Left ($02), == target -> Down/drop ($04). (Reuses v17 movement.)
```

### Clear detection (the real Dr. Mario rule)

For each placed cell, `scan_run` finds the **contiguous same-color run THROUGH
that cell** along an axis (row: step 1, clamped to the 8-wide row; column: step
8, clamped to rows 0..15). If the run length is **>= 4** it commits the run's
cell count and its virus count. This matches the faithful engine
(`faithful_game.py`: horizontal/vertical runs of >= 4, never diagonal/flood-fill)
and the faithful tests (`test_horizontal_four_clears`, `test_vertical_four_clears`,
`test_three_does_not_clear`, `test_l_shape_does_not_clear`,
`test_mixed_color_run_not_cleared`, `test_five_in_row_clears_all_five`,
`test_virus_in_line_is_cleared`).

### Tile / color model (validated vs ROM via rl-training-new/src/heuristics.py)

```
empty            = $FF
virus  color k   = $D0 + k        (k = 0 yellow, 1 red, 2 blue)
settled capsule  = $4C + k
color(tile)      = tile & 3       (empty $FF -> 3, which is never a real color)
```

Two occupied cells share a color iff `(a & 3) == (b & 3)`. Because empty maps to
3 and real colors map to 0/1/2, equal low-2-bits automatically excludes empties —
this is what makes the run scan cheap. Simulated capsule halves are written as
`$4C | color` so the scan treats them like any other colored cell.

### Scoring

```
vir' = min(viruses_cleared, 3)
score = vir'*32 + cells_cleared*2 + height_term      (max 96 + 16 + 15 = 127)
height_term = resting row of the higher placed cell (0..15); larger = lower on
              the board = safer, so deeper placements win ties.
```

All scores are small non-negative bytes, so the "is this better?" test is a plain
unsigned `CMP` and `best` seeds at 0. A virus clear scores >= 32, while any
non-clearing drop scores only its height term (0..15), so **any real clear always
beats any non-clear**; among clears, more viruses > more cells > lower placement.

## ROM layout

| Region | ROM offset | CPU addr | Notes |
|--------|-----------|----------|-------|
| v18 AI routine | `0x7B10`–`0x7D0A` | `$FB00`–`$FCFA` | 506 bytes, in former padding |
| (free tail) | `0x7D0A`–`0x7D10` | `$FCFA`–`$FD00` | 6 bytes spare |
| v17 toggle | `0x7F40` | `$FF30` | unchanged from v17 |
| v17 mirror | `0x7F5B` | `$FF4B` | unchanged |
| v17 AI (dormant in v18) | `0x7F64` | `$FF54` | left in place, no longer hooked |
| JMP table | `0x7FE0` | `$FFD0` | untouched |

- The block `0x7B10`–`0x7D10` (512 bytes, CPU `$FB00`–`$FD00`) was alternating
  `$00`/`$FF` padding in the stock ROM (verified: only two stray non-pad bytes,
  which v18 overwrites). It is **not referenced** by any real code path.
- Hook: `0x37CF` is changed from the v17 `JMP $FF54` to `JMP $FB00`. Everything
  else (menu toggle `0x18E5`, level-select mirror `0x10AE`, Study Mode) is the
  v17 behavior, inherited unchanged.
- The ROM stays a valid iNES image: 65552 bytes = 16 (header) + 32768 PRG (2 ×
  16 KB banks, mapper 1 / MMC1) + 32768 CHR. No PRG expansion was needed.

### Byte budget (506 bytes total)

| Component | ~Bytes |
|-----------|-------|
| Plumbing (store/VS-CPU/mirror/mode checks) | ~26 |
| Setup (defaults + build placement tiles) | ~22 |
| Vertical pass (loop + landing + place) | ~55 |
| Horizontal pass (loop + 2-col landing + place) | ~75 |
| Movement decision | ~21 |
| `eval_pair` (place / orientation-aware scans / undo / score) | ~85 |
| `land_col` (drop / top-row guard) | ~40 |
| `clear_cell` + `scan_cell_row`/`scan_cell_col` (axis setup) | ~50 |
| `scan_run` (through-cell run finder) | ~95 |
| `score_update` (compact score + best-update) | ~45 |

### Cycle budget

Worst-case (a nearly full board) is ~4,500 simulator instructions per call ≈
15k–22k real 6502 cycles. The hook fires on the controller read; this is under a
frame (~29,780 cycles) but is **not yet validated on real hardware/emulator** —
see Known Limitations.

## RAM usage

- **Simulation is done in-place on the live P2 board `$0500`–`$057F` with undo**
  (write the 2 capsule cells, scan, then restore to `$FF`). This needs **no
  separate scratch page**, so there is zero risk of clobbering RAM the game uses.
  The `test_v18_restores_board_after_simulation` test asserts the board is left
  byte-for-byte unchanged.
- A copy-the-board variant (if ever wanted) could use the unused RAM windows
  `$0480`–`$04FF` or `$0580`–`$05FF` (the playfields proper are only
  `$0400`–`$047F` and `$0500`–`$057F`).
- Zero-page temps use **only bytes the game never touches** (verified by a static
  scan of all PRG zero-page accesses): `$00` (target col, v17-compatible),
  `$01` (best score), and working temps in `$6B`–`$6F` and `$CA`–`$DB`.
  Specifically: `$6B` col, `$6D`/`$6E` cell offsets, `$6F` higher-cell row,
  `$CA` cells-cleared, `$CB` viruses-cleared, `$CC` score, `$CD` run length,
  `$CE` match color, `$CF` scan offset, `$D2`/`$D3` placement tiles, `$D4` scan
  cell offset, `$D6` step, `$D7`/`$D8` scan bounds, `$D9` orientation,
  `$DB` scan virus count.

## What's in vs out of scope

In scope (implemented + tested):
- Real drop / resting-position computation per column and orientation.
- Real row-of-4 and column-of-4 clear detection at the resting position.
- Counting cells cleared and **viruses** cleared.
- Both orientations (vertical and horizontal) × all valid columns.
- Virus-dominant scoring with a height tie-break.
- In-place simulation with undo (board preserved).

**Out of scope (explicitly deferred — too expensive for the byte/cycle budget):**
- **No gravity cascade / combos.** v18 detects only the *immediate* line-of-4 at
  the resting position. The faithful engine's `resolve()` loop (clear → gravity →
  clear …) and multi-step chains (`test_chain_combo`) are **not** simulated.
- **No 2-ply / lookahead.** Only the current capsule's placement is evaluated;
  the next pill is not considered.
- **No loose-half gravity** after a partner clears (`faithful_game._apply_gravity`
  rigid-body falling) — irrelevant at depth 1 with no cascade.

## Known limitations

1. **No gravity cascade (by design).** A placement that would trigger a chain is
   scored only for its first clear. This is the dominant simplification.
2. **Depth-1 only.** No next-pill lookahead.
3. **Cross-axis single-cell double count.** If a placed cell sits in BOTH a
   row-of-4 and a column-of-4 through it, that one cell is counted in both runs
   (the faithful engine would dedup via a set). This only inflates `cells_cleared`
   by 1 in a rare geometry and never changes the *virus* count, so it does not
   flip the clear/no-clear decision. The orientation-aware scan in `eval_pair`
   already removes the common, large double-count (the shared axis of the pair).
   The exact ROM semantics are captured by `rom_clears()` in the cross-check.
4. **Movement does not rotate or pathfind.** Like v17, v18 moves toward the best
   *column* and drops; it does not rotate the capsule to match the chosen
   orientation, nor navigate around obstacles/overhangs. The orientation is used
   for *scoring/selection* but the on-field capsule keeps whatever orientation it
   spawned with. (Future work: emit a rotate input when best orient != current.)
5. **Right-color / A-vs-B asymmetry.** `tileA` is always the left/top color and
   `tileB` the right/bottom color; v18 does not also try the swapped assignment
   (which the game allows via rotation). Minor at depth 1.
6. **Unit-test-only validation.** As the v17 notes warn, the hand-written 6502
   simulator can pass while real ROM behavior differs (timing, the exact frame
   the hook fires, real capsule-orientation RAM, MMC1 bank state). The clear
   detection + scoring + drop are exhaustively cross-checked against a Python
   reference (8,000 random boards, 0 mismatches; 45k random `eval_pair` cases, 0
   mismatches; 20k random `clear_cell` cases, 0 mismatches), but **real-ROM /
   emulator validation of the in-game behavior is still needed** and was not done
   here (no emulator was launched).

## Test coverage

`test_vs_cpu.py` adds 14 v18 test functions (32 assertions) on top of the 44 v17
assertions, for **76 assertions total, all passing**. The 6502 simulator was
extended with the opcodes v18 needs: `ORA #`/`ORA zp` (`$09`/`$05`),
`ASL A` (`$0A`), `ADC zp` (`$65`), `SBC zp` (`$E5`), `PHA`/`PLA` (`$48`/`$68`),
`STA abs,X`/`STA abs,Y` (`$9D`/`$99`), `LDX zp`/`LDY zp` (`$A6`/`$A4`), and
nested `JSR`/`RTS` (the simulator now tracks the stack and only the top-level
`RTS` ends the run — v17 had no subroutines so the old "first RTS ends" shortcut
sufficed there).

v18 tests:

| Test | Covers |
|------|--------|
| `test_v18_detects_vertical_line_of_4` | (d) column run of 4, virus count |
| `test_v18_detects_horizontal_line_of_4` | (b) row run of 4, virus count |
| `test_v18_three_in_a_row_does_not_clear` | rule: run of 3 must not clear |
| `test_v18_mixed_color_run_not_cleared` | rule: mixed colors do not clear |
| `test_v18_l_shape_does_not_clear` | rule: L of 4 is not a line |
| `test_v18_five_in_row_clears_all` | rule: run of 5 clears 5 |
| `test_v18_targets_vertical_clear_column` | (a) full AI picks vertical clear col |
| `test_v18_targets_horizontal_clear_column` | (b) full AI picks horizontal clear col |
| `test_v18_prefers_clearing_over_nonclearing` | (c) clear beats center default |
| `test_v18_counts_viruses_cleared` | (d) 2 viruses score > 1 virus |
| `test_v18_no_clear_picks_center_default` | fallback to center when no clear |
| `test_v18_does_not_activate_without_vscpu` | inert outside VS CPU |
| `test_v18_restores_board_after_simulation` | in-place sim leaves board intact |
| `test_v18_fits_in_rom_region` | (e) <= 512 bytes, installed + hooked correctly |

Clear scenarios are reused from the faithful engine tests
(`/home/struktured/projects/dr_mario_rl/.claude/worktrees/faithful-sim/tests/test_faithful_game.py`).

A standalone cross-check harness (`tmp/v18_crosscheck.py`, plus the reference
model `tmp/v18_ref.py`) fuzzes the full routine and the `eval_pair`/`clear_cell`
primitives against the Python reference over tens of thousands of random boards
with zero mismatches. (These live under `tmp/`, which is git-ignored.)

## Future work (v19+)

1. **Emulator validation.** Run `drmario_v18.nes` in Mesen/mednafen in VS CPU mode
   and confirm the AI actually clears lines in play (the highest-priority gap).
2. **Gravity cascade / combos** — simulate `resolve()`'s clear→gravity loop to
   score chains. Expensive; likely needs the scratch-board RAM + a real PRG bank.
3. **Rotation + pathfinding** so the on-field capsule reaches the chosen
   orientation and column around overhangs.
4. **Next-pill lookahead (2-ply)** for setups.
5. **Swapped A/B color assignment** as an extra candidate per column.
