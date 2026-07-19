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
**wrong** — the background is blanked too.) `$B670` is an identical frame-wait **without** the
OAM-clear tail.

## What persists, and the preview

The main loop populates OAM **before** the pause-check, but only the **falling capsule** (OAM
slots 0-1) is drawn before `$814B`; the decorative sprites — next-pill preview, Dr.Mario,
magnifier viruses — are drawn *after* the pause-check (measured: buffer holds 2 sprites at
`$814B`, fills to 46 later). So preserving the buffer keeps the capsule + background but not the
preview. Since the **next-pill preview is required study info**, we hand-draw it during pause.

## The patch (5 edits inside `$97B6`–`$97F2` + one 47-byte routine at `$D2CC`)

| CPU addr | before | after | effect |
|---|---|---|---|
| `$97B6` | `20 54 B6` `JSR $B654` | `20 70 B6` `JSR $B670` | entry wait, no OAM clear |
| `$97BA` | `A9 16` `LDA #$16` | `A9 1E` `LDA #$1E` | keep background rendering ON |
| `$97C4` | `20 94 B8` `JSR $B894` | `EA EA EA` NOP | drop entry OAM clear |
| `$97D3` | `20 F6 88` `JSR $88F6` | `20 CC D2` `JSR $D2CC` | draw preview instead of "PAUSE" |
| `$97E2` | `20 54 B6` `JSR $B654` | `20 70 B6` `JSR $B670` | loop wait, no OAM clear |

Base-ROM file offsets (`= CPU − $8000 + $10`): `$17C7`(`54→70`), `$17CA`(`16→1E`),
`$17D4`–`$17D6`(`→EA EA EA`), `$17E3`–`$17E5`(`→20 CC D2`), `$17F3`(`54→70`).

**Preview routine** at CPU `$D2CC` (file `$52DC`) — 47 bytes of dead padding after the routine
ending `$D2CB RTS`, **filler in base AND v28cs**, reachable via JSR from the pause loop (fixed
bank). It reads the next-pill colors and writes the two preview half-pill sprites to OAM slots
2-3 (unused during pause; capsule holds 0-1):

```
LDA $031A / AND #$03 / ORA #$60 / STA $0209   ; slot2 tile = $60|colorA  (left half)
LDA $031B / AND #$03 / ORA #$70 / STA $020D   ; slot3 tile = $70|colorB  (right half)
LDA #$45  / STA $0208 / STA $020C             ; Y = 69   (both halves)
LDA #$02  / STA $020A / STA $020E             ; attr = 2 (palette)
LDA #$BE  / STA $020B                         ; slot2 X = 190
LDA #$C6  / STA $020F                         ; slot3 X = 198
RTS
```

Position/tile/attr match the game's own preview exactly (Mesen byte-verified:
`nextA=$01 nextB=$00` → tiles `$61/$70`, `Y=$45`, `X=$BE/$C6`, `attr=$02`).

## Validation (base ROM, Mesen headless — `tmp/study_pause/`)

`Mesen --testrunner tmp/study_pause/study_probe.lua tmp/drmario_study.nes`

- `study_pre.png` — playing; `study_paused.png` — PAUSED: bottle, **all viruses**, the
  **falling capsule**, and the **next-pill preview** stay visible and frozen (`$2001`=`$1E`,
  pill-y frozen at 10 for 90 frames); `study_post.png` — after unpause: full render restored,
  pill advanced, **no corruption** (on-screen sprites 46 → 4 while paused → 46 after resume).
- `verify_preview.lua`: drawn preview tiles == `$60|($031A&3)` / `$70|($031B&3)` → MATCH.

## Remaining limitation

The Dr.Mario figure and the magnifier viruses are still not restored (decorative sprites built
by the skipped main-loop phase). The board (bottle + viruses), falling capsule, and next-pill
preview — the study-relevant content — are all shown.

## DRSTUDY flag (`patch_cartridge_copro.py`)

`apply_study_pause()` locates the pause routine via a stable, never-edited 12-byte anchor,
asserts each target holds an accepted original **or** the already-patched value (idempotent),
writes the preview blob into dead padding (asserting it is filler or already ours), and fails
loudly otherwise. Default **ON** when `DRHUMAN=1`; disable with `DRSTUDY=0`. Note:
`drmario_v28cs.nes` (the copro build base) already carries 2 of the 5 pause edits from an
earlier partial attempt, so on the carts 4 new writes are made (3 edits + blob).

Builds (all `tmp/`, gitignored):
- `drmario_study.nes` — base ROM + study patch (emulator use, mapper 1). Rebuild:
  `python3 -c "from patch_cartridge_copro import apply_study_pause as f; d=bytearray(open('drmario.nes','rb').read()); f(d); open('tmp/drmario_study.nes','wb').write(d)"`
- `drmario_copro_pocket_nofreeze_study.nes` — `DRHUMAN=1 DRPOCKET=1 DRNOFREEZE=1`
- `drmario_copro_human_study.nes` — `DRHUMAN=1 DRNOFREEZE=1` ($5200 window)

**Copro-cart validation basis:** mapper 100 is not Mesen-emulable, so the carts are validated by
the base-ROM Mesen proof above **plus** byte-level asserts that the pause opcodes were found at
the same offsets and the blob landed in confirmed-dead padding (`$D2CC` is filler in base,
v28cs, and both carts; the blob is present in both fixed-bank copies of the expanded cart). The
carts run in VS-CPU mode; **pause-reachability and 2P preview correctness are not emulator-
verified**. Before surgically byte-patching any already-deployed cart, confirm `$D2CC-$D2FF` is
still dead in that binary.
