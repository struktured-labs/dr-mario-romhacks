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

## The patch (5 edits inside `$97B6`–`$97F2` + a 5-part routine at `$D2CC`/`$9FF8`/`$A371`/`$BE56`/`$BC26`)

| CPU addr | before | after | effect |
|---|---|---|---|
| `$97B6` | `20 54 B6` `JSR $B654` | `20 70 B6` `JSR $B670` | entry wait, no OAM clear |
| `$97BA` | `A9 16` `LDA #$16` | `A9 1E` `LDA #$1E` | keep background rendering ON |
| `$97C4` | `20 94 B8` `JSR $B894` | `EA EA EA` NOP | drop entry OAM clear |
| `$97D3` | `20 F6 88` `JSR $88F6` | `20 CC D2` `JSR $D2CC` | draw STUDY text + both previews (v3.3) |
| `$97E2` | `20 54 B6` `JSR $B654` | `20 70 B6` `JSR $B670` | loop wait, no OAM clear |

Base-ROM file offsets (`= CPU − $8000 + $10`): `$17C7`(`54→70`), `$17CA`(`16→1E`),
`$17D4`–`$17D6`(`→EA EA EA`), `$17E3`–`$17E5`(`→20 CC D2`), `$17F3`(`54→70`).

**STUDY-draw routine (v3.3)** — a five-part trampoline in dead padding **filler in base AND v28cs**
(part1 in the fixed bank; parts 2-3c in bank 0, where the pause routine already runs so they are always
mapped). It reconnects "STUDY" AND draws **both players'** next-pill previews during pause, **without
disturbing any capsule, in 1P / 2P / VS**. STUDY → OAM slots 32-36, P1 preview → 37-38, P2 preview
(2P/VS only) → 39-40 — all **above the slot-15 gameplay-buffer max**, so both capsules (slots 0-3 in
2P/VS) stay byte-untouched. Both players consume the shared pill sequence at different rates, so P2's
next pill (`$039A/$039B`) differs from P1's (`$031A/$031B`) and is drawn separately (the game itself
draws both — `$87DA` P1 @ X=$38, `$87FE` P2 @ X=$B8). In 2P/VS the STUDY letters are also **lifted**
(part3c) to clear the score header (see below).

```
part1 @ $D2CC (52 B, fills the run):
  LDA #$80 / STA $42 / JSR $88F6      ; STUDY -> slots 32-36
  LDA $031A/ORA #$60/STA $0295        ; P1 slot37 tile         LDA $031B/ORA #$70/STA $0299  ; P1 slot38
  LDA #$02 / STA $0296 / STA $029A    ; P1 attr
  LDA #$45 / STA $0294 / STA $0298    ; P1 Y=$45  (1P default)
  LDA #$BE / STA $0297 ; LDA #$C6 / STA $029B  ; P1 X=$BE/$C6 (1P)      JMP $9FF8
part2 @ $9FF8 (34 B):
  LDY $0727 / DEY / BEQ RTS           ; 1P -> keep part1's defaults, no P2
  LDA #$33 / STA $0294/$0298/$029C/$02A0   ; all four preview Y = $33 (2P/VS)
  LDA #$38 / STA $0297 ; LDA #$40 / STA $029B  ; P1 X = $38/$40         JMP $A371
part3a @ $A371 (27 B):
  LDA $039A/ORA #$60/STA $029D        ; P2 slot39 tile         LDA $039B/ORA #$70/STA $02A1  ; P2 slot40
  LDA #$02 / STA $029E / STA $02A2    ; P2 attr                JMP $BE56
part3b @ $BE56 (13 B):
  LDA #$B8 / STA $029F ; LDA #$C0 / STA $02A3  ; P2 X = $B8/$C0 (above P2 board)   JMP $BC26
part3c @ $BC26 (18 B):
  LDA #$08 / STA $0280/$0284/$0288/$028C/$0290 ; 2P/VS: STUDY Y (slots 32-36) $0F -> $08   RTS
```

Why slots 32-40: `$88F6` (a shared drawer, 37 call sites) writes starting at slot `$42/4`; `$42` is 0
at pause entry, and in 2P/VS the capsules occupy slots 0-3 while the full 2-player buffer only reaches
slot 15, so `$42=$80` (STUDY → 32-36) plus previews at 37-40 land **above everything**, untouched. No
color mask needed: the game's own preview (`$8772`) uses `template + color` (ADC) and never masks, so
raw colors are 0-2 and `$60|c == $60+c`. Positions match the game's own previews per mode (1P P1
`Y=$45 X=$BE/$C6`; 2P/VS P1 `Y=$33 X=$38/$40`, P2 `Y=$33 X=$B8/$C0`).

**STUDY lift (part3c, 2P/VS only):** `$88F6` draws STUDY at the base Y (`$45` → OAM Y=`$0F`, sprite
rows 16-23). In the 2P/VS layout the header box's topmost pixel row is screen row 18 (measured in
Mesen — the "1P/2P" label; checkerboard above it), so rows 16-23 overlap it. part3c rewrites the five
STUDY letters' OAM Y (slots 32-36 = `$0280/$0284/$0288/$028C/$0290`) to **`$08`** (sprite rows 9-16):
clears the header (1-px gap above row 18) and stays below scanline 8 so it survives an NTSC top-8-line
CRT trim. Valid window was Y ∈ [7,9]; `$08` was chosen for a legibility gap with overscan margin. 1P
never reaches part3c (part2 returns first), so **1P STUDY stays at `$0F`, byte-for-byte unchanged**.

## Validation

**v3.3, TE v6 ROM, Mesen headless — `tmp/study_v3/` (`te33_{1p,2p,vs}_*`, `te32_2pd_*`).** Validated on
the full public build (`tmp/drmario_te_v6.nes` = base + VS-CPU + STUDY apparatus + this study-pause) in
**all three** game modes. STUDY at slots 32-36 (`$0D $A0 $0C $A1 $A2` = S,T,U,D,Y); pill-y frozen 90
frames (`$2001`=`$1E`); clean resume.

- **1-player** (`$0727=1`): STUDY **Y=15** (unchanged); capsule slots 0-1 untouched; single P1 preview
  at `Y=69 X=190/198` (right box); P2 slots 39-40 stay off-screen. **1P paused OAM is byte-identical to
  v3.2** (diffed).
- **2-player** (`$0727=2 $04=0`): STUDY **Y=8** (lifted, clears the header — screenshot `te33_2p_paused`);
  all four capsule halves (slots 0-3) byte-unchanged (P1 X=56/64, P2 X=184/192); P1 preview `Y=51 X=56/64`,
  P2 preview `Y=51 X=184/192`. On-screen 13.
- **2-player, diverged** (`te32_2pd`, P1 fast-dropped ahead of idle P2): P1next=`$00/$01`, P2next=`$00/$00`
  → P1 preview tiles `$60/$71` vs P2 `$60/$70` — **the two previews show each player's actual, different
  next pill** (proof per-player, not copies); both capsules untouched.
- **VS CPU** (`$0727=2 $04=1`): STUDY **Y=8** (lifted); P2 preview at slots 39-40 (X=184); capsule
  untouched; pill frozen (y stable across pz+30/60/90).

The pause path (`$978E`, single call site `$814B`) is shared across modes; part2 keys off `$0727` so the
previews (and the STUDY lift) apply to 2P/VS but not 1P. **Cart basis:** copro carts are mapper 100 (not
Mesen-emulable); the 2P *base* test reproduces the both-capsules-in-buffer layout the cart
exhibits, and the same asserted bytes are applied.

**Earlier proofs (superseded):** v3.1 (`te31_*`, P1 preview only), v3 (slots 2-6/7-8, clobbered P2
capsule in 2P/VS), v2 (`tmp/study_pause/`, preview-only slots 2-3, no STUDY text).

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
