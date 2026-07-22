# Dr. Mario AI — Roadmap

> **North star:** the strongest NES-native Dr. Mario player in the world, under a real
> time budget — no pause/freeze cheating. The brain lives in the cartridge's address
> space (enhancement-chip model: a coprocessor in the cart slot, SA-1/SuperFX lineage),
> playing as a legitimate second player on console-accurate hardware.
>
> Maintained by the project's AI coordinator; updated at every milestone.
> Last update: **2026-07-19**.

## Platform targets (both first-class)

| Platform | Status |
|---|---|
| **Analogue Pocket** (agg23.NES fork + copro, mapper 100) | ✅ Shipped — human-vs-depth-3 on real silicon |
| **MiSTer** (NES core + copro) | ✅ Shipped — CPU-vs-CPU duel live; human play awaits BliSSTer Rev.3 |
| Physical FPGA-in-cart for stock NES | 🔭 Someday — the literal SA-1 move |
| **P2-port peripheral** (vision → brain → controller; stock console, stock cart) | 🔭 Someday, bottom of list — enabled by the vision pipeline |

## Shipped milestones

- **2026-07-11** — FPGA coprocessor: depth-3 expectimax on a second 6502 @ 85.9 MHz
  in the cart's address space; zero-input demo cart plays VS-CPU L11 on MiSTer.
- **2026-07-18** — Analogue Pocket port (core trim 99%→65% ALM, +copro = 96%);
  human-vs-AI validated on real hardware. **Anytime/no-freeze steering** (v2): AI
  plays under real gravity, no pauses — 2× throughput vs freeze, A/B-proven.
- **2026-07-18** — Household-coached eval terms: temporal discount, excavation,
  hanging-half (all py65-gated, cross-validated, in firmware).
- **2026-07-19** — **Combo brain**: color-aware buried (stop taxing correct covers)
  + retuned excavation/readiness weights. Obvious-move take-rate **66.5% → 85.2%**
  (236-scenario adversarial suite), L11 regression clean. Live on both platforms.
- **2026-07-19** — **Study mode (TE lineage) complete**: pause shows frozen board +
  falling capsule + **both players' next-pill previews** + STUDY text, per-mode
  positioned (1P/2P/VS all validated). **TE v6 published on romhacking.net.**
- **2026-07-19** — **Fair driver shipped**: zero gravity pins (strictly fairer than
  every prior build), rotation pre-phase, feasibility-gated retargeting, orientation
  map fix — validated by hardware A/B after the unit tests missed a placement bug the
  silicon caught. Patcher divergence root-caused (nav gate); quarantine lifted;
  clean builds from `copro-canonical` are the ship path again.
- **2026-07-19** — **R4–R7 brain validated**: obvious-move take-rate **93.6% raw /
  97.0% widened** (clears the 95% gate), L11 100%. Cell-exact RTL + firmware port.
- **2026-07-22** — **R47 on silicon**: the 85.9 MHz timing wall (field freeze on
  Pocket) solved structurally — copro moved to its own clock domain (21.47 MHz,
  SDRAM keeps 85.9 exclusively; +2.2 ns margin) on Pocket; score-combine pipeline
  recovers full speed on MiSTer. **TE v7 (Codex)**: title-screen TRAINING EDITION
  branding + STRUK LABS credit footer.

## Active (in flight)

- **TE v8**: unify v6 study features + v7 title branding (they collide on two
  byte runs; relocation in progress) — supersedes both on romhacking.net.
- **Driver rev 2**: confidence-gated slam (commit when the search's answer is
  stable, not when it's exhaustively confirmed) + speed-aware gates — closes the
  human tempo gap on obvious placements and the late-game search-vs-gravity
  crossover; primary commit mechanism at the Pocket's new clock.
- **E1 endgame regime**: route-aware kill costs (dig / scaffold-through /
  under-clear) with regime switching by virus count × gravity speed — the fix for
  deep-buried endgame stalls.
- **Expert corpus (DRMC 2017–2026)**: **96 GB banked** (2024 championship + most
  of 2025 + regionals + 2021); champions table 2017–2024 complete; full bracket
  database reconstructed (brackets.json); remaining years rate-limit-walled.
- **LLAPI/BliSSTer runway**: port branch ready for real-controller P1 vs AI P2 on
  MiSTer (board arrived; install pending).

## Next up

- **Incremental leaf eval in firmware** (validated 6.1×/leaf, not yet deployed) —
  recovers the Pocket clock change and dissolves the late-game crossover entirely.
- **Vision pipeline**: broadcast footage → (board, move) pairs at scale.
  Calibrated OCR exists; needs a learned cell classifier. Unblocked (2024 footage
  is complete); the gate to everything below.
- **Tuck generation**: the pro move space (weave down, last-second snap) — new
  placement class for the search + driver.
- **Publication**: paper lane (enhancement-chip AI, fairness framework, the
  DRMC benchmark) — arXiv → IEEE CoG / AIIDE.

## Programs (longer horizon)

- **Expert-agreement scoring**: ship brain vs champions' actual tournament moves —
  the first benchmark the Dr. Mario AI space has ever had. Then pattern mining
  (principled term weights) and personalized coaching reports (the household loop,
  industrialized, pointed both ways).
- **One brain, N personas**: universal trunk trained on the full corpus (the
  "beats all styles" mainline) + small per-player style heads (NNUE/LoRA-scale),
  selectable at runtime via a mailbox byte. One FPGA image, pick your opponent.
  Companion: a Quarto deck with LLM-written scouting reports per persona.
- **Native-AI distillation**: shrink/memoize/port the copro brain down to the pure
  2A03 budget so the IPS-patchable TE release offers real AI on stock hardware and
  every emulator. (Publishes only past the author's embarrassment bar.)
- **Release channels**: TE patches on romhacking.net (everyone) · FPGA cores on
  GitHub (MiSTer/Pocket faithful) · custom emulator core implementing the copro
  (RetroArch crowd, medium effort, spec in hand).

## Events

- **Retro World Expo, Hartford CT — Sept 12–13, 2026**: Struktured Labs studio
  showcase (this project + Quintra + Penta Dragon DX + Cowardly Irregular).
  Human-vs-AI station (pending BliSSTer), demo-station capture rig doubles as
  clean-footage collector. Same venue hosted the DrMC 2025 Connecticut Regional.

## Parked

- Dual-copro parallel search (multicore) — until MiSTer controllers (BliSSTer).
- Cascade-aware node-resolve — measured negative (chasing combos = topouts).
- Depth-4 at current eval weights — measured negative (horizon effect).
