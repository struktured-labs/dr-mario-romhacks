#!/usr/bin/env python3
"""
Self-play PPO training loop for Dr. Mario 2P.

Outline:
  - The learner controls P2 in DrMario2PEnv.
  - The opponent (P1) is sampled uniformly from a pool of past snapshots
    (default pool size K=5). On the very first iteration the pool is empty
    so the opponent is uniform-random.
  - Each iteration we train for N=200_000 timesteps, snapshot the model,
    push the snapshot into the pool, evict the oldest if we are over capacity,
    then advance the curriculum.
  - Curriculum: virus level 5 -> 10 -> 15 -> 20 -> mixed, advanced by
    iteration index (NOT timesteps, per project spec).

This script does NOT call model.learn() at import / module load time. The
actual training kicks off only from `if __name__ == "__main__":`. We expose
helper functions (`build_env`, `build_model`, `level_for_iteration`,
`SnapshotPool`) so unit tests and downstream notebooks can exercise the
loop logic without an emulator.

Usage:
    cd /home/struktured/projects/dr-mario-mods
    .venv/bin/python rl-training-new/scripts/train_selfplay.py \
        --iterations 10 --timesteps-per-iter 200000

Add --mock to run without an emulator (useful for end-to-end pipe checks).
"""

from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path
from typing import Callable, Deque, List, Optional

import numpy as np

# Make `src/` importable.
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import torch  # noqa: E402
from stable_baselines3 import PPO  # noqa: E402
from stable_baselines3.common.callbacks import CheckpointCallback  # noqa: E402
from stable_baselines3.common.monitor import Monitor  # noqa: E402
from stable_baselines3.common.vec_env import DummyVecEnv  # noqa: E402

from custom_cnn import DrMarioCNN  # noqa: E402
from drmario_2p_env import (  # noqa: E402
    NUM_ACTIONS,
    DrMario2PEnv,
    OpponentPolicy,
    random_opponent_policy,
)


# ---------------------------------------------------------------------------
# Curriculum
# ---------------------------------------------------------------------------

# Levels indexed by iteration (1-based in the design doc, 0-based here). The
# 4 leading entries cover virus difficulties; once we run out we sample
# uniformly from the mix bucket. This matches MULTI_AGENT_PLAN.md's
# "5 -> 10 -> 15 -> 20 -> mix" schedule but keyed off the SELF-PLAY
# iteration counter rather than timesteps, per project spec.
_CURRICULUM = (5, 10, 15, 20)
_MIX_BUCKET = (5, 10, 15, 20)


def level_for_iteration(iteration: int, rng: Optional[np.random.Generator] = None) -> int:
    """Return the virus level for a 0-based self-play iteration index.

    Iterations 0..3 walk through (5, 10, 15, 20). Iterations >= 4 sample
    uniformly from {5, 10, 15, 20} so the agent generalises across levels.
    """
    if iteration < len(_CURRICULUM):
        return _CURRICULUM[iteration]
    rng = rng if rng is not None else np.random.default_rng()
    return int(rng.choice(_MIX_BUCKET))


# ---------------------------------------------------------------------------
# Snapshot pool
# ---------------------------------------------------------------------------


class SnapshotPool:
    """Bounded FIFO of frozen PPO snapshots for self-play.

    Each snapshot is just the on-disk path to a `.zip` saved with
    `PPO.save()`. We materialize the model lazily — when the pool is asked
    for an opponent policy, it picks a snapshot at random and loads it onto
    CPU (cheap, and keeps GPU bandwidth focused on the learner).
    """

    def __init__(self, capacity: int = 5):
        if capacity < 1:
            raise ValueError(f"SnapshotPool capacity must be >= 1, got {capacity}")
        self.capacity = capacity
        self._paths: Deque[Path] = deque()
        # Cache of (path -> loaded PPO model) so we don't reload every call.
        self._cache: dict[Path, PPO] = {}

    def add(self, path: Path) -> None:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"snapshot does not exist: {path}")
        self._paths.append(path)
        while len(self._paths) > self.capacity:
            evicted = self._paths.popleft()
            self._cache.pop(evicted, None)

    def __len__(self) -> int:
        return len(self._paths)

    @property
    def paths(self) -> List[Path]:
        return list(self._paths)

    def sample(self, rng: Optional[np.random.Generator] = None) -> Optional[PPO]:
        """Pick a snapshot uniformly at random; return None if empty."""
        if not self._paths:
            return None
        rng = rng if rng is not None else np.random.default_rng()
        choice = rng.choice(len(self._paths))
        path = self._paths[int(choice)]
        if path not in self._cache:
            # `device='cpu'` keeps the GPU dedicated to the learner. The
            # opponent forward pass on a single 16x8x12 obs is fast on CPU.
            self._cache[path] = PPO.load(str(path), device="cpu")
        return self._cache[path]

    def make_opponent_policy(
        self,
        rng: Optional[np.random.Generator] = None,
    ) -> OpponentPolicy:
        """Build an opponent callable that re-samples a snapshot per episode.

        We pick a snapshot once (at construction) and then return its
        action for the rest of that opponent's lifetime. The self-play loop
        builds a fresh opponent per iteration, so the pool is re-sampled at
        the natural episode boundary.
        """
        model = self.sample(rng=rng)
        if model is None:
            return random_opponent_policy

        def _policy(obs: np.ndarray) -> int:
            # PPO expects a batched observation; predict() returns a numpy
            # array of actions. Since our env exposes MultiDiscrete([9,9]),
            # the snapshot was trained with that head and returns a (2,)
            # vector — we want p2's slot (the trained side).
            action, _ = model.predict(obs[None, ...], deterministic=False)
            action = np.asarray(action).reshape(-1)
            if action.size == 2:
                return int(action[1]) % NUM_ACTIONS
            return int(action[0]) % NUM_ACTIONS

        return _policy


# ---------------------------------------------------------------------------
# Env / model builders
# ---------------------------------------------------------------------------


def build_env(
    *,
    opponent_policy: Optional[OpponentPolicy],
    level: int,
    mesen_host: str = "localhost",
    mesen_port: int = 8000,
    max_episode_steps: int = 10_000,
    frame_skip: int = 1,
    mock_mode: bool = False,
    monitor_dir: Optional[Path] = None,
) -> DummyVecEnv:
    """Build a single-env DummyVecEnv wrapping DrMario2PEnv."""

    def _factory() -> Monitor:
        env = DrMario2PEnv(
            mesen_host=mesen_host,
            mesen_port=mesen_port,
            opponent_policy=opponent_policy,
            level=level,
            max_episode_steps=max_episode_steps,
            frame_skip=frame_skip,
            mock_mode=mock_mode,
        )
        if monitor_dir is not None:
            monitor_dir.mkdir(parents=True, exist_ok=True)
            return Monitor(env, filename=str(monitor_dir / f"level_{level}"))
        return Monitor(env)

    return DummyVecEnv([_factory])


def build_model(
    env: DummyVecEnv,
    *,
    device: str = "auto",
    learning_rate: float = 3e-4,
    n_steps: int = 2048,
    batch_size: int = 64,
    n_epochs: int = 10,
    tensorboard_log: Optional[Path] = None,
) -> PPO:
    policy_kwargs = dict(
        features_extractor_class=DrMarioCNN,
        features_extractor_kwargs=dict(features_dim=256),
    )
    return PPO(
        policy="CnnPolicy",
        env=env,
        learning_rate=learning_rate,
        n_steps=n_steps,
        batch_size=batch_size,
        n_epochs=n_epochs,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        vf_coef=0.5,
        max_grad_norm=0.5,
        policy_kwargs=policy_kwargs,
        verbose=1,
        device=device,
        tensorboard_log=str(tensorboard_log) if tensorboard_log else None,
    )


# ---------------------------------------------------------------------------
# Self-play loop
# ---------------------------------------------------------------------------


def run_selfplay(
    *,
    iterations: int,
    timesteps_per_iter: int,
    snapshot_capacity: int,
    snapshot_dir: Path,
    tensorboard_log: Optional[Path],
    device: str,
    mesen_host: str,
    mesen_port: int,
    mock_mode: bool,
    rng_seed: Optional[int] = None,
) -> Path:
    """Run the full self-play loop. Returns the final snapshot path."""
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    pool = SnapshotPool(capacity=snapshot_capacity)
    rng = np.random.default_rng(rng_seed)

    # ITER 0: opponent is uniform random (pool is empty).
    opponent_policy: Optional[OpponentPolicy] = random_opponent_policy
    model: Optional[PPO] = None
    final_snapshot: Optional[Path] = None

    for it in range(iterations):
        level = level_for_iteration(it, rng=rng)
        print("=" * 70)
        print(f"[selfplay] iter {it + 1}/{iterations}  level={level}  "
              f"pool={len(pool)}/{snapshot_capacity}")
        print("=" * 70)

        env = build_env(
            opponent_policy=opponent_policy,
            level=level,
            mesen_host=mesen_host,
            mesen_port=mesen_port,
            mock_mode=mock_mode,
            monitor_dir=snapshot_dir / "monitor",
        )

        if model is None:
            model = build_model(
                env,
                device=device,
                tensorboard_log=tensorboard_log,
            )
        else:
            # Reuse the learner across iterations; just swap the env so the
            # new opponent is picked up.
            model.set_env(env)

        # Checkpoint roughly 4x per iteration as a safety net.
        ckpt_freq = max(timesteps_per_iter // 4, 1)
        checkpoint_cb = CheckpointCallback(
            save_freq=ckpt_freq,
            save_path=str(snapshot_dir / f"iter_{it:03d}_ckpts"),
            name_prefix="ppo_drmario_2p",
        )

        model.learn(
            total_timesteps=timesteps_per_iter,
            callback=[checkpoint_cb],
            reset_num_timesteps=False,
            progress_bar=False,
        )

        # Snapshot + push into pool.
        snapshot_path = snapshot_dir / f"snapshot_iter_{it:03d}.zip"
        model.save(str(snapshot_path))
        pool.add(snapshot_path)
        final_snapshot = snapshot_path
        print(f"[selfplay] iter {it + 1} saved snapshot -> {snapshot_path}")

        # Next iteration's opponent samples from the (now non-empty) pool.
        opponent_policy = pool.make_opponent_policy(rng=rng)

        env.close()

    assert final_snapshot is not None
    return final_snapshot


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dr. Mario 2P self-play training")
    parser.add_argument("--iterations", type=int, default=10,
                        help="Number of self-play iterations (default: 10)")
    parser.add_argument("--timesteps-per-iter", type=int, default=200_000,
                        help="PPO timesteps per iteration (default: 200000)")
    parser.add_argument("--snapshot-capacity", type=int, default=5,
                        help="Max snapshots retained in the pool (default: 5)")
    parser.add_argument("--snapshot-dir", type=Path,
                        default=REPO_ROOT / "models" / "selfplay",
                        help="Directory for snapshots / monitor logs")
    parser.add_argument("--tensorboard-log", type=Path,
                        default=REPO_ROOT / "logs" / "tensorboard_selfplay",
                        help="Tensorboard log dir (use '' to disable)")
    parser.add_argument("--device", type=str, default="auto",
                        choices=["auto", "cpu", "cuda"],
                        help="Torch device (default: auto)")
    parser.add_argument("--mesen-host", type=str, default="localhost")
    parser.add_argument("--mesen-port", type=int, default=8000)
    parser.add_argument("--mock", action="store_true",
                        help="Use mock env (no emulator, for plumbing checks)")
    parser.add_argument("--seed", type=int, default=None)
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()

    if args.device == "cuda" and not torch.cuda.is_available():
        print("[selfplay] cuda requested but not available, falling back to cpu")
        args.device = "cpu"

    tb = args.tensorboard_log if str(args.tensorboard_log) else None

    final = run_selfplay(
        iterations=args.iterations,
        timesteps_per_iter=args.timesteps_per_iter,
        snapshot_capacity=args.snapshot_capacity,
        snapshot_dir=args.snapshot_dir,
        tensorboard_log=tb,
        device=args.device,
        mesen_host=args.mesen_host,
        mesen_port=args.mesen_port,
        mock_mode=args.mock,
        rng_seed=args.seed,
    )
    print(f"[selfplay] DONE — final snapshot: {final}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
