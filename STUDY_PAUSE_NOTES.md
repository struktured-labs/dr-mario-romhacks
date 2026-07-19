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

## The patch (5 edits inside `$97B6`–`$97F2` + a 2-part routine at `$D2CC`/`$9FF8`)

| CPU addr | before | after | effect |
|---|---|---|---|
| `$97B6` | `20 54 B6` `JSR $B654` | `20 70 B6` `JSR $B670` | entry wait, no OAM clear |
| `$97BA` | `A9 16` `LDA #$16` | `A9 1E` `LDA #$1E` | keep background rendering ON |
| `$97C4` | `20 94 B8` `JSR $B894` | `EA EA EA` NOP | drop entry OAM clear |
| `$97D3` | `20 F6 88` `JSR $88F6` | `20 CC D2` `JSR $D2CC` | draw STUDY text + preview (v3.1 routine) |
| `$97E2` | `20 54 B6` `JSR $B654` | `20 70 B6` `JSR $B670` | loop wait, no OAM clear |

Base-ROM file offsets (`= CPU − $8000 + $10`): `$17C7`(`54→70`), `$17CA`(`16→1E`),
`$17D4`–`$17D6`(`→EA EA EA`), `$17E3`–`$17E5`(`→20 CC D2`), `$17F3`(`54→70`).

**STUDY-draw routine (v3.1)** — a two-part trampoline in dead padding **filler in base AND v28cs**.
It reconnects the "STUDY" text AND draws the next-pill preview during pause, **without disturbing any
capsule, in 1-player *and* 2-player/VS layouts**. (v3 drew STUDY into slots 2-6 and the preview into
7-8; that clobbered P2's capsule at slots 2-3 in 2P/VS — confirmed on real Pocket hardware.)

**part1** @ CPU `$D2CC` (file `$52DC`; padded with `$00` to 50 B):
```
LDA #$80 / STA $42               ; OAM cursor = 128 -> $88F6 writes STUDY into slots 32-36
JSR $88F6                        ; game's letter drawer ($53=0); STUDY at Y=$45/X=$70.. (top)
LDA $031A / ORA #$60 / STA $0295 ; slot37 tile = $60|colorA   (preview left half)
LDA $031B / ORA #$70 / STA $0299 ; slot38 tile = $70|colorB   (preview right half)
LDA #$02  / STA $0296 / STA $029A ; attr = 2 (both halves)
JMP $9FF8                         ; -> part2 (mode-correct Y/X, then RTS)
```
**part2** @ CPU `$9FF8` (file `$2008`, bank 0 — the pause routine itself runs here, so it is mapped):
```
LDA #$45 / LDX #$BE              ; 1P defaults: Y=$45 (69), XL=$BE (190) — right-side "next" box
LDY $0727 / DEY / BEQ w          ; player mode: 1 -> 1P (keep defaults); 2 -> 2P/VS (override)
LDA #$33 / LDX #$38             ; 2P/VS: Y=$33 (51), XL=$38 (56) — above P1's left board
w: STA $0294 / STA $0298         ; slot37/38 Y
   STX $0297                     ; slot37 X = XL
   TXA / CLC / ADC #$08 / STA $029B  ; slot38 X = XL + 8
   RTS
```

Why slots 32-36 / 37-38: `$88F6` (a shared drawer, 37 call sites) writes starting at slot `$42/4`.
At pause entry `$42` is 0 and, in 2P/VS, the capsules occupy slots 0-3 (P1 0-1, P2 2-3) while the
full 2-player buffer only reaches slot 15 — so writing STUDY at slots 32-36 and the preview at 37-38
(via `$42=$80`) lands **above every capsule/preview**, leaving them untouched. No color mask is
needed: the game's own preview (`$8772`) computes `template + color` (ADC) and never masks, so raw
colors are 0-2 and `$60|c == $60+c`. Position/tile match the game's own preview exactly in each mode
(Mesen byte-verified, `next=$01/$00`: 1P `Y=$45 X=$BE/$C6`; 2P/VS `Y=$33 X=$38/$40`; tiles `$61/$70`).

## Validation

**v3.1, TE v6 ROM, Mesen headless — `tmp/study_v3/` (`te31_{1p,2p,vs}_*`).** Validated on the full
public build (`tmp/drmario_te_v6.nes` = base + VS-CPU + STUDY apparatus + this study-pause) in **all
three** game modes. STUDY always at slots 32-36 (`$0D $A0 $0C $A1 $A2` = S,T,U,D,Y, Y=15); preview at
slots 37-38 (`$61/$70`); pill-y frozen for 90 frames (`$2001`=`$1E`); clean resume.

- **1-player** (`$0727=1`): capsule slots 0-1 (`$62/$72` X=120/128) untouched; preview at
  `Y=69 X=190/198` (right box). On-screen 46 → 9 paused → 46.
- **2-player** (`$0727=2 $04=0`) — the regression test that reproduces the cart's buffer: **BOTH**
  capsules survive — P1 slots 0-1 (X=56/64) and **P2 slots 2-3 (X=184/192)** are byte-unchanged;
  preview at `Y=51 X=56/64` (above P1's left board). On-screen 11 paused.
- **VS CPU** (`$0727=2 $04=1`): capsule slots 0-1 untouched; preview at `Y=51 X=56/64` (same as 2P).

The pause path (`$978E`, single call site `$814B`) is shared across modes, and part2 keys off `$0727`
(1 vs 2), so the preview lands in the game's own per-mode "next" position. Minor cosmetic: the STUDY
sprites sit at the very top and slightly overlap the 2-player score header (the VS layout owns that
row). **Cart basis:** copro carts are mapper 100 (not Mesen-emulable); the 2P *base* test reproduces
the both-capsules-in-buffer layout the cart exhibits, and the same asserted bytes are applied.

**Earlier proofs (superseded):** v3 (`te_v6_*`, slots 2-6/7-8, clobbered P2 capsule in 2P/VS);
v2 (`tmp/study_pause/`, preview-only slots 2-3, no STUDY text).

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
