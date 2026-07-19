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
- **2026-07-19** — **Study mode v2/v3 (TE lineage)**: pause shows frozen board +
  falling capsule + next-pill preview; STUDY text reconnected (v3). TE v6 release
  package built (BPS + notes) — publication pending the v3.1 VS-mode fix.

## Active (in flight)

- **Obvious-move gate, phase 2 (R4–R7)**: depth-proportional hang credit,
  matched-cover setup credit, targeted caps. Target: **≥95% take-rate**
  (the "wife-readiness gate"); projected ~96–97%.
- **TE v6 (study v3.1)**: ✅ built & validated all modes (1P/2P/VS — both players'
  frozen capsules intact + STUDY + mode-correct preview). BPS in `release/`;
  romhacking.net upload = author's move.
- **Expert corpus (DRMC 2017–2026)**: ~41 GB banked (2024 championship complete,
  2025 partial); self-healing download loop working through YouTube rate limits.
  Champions table complete except 2025. Match-timestamp index parsed (305 matches).

## Next up

- **Vision pipeline**: broadcast footage → (board, move) pairs at scale.
  Calibrated OCR exists; needs a learned cell classifier. Unblocked (2024 footage
  is complete); the gate to everything below.
- **Driver fidelity**: rotation-plan-aware steering ("pre-phase early, snap late"),
  feasibility-gated retargeting (root cause of observed backwards locks), and
  eventually tuck generation — the pro move space (weave down, last-second snap).
- **v4 patcher divergence root-cause** (nav-region delta between patcher HEAD and
  deployed carts; until then, hardware ships via surgical byte-patches only).

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
