# Paper lane — Dr. Mario enhancement-chip AI

Publication workstream for the Dr. Mario FPGA-coprocessor AI. Founding session 2026-07-22.

**Working title:** *An Enhancement-Chip AI: Depth-3 Expectimax Dr. Mario on a Cartridge
Coprocessor, Playing Fair.* **Primary venue:** IEEE CoG 2027 (full paper, ~Mar 1, 2027).

## Files
- **[OUTLINE.md](OUTLINE.md)** — section-by-section skeleton, contributions C1–C6, the
  artifact→section map, figure/table shot list, open decisions for the lead.
- **[RELATED_WORK.md](RELATED_WORK.md)** — adversarial prior-art sweep with per-item threat
  ratings, the prior-art matrix (Table T1), and the two load-bearing corrections.
- **[VENUES.md](VENUES.md)** — CoG/AIIDE/FDG/ToG + FPGA-spinoff dates and the arXiv→CoG→ToG
  timeline.
- **[CLAIMS.md](CLAIMS.md)** — three victory-claim formulations, the caliber ladder, and the
  pre-registered RWE evaluation protocol.
- **[EXPERIMENTS.md](EXPERIMENTS.md)** — handoff spec for the experiment lane: the meatfighter
  head-to-head (E1–E3, the load-bearing C1 evidence) + tournament-setting revalidation (E4).
- **[REFERENCES.bib](REFERENCES.bib)** — BibTeX for every citation in the sweep.

## Lead decisions (2026-07-22)
- **IEEE CoG 2027 = primary** (arXiv late-Sept post-RWE → CoG 2027 → ToG extension; AIIDE 2027 fallback).
- **meatfighter head-to-head AUTHORIZED** — runs in the experiment lane; specced in `EXPERIMENTS.md`.
- **README/ROADMAP corrections DONE by the lead** (ROADMAP now credits meatfighter + Seta; the
  "first benchmark" line scoped to the corpus) — items 1–2 below are resolved at the source.

## Standing before drafting prose (from the sweep — see RELATED_WORK.md)
1. **Do not claim "first AI for Dr. Mario"** — meatfighter (2017) exists. Claim the conjunction
   (on-hardware/in-cartridge + depth-3 expectimax + benchmarked) and cite meatfighter.
2. **"No enhancement chip ran AI" is false** — the Seta ST010/ST018 did (racing/shogi).
   *(Fixed in root `ROADMAP.md` by the lead; keep it corrected in the paper prose too.)*
3. **Do not claim algorithmic novelty** (depth-3 expectimax + linear eval is textbook) or
   "first strong versus falling-block AI" (Puyo) or "we invented fairness-by-constraint"
   (AlphaStar). Novelty = game + hardware locus + fairness discipline + benchmark corpus.
4. **Run the meatfighter head-to-head** — the one experiment that makes C1 demonstrated
   (authorized; see `EXPERIMENTS.md`).

## Branch
`paper-lane` (off `origin/main`), worktree at `dr-mario-mods-wt/paper-lane`. Pushed to origin.
