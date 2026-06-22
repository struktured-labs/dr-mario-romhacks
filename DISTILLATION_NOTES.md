# PPO -> Decision Tree Distillation: Feasibility Study

**Date:** 2026-06-21
**Author:** distillation feasibility agent
**Script:** `rl-training-new/scripts/eval_distill.py`
**Log:** `tmp/eval_distill_run.log`
**End goal:** distill the PPO policy into a tiny decision tree (~500 bytes) that
can be hand-compiled to 6502 assembly and embedded in an expanded NES ROM.

## 1. Does the existing model load?

**Yes.** `PPO.load("/home/struktured/projects/dr-mario-mods/rl-training-new/models/ppo_drmario_final.zip", device="cpu")` succeeds cleanly under sb3 2.7.1 / torch 2.9.1+cu128 with the `DrMarioCNN` feature extractor on the import path.

## 2. Policy architecture

- Policy class: `ActorCriticCnnPolicy`
- Observation space: `Box(0.0, 1.0, (16, 8, 12), float32)` — channels-last
- Action space: `Discrete(9)` (NOOP, LEFT, RIGHT, DOWN, A, B, L+D, R+D, L+A)
- Feature extractor (shared instances for pi / vf): `DrMarioCNN`
  - `Conv2d(12 -> 32, 3x3, pad=1) -> ReLU`
  - `Conv2d(32 -> 64, 3x3, pad=1) -> ReLU -> MaxPool2d(2)`
  - `Conv2d(64 -> 64, 3x3, pad=1) -> ReLU -> Flatten`
  - `Linear(2048 -> 256) -> ReLU`
- MLP extractor: two 256 -> 64 (Tanh) heads (policy_net, value_net)
- Output heads: `action_net = Linear(64 -> 9)`, `value_net = Linear(64 -> 1)`

## 3. Critical finding: action distribution collapses on synthetic states

Over 20,000 random sparse playfields, the PPO policy in deterministic mode chose only 3 of the 9 actions:

| Action | Name        | Count | Percent |
|-------:|-------------|------:|--------:|
| 4      | A (rotate)  |  6,579| 32.90%  |
| 5      | B (rotate)  | 13,420| 67.10%  |
| 7      | RIGHT+DOWN  |     1 |  0.01%  |
| others | -           |     0 |  0.00%  |

A trivial "always predict B (action 5)" classifier already hits **67.1%** accuracy. The 70% bar in this study is therefore *barely* above the majority-class baseline. The distillation trees report 78-82% test accuracy, which is real signal — but not nearly as impressive as it looks if you naively read "80% accurate decision tree".

This collapse is the most important diagnostic in the whole study. Two ways to interpret it:

- **Out-of-distribution prompts**: the synthetic sampler produces playfields the PPO never saw during dense-color-matching training, and the policy degenerates. This is plausible — the per-channel statistics differ from real gameplay (sparser viruses, no realistic capsule chain history, no opponent playfield).
- **Policy genuinely degenerate**: in real play it's mostly mashing rotate. Consistent with `TRAINING_NOTES.md` which notes session 1 was a total failure (0 wins / 100% topped out) and session 2 is still early — with no on-policy rollout reported, "the policy actually does something useful" is unverified.

Either way: **distilling this specific checkpoint gives you a tree that mostly outputs "press B".** That isn't a useful Dr. Mario AI.

## 4. Distillation accuracy table (train accuracy / test accuracy / node count / estimated ROM bytes)

ROM size estimated as `internal_nodes * 5` bytes (feature_idx + threshold + jump_left + jump_right + 1 overhead). Leaves assumed to fit in the parent's branch slots.

### 4.1 Raw observation input (1536 features = 16x8x12 flattened)

| max_depth | train_acc | test_acc | nodes | actual_depth | ROM bytes |
|----------:|----------:|---------:|------:|-------------:|----------:|
|         6 |     0.810 |    0.804 |   115 |            6 |       285 |
|         8 |     0.823 |    0.792 |   325 |            8 |       810 |
|        12 |     0.884 |    0.797 |  1071 |           12 |     2,675 |
|        16 |     0.932 |    0.786 |  1967 |           16 |     4,915 |
|      None |     1.000 |    0.761 |  3789 |           48 |     9,470 |

### 4.2 Engineered features (16 hand-rolled scalars)

Features: 8 column heights, virus count per color (3), capsule_x, capsule_y, left_color, right_color, next_left_color.

| max_depth | train_acc | test_acc | nodes | actual_depth | ROM bytes |
|----------:|----------:|---------:|------:|-------------:|----------:|
|         6 |     0.823 |    0.824 |   125 |            6 |       310 |
|         8 |     0.843 |    0.814 |   449 |            8 |     1,120 |
|        12 |     0.918 |    0.782 |  2299 |           12 |     5,745 |
|        16 |     0.975 |    0.762 |  4009 |           16 |    10,020 |
|      None |     1.000 |    0.755 |  4689 |           26 |    11,720 |

### 4.3 Verdict against 500-byte budget

- **Raw obs, depth=6:** 80.4% test accuracy, 285 ROM bytes — **fits**.
- **Engineered, depth=6:** 82.4% test accuracy, 310 ROM bytes — **fits**, slightly better accuracy.
- Both clear the >=70% accuracy gate, but again: majority-class baseline is 67.1%.

Note the strong overfitting at higher depths in both tables — test accuracy peaks at depth 6 and degrades thereafter while train accuracy approaches 1.0. The decision surface is shallow on these distributions.

## 5. Recommendation: distill this model, or wait for self-play?

**Wait for the self-play (or at least a verifiably competent) model.** Reasons:

1. The action distribution collapse (67% to a single rotate button) means any tree we ship right now is approximately "press B forever, occasionally press A". Even if it loads and runs on the NES, it won't play Dr. Mario meaningfully.
2. The 80% test accuracy figure is misleading — it's roughly 13 percentage points above majority-class baseline (67.1%). Most of the "signal" in the distillation is just learning the dominant action.
3. `TRAINING_NOTES.md` itself flags session 2 (dense color matching) as "Current" with no win-rate data reported. There is no rollout evidence that the policy can actually clear viruses — distilling an unproven teacher is wasted effort.
4. The distillation pipeline is now built and validated end-to-end. Once a better PPO (self-play, or at least one with documented win-rate) lands, swap `MODEL_PATH` in `scripts/eval_distill.py` and re-run. The infrastructure is ready.

**What to do in the meantime** (suggested, not required by the task):

- Add an *on-policy* sampler: run the policy in the env for K episodes and harvest (obs, action) pairs along the actual trajectory. That gives a much better training set for the tree and a more honest accuracy number (since now the distribution matches deployment).
- Track per-class precision/recall in the tree — the "always-B" baseline is what we need to beat per-action, not on aggregate.
- Consider distilling the policy *logits* (soft labels via cross-entropy from `model.policy.get_distribution(...).distribution.logits`) instead of just hard argmax actions. Gives the tree a richer regression signal and often distills better.

## 6. Recommendation: raw observations vs engineered features?

**Engineered features win on every meaningful axis** for this target:

- **Accuracy at small size:** depth-6 tree on engineered features beats depth-6 on raw obs (82.4% vs 80.4%) at virtually identical ROM cost (310B vs 285B).
- **6502 friendliness:** A raw-obs split looks like "is pixel (row=11, col=4, channel=2) above threshold t" — the runtime has to keep the full 1536-element float observation in zero page or RAM, which is impractical. Engineered features ("column heights", "yellow virus count") map to ~16 byte-sized registers that the cart can compute on the fly from the live `$0500-$057F` playfield bytes, exactly as we'd want.
- **Interpretability / debuggability:** "if col 3 height >= 11 and yellow_virus_count >= 4 then move LEFT" is something a human modder can read and verify on a real NES; opaque pixel splits are not.
- **Risk of overfitting:** both feature sets show identical overfitting at depth >= 12. That's a property of the noisy synthetic teacher, not the input representation. Keeping depth <= 6 sidesteps it.

The one caveat is that the engineered features must be representable using state the cart already has cheap access to. Column heights and per-color virus counts are trivial scans over `$0500-$057F`. Capsule x/y/color come straight from `$0381-$0386`. Next-piece color is `$039A`. All read/computed in a single frame of CPU time, no SRAM gymnastics required.

If/when we move beyond the 16-feature set, consider adding: "is current capsule color present in column k", "topmost virus row per column", "is there a 3-in-a-row of matching color in column k". Those bring more semantically rich predicates without bloating the feature vector.

## 7. Reproducing this study

```bash
# From repo root
/home/struktured/projects/dr-mario-mods/.venv/bin/python \
    /home/struktured/projects/dr-mario-mods/rl-training-new/scripts/eval_distill.py
```

Output goes to stdout. Tweak constants at the top of the script:
- `MODEL_PATH` — point at the next PPO checkpoint when it's ready.
- `N_SAMPLES` — bump to 100k once you start training real candidate trees.
- `DEPTHS` — already sweeps {6, 8, 12, 16, None}.
- `ROM_BUDGET_BYTES = 500` and `BYTES_PER_DECISION = 5` — adjust if your 6502 codec is more compact (e.g. packed feature indices could push closer to 3 bytes/node).
