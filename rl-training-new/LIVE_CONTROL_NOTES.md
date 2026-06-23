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
