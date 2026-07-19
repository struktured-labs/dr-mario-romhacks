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
| `$97D3` | `20 F6 88` `JSR $88F6` | `20 CC D2` `JSR $D2CC` | draw STUDY text + preview (v3 routine) |
| `$97E2` | `20 54 B6` `JSR $B654` | `20 70 B6` `JSR $B670` | loop wait, no OAM clear |

Base-ROM file offsets (`= CPU − $8000 + $10`): `$17C7`(`54→70`), `$17CA`(`16→1E`),
`$17D4`–`$17D6`(`→EA EA EA`), `$17E3`–`$17E5`(`→20 CC D2`), `$17F3`(`54→70`).

**STUDY-draw routine (v3)** at CPU `$D2CC` (file `$52DC`) — 50 bytes of dead padding after the
routine ending `$D2CB RTS`, **filler in base AND v28cs** (52-byte run), reachable via JSR from the
pause loop (fixed bank). It does BOTH jobs the single `$97D3` call site must now cover — reconnect
the "STUDY" text AND draw the preview — without clobbering the frozen capsule:

```
LDA #$08 / STA $42               ; OAM cursor = 8 -> $88F6 writes STUDY into slots 2-6
JSR $88F6                        ; the game's letter drawer, drawing the STUDY quads ($53=0);
                                 ;   leaves the capsule at slots 0-1, ends with $42=28
LDA $031A / ORA #$60 / STA $021D ; slot7 tile = $60|colorA  (preview left half)
LDA $031B / ORA #$70 / STA $0221 ; slot8 tile = $70|colorB  (preview right half)
LDA #$45  / STA $021C / STA $0220 ; Y = 69  (both halves)
LDA #$02  / STA $021E / STA $0222 ; attr = 2 (palette)
LDA #$BE  / STA $021F             ; slot7 X = 190
LDA #$C6  / STA $0223             ; slot8 X = 198
RTS
```

Why `$42=8`: `$88F6` (a shared drawer with 37 call sites) writes its sprite list starting at OAM
slot `$42/4`, and `$42` is 0 at pause entry — so an unguarded `JSR $88F6` would draw the 5 STUDY
letters into slots 0-4 and **overwrite the falling capsule** (slots 0-1). Presetting `$42=8` moves
the letters to slots 2-6 and spares the capsule. No color mask is needed: the game's own preview
(`$8772`) computes `template + color` (ADC) and never masks, so the raw colors are 0-2 and
`$60|c == $60+c`. Slot map while paused: **0-1 capsule, 2-6 STUDY, 7-8 preview.**

Position/tile/attr match the game's own preview exactly (Mesen byte-verified: `nextA=$01 nextB=$00`
→ tiles `$61/$70`, `Y=$45`, `X=$BE/$C6`, `attr=$02`).

## Validation

**v3 (STUDY text + preview), TE v6 ROM, Mesen headless — `tmp/study_v3/`.** The v3 blob was
validated on the full public build (`tmp/drmario_te_v6.nes` = base + VS-CPU + STUDY apparatus +
this study-pause) in **both** game modes:

- **1-player** (`te_v6_1p_*`): paused OAM = slots 0-1 capsule (`$62/$72`), 2-6 STUDY
  (`$0D $A0 $0C $A1 $A2` = S,T,U,D,Y at Y=15), 7-8 preview (`$61/$70` at Y=69, X=190/198 —
  matches the game's own preview for `next=$01/$00`); pill-y frozen at 11 for 90 frames
  (`$2001`=`$1E`), clean resume (on-screen 46 → 9 paused → 46).
- **VS CPU** (`te_v6_vs_*`, `$0727=2 $04=1`): identical slot map and freeze/resume; capsule X
  reflects P1's left board. The pause path (`$978E`, single call site `$814B`) is shared, so
  1P and VS behave identically. Minor: in VS the STUDY sprites sit at the very top and slightly
  overlap the 2-player score header (cosmetic; the VS background layout owns that row).

**v2 base-ROM proof (superseded)** — `tmp/study_pause/`: earlier preview-only blob (slots 2-3,
no STUDY text), byte-verified `$60|($031A&3)` / `$70|($031B&3)` tiles.

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
