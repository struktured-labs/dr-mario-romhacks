# Live NES control via the bridge — verified findings (2026-06-22)

Goal: drive the real Dr. Mario ROM with the faithful depth-2 planner so the CPU
opponent is strong. The pipeline is **proven working** (planner reads the live
board and steers the capsule to chosen columns); the remaining work is rotation
+ planner strength under real-time.

## Verified live RAM (VS CPU, save state slot 1, level 5)

| What | Address | Notes |
|---|---|---|
| P1 board | `$0400`–`$047F` | 16×8, row-major. Only valid **during active gameplay** (it's the display buffer; shows menus/GAME-OVER otherwise) |
| P2 board | `$0500`–`$057F` | same |
| Cell encoding | — | empty=`$FF`/`$00`; virus=`$Dx` (D0/D1/D2); pill/pellet=`$40`–`$8F`; **color = byte & 0x0F** (0=Y,1=R,2=B) |
| P1 capsule X (col) | **`$0090`** | 0–7, verified by LEFT/RIGHT correlation. (Documented `$0305` was wrong/stale.) |
| P1 pill colors | `$0301`/`$0302` | left/right, color = byte & 0x0F |
| P1 next pill | `$031A`/`$031B` | |
| capsule rotation | **unknown** | not a clean 0–3 RAM byte; track via A-press count instead |
| game mode | `$0046` | shifts a lot; unreliable as a single gameplay flag |

OAM (`$0200`) holds the falling-capsule **sprites** (it animates every frame); the
logical board is the `$0400`/`$0500` buffers above.

## Bridge capabilities (all added + working)

- `read_memory` / `write_memory` (emu.memType.**nesMemory** — the original bug was
  `cpuMemory`).
- `set_input(port, buttons)` — injects via `emu.setInput` on the **inputPolled**
  event (direct `$F5/$F6` writes get overwritten by the poll, so this is the only
  reliable way). `release(port)` hands control back to the real gamepad.
- `load_state(path)` — loads a `.mss` via a one-shot **exec** memory callback
  (loadSavestate requires `IsSaveStateAllowed`).
- NES button mask bits: 1=a 2=b 4=up 8=down 16=left 32=right 64=start 128=select.

## Match flow (from the user)

- Save state **slot 1** = VS CPU level-5, dumb AI on P2. **Press Start** to begin a round.
- From the title: **Select ×2 + Start** activates VS CPU (then slide to the level).
- A match is **first-to-3 rounds**; press **Start between rounds**.
- Simplest for automation: `load_state(slot1)` + Start gives a fresh round-1 every
  time (auto-reload), so we never fight the between-round flow.

## Proven

`scripts/play_rom_live.py` (horizontal-only v3): loads slot 1, starts the round,
and the **depth-1 planner steers the capsule to its chosen column and drops it**,
replanning on each lock, auto-reloading on round loss. It places pills correctly
at planned columns on the real ROM. (It clears poorly — horizontal-only can't set
up most clears — which is expected.)

## Remaining to get a *winning* CPU

1. **Rotation** — track orientation by counting A-presses (spawn = horizontal;
   1 A ≈ vertical) rather than reading RAM. Needed for vertical placements (most
   clears). Verify "1 A press = vertical" + handle color-order (which half is which).
2. **Strength vs real-time** — depth-2 (~1–2 s/decision) is strong but the capsule
   falls during planning; plan **once per pill at spawn** and execute over the fall
   (level-5 medium fall is slow enough). depth-1 is fast but weak.
3. **New-pill detection** without a Y address — use board-fill change (lock) +
   capsule X returning to spawn.

## Why real-time control keeps failing — and the real fix

Tried depth-1/depth-2, horizontal-only, and tracked-rotation loops. All place
pills but clear ~1 virus then top out (~8 pills). Root causes, all from the same
issue — **the loop is too coarse for real-time**:

- Each iteration sent ~3-6 bridge commands; the emulator runs at 60 fps
  *independently*, so the capsule fell/locked before the loop steered it to the
  planned column → pills pile up near spawn → top out.
- Rotation isn't a clean RAM byte; tracking it by A-press count is fragile under
  this timing.
- New-pill detection via "X returns to spawn" never re-triggers when the planned
  column ≈ the spawn column (X never leaves), so the loop holds **down** and the
  capsule drops instantly at spawn every pill (observed on screen).
- The planner is correct (it reads the board fine) but its plan can't be executed
  precisely in real time.

**The fix is architectural, not more tuning: frame-perfect stepping.** Mesen's Lua
exposes `emu.breakExecution`, `emu.resume`, and `emu.step`. Rework the bridge so
the emulator advances **only** on an explicit STEP from Python (pause between
frames). Then each game-frame: read state, decide, inject input, step one frame —
with unlimited wall-clock to plan (depth-2/3 fine) and exact, deterministic
placement. This also gives reliable lock/new-pill detection (compare board
between steps). That is the clean path to a live winning CPU; the real-time
free-running approach here is fundamentally too imprecise.

Alternative quick mitigation if frame-stepping is too invasive: slow Mesen's
emulation speed (so the ~30 Hz loop gets many real-frames of slack per game-frame)
— less clean but may be enough to place precisely.

## UPDATE 2 (2026-06-22, later): frame-perfect bridge DONE + control proven

**Frame-perfect stepping is implemented and verified.** New bridge commands:
`STEPMODE 1/0` (toggle), and in step-mode the endFrame callback *blocks* until a
`STEP` (advance exactly one frame). Verified: state is frozen between STEPs (3
identical reads) and exactly 12 RAM bytes change per STEP. `ScriptTimeout` raised
to 86400 in settings.json so the blocking callback isn't killed. Client:
`set_step_mode(on)`, `step_frame(n)` sends n individual STEPs. This removes the
real-time race entirely — unlimited reads/planning per frame, deterministic.

**Live placement control PROVEN** — with frame-perfect stepping the planner steers
the capsule to its chosen column and drops it, locking every pill (`locked=True`
at varied columns col0..7). The earlier real-time failures were 100% the control
rate; frame-perfect fixes placement.

**The remaining wall is per-ROM RE, on the BASE rom (`drmario.nes`):**
- The VS-CPU rom's AI **hook on the controller read intercepts input**, so
  external `setInput` only works in *menus* there, not gameplay. Use the base
  `drmario.nes` (no hook): confirmed port-0 DOWN locks a pill on `$0400`.
- Base-rom verified addrs: board `$0400`, capsule **column = `$004B`** (0-7),
  capsule sprites `$0203/$0207`. Board decode (virus `$Dx`, color = low nibble) is
  correct (reads a clean 4-virus level-0 board).
- **Still murky (the blockers to a winning loop):**
  1. **Pill colors**: `$0301/$0302` (from the VS-CPU map) don't reliably match the
     colors that actually land on the base rom — need to find the base rom's true
     current-pill color addresses (correlate read vs landed cell over many pills).
  2. **Rotation**: pressing A 0/1/2/3 times all landed *horizontal* — A doesn't
     visibly rotate to vertical here; need to find the real rotate input/mechanic
     (try B, or write orientation RAM directly) and map variant->orientation.
  Without correct colors + rotation, the planner's setups don't align, so it
  places pills accurately but never completes a clear (level-0: 0 cleared in ~18
  pills despite perfect placement).

**Recommended finish:** on the base rom, (a) pin the true current-pill color
addresses by correlating reads against landed cells frame-by-frame, (b) map the
real rotation control, then the existing frame-perfect loop (`play_rom_live.py`)
should clear and win. All the hard infrastructure (frame-perfect bridge, input
injection, board/capsule/X decode, save-state load) is done and verified.
