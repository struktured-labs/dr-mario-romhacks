# TE v8 branding — copro-cart folding spec

How to add the TE v8 title branding (`TRAINING EDITION` subtitle + `V8.00 STRUK LABS` footer) to
the **coprocessor carts** (v28cs depth-2 core + DRSTUDY v3.3, mapper 100, 64 KB PRG).

Status: **byte-precondition-verified, NOT hardware-validated.** Mapper-100 carts are not
Mesen-emulable; the base-ROM v8 is fully Mesen-validated, and every fold precondition below is
asserted against the real study-v3.3 core, but the folded cart itself must be checked on
MiSTer/Pocket. All offsets/asserts here come from `tmp/cart_fold_check.py`.

## 1. Cart PRG layout (authoritative: `expand_prg.py`)

The game runs MMC1 in 32 KB PRG-switch mode. `expand()` turns the 32 KB core into 4×16 KB banks:

| index | file range | mapping | contents |
|-------|-----------|---------|----------|
| 0 | `0x00010-0x0400F` | unit0 `$8000-$BFFF` | original low half |
| 1 | `0x04010-0x0800F` | unit0 `$C000-$FFFF` | original high half (vectors, fixed AI, study `part1`) |
| 2 | `0x08010-0x0C00F` | unit1 `$8000-$BFFF` | depth-2 search code (mapped only when PRG-bank=2) |
| 3 | `0x0C010-0x1000F` | unit1 `$C000-$FFFF` | duplicate of index 1 (so the high half is always mapped) |

At reset PRG-bank=0 → **unit0 = the original 32 KB runs the title, menus, gameplay and study
pause.** The title footer hook, the relocated footer routine (`$C0A9`) and the metasprite
(`$CF00`) all live in unit0. **Fold the branding into the 32 KB v28cs core BEFORE `expand()`** —
`expand()` then duplicates the high-half edits into index 3 and carries the CHR through unchanged.

## 2. What folds UNIFORMLY (identical bytes/offsets to base-ROM v8) — verified filler

Applied to the study-v3.3 v28cs core (`drmario_v28cs.nes` + `apply_study_pause`):

| piece | file offset | CPU | precondition (verified) | write |
|-------|-------------|-----|--------------------------|-------|
| title hook | `0x0C34` | `$8C24` | `== 20 F6 88` (JSR $88F6) ✓ | `20 A9 C0` (JSR `$C0A9`) |
| footer routine (23 B) | `0x40B9` | `$C0A9` | 24-byte run filler ✓ | `footer_routine(data_cpu)` |
| footer CHR tiles `0xE8-0xEF` (pg 2) | `0x0AE90-0x0AF0F` | — | filler ✓ | 8 footer tiles |
| subtitle CHR (title pages 3/4) | see `title_screen.py` | — | `TITLE_TOP` tiles == base ✓ | subtitle overlay |
| title tilemap | `0x3B06-0x3B0F` | — | `== 42 FC×9` (untouched) ✓ | *(no write)* |

So the **subtitle is a zero-risk, byte-identical fold** (pure CHR on pages 3/4; the title
nametable is untouched, so the attract-demo handoff is preserved exactly as on the base ROM), and
the **footer routine + hook fold uniformly** at `$C0A9`.

## 3. The one conflict: the 33-byte footer metasprite table

Base-ROM v8 puts the metasprite at **`$CF00`** (file `0x4F10`). On the cart that run is **occupied
by the depth-2 AI's `swap_eval`** (`0x4F10` first bytes `a5 01 d0 01 60 …`, filler=False). And a
study-v3.3 core has **no ≥33-byte always-mapped free run** left:

- high half (`$C000-$FFFF`): only 24-byte runs survive (`$C0A9`, `$C0EF`, and the `$CAED…$CCA8`
  series) — the routine takes `$C0A9`; none is ≥33 B for the table.
- bank0 (`$8000-$BFFF`): largest free run 22 B.
- bank2 tails are large (82-180 B) but map at `$8000` only under PRG-bank=2, so a title-time
  pointer read cannot reach them, and `$8906` (the renderer) is itself in the low half that
  bank-switching would replace.

`apply_training_edition_title(core, data_off=0x4F10, …)` therefore raises
`title footer metasprite space at 0x4F10 is not unused` — the assertion correctly refuses a bad
overwrite.

### Resolution options (pick per build; ranked)

1. **Subtitle-only fold (recommended default).** Apply §2 minus the footer routine/hook/CHR. The
   cart gets `TRAINING EDITION` with zero PRG conflict. The credit footer is a nicety on an
   autoplay demo cart where the title only flashes by; skipping it costs nothing visible in play.
2. **Free `$CF00`, then fold uniformly.** Build the depth-2 core without `color_swap` (or relocate
   `swap_eval`'s 48 B into a bank2 tail — it is AI code that already runs under unit1). That frees
   `$CF00`, after which the footer table lands at `$CF00` byte-identically with base-ROM v8. Assert
   `set(core[0x4F10:0x4F10+33]) <= {0x00,0xFF}` before writing.
3. **RAM-staged table.** Keep the table in a bank2 tail; extend the footer routine to `_sel(2)`,
   copy 33 B into a free RAM buffer, `_sel(0)`, point `$47/$48` at RAM, `JSR $8906`. Costs extra
   routine bytes (won't fit the 24-byte `$C0A9` run) + a 33-byte RAM scratch; only worth it if the
   credit is required and the AI can't be rebuilt.

## 4. Verification snippet (run before patching any specific cart core)

```python
from patch_cartridge_copro import apply_study_pause
from title_screen import apply_training_edition_title            # te-v8 parameterized module
core = bytearray(open("drmario_v28cs.nes","rb").read()); apply_study_pause(core)   # v3.3 core
assert bytes(core[0x0C34:0x0C37]) == b"\x20\xF6\x88"             # hook original
assert set(core[0x40B9:0x40B9+23]) <= {0x00,0xFF}               # routine run free
DATA = 0x4F10                                                    # base home; assert free OR relocate
free = set(core[DATA:DATA+33]) <= {0x00,0xFF}
apply_training_edition_title(core, routine_off=0x40B9,
    data_off=(DATA if free else <cart-free ≥33B run>), footer_text="V8.00 STRUK LABS")
# then: expand(core-as-2bank, out, new_bank_bytes=<AI bank2>) ; set mapper-100 header bytes
```

Fold into the 32 KB core, THEN `expand()` + set the mapper-100 header (`out[6]|=0x40`, `out[7]|=0x60`),
exactly as `patch_cartridge_copro.main()` does today. Verify on MiSTer/Pocket that the title shows
the subtitle (and footer, if folded) and that VS-CPU autoplay + study pause are unaffected.
