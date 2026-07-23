# Dr. Mario (NES) ROM Architecture Survey

**Purpose.** Mine the community's accumulated knowledge of the Dr. Mario (NES) ROM to
build an architecture map for the TE v9 roadmap, and to identify the DRMC tournament
build (issue #4). Primary evidence: the two public disassemblies, the Dr. Mario
Community wiki, and **byte-level diffs of the community IPS patches applied to our exact
base ROM**.

**Our base ROM.** `drmario.nes`, md5 `d3ec44424b5ac1a4dc77709829f721c9`. This is
bit-identical to brianhuffman's `drmario.nes` reference, i.e. **Dr. Mario (Japan, USA)
Rev 0** (the common USA cart). Rev A is a *different* ROM (md5 `8181d696…`); the
Nostaljipi disassembly builds Rev A, brianhuffman builds both. Every community NES patch
surveyed here applies cleanly to our Rev 0 base at sensible code offsets, so they are all
built against the same ROM we ship on.

**Method / access note.** `romhacking.net` (RHDN) now sits behind a Cloudflare
challenge; neither WebFetch nor curl can scrape its game/hack pages, and archive.org is
also blocked to our fetcher. The RHDN census below is therefore assembled from search
snippets plus cross-references, and is *best-effort* on descriptions. The architecture and
patch-footprint sections do **not** depend on RHDN — they come from the GitHub
disassemblies, Data Crystal, the drmar.io wiki, and direct IPS diffing, which are stronger
sources than RHDN prose anyway. Reproduce with `tools/ipsdiff.py` (single-patch footprint),
`tools/analyze_overlap.py` (TE × community byte-overlap), `tools/disasm_drmc.py` (DrMC
feature dissection).

---

## 1. Census — hacks, disassemblies, tools

### 1a. NES ROM hacks

Two distribution channels exist and only partly overlap: **romhacking.net** (older,
general-audience hacks) and **playdm.net** (the Dr. Mario Championship community's own
patch host, curated on `wiki.drmar.io`). The competitive/tournament-relevant work lives on
playdm.net, not RHDN.

| Hack | Source | What it changes | Roadmap interest |
|---|---|---|---|
| **DR. MARIO TE (Training Edition)** #9292 | RHDN (ours) | Pause → study mode | ours |
| **Dr. Mario Turbo** #6158 | RHDN + playdm | Halves clear/drop time, adds **hard-drop (Up)**, SNES RNG, better VS garbage; expands ROM to 128K+128K, new CHR | speed/garbage mechanics |
| **Dr. Mario NROM Hack** #7640 | RHDN | MMC1→NROM mapper conversion (tilesets/anims dropped) | mapper reference |
| **Dr. Mario – no punish** #3330 | RHDN | Removes VS punishment blocks on 2+ combos | garbage logic |
| **Dr. Mario – 2 Players Inverse** #2792 | RHDN | Same virus layout both sides, colors swapped per side | virus-placement mirror |
| **Dr. Mario Combo Levels** #5922 | RHDN | Combo-oriented level set | level tables |
| **Dr. Wario** #647 | RHDN | WarioWare "Dr. Wario" reskin | cosmetic |
| **Super Dr. Mario Bros.** #6962 | RHDN | *SMB1* hack (platformer), not the DM engine | out of scope |
| **Dr. Mario DX** #5281 | RHDN | Cosmetic/QoL DX-style hack | cosmetic |
| **DrMC (seed + speed)** `Dr._Mario_-_DrMC_v1.0.ips` | **playdm.net** | **Seed select+display, fine-speed display, ULT speed, disables music select** | **the tournament build — see §4** |
| **Seed mod** `Dr._Mario_-_Seed.ips` | playdm.net | Seed select+display via menu ("Down" from music), deterministic pills | seed UI |
| **Speed display mod** | playdm.net (Discord CDN) | Shows combined/fine speed instead of LOW/MED/HI | SPD readout |
| **Level cap mod** | playdm.net (Discord CDN) | Removes the level-24 cap | extended study |
| **SNES RNG mod** `Dr_Mario_SNES_RNG.ips` | playdm.net | Swaps NES pill RNG for the SNES algorithm | RNG swap |
| **God speed** `Dr_Mario_IL_Stars_Japan_USA.ips` | playdm.net | Seeds pinned to per-level world-record seeds | seed pinning |
| **Self-garbage / Combo-rollback / Combo-only** | playdm.net | VS-garbage-to-self; retry on non-combo; reset-unless-full-clear | training variants |
| **Versus Trainer v1 / v2** | playdm.net | AI-opponent practice, difficulty via 2P level select | AI-practice |

SNES-only community hacks (for completeness): **Statistics mod**, **Seed+Stats mod**
(playdm.net) — in-game timers (Throw/Drop/Land/Clear/Fall) and seed select.

> **Disambiguation for issue #4:** RHDN **#8245 "Dr. Mario Tournament Edition" is a
> SNES/SFC hack** (updated Nov 2023), unrelated to the DRMC NES broadcast build. Do not
> confuse it with the NES tournament ROM.

### 1b. Disassemblies (the highest-value architecture resource)

| Project | Builds | Toolchain | Notes |
|---|---|---|---|
| **Nostaljipi/dr-mario-disassembly** | Rev A | ASM6f | Fully labeled, modular: `defines/` (RAM, ZP, constants, registers), `data/drmario_data_game.asm` (all tables), `prg/` split by subsystem (game_logic, level_init, level_end, visual_*, audio_*), and an **`unused/` dir documenting every free region** ($CED5, $D2CC, $FAFD, $FF32, $FFD9, EU $FC29). This is the reference to port our planner/AI against. |
| **brianhuffman/drmario** | Rev 0 **and** Rev A | ca65 | `make all` / `make test` with md5 verification; `drmario.nes.md5` == our base. Good for byte-exact rebuilds and revision checks. |

RHDN forum thread **#33836 "Dr.Mario NES Disassembly"** (Nostaljipi, Nov 2021) is the
announcement for the first project.

### 1c. Tooling ecosystem (all by **dmwit** unless noted — the community's technical anchor)

| Tool | What it is |
|---|---|
| **dmvs** (`github.com/dmwit/dmvs`) | fceux Lua for online 1v1 (host/connect). The netplay layer; also the natural place a broadcast memory-overlay would hook. |
| **maryodel** (`github.com/dmwit/maryodel`) | dmwit's Dr. Mario engine (Haskell): board model, **exact RNG (`advanceRNG`/`decodeColor`/`decodePosition`)**, pathfinding, fceux client. The authority on the seed encoding (§4b). |
| **dr-mario-ngrams** | Exact reimplementation of the NES pill-generation RNG + statistics; ships a 32767-seed pill-sequence corpus |
| **seed map** (`dmwit.com/dr_mario_seed_map.bin`) | Successive-seed data; index = `65534*level + (seed & ~1) - 2` |
| **Granivore** (`tools.drmar.io/granivore`) | Identifies the exact seed from a board state |
| **Identify** (`tools.drmar.io/identify`) | ROM-variant validator (patches are ROM-specific) |
| **DM Glampers** | Level-range calculator for timed races/tournaments |
| **MC Mario** | Elo-style rating + handicap for 2P |
| **Bo Krif Ulse** | fceux maneuver-trainer (custom boards, repeat scenarios) |
| **DM Effects** | fceux "crowd-control" random-challenge mod |
| **meatfighter AI** (`meatfighter.com/drmarioai/`) | The 2017 Dr. Mario AI our roadmap already credits |

---

## 2. Architecture knowledge map (mechanism → known → address → source)

Addresses are CPU/RAM unless noted "file". Sources: **[DC]** Data Crystal, **[N]**
Nostaljipi disasm, **[Δ]** proven by our IPS diffs, **[mem]** our existing notes.

### 2a. RAM map — player state (`p1_RAM $0300`, `p2_RAM $0380`, `$30` bytes each) [N][DC]

| Addr (P1 / P2) | Meaning |
|---|---|
| `$0301-0304 / $0381-0384` | Falling pill colors, 1st–4th half (00=Yellow 01=Red 02=Blue) |
| `$0305 / $0385` | Falling pill X · `$0306 / $0386` Falling pill Y |
| `$030A / $038A` | **speedUps** (increments every 10 pills; capped) |
| `$030B / $038B` | **speedSetting** (LOW/MED/HI; frames form, 0x26 fast … 0x85 slow) |
| `$0312 / $0392` | **speedCounter** (compared against gravity table) |
| `$0316 / $0396` | **level** |
| `$031A-031B / $039A-039B` | **Next-pill preview** colors (1st/2nd half) — broadcast next-pill panel source |
| `$0320 / $03A0` | **speedIndex** ← the fine "SPD" number shown on the DRMC broadcast |
| `$0324 / $03A4` | **virusLeft** — broadcast "VIR" panel source |
| `$0325 / $03A5` | **fallingPillRotation** (00=orig 01=CCW 02=180 03=CW) — reconciles [mem]'s `$03A5`; DC's `$00A5` is the zero-page working copy |
| `$0327 / $03A7` | pillsCounter · `$0328/$03A8` virusToAdd · `$0329` attackColors(4B) |
| Playfield | P1 board `$0400-$047F` (8 cols × 16 rows = `$80` cells) [DC] |

Global/ZP [N][DC]: `$17` rng0, `$18` rng1, `$89` **rngSeed** (2 bytes), `$42`
spritePointer, `$43` frameCounter, `$46` mode, `$65` game-option cursor, `$F5/$F6` P1/P2
buttons pressed, `$F7/$F8` P1/P2 held, `$0727` number-of-players, `$0731` music type,
`$0740` anti-piracy flag (FF=on).

### 2b. Pill-generation RNG [Δ][N]

- **Entry the community replaces: `JSR $B771`**, called from exactly **4 sites** —
  `$82AD, $99DD, $9D0B, $9D3E` (file `0x2BD, 0x19ED, 0x1D1B, 0x1D4E`). Proven because
  `SNES_RNG.ips` and `Turbo.ips` redirect precisely these four `20 71 B7` instructions.
- Low-level primitive `randomNumberGenerator` (~`$B78B` [N]) rotates zp `rng0/rng1`
  ($17/$18); the 16-bit LFSR is specified exactly in §4b. Virus placement reads `rng0` for
  height, `rng1` for column/color, forcing one virus of each color per 4 (`rndColorQty=$01`).
- The **SNES RNG mod** is an 84-byte drop-in: 4 call-site redirects + a new generator at
  `$FB00`. This is the cleanest template for swapping RNG.

### 2c. Speed / gravity [Δ][N][mem]

- **Gravity table at `$A795`** (`LDA $A795,X`). Drop cadence: `speedUps ($030A) →
  speedIndex ($0320)`; the running `speedCounter ($0312)` must exceed `table[index]` for
  the pill to fall one row. `speedUps_max = $31` (49) caps the ramp.
- **The broadcast "SPD" number is `speedIndex $0320` / the `$A795` index** — DrMC hooks
  the table read at **`$8D8D`** (`LDA $A795,X` → `JSR $FC60`) to render it, and blanks the
  coarse LOW/MED/HI text (see §4a). The broadcast "Speed Guide" maps SPD 32→Tetris L7 …
  80→L29.

### 2d. Levels, viruses, field geometry (constants) [N]

`selectableLvCap=$14` (20), `lvCap=$18` (24, the level-cap mod's target),
`finalCutsceneLv=$14`; `match_length=$04`; field `rowSize=$08 × heightSize=$10 =
fieldSize=$80`; `pillStartingX=$03 pillStartingY=$0F`; `attackSize_min/max=$02/$04`;
`demo_virus=$44 demo_level=$0A`. Level init/virus placement: `toLevel $817E`,
`initData_level $8216`.

### 2e. Text / HUD tile data (file offsets) [DC][Δ]

Congrats screen `0x20CC` "CONGRATULATIONS-", `20DC` VIRUS, `20E1` LEVEL, `20E7` SPEED.
In-game coarse speed labels `0x224D/2251/2255` LOW/MED/HI (`$A23D`, **blanked by DrMC**).
Menu `0x3E49` "1 PLAYER GAME", `0x4075` MUSIC TYPE, `0x40E0/40E7/40EE` FEVER/CHILL/OFF
(**overwritten by DrMC** to reclaim space). Title logo GFX `0x3A29-0x3AC3`. The title-art
"pocket" beneath MARIO (tilemap anchor file `0x3B06`; subtitle rendered in **CHR**) is
shared by our TE subtitle **and** Dr. Mario Turbo's — the one TE×community collision (§3).
HUD label tile runs [N]: VIRUS=`$88-8C`, LEVEL=`$8E-92`, SPEED=`$C8-CC`, values `$95`/`$D4`.

### 2f. Community free-space convention [Δ][N]

**Every** community NES hack parks its new code in the **fixed-bank tail `$FB00-$FFFF`**
(file `0x7B10-0x7FFF`), which the disassembly documents as unused (`$FAFD/$FF32/$FFD9`).
DrMC uses `$FB00-$FFAF`, Seed `$FB00-$FC5x`, SNES-RNG `$FB00-$FB2A`, GodSpeed
`$FB00-$FB51`, Turbo `$FB00-$FC44`. **This is the single most important compatibility
fact** (see §3).

---

## 3. Overlap / conflict analysis vs OUR footprint (measured, byte-exact)

I built the real TE v7 ROM (`build_te_v7.py`, md5 `f9403fb1…`) and intersected its
changed-offset set with each community patch (`tools/analyze_overlap.py`):

| Community patch | bytes changed | TE v7 ∩ | verdict |
|---|---|---|---|
| DrMC v1.0 | 839 | **0** | clean — stacks |
| Seed | 458 | **0** | clean — stacks |
| SNES-RNG | 51 | **0** | clean — stacks |
| God speed | 84 | **0** | clean — stacks |
| Turbo | 228127 | 316 | collision — **CHR graphics only** |

**Headline: TE is byte-clean against the entire seed/SPD ecosystem (DrMC, Seed, SNES-RNG,
GodSpeed) — zero overlapping bytes.** TE can be layered on top of any of them (or they on
TE) with no code or data conflict, because every community hack lives in the fixed-bank
tail `$FB00-$FFFF`, whereas TE lives in the pause routine (`$97xx`), a footer routine at
`$BE56`, footer metasprite data at `$9FF9-$A017`, a sprite-table tweak at `$A959`, and CHR
— none of which the community touches.

**The only collision is Turbo, entirely in CHR graphics (316 bytes).** Both TE and Turbo
render a subtitle into the same title-art pocket and rewrite the same title/font CHR tiles
(`title_screen.py` itself notes "Dr. Mario Turbo uses the same pocket for its subtitle").
No PRG/code conflict. A TE+Turbo combo needs the subtitle relocated; every other combo is
free. (Turbo is also a whole-ROM 128K+128K replacement with a `DiskDude!` header — the
least stack-friendly hack regardless.)

Measured TE v7 footprint (75 runs): PRG `$8C25` (footer hook), `$97BA/$97C4/$97CC` (pause),
`$9FF9-$A017` (footer metasprite data), `$A959` (sprite table), `$BE56` (footer routine,
23 B); CHR title/subtitle/STUDY tiles. STUDY v3.3 additionally uses the unused `$D2CC`
block + nametable-gap routines (`$9FF8/$A371/$BC26`) — also outside every community
footprint. Internal-only note: our v6/v7 footer routine and STUDY v3.3 part3b both sit at
`$BE56` (deconflicted in the combined DRROTFIX build).

---

## 4. DrMC tournament ROM — deep dissection

Issue #4 identity is settled (see the issue-4 comment): the DRMC broadcast build is the
community **"DrMC" NES hack** `playdm.net/ips/Dr._Mario_-_DrMC_v1.0.ips` on our exact
Rev 0 base, with the styled broadcast VIR/SPD/next-pill panels an **OBS overlay** over the
ROM's own on-screen values (SPD←`$0320`, VIR←`$0324/$03A4`, next←`$031A/1B`+`$039A/9B`).
RHDN #8245 is SNES — not it. This section maps *where each feature lives*, from
disassembling the patch (`tools/disasm_drmc.py`).

### 4a. Feature → location (all new code in the `$FB00-$FFFF` tail)

| Feature | Address | What it does |
|---|---|---|
| **Seed-select UI** | `$FB00` (from main-loop hook `$9A39`) | digit editor: `$F5` buttons — SELECT (`&$20`) advances digit cursor `$0B` (0-3); Left/Right (`&$03`) ±1 the current hex nibble of the working seed `$19/$1A`; sets dirty `$0C` |
| **Seed menu widget** | `$FB90` (from music hook `$9AA8`) | draws the seed selector as OAM sprites in the menu, replacing the music-type display (music-select sacrificed) |
| **Seed on-field render** | `$FF40` (PPU-addr table `$FF78`) | draws committed seed `$1B/$1C` to the nametable via `JSR $864E` (draw-hex), per player |
| **Seed → RNG commit** | `$FC00` | writes the edited seed `$19/$1A` into the **live LFSR state `rng0/rng1 = $17/$18`**, with a clamp rejecting seed 0 (LFSR would stick) |
| **SPD shim + cache** | `$FC60` (replaces `LDA $A795,X` at `$8D8D`) | *transparent*: returns `gravityTable[X]` unchanged (gameplay identical), but caches the speed index per player `$0D/$0E`; on change converts it to 2 digits `$0F/$10` (`JSR $FC30`), sets dirty `$11` |
| **SPD on-field render** | `$FC81` | draws the fine SPD digits to the nametable — 2P at PPU `$20ED`/`$20F1`, 1P at `$22DB` |
| **ULT speed tier** | `$FF80` (from speedup hook `$8F38`, orig `INC $8A`) | a speed setting faster than HI (traced to the hook site; `$FF80` body not fully disassembled) |
| **Config init** | `$80B4` area | forces DrMC defaults (music off; speed/seed setup) |

DrMC zero-page usage: `$0B` seed-digit cursor, `$0C` seed-edit dirty, `$0D/$0E` last speed
index (per player), `$0F/$10` SPD display digits, `$11` SPD dirty, `$17/$18` live LFSR
(stock), `$19/$1A` working seed, `$1B/$1C` committed/displayed seed, `$1D` seed-display
dirty, `$58` player parity. **Correction to earlier note:** DrMC stores the seed in the
**live RNG state `$17/$18`**, not the stock `rngSeed $89`. Both the SPD and seed numbers
are genuinely rendered *in-ROM* to the playfield nametable; the broadcast overlay restyles
them.

### 4b. Seed encoding — the deterministic-replay spec (for TE issues #2/#3)

From dmwit's `maryodel` engine (`Dr/Mario/Model.hs`) + the `dr-mario-ngrams` corpus — the
exact NES pill/virus RNG, which the base ROM (and therefore TE and DrMC) already runs:

- **LFSR:** `advanceRNG(seed) = (seed >> 1) | ((bit1(seed) XOR bit9(seed)) << 15)` — 16-bit,
  taps at bits 1 and 9. (`retreatRNG` inverts it.)
- **Pill/virus color:** `decodeColor(seed) = colorTable[seed & 0xF]`, colorTable =
  `[Y,R,B,B,R,Y,Y,R,B,B,R,Y,Y,R,B,R]` (deliberately non-uniform → the ngrams "some
  sequences too likely" result).
- **Virus position:** `decodePosition(seed) = { x = seed & 0x7 (col 0-7),
  y = (seed & 0x0F00) >> 8 (row 0-15) }`, re-rolled until the cell is valid/empty and below
  the level's max-height line.
- **Seeds are even 16-bit:** seed 0 is never used (LFSR sticks); an odd seed produces the
  same sequence as its even neighbor (`seed & ~1`). There are **32767 distinct sequences**
  (even seeds 2…65534). `dr_mario_seed_map.bin` indexes by `65534*level + (seed & ~1) - 2`
  → the two bytes of the next seed / initial state.

**What TE must do to be DrMC/corpus-compatible:** (1) let the player set a 16-bit even
seed, stored into the live LFSR state `$17/$18` at game start — exactly as DrMC does via
`$FC00`; (2) leave stock pill/virus generation untouched (it already implements the above).
Then any `(seed, level)` deterministically reproduces the full 128-pill sequence *and* the
initial virus board — making the corpus replayable and TE runs directly comparable to
tournament seeds. `Granivore` (board→seed) and `Identify` (ROM variant) define the interop.

### 4c. TE × DrMC compatibility verdict

**Proven compatible — 0 overlapping bytes (§3).** TE (pause `$97xx` + `$BE56`/`$9FF9` +
CHR) and DrMC (`$FB00-$FFFF` tail + hooks at `$80B4/$8D8D/$8F38/$9A39/$9AA8`) share no
byte. A combined "TE-over-DrMC" study cart is mechanically a straight IPS stack; the only
care item is CHR tile budget if both add glyphs (DrMC adds digit tiles at CHR
`0xB170/0xC170`; TE adds STUDY/subtitle tiles at CHR `0xAA18…/0xAE99…` — currently
disjoint). This makes "study the actual tournament ROM" a first-class, low-risk option.

---

## 5. TE v9+ candidate features from the community (ranked training-feature harvest)

Every community feature with pedagogical value, ranked for a *study/training* edition.
Port difficulty: **L** = Lua overlay (no ROM change), **P** = small ROM patch in our free
space, **PP** = larger ROM work. "Conflict" = vs our study-chain/branding bytes.

1. **Fine SPD display** — exact drop-speed as a number. *Source:* DrMC `$FC60` / Speed-display
   mod. *Port:* **P** (hook `$8D8D`, render `speedIndex`; blank LOW/MED/HI `$A23D`).
   *Conflict:* none (free-space). Highest study value — a trainee must feel speed precisely.
2. **Seed set + display** — reproducible drills, comparable to tournament seeds. *Source:*
   Seed.ips / DrMC (`$FB00`+`$FC00`). *Port:* **P** (seed editor → `$17/$18`). *Conflict:*
   none. Unlocks deterministic replay (§4b) → closes TE issues #2/#3.
3. **Board/scenario editor + maneuver trainer** — set up a specific board, repeat a drill.
   *Source:* **Bo Krif Ulse** (dmwit, fceux Lua). *Port:* **L** now (ship the Lua alongside
   TE); **PP** for an in-ROM pause-time editor (a natural extension of our STUDY pause).
   *Conflict:* none. The single most "training" feature in the ecosystem.
4. **Statistics HUD (Throw/Drop/Land/Clear/Fall timers)** — quantifies execution. *Source:*
   SNES Stats mod (reimplement for NES). *Port:* **P/PP** (frame-count state transitions,
   render like SPD). *Conflict:* none. Objective per-input feedback.
5. **Specific-level / speed-pinned drills** — start at any level & pinned speed. *Source:*
   Level-cap mod (`lvCap=$18`), God speed (WR-seed pinning). *Port:* **P**. *Conflict:* none.
6. **Constrained-practice modes** — combo-only, combo-rollback (retry until you combo),
   self-garbage. *Source:* playdm combo/garbage mods (`rndColorQty`, match logic). *Port:*
   **P**. *Conflict:* none. Forces a specific skill (combo building / recovery).
7. **AI sparring w/ adjustable difficulty** — practice vs a bot. *Source:* Versus Trainer
   v1/v2; meatfighter AI; **our own copro/planner**. *Port:* **L/PP**. *Conflict:* none. We
   already have a stronger AI than the community — expose it as a training opponent.
8. **Piece-sequence lookahead / history panel** — show pills beyond "next", plus history.
   *Source:* seed determinism + `lookaheadTable` (§4b); Granivore for seed-ID. *Port:* **L**
   (compute from seed) or **P**. *Conflict:* none. Lets a student plan multi-pill.
9. **Slow-motion / frame-step study** — step the game to inspect placements. *Source:*
   emulator/Lua (fceux). *Port:* **L**. Pairs with our STUDY pause.
10. **Hard-drop (Up to place)** — faster iteration during drills. *Source:* Turbo. *Port:*
    **P** (input hook). *Conflict:* CHR-only vs Turbo; the mechanic alone is a small patch.
11. **Handicap / rating for practice ladders** — *Source:* MC Mario, DM Glampers (session
    length). *Port:* **L** (external companions).
12. **Seed-analysis companions** — board→seed (Granivore), ROM-ID (Identify), n-gram drought
    stats (dr-mario-ngrams). *Port:* **L**. *Conflict:* none.

Cross-cutting guidance: **stack, don't fork** — TE is byte-clean vs the seed/SPD hacks (§3),
so the cleanest path is TE + the community IPS as layered patches plus Lua companions,
rather than re-implementing everything in one ROM. **Port the engine against the
disassembly** (Nostaljipi Rev A labels / brianhuffman buildable) for anything deeper.

---

*Reproduce:* `tools/ipsdiff.py <patch.ips>` (footprint vs Rev 0 base) ·
`tools/analyze_overlap.py <te.nes> <patches…>` (TE × community overlap) ·
`tools/disasm_drmc.py <DrMC.ips>` (feature dissection). Set `DRMARIO_BASE` to the clean
Rev 0 ROM. Community IPS files are hosted at `playdm.net/ips/`.
