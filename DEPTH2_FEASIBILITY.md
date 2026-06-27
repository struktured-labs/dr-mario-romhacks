# Depth-2 cartridge AI — feasibility study (2026-06-26)

Goal: get the in-cart 6502 AI to play L11 VS-CPU "near the emulator path."
This document records what was **measured** (not estimated) about whether that
is achievable, and what the remaining blocker is.

## 1. The real target (the premise was wrong)

The goal assumed the Python planner *wins* L11 clearing ~48 viruses. It does not.
Measured via the canonical `FaithfulDrMarioEnv` (`scripts/highlevel_eval.py`
`winrate`, seeds 3000+, max_pills=250, 6 games):

| policy | L11 win | L11 clear_rate | per-game cleared |
|---|---|---|---|
| greedy2 (depth-2, full eval) | 17% | **71%** | [14,48,40,43,38,22] |
| greedy1 (depth-1, **full** eval) | 0% | **15%** | [1,3,7,11,14,7] |

So "emulator path" = ~71% of viruses cleared, ~1 win in 6. The current cartridge
(v28cs) clears ~9% (4.2/48).

## 2. Depth, not eval, is the lever — depth-1 is a dead end for L11

`greedy1` with the planner's *full* multi-term eval still caps at **15% / 0 wins**
on L11. Confirmed by BENCHMARK.md ("depth, not weight tuning, is the real lever").
=> Polishing the cartridge depth-1 eval cannot exceed ~7/48. **Only depth-2
lookahead (next-pill preview $031A/$031B) can approach the goal.**

## 3. Depth-2 cannot be cheaply pruned

The 6502 cannot afford the full ~30×30 branching. Two pruning strategies tested:

- **First-ply prune** (shortlist top-K current-pill placements by cheap depth-0
  score, lookahead only those K): K=2→21%, K=4→29%, K=8→41%, full→71%. Climbs
  ~linearly with K — recovering 71% needs K≈full. **Pruning the first ply throws
  away the setup placements depth-2 relies on.**
- **Second-ply prune**: a no-op for depth-2. The second ply is leaf evaluation
  (take the max depth-0 score over next-pill placements); finding the best still
  requires evaluating all of them. K=1==full (53% portable). **Not prunable.**

=> Depth-2 must evaluate **all ~30 first-ply placements, each with a full
~30-placement second ply ≈ 900 board evaluations per pill.** Inherent.

## 4. The portable eval is good enough (~53%)

The 6502 can't afford the planner's most expensive terms (`setup_runs`,
`buried_virus_count`, `clear_readiness`). Tested which matter at depth-2:

| eval | L11 clear_rate |
|---|---|
| cheap only (virus, clear, combo, height, holes, top_risk) | 24% |
| cheap + **buried_pen** | **53%** |
| full (… + setup_bonus + readiness) | 71% |

**`buried_pen` is the single most important expensive term** (24→53). A *capped*
buried-scan already runs stable on the 6502 (see memory: v28 budget-wall
breakthrough). So a portable depth-2 with {virus, clear, combo, height, holes,
top_risk, capped-buried} should reach ~50% on L11 — far above depth-1's 15%, and
genuinely "near" the 71% emulator path. Adding setup_bonus (also portable, already
in v18) pushes toward 71%.

## 5. Core 6502 primitives built and validated (py65, cell-for-cell)

New reusable harness `tests/py65_harness.py` (py65; `uv pip install py65`) loads
assembled routine bytes, sets up a board in $0500-$057F, runs a subroutine to RTS,
and reports memory + **cycle count** — so any cartridge routine is unit-testable
and cycle-countable offline, no Mesen. (nes_py can't run drmario — MMC1 unsupported.)

| primitive | file | bytes | validation | cost |
|---|---|---|---|---|
| `score_board_shape` (max_height, holes, top_risk) | test_shape_eval.py | 97 | 600/600 boards | ~5310 cyc (2.4 frames) |
| `find_clears` (mark+clear all >=4 runs, count cells/viruses) | test_clear_detect.py | 217 | 800/800 boards | ~25k cyc (11.8 frames) full-board |
| `apply_gravity` (column-compact, viruses fixed) | test_gravity.py | 98 | 800/800 boards | ~5.9k cyc (2.9 frames) |
| **`resolve`** (find_clears→gravity loop, cascades) | test_resolve.py | 347 | **500/500 vs Python AND 500/500 vs faithful engine** | ~32k avg / 114k max cyc |

**find_clears full-board is ~25k cyc** — too slow to run per placement. The port
must use a **targeted scan** (only the placed cells' row + 2 columns, ~3 lines vs
24 → ~3k cyc common case); fall back to a wider rescan only after a clear+gravity
cascade. Same lesson as the eval: full-board ops are 5–25k cyc; the search must
scan incrementally/targeted.

## 6. The remaining blocker is the per-pill compute BUDGET

~900 evals/pill × ~5310 cyc (full) ≈ 4.9M cyc/pill ≈ **165 vblank frames ≈ 2.7 s**.
With incremental eval (re-walk only the 1-2 touched columns per placement, ~1.3k
cyc) it's ~1.2M cyc/pill ≈ 0.7 s in the main loop but still ~8 s in vblank.

The AI hook currently runs **only inside the vblank NMI** (~2273 usable
cyc/frame), where even one full-board eval is 2.4 frames. So depth-2 fits only via:

- **(A) Main-loop execution** (~27000 cyc/frame, 13× headroom) → ~0.25–0.7 s/pill,
  feasible if the pill's maneuver window is long enough. A prior offload attempt
  "failed" (target stayed 0) but the diagnosis was thin — **this is the highest-
  leverage thing to re-investigate.**
- **(B) Incremental shape eval** (maintain running per-column height/holes +
  top_risk; O(1) updates; full rescan only after the rare clear). Keystone that
  also unblocks any shape-aware *depth-1* search (which hits the same wall today).
- **(C) Cheap immediate-clear-only second ply**: approximate the next-pill value
  as `board_score(after_first) + best_next_immediate_clear` (cheap 4-run scan, no
  per-placement shape eval). **MEASURED: 40% clear** (vs 53% full portable) —
  only a moderate drop, still 2.6× the cartridge's current 9% and >2× depth-1's
  15% ceiling. Makes the second ply ~30× cheaper (immediate checks, no shape eval).

## The viable recipe (quantified)

**depth-2 · full first ply · cheap clear-only second ply · portable eval
(cheap + capped-buried) · incremental first-ply shape eval.**
- Expected L11: **~40% clear (~19/48)** — 4.6× v28cs, >½ the full planner's 71%.
- Budget with incremental eval: ~30 × (resolve + incremental board_score ~1.3k +
  30 cheap-immediate ~100) ≈ **~174k cyc/pill ≈ 77 vblank frames**. Fits the main
  loop trivially (~0.1 s); borderline vblank-only (must spread across the pill's
  fall via the existing per-pill cache framework).

## Search-driver integration (in progress)

Shared primitives now live in `tests/primitives.py` (single source of truth,
`emit_*` labeled subroutines). Built on top and validated:

| unit | file | validation | cost |
|---|---|---|---|
| `eval_placement_deep` (backup→place→resolve→shape→restore) | test_kernel.py | **4500/4500** placements match Python + 4500/4500 board restored | ~35k cyc avg (full) |
| `resolve_targeted` (scan only placed cells' lines first pass) | primitives.py | matches full resolve **4500/4500** on resolved boards | **~17k cyc avg (2×)** |

`resolve_targeted` exploits the invariant that a real mid-game board is always
run-free (the game resolves after every pill), so the only new run is through a
placed cell — scan 4 lines, and on the common no-clear case (~95% of placements)
return immediately. Remaining per-placement cost is dominated by board
backup/restore (~3.5k) + full-board shape (~5.3k), both incrementalizable.

**The second ply is now the cost frontier**: even cheap clear-only, ~30×30 ≈ 900
next-pill clear-detections/pill (~2k each) ≈ 2M cyc. The likely fix is to
approximate the next-pill value with a single per-first-ply *clear-readiness*
scan (planner's `readiness` term) instead of 30 simulations — needs a Python
experiment to confirm it preserves ~40%.

## 7. Main-loop execution: the injection point (FOUND)

The gating budget question — can the AI compute outside the ~2273-cyc vblank NMI?
— has a concrete answer. The game's `wait_for_vblank` is a busy-spin:

```
$B660: STA $33        ; clear frame-ready flag
$B662: LDA $33        ; spin:
$B664: BEQ $B662      ;   idle until the NMI sets $33
```

This spin runs **every frame during gameplay**, eats **most of the frame**
(~25k of ~29830 cyc) idling, and runs with the **full main-loop budget** (not the
vblank window). Patch the 4-byte spin to a trampoline that runs ONE bounded search
slice (e.g. one placement eval, ~17k cyc) then falls through to check `$33` — the
search resumes on the next frame's spin. That is the resumable depth-2 state
machine, driven by the spin, at ~25k cyc/frame. This is a DIFFERENT mechanism than
the prior failed "offload to a (nonexistent) main-loop AI call" — here we ADD a
hook at the spin itself. Budget then: ~520k–2M cyc/pill ÷ ~25k/frame ≈ 20–80 frames,
spread across the pill's fall. Feasible.

Code size: the search (~600B primitives + enumeration + scoring + state machine,
~1.2KB) exceeds the ~392B fragmented free space in the fixed bank → **Path B (MMC1
PRG expansion, add a 16KB bank)**; the small trampoline lives in existing free ROM
and bank-switches in/out per slice.

## Status / next steps

- ✅ Quality solved: portable (cheap+capped-buried) = 53%; cheap-2nd-ply = 40%.
- ✅ Board-sim + per-placement kernel + targeted resolve built, validated, cycle-counted.
- ✅ Budget quantified: first ply ~520k cyc/pill; second ply is the frontier.
- ✅ Main-loop execution path FOUND: patch the $B662 vblank-wait spin (full-frame budget).
- ⏭ Next: (1) PRG-expand (Path B) + spin-trampoline + bank switch; (2) port v18's
  enumeration to drive the kernel + multi-term score + best-tracking; (3) make it
  resumable (one slice per spin entry); (4) measure on L11 via measure_l11.sh.
- Next: (1) build + validate **incremental shape eval** (B) on py65 — the keystone;
  (2) build the **6502 resolve board-sim** (find-4→clear→column-compact gravity),
  validate cell-for-cell vs `faithful_game.resolve`; (3) wire the resumable depth-2
  state machine into the v18 search; (4) settle **main-loop execution** (A) if the
  vblank spread proves too tight.
- Stable demo fallback remains **v28cs** (no crashes, ~4.2 clears).
