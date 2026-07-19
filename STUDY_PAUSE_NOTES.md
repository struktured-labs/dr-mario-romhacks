# Study pause (DRSTUDY)

A ROM patch so pausing NES Dr. Mario **freezes game logic but keeps the board on screen**
(for studying positions), instead of the vanilla behaviour that blanks everything.

## Vanilla pause mechanism (base `drmario.nes`, MMC1)

Pause is a **self-contained blocking routine at CPU `$978E`** (PRG bank 0), called once per
frame from the 1P main loop at `$814B`:

```
$8148 JSR $8157   ; build gameplay sprites into the OAM buffer ($0200)
$814B JSR $978E   ; pause-check  <-- START here enters a blocking spin loop
$814E JSR $B654   ; frame-wait; its tail JSR $B894 CLEARS the OAM buffer to $FF every frame
$8154 JMP $8148
```

On START the routine (once): writes `$16`→`$2001` (background rendering **off**, bit 3),
`JSR $B894` (fills the `$0200` OAM buffer with `$FF` = all sprites off-screen), `JSR $88F6`
(draws "PAUSE"), then spins `JSR $B654 / JMP` until START is pressed again. Because `$B654`
re-clears OAM every frame and the main loop is blocked, the whole field disappears — only the
5 "PAUSE" letter sprites remain. (Confirmed in Mesen: `$2001` `$1E`→`$16`, on-screen sprite
count 46→5, screen goes black. The lead's assumption that viruses survive as background is
**wrong** — the background is blanked too.)

`$B670` is an identical frame-wait **without** the OAM-clear tail.

## The patch (5 confined edits, all inside `$97B6`–`$97F2`)

| CPU addr | before | after | effect |
|---|---|---|---|
| `$97B6` | `20 54 B6` `JSR $B654` | `20 70 B6` `JSR $B670` | entry wait, no OAM clear |
| `$97BA` | `A9 16` `LDA #$16` | `A9 1E` `LDA #$1E` | keep background rendering ON |
| `$97C4` | `20 94 B8` `JSR $B894` | `EA EA EA` NOP | drop entry OAM clear |
| `$97D3` | `20 F6 88` `JSR $88F6` | `EA EA EA` NOP | drop "PAUSE" draw |
| `$97E2` | `20 54 B6` `JSR $B654` | `20 70 B6` `JSR $B670` | loop wait, no OAM clear |

Base-ROM file offsets (`= CPU − $8000 + $10`): `$17C7`(`54→70`), `$17CA`(`16→1E`),
`$17D4`–`$17D6`(`→EA EA EA`), `$17E3`–`$17E5`(`→EA EA EA`), `$17F3`(`54→70`). 9 bytes.

The main loop populates OAM **before** the pause-check, so at pause entry the buffer holds the
live sprites; the two `B654→B670` swaps stop them being wiped, and the background stays on.

## Validation (base ROM, Mesen headless — `tmp/study_pause/`)

`Mesen --testrunner tmp/study_pause/study_probe.lua tmp/drmario_study.nes`

- `study_pre.png` — playing; `study_paused.png` — PAUSED: bottle, **all viruses**, and the
  **falling capsule** stay visible and frozen (`$2001`=`$1E`, pill-y frozen 90 frames);
  `study_post.png` — after unpause: full render restored, pill advanced, **no corruption**
  (on-screen sprites 46→2 while paused → 46 after resume).

## Known limitation

The **next-pill preview**, the Dr.Mario figure, and the magnifier viruses are built by a
later main-loop phase that the blocking pause skips, so they are **not** restored (the falling
capsule + bottle + all viruses — the actual position — are). Full fidelity would need a
snapshot-restore of the OAM buffer during the spin (extra RAM + code, doesn't port cleanly to
the copro carts), so it is out of scope for this confined patch.

## DRSTUDY flag (`patch_cartridge_copro.py`)

`apply_study_pause()` applies the same edits by locating the pause routine via a stable,
never-edited 12-byte anchor (the loop's START/`$F7` check), asserting each target holds an
accepted original **or** the already-patched value (idempotent), and failing loudly otherwise.
Default **ON** when `DRHUMAN=1`; disable with `DRSTUDY=0`.

Note: `drmario_v28cs.nes` (the copro build base) already carries 2 of the 5 edits from an
earlier partial attempt, so on the carts only 3 new edits are written.

Builds (all `tmp/`, gitignored):
- `drmario_study.nes` — base ROM + study patch only (emulator use, mapper 1). Rebuild:
  `python3 -c "from patch_cartridge_copro import apply_study_pause as f; d=bytearray(open('drmario.nes','rb').read()); f(d); open('tmp/drmario_study.nes','wb').write(d)"`
- `drmario_copro_pocket_nofreeze_study.nes` — `DRHUMAN=1 DRPOCKET=1 DRNOFREEZE=1`
- `drmario_copro_human_study.nes` — `DRHUMAN=1 DRNOFREEZE=1` ($5200 window)

**Copro-cart validation basis:** mapper 100 is not Mesen-emulable, so the carts are validated
by the base-ROM Mesen proof above **plus** a byte-level assert that the same original pause
opcodes were found at the same offsets (anchor `$17E6` in all three) before patching. Whether
pause is reachable in the carts' VS-CPU mode is not emulator-verified.
