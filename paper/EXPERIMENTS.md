# Experiment specs — for the experiment lane (handoff)

> Authorized by the team lead 2026-07-22. These run in the **experiment lane, not the paper
> lane**, once the current sweeps drain. This file is the handoff spec. Two experiment
> families: **E1–E3** the meatfighter head-to-head (the load-bearing C1 evidence), **E4** the
> tournament-setting revalidation (closes the "100% is L11-MED-solo" gap for `CLAIMS.md`
> Formulation B). Report *both directions honestly* — a loss is a result, not a failure.

## Why these matter (tie-back)
- **C1** ("first *strong* Dr. Mario AI…") is currently *arguable* against meatfighter's 2017
  depth-2 agent. E1–E3 convert it to *demonstrated*: our depth-3 expectimax vs a faithful
  reimplementation of his depth-2 heuristic, head to head. This is the single experiment a
  hostile reviewer most wants to see (`RELATED_WORK.md` §meatfighter).
- **Formulation B** (the recommended victory headline in `CLAIMS.md`) asserts strong play at a
  *tournament* setting, but our measured 100% is **L11 MED solo only**. E4 measures the
  strong-play envelope across the levels/speeds the DRMC corpus actually uses.

## Shared harness (reuse — do not rebuild)
All in the repo (`~/projects/dr-mario-mods`; `tmp/` is gitignored, lives in the main checkout):
- **`drmario.faithful_env.FaithfulDrMarioEnv`** — the faithful (cell-exact) single-player
  engine. **NOTE: it is SOLO — it does NOT model VS garbage.** See E3 prerequisite.
- **`tests/nes_d3_golden.py`** (`_placements4`, `_place`, `_virus_count`, `_imm`,
  `_cap1_targeted`) — placement enumeration + board sim primitives, cell-exact.
- **`tests/nes_d2_golden.py`** — the depth-2 golden; the natural substrate for a depth-2
  baseline (reuse its enumeration/board-sim, swap in meatfighter's eval).
- **`tmp/tempo/measure_stab.py`** — worked example of driving the exact decider over full L11
  games via `FaithfulDrMarioEnv` + `decide_anytime`; copy its game-loop scaffolding.
- **`build_copro_d3.py`** / `fpga/copro/LeafEval.sv` — our depth-3 eval (the "ours" side).
- Gravity model: **`tmp/tempo/TEMPO_DESIGN.md` §2.5** (ROM-exact `gravityTable $A795`; speedBase
  LOW/MED/HI = 15/25/31; frames/row per level+speedup) — E4 needs this for correct speeds.
- The `.out` regression artifacts (`tmp/final_regress.out`, `tmp/r4r6r7_sweep.out`) show the
  target report format; their exact driver scripts are **not in-tree** and may need light
  reconstruction from `measure_stab.py`'s scaffolding.

---

## E1 — Faithful meatfighter depth-2 baseline
**Objective.** A faithful, documented reimplementation of meatfighter's Dr. Mario AI to serve as
the C1 comparison baseline. Not a strawman — reproduce his algorithm as published.

**Method.**
1. **Extract the exact algorithm** by fetching **https://meatfighter.com/drmarioai/** (he
   documents it). Capture: the placement enumeration (BFS over every lock of *current × next*
   pill = depth-2), and the exact weighted heuristic terms + **weights** (reported terms: virus
   count, consecutive same-color tiles, virus-color adjacency, non-empty-tile count, column-
   height penalties). If a weight is not published, record the assumption explicitly.
2. **Implement** on our board substrate: reuse `nes_d2_golden.py` enumeration + `FaithfulDrMarioEnv`
   for legality/gravity/resolve; implement only his eval as a drop-in scorer. Keep it a separate
   module (`experiments/meatfighter_baseline.py`) so ours and his share the *same* board sim and
   differ *only* in the decision function — this isolates the comparison to the AI, not the sim.
3. **Validate the reimplementation** before comparing: reproduce a documented meatfighter
   behavior as a sanity check (e.g., his demonstrated ability to survive/clear at L20–24 solo;
   confirm it does not top out immediately at low levels). Record the check in the writeup.

**Deliverable.** `experiments/meatfighter_baseline.py` + a short fidelity note (what was
published vs assumed). **Attribution: Michael Birken (meatfighter), not "Colin M."**

**Risk.** If the site under-specifies weights, the baseline is approximate — state it, and if
feasible tune his weights on his stated objective (survival) rather than ours, to avoid
strawmanning.

## E2 — Solo efficiency comparison (ours depth-3 vs his depth-2)
**Objective.** Head-to-head on *solo* virus-clearing at matched settings — the cleanest,
dependency-free comparison (no garbage model needed).

**Method.** Both deciders play the **same seeds** (paired design) through `FaithfulDrMarioEnv` at
matched (level, speed). Start at **L11 MED** (our benchmark), then include E4's settings.
**Metrics** per (level, speed): clear rate (fraction of boards fully cleared), **median
pills-to-clear** (efficiency, on cleared games), and topout rate. **N ≥ 100 shared seeds** per
cell. **Tests:** McNemar on paired clear/no-clear; Wilcoxon signed-rank on paired pills-to-clear.

**Deliverable.** A table (level × speed × {ours, his}) with the paired-test p-values, in the
`final_regress.out` format. **Report both directions of every result**, including any cell where
his depth-2 matches or beats ours (e.g., if his survival-tuned eval tops out less at very high
gravity — that would be a genuine, publishable nuance).

## E3 — VS head-to-head (ours vs his, under faithful garbage rules)
**Objective.** The direct competitive claim: does depth-3 expectimax beat depth-2 BFS in a
*versus* race with garbage?

**PREREQUISITE (a day of wiring, NOT research — the rule is already extracted).**
`FaithfulDrMarioEnv` is **solo**, so E3 needs a 2-player env. But the VS garbage rule does **not**
need reverse-engineering — it was deterministically extracted from the ROM and verified
(`tmp/probe_attack.lua`: freezes P2, injects P1 clears, diffs P2's board cell-by-cell). **The rule:**
- **1 line cleared → 0 garbage tiles.** **≥2 lines cleared *simultaneously* → exactly 2 tiles.**
- Garbage **colors = the cleared runs' colors**; tiles **enter at row 0 and fall**; columns are
  **4 apart**, from the fixed pair set **{1,5} / {2,6} / {3,7}**.

So the prerequisite is **wiring this known rule into a 2-player env** (`experiments/vs_env.py`
wrapping two `FaithfulDrMarioEnv` boards + the garbage exchange above) — ~a day, deterministic,
high-throughput, and reusable for the C6 tempo/competitive-theory section. **Spot-check it against
the real ROM's VS mode** on mapper-100 hardware/emulator (which implements garbage natively) on a
handful of games. The **experiment lane owns the wiring.**

**Method.** Once garbage is modeled: run ours-vs-his VS games, **both directions** (ours as P1 /
his P2, then swapped) to control P1/P2 asymmetry, at matched (level, speed), **paired seeds**
where the RNG allows. **Metric:** win rate (+ 95% Wilson CI). **N / stopping rule (pre-register,
no peeking):** floor **N ≥ 200 games per direction**; report the Wilson CI and whether it
excludes 50%. (Power note: distinguishing a true 60% from 50% at 80% power needs ~200 games; 55%
vs 50% needs ~780 — size to the effect you see in a pilot of ~50.)

**Deliverable.** Win-rate table (both directions, CIs) + the `vs_env.py` garbage wiring and its
hardware spot-check. Honest reporting: if it's close, say so with the CI.

## E4 — Tournament-setting revalidation (the L11-MED-solo gap)
**Objective.** Establish the *envelope* where our strong-play claim holds — required before any
`CLAIMS.md` Formulation B/C headline at a non-L11-MED setting.

**Method.**
1. **Consume the DRMC settings → in-game (level, speed) mapping from the corpus.** *(Routed to the
   corpus program / obs-studio by the lead: broadcast overlays show LEVEL/SPD per match on screen,
   so the mapping is extractable from on-disk footage + rules pages and will land in
   `players.json` / `brackets.json` metadata.)* Read it from there rather than re-deriving it;
   until it's populated, sweep the full grid in step 2 so no cell is missed.
2. **Solo clear-rate sweep** through `FaithfulDrMarioEnv` across the confirmed grid — levels
   spanning at least {10 … 20} × speeds {MED, HI} (and LOW if any bracket uses it), honoring the
   ROM-exact gravity per `TEMPO_DESIGN.md §2.5`. **N ≥ 50 seeds per cell.**
**Metrics.** Clear rate + median pills-to-clear per (level, speed) cell → a heat-table of the
strong-play envelope (this becomes paper Figure F5's companion and the evidence basis for
Formulation B's stated setting).

**Deliverable.** A (level × speed) clear-rate table with N per cell, plus a one-line envelope
statement ("≥X% clear holds for levels ≤L at speed S") for `CLAIMS.md`.

---

## Acceptance criteria (what "done" furnishes the paper)
- **C1 demonstrated** if E2 (and ideally E3) shows ours ≥ his by a statistically significant
  margin on solo efficiency and/or VS win rate at matched settings — reported honestly in both
  directions.
- **Formulation B unblocked** if E4 shows the strong-play envelope covers the tournament setting
  the RWE opponents will actually play (else the headline must state the setting E4 *does* support).
- All results land in `paper/` as tables in the `final_regress.out` format, with N and the
  statistical test named, ready to drop into §5/§10 and Table T2.

## Dependencies — both RESOLVED by the lead (2026-07-22)
- **VS garbage rule** (E3) — RESOLVED: already extracted + verified from the ROM
  (`tmp/probe_attack.lua`); rule stated inline in E3. Remaining work is *wiring* it into
  `experiments/vs_env.py` (~a day), owned by the experiment lane. Not a research blocker.
- **DRMC setting mapping** (E4 step 1) — ROUTED to the corpus program (obs-studio); will arrive
  as `players.json` / `brackets.json` metadata (LEVEL/SPD from broadcast overlays). E4 consumes it.

**Status: parked.** The experiment queue picks up E1/E2 when tonight's sweeps drain; E3 unblocks
once `vs_env.py` is wired; E4 unblocks as the corpus metadata lands.
