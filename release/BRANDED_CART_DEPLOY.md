# Branded copro-cart deploy pipeline (standing)

**Mandate:** every deployed coprocessor cart (MiSTer AB duel + Pocket human/slam) ships on the
**TE v8 branded base** — the `TRAINING EDITION` title logo + `V8.00 SL` version footer must be
visible. The public TE v8 BPS is the byte-basis; a cart is strictly *public TE v8 branding + the
driver/AI additions*, with zero divergent branding bytes.

The branding is **cart-side** (rendered by the ROM's own title code) and **byte-disjoint** from the
depth-2 AI, the DRSTUDY chain, and the coprocessor driver. So it composes with any driver lineage.

## Two equivalent build paths (proven byte-identical)

**A. Bake-in (v28cs → branding → driver → expand)** — `build_copro_branded.py`:
```
cd <canonical-driver-worktree>          # its patch_cartridge_copro.py is picked up from cwd
TE_DIR=~/projects/dr-mario-te-v8 [DRHUMAN=1 DRPOCKET=1 ...] \
  python $TE_DIR/build_copro_branded.py drmario_v28cs.nes tmp/<cart>.nes
```
Brands the clean 32 KB core, then runs the driver, whose `expand()` duplicates the branded high
half into index 3.

**B. Overlay a finished cart (driver → expand → branding)** — `brand_copro_cart.py`:
```
python brand_copro_cart.py <finished_cart>.nes tmp/<cart>_te.nes tmp/drmario_te_v8.nes
```
Overlays the identical branding onto an already-built mapper-100 cart (adjusts CHR_START for the
64 KB PRG and duplicates the high-half branding into index 3). **Use this for combo-port's
freeze-fixed Pocket cart and the future DRNAVFIX cart** — brand whatever the driver produces.

Path A and Path B produce the **byte-identical** cart (verified: AB cart md5 matches both ways).

## Branding bytes (identical to public TE v8)

| piece | file offset(s) | value |
|-------|----------------|-------|
| title hook | `0x0C34` | `20 A9 C0` (JSR `$C0A9`) |
| footer routine (23 B) | `0x40B9` + index-3 `0xC0B9` | `footer_routine($C0EF, base_x=$70)` |
| footer metasprite (17 B) | `0x40FF` + index-3 `0xC0FF` | 4-tile `V8.00 SL` table + `$80` |
| footer CHR `0xE8-0xEB` | CHR page 2 | 4 tiles |
| subtitle CHR | CHR pages 3/4 | 10 tiles ×2 |
| `™`→`TE` mark CHR `$0F` | CHR pages 3/4 | 1 tile ×2 |

`brand_copro_cart.py` asserts, for every cart: (1) the runs are filler pre-brand; (2) **only** these
bytes change (⇒ DRSTUDY chain `$D2CC/$9FF8/$A371/$BE56/$BC26` + driver wrapper `$FF54` + AI bank 2
are byte-intact — 0 stray); (3) every branding byte equals public TE v8. A green run gates a deploy.

## Carts produced (this pass, driver = canonical b92ec32 slam-maturity)

| cart | flags | study | branded md5 | staged |
|------|-------|-------|-------------|--------|
| `drmario_copro_ab_slam_te.nes` | *(default: DRROTFIX+DRSLAM+MATURE)* | no (CPU-vs-CPU) | `4536242d…` | `tmp/` |
| `drmario_copro_pocket_slam_mat_te.nes` | `DRHUMAN=1 DRPOCKET=1` | yes (v3.3) | `ba61cc61…` | `tmp/` |

Unbranded canonical references: AB `d14f0bee…`, Pocket `a2609cf1…`.

## Validation

- **Branding renders** — the branded cart core (unit 0, a Mesen-emulable mapper-1 ROM) shows
  `Dr. MARIO ᵀᴱ`, `TRAINING EDITION` + `V8.00 SL` on the title (menu is clean — the v6/v17
  middle-row artifact is not in the v28cs lineage). The human/Pocket cart lingers on the title.
- **Study + branding coexist** — the Pocket core (v28cs + study-v3.3 + branding) still shows the
  frozen board, `STUDY` (OAM 32-36) and the next-pill preview (37-38) on pause.
- Mapper-100 carts are not Mesen-emulable, so the assembled cart itself needs a MiSTer/Pocket check
  (title shows on auto-nav; VS-CPU auto-play + study pause unaffected). Byte-identity to the
  validated public ROM means only the brief on-cart title *appearance* is unverified, not its content.

## Coordination notes

- Driver lineage: build against **canonical b92ec32** (slam maturity). When **DRNAVFIX** (driver-nav)
  merges, rebuild the AB cart as `..._ab_slam_nav_te.nes` — the branding overlay is unchanged.
- **combo-port's Pocket freeze-fix** rolls forward under the same overlay: brand combo-port's
  freeze-fixed cart with `brand_copro_cart.py` (branding is independent of the freeze/core).
- Every future cart deploy runs `brand_copro_cart.py` (or path A) and checks the green assertions.
