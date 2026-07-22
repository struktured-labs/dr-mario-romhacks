# Dr. Mario NES — FPGA AI Coprocessor

> **ROM-hack release:** [Dr. Mario Training Edition v7](release/RELEASE_NOTES_V7.md) —
> [download the BPS patch](release/drmario_te_v7.bps). This release carries the published
> Training Edition v5 forward with crash-safe `TRAINING EDITION` title branding.

A hardware-accelerated depth-3 AI that plays Dr. Mario (NES) on a real
[MiSTer](https://github.com/MiSTer-devel/Main_MiSTer/wiki) FPGA **and on the Analogue
Pocket** (custom openFPGA core). A custom mapper drops a
**second 6502 core plus an RTL board-engine** into the NES core; a companion cartridge
auto-navigates into a VS-CPU match and lets the coprocessor drive a player — no controller,
no host PC in the loop. It is a self-running demo of an expectimax search running on silicon
alongside the game it is playing.

## Milestone — depth-3 on hardware at ~1 second per move

The AI runs a **depth-3 expectimax search** (current pill + preview pill known, third pill
averaged over a pill subset) with an endgame-tuned evaluation. In pure simulation the
decision function clears **93.8%** of L11 boards solo (n=48, exact firmware model). The whole
pipeline — search → firmware → cycle-accurate sim → Quartus → hardware — is validated
cell-exact at each stage.

**Latency, start of port → now:**

| Build | First-pill decision | What changed |
| --- | --- | --- |
| initial | ~400 s | copro fed the 21.5 MHz NES clock (never the intended 85.9 MHz) |
| `clk85` | ~100 s | dual-clock fix: 6502 + engine on the master clock |
| 4-pill | ~50 s | 4-pill expectimax subset (measured 100% solo, no quality loss) |
| LeafEval | ~4 s | full leaf evaluation in RTL (~1.5k cycles vs ~50k on the 6502) |
| **BoardEngine** | **~1 s** | land + place + resolve + leaf + board copies all in RTL; 6502 is pure search control |

Steady-state moves are sub-second — the demo is now paced by the game's own pill-drop and
clear animations, not by the AI.

## Milestone 2 — Analogue Pocket port + the honest (anytime) AI

The same coprocessor now ships on a **handheld**: a single-copro variant of the mapper
lives inside a trimmed [agg23/openfpga-NES](https://github.com/agg23/openfpga-NES) core
(mapper farm stripped to MMC1 + mapper 100 — the stock core is 99% ALM-full; the trim
reclaims ~6.2K ALMs and the copro fits at ~96% with timing closed at the full 85.9 MHz).
Human-vs-AI on the couch: **you are P1 on the Pocket's buttons, the depth-3 copro is P2.**

The AI itself crossed from "solver with pause privileges" to **honest real-time player**:

- **Anytime search** — the firmware live-publishes its best-so-far move into the result
  mailbox as the search runs (orient `0xFF` = not-yet-valid sentinel; zero RTL change).
  The driver never freezes the pill: it weave-steers toward the current best while the
  search refines, and only fast-drops after DONE. **The pill's own fall time is the AI's
  time budget.** Hardware A/B (P1 freeze vs P2 anytime, same match): anytime cleared
  viruses at 2× the rate with no mid-air pauses.
- **Temporal discount** (`val = imm + leaf + (deep−leaf)/2`) — fixes a search pathology
  where deferring an obvious placement is value-neutral in the model ("procrastination"),
  found by a human player in one game. Also worth ~14% solo pill-efficiency.
- **Household-coached eval terms** — `g_excav` (scaffolding credit for clearing junk off
  buried viruses) and `g_hang` (a hovering capsule half whose gap-drop lands on a matching
  color pairs automatically when its partner clears — the delayed-drop setup). Computed by
  the 6502 once per ply-1 candidate on top of the RTL leaf; py65-gated bit-exact.
- **Deterministic match entry** — auto-nav STARTs only when `$0727 == 2` (VS-CPU exactly);
  no more mode roulette.
- **Human-challenge carts** — `DRHUMAN=1` builds leave P1 as a pure human passthrough
  (`drmario_copro_human.nes` for MiSTer, `DRPOCKET=1` single-window variant for Pocket).

One canonical source (`fpga/copro/`) feeds both platforms: the Pocket tree vendors the RTL
via `fpga/copro/sync_to_pocket.sh`, and one `copro_rom.hex` firmware ships everywhere.

## How it works

- **Mapper 100** (`fpga/copro/CoproDrMario.sv`) = MMC1 banking + this block. A second 6502
  (`copro6502.v`, Arlet core) free-runs at the core master clock (`clk85`), with a host
  register window at `$5000–$51FF` (one window per player, dual-copro so P1/P2 never
  time-share). The game CPU writes the board + pill colors, pulses GO, polls DONE, reads back
  the chosen column + orientation.
- **BoardEngine** (`fpga/copro/LeafEval.sv`) is the RTL accelerator at `$7000–$70FF`: a single
  `NODE` command does landing + placement + a capped targeted resolve + the full leaf eval,
  plus single-command snapshot/restore of the working boards. This is what collapsed the
  per-search-node cost and made depth-3 practical on hardware.
- **The cartridge** (`patch_cartridge_copro.py` → `drmario_copro.nes`) is a patched ROM whose
  every-frame hook auto-navigates to VS-CPU L11 and, in play, uploads each locked pill to the
  coprocessor and executes the returned move. It also carries a per-player **seeded tie-break**
  so the two same-strategy copros desync into distinct games (same evaluation, different
  near-tie resolution — not a strategy divergence).

## Validation chain

Every acceleration step is proven the same way before it reaches hardware:

1. **py65** — the 6502 search vs a Python golden (`tests/`, cell-exact).
2. **Verilator** — the RTL block vs the same board-suite goldens the 6502 primitives passed
   (`fpga/copro/tb_leafeval.cpp`: 205/205 leaf, 250/250 node), and the full mapper vs an oracle
   (`fpga/copro/sim_mister.cpp`).
3. **Quartus** — timing closed at 85.9 MHz; the generated firmware MIF is byte-verified against
   `copro_rom.hex` before every deploy.
4. **Hardware** — deployed to the MiSTer, pace + play confirmed live.

## Build / deploy

```bash
# firmware (depth-3 4-pill BoardEngine) — writes fpga/copro/copro_rom.hex, validates in py65
.venv/bin/python fpga/copro/build_copro_d3.py

# auto-nav cartridge (level/speed via env)
DRLEVEL=11 DRSPEED=1 .venv/bin/python patch_cartridge_copro.py   # -> drmario_copro.nes

# FPGA core: copy copro_rom.hex into the NES_MiSTer tree, then
#   quartus_sh --flow compile NES   -> output_files/NES.rbf
# deploy NES.rbf + drmario_copro.nes to the MiSTer and launch.
```

The RTL sources here (`fpga/copro/CoproDrMario.sv`, `LeafEval.sv`) are the source of truth;
they are mirrored into a local `NES_MiSTer` checkout for Quartus synthesis.

## Further reading

- `INTEGRATION_SPEC.md`, `ROM_WIRING_PLAN.md` — cartridge/mapper wiring
- `DEPTH2_BUILD.md`, `DEPTH2_FEASIBILITY.md` — the depth-2 predecessor
- `VS_CPU_PLAN.md` — auto-nav VS-CPU demo design
- `CLAUDE.md` — memory map, tile encoding, mechanics reference

## Known open items

- **Match clear-rate is unmeasured on hardware** — the screenshot OCR's hamming gate rejects
  the near-clear virus-count reads, so the automated clear tally is currently blind. Fix the
  detector before trusting a hardware clear-rate figure.
- **Cascade-resolve: tested, rejected** — a full chained resolve in the search halved solo
  clear-rate (100%→50%) chasing combos into topouts; the capped resolve is the better player.
- **v4 AB-cart regression (quarantined)** — the CPU-vs-CPU cart built from the current patcher
  stalls both players on hardware; the v2-era build (`tmp/ab_v2era.nes`, patcher @ `822579e`)
  plays perfectly on the same rbf and is pinned for the duel. Root cause not yet found (byte
  delta is confined to the nav region; branch-range overflow ruled out).
- **Next programs** — expert player data (Twitch/DRMC VOD → frame OCR → (state, move) pairs;
  the board OCR machinery exists), an NNUE-style learned eval in the idle DSP blocks, and
  dual-copro parallel search on MiSTer once its controllers are back.
