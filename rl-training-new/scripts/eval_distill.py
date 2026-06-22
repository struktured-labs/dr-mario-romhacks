"""
eval_distill.py — Distillation feasibility study for the existing PPO Dr. Mario model.

End goal: distill the PPO policy into a small decision tree (~500 bytes) that can be
hand-compiled to 6502 assembly and embedded in an expanded NES ROM.

This script:
  1. Loads ppo_drmario_final.zip (sb3 PPO with custom CNN over (16, 8, 12) obs).
  2. Generates N synthetic observations by sampling random sparse playfields
     (variable virus count, optional in-flight capsule, random next-piece preview),
     then encoding via StateEncoder.
  3. Queries the PPO policy with deterministic=True to harvest (X, y) pairs.
  4. Trains sklearn DecisionTreeClassifier at several depths on (a) the raw 1536-dim
     observation and (b) a hand-engineered 16-feature representation.
  5. Estimates 6502 ROM footprint (5 bytes per decision node) and compares to 500-byte
     budget.

NOTE: Synthetic obs are off-distribution wrt the policy's training trajectory, but
they're sufficient to estimate "how compressible is this policy's decision surface"
and to validate that the distillation pipeline works end-to-end.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import numpy as np

# Make rl-training-new/src importable
_THIS_DIR = Path(__file__).resolve().parent
_SRC_DIR = _THIS_DIR.parent / "src"
sys.path.insert(0, str(_SRC_DIR))

from stable_baselines3 import PPO  # noqa: E402
from sklearn.tree import DecisionTreeClassifier  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402

from state_encoder import StateEncoder  # noqa: E402
from memory_map import (  # noqa: E402
    TILE_EMPTY,
    TILE_VIRUS_YELLOW,
    TILE_VIRUS_RED,
    TILE_VIRUS_BLUE,
    PLAYFIELD_WIDTH,
    PLAYFIELD_HEIGHT,
    COLOR_YELLOW,
    COLOR_RED,
    COLOR_BLUE,
)


MODEL_PATH = "/home/struktured/projects/dr-mario-mods/rl-training-new/models/ppo_drmario_final.zip"
N_SAMPLES = 20_000
DEPTHS = [6, 8, 12, 16, None]
ROM_BUDGET_BYTES = 500
BYTES_PER_DECISION = 5  # feature_idx + threshold + jump_left + jump_right + 1 overhead
TARGET_ACCURACY = 0.70

VIRUSES = (TILE_VIRUS_YELLOW, TILE_VIRUS_RED, TILE_VIRUS_BLUE)
PILL_TILES_BY_COLOR = {
    # Approximation: pick representative pill bytes within each color band.
    COLOR_YELLOW: 0x40,
    COLOR_RED: 0x5C,
    COLOR_BLUE: 0x68,
}


# ----------------------------------------------------------------------------
# Synthetic state sampler
# ----------------------------------------------------------------------------

def sample_random_state(rng: np.random.Generator) -> dict:
    """Sample a plausible-looking Dr. Mario state for distillation queries.

    The sampler intentionally stays sparse (most cells empty, few viruses, a
    handful of stray pill pieces). It is NOT trying to be game-legal — it just
    needs to span the input distribution well enough to expose the policy's
    decision boundaries.
    """
    playfield = np.full(PLAYFIELD_WIDTH * PLAYFIELD_HEIGHT, TILE_EMPTY, dtype=np.uint8)

    # 0-30 viruses, biased toward the bottom of the playfield (Dr. Mario reality).
    n_viruses = int(rng.integers(0, 31))
    if n_viruses:
        # Viruses live in rows 6-15 in real games. We'll allow rows 4-15 here.
        rows = rng.integers(4, 16, size=n_viruses)
        cols = rng.integers(0, 8, size=n_viruses)
        for r, c in zip(rows, cols):
            idx = int(r) * PLAYFIELD_WIDTH + int(c)
            playfield[idx] = int(rng.choice(VIRUSES))

    # 0-10 stray pill pieces scattered around (simulates partial gameplay).
    n_pills = int(rng.integers(0, 11))
    if n_pills:
        rows = rng.integers(2, 16, size=n_pills)
        cols = rng.integers(0, 8, size=n_pills)
        for r, c in zip(rows, cols):
            idx = int(r) * PLAYFIELD_WIDTH + int(c)
            if playfield[idx] == TILE_EMPTY:
                color = int(rng.integers(0, 3))
                playfield[idx] = PILL_TILES_BY_COLOR[color]

    # Active capsule: usually present (row 0-3), occasionally absent (-1).
    if rng.random() < 0.9:
        capsule_x = int(rng.integers(0, 7))  # leave room for right half
        capsule_y = int(rng.integers(0, 4))
    else:
        capsule_x = -1
        capsule_y = -1

    left_color = int(rng.integers(0, 3))
    right_color = int(rng.integers(0, 3))
    next_left = int(rng.integers(0, 3))
    next_right = int(rng.integers(0, 3))

    return {
        "playfield": playfield.tolist(),
        "capsule_x": capsule_x,
        "capsule_y": capsule_y,
        "left_color": left_color,
        "right_color": right_color,
        "next_left_color": next_left,
        "next_right_color": next_right,
        # P1 fields intentionally omitted -> P2-only encoder behavior; channels 6-11
        # stay zero, matching the policy's input distribution when P1 data is
        # unavailable.
    }


# ----------------------------------------------------------------------------
# Engineered feature extractor (16 floats)
# ----------------------------------------------------------------------------

ENGINEERED_FEATURE_NAMES = [
    "col0_height", "col1_height", "col2_height", "col3_height",
    "col4_height", "col5_height", "col6_height", "col7_height",
    "yellow_virus_count", "red_virus_count", "blue_virus_count",
    "capsule_x", "capsule_y",
    "left_color", "right_color", "next_left_color",
]


def engineered_features(state: dict) -> np.ndarray:
    """Reduce a state to 16 hand-engineered floats — the kind of features a 6502
    cart could actually compute cheaply at runtime."""
    playfield = np.array(state["playfield"], dtype=np.uint8).reshape(
        PLAYFIELD_HEIGHT, PLAYFIELD_WIDTH
    )
    occupied = playfield != TILE_EMPTY

    # Column heights: distance from top of playfield to first occupied cell.
    heights = np.full(PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT, dtype=np.float32)
    for col in range(PLAYFIELD_WIDTH):
        col_occupied = np.where(occupied[:, col])[0]
        if col_occupied.size:
            heights[col] = float(PLAYFIELD_HEIGHT - col_occupied[0])

    yellow_v = float(np.sum(playfield == TILE_VIRUS_YELLOW))
    red_v = float(np.sum(playfield == TILE_VIRUS_RED))
    blue_v = float(np.sum(playfield == TILE_VIRUS_BLUE))

    return np.array(
        [
            *heights.tolist(),
            yellow_v, red_v, blue_v,
            float(state.get("capsule_x", -1)),
            float(state.get("capsule_y", -1)),
            float(state.get("left_color", -1)),
            float(state.get("right_color", -1)),
            float(state.get("next_left_color", -1)),
        ],
        dtype=np.float32,
    )


# ----------------------------------------------------------------------------
# Tree size estimator
# ----------------------------------------------------------------------------

def estimate_rom_bytes(tree_clf: DecisionTreeClassifier) -> int:
    """Estimate compiled-tree ROM footprint at BYTES_PER_DECISION per internal
    node. Leaves are assumed to fit inside the parent's branch slots, so they
    don't add bytes beyond the parent's accounting."""
    tree = tree_clf.tree_
    # An internal node has children_left != -1 (and -1 indicates leaf).
    n_internal = int(np.sum(tree.children_left != -1))
    return n_internal * BYTES_PER_DECISION


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> None:
    print("=" * 78)
    print("Dr. Mario PPO -> Decision Tree distillation feasibility study")
    print("=" * 78)

    print(f"\n[1/5] Loading PPO model from {MODEL_PATH}")
    model = PPO.load(MODEL_PATH, device="cpu")
    print(f"  policy class : {type(model.policy).__name__}")
    print(f"  obs space    : {model.observation_space}")
    print(f"  action space : {model.action_space}")
    print()
    print("  full policy architecture:")
    print(model.policy)

    encoder = StateEncoder(player_id=2)

    # ------------------------------------------------------------------
    # Phase 1: Generate synthetic observations and collect policy actions.
    # ------------------------------------------------------------------
    print(f"\n[2/5] Sampling {N_SAMPLES} synthetic states and querying PPO policy...")
    rng = np.random.default_rng(seed=20260621)

    obs_raw = np.zeros((N_SAMPLES, PLAYFIELD_HEIGHT, PLAYFIELD_WIDTH, 12),
                       dtype=np.float32)
    eng = np.zeros((N_SAMPLES, len(ENGINEERED_FEATURE_NAMES)), dtype=np.float32)

    t0 = time.time()
    for i in range(N_SAMPLES):
        state = sample_random_state(rng)
        obs_raw[i] = encoder.encode(state)
        eng[i] = engineered_features(state)
        if (i + 1) % 5000 == 0:
            print(f"    {i + 1}/{N_SAMPLES} states encoded "
                  f"({time.time() - t0:.1f}s)")
    print(f"  sampling+encoding done in {time.time() - t0:.1f}s")

    # Batched predict
    print("  running PPO.predict (batched)...")
    t0 = time.time()
    actions, _ = model.predict(obs_raw, deterministic=True)
    actions = np.asarray(actions, dtype=np.int64)
    print(f"  predict done in {time.time() - t0:.1f}s; action distribution:")
    counts = np.bincount(actions, minlength=9)
    for a, c in enumerate(counts):
        pct = 100.0 * c / N_SAMPLES
        print(f"    action {a}: {c:5d} ({pct:5.2f}%)")
    n_unique = int(np.sum(counts > 0))
    top_action = int(np.argmax(counts))
    top_pct = 100.0 * counts[top_action] / N_SAMPLES
    if n_unique <= 3:
        print(f"  WARNING: only {n_unique} of 9 actions ever chosen "
              f"(top action {top_action} -> {top_pct:.1f}%).")
        print(f"  This suggests the PPO policy collapses on off-distribution "
              f"inputs — a trivial distillation tree could match it.")

    X_raw = obs_raw.reshape(N_SAMPLES, -1)  # (N, 1536)
    print(f"  raw flat feature dim: {X_raw.shape[1]}")
    print(f"  engineered feature dim: {eng.shape[1]}")

    # ------------------------------------------------------------------
    # Phase 2: Train decision trees on raw observations.
    # ------------------------------------------------------------------
    print("\n[3/5] Training DecisionTreeClassifier on RAW observations")
    print(f"      (input dim = {X_raw.shape[1]}, classes = 9)")
    # Drop stratification: highly collapsed action distributions (e.g. one rare
    # action with a single sample) make stratified splits raise. A plain random
    # split is fine for our purposes.
    X_tr, X_te, y_tr, y_te = train_test_split(
        X_raw, actions, test_size=0.2, random_state=42
    )

    raw_results = []
    for depth in DEPTHS:
        clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
        clf.fit(X_tr, y_tr)
        train_acc = clf.score(X_tr, y_tr)
        test_acc = clf.score(X_te, y_te)
        nodes = int(clf.tree_.node_count)
        depth_actual = int(clf.get_depth())
        rom = estimate_rom_bytes(clf)
        raw_results.append({
            "depth": depth, "train_acc": train_acc, "test_acc": test_acc,
            "nodes": nodes, "depth_actual": depth_actual, "rom_bytes": rom,
        })
        print(f"  depth={str(depth):>4}  train={train_acc:.3f}  test={test_acc:.3f}"
              f"  nodes={nodes:>5}  depth_actual={depth_actual:>3}"
              f"  rom_est={rom:>6}B")

    # ------------------------------------------------------------------
    # Phase 3: Train decision trees on engineered features.
    # ------------------------------------------------------------------
    print("\n[4/5] Training DecisionTreeClassifier on ENGINEERED features")
    print(f"      (input dim = {eng.shape[1]}, classes = 9)")
    X_tr_e, X_te_e, y_tr_e, y_te_e = train_test_split(
        eng, actions, test_size=0.2, random_state=42
    )

    eng_results = []
    for depth in DEPTHS:
        clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
        clf.fit(X_tr_e, y_tr_e)
        train_acc = clf.score(X_tr_e, y_tr_e)
        test_acc = clf.score(X_te_e, y_te_e)
        nodes = int(clf.tree_.node_count)
        depth_actual = int(clf.get_depth())
        rom = estimate_rom_bytes(clf)
        eng_results.append({
            "depth": depth, "train_acc": train_acc, "test_acc": test_acc,
            "nodes": nodes, "depth_actual": depth_actual, "rom_bytes": rom,
        })
        print(f"  depth={str(depth):>4}  train={train_acc:.3f}  test={test_acc:.3f}"
              f"  nodes={nodes:>5}  depth_actual={depth_actual:>3}"
              f"  rom_est={rom:>6}B")

    # ------------------------------------------------------------------
    # Phase 4: Budget verdict.
    # ------------------------------------------------------------------
    print("\n[5/5] ROM-budget verdict")
    print(f"  target accuracy : >={TARGET_ACCURACY:.0%}")
    print(f"  rom budget      : {ROM_BUDGET_BYTES} bytes "
          f"({BYTES_PER_DECISION}B per decision)")

    def best_under_budget(results, label):
        # Smallest tree (by ROM bytes) that hits the accuracy target.
        passing = [r for r in results if r["test_acc"] >= TARGET_ACCURACY]
        if not passing:
            best = max(results, key=lambda r: r["test_acc"])
            print(f"  [{label}] NO depth reaches {TARGET_ACCURACY:.0%} test accuracy. "
                  f"Best={best['test_acc']:.3f} at depth={best['depth']} "
                  f"(rom_est={best['rom_bytes']}B)")
            print(f"  [{label}] Tree fits in ROM budget: NO")
            return
        winner = min(passing, key=lambda r: r["rom_bytes"])
        verdict = "YES" if winner["rom_bytes"] <= ROM_BUDGET_BYTES else "NO"
        print(f"  [{label}] smallest tree >=70% accuracy: depth={winner['depth']}, "
              f"test_acc={winner['test_acc']:.3f}, nodes={winner['nodes']}, "
              f"rom_est={winner['rom_bytes']}B")
        print(f"  [{label}] Tree fits in ROM budget: {verdict}")

    best_under_budget(raw_results, "RAW       ")
    best_under_budget(eng_results, "ENGINEERED")

    print("\nDone.")


if __name__ == "__main__":
    main()
