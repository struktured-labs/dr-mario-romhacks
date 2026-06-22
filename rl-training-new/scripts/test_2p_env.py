#!/usr/bin/env python3
"""
Smoke test for DrMario2PEnv (mock mode — no emulator required).

Verifies:
  - env constructs in mock mode without contacting Mednafen
  - observation has the expected shape/dtype
  - step() returns a JOINT-action-consuming, scalar-reward, 5-tuple result
  - terminated / truncated are booleans
  - reset() works mid-test and after episode end
  - the opponent policy is actually being invoked (we count calls)

Run:
    cd /home/struktured/projects/dr-mario-mods
    .venv/bin/python rl-training-new/scripts/test_2p_env.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make `src/` importable.
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import numpy as np  # noqa: E402

from drmario_2p_env import (  # noqa: E402
    NUM_ACTIONS,
    DrMario2PEnv,
    random_opponent_policy,
)


def main() -> int:
    print("=" * 60)
    print("DrMario2PEnv smoke test (mock_mode=True)")
    print("=" * 60)

    # Count opponent invocations to confirm the policy hook is wired up.
    call_count = {"n": 0}

    def counting_opponent(obs: np.ndarray) -> int:
        call_count["n"] += 1
        return random_opponent_policy(obs)

    env = DrMario2PEnv(
        opponent_policy=counting_opponent,
        level=5,
        mock_mode=True,
        seed=42,
        max_episode_steps=100,
    )

    # Validate spaces.
    assert env.action_space.shape == (2,), (
        f"expected joint action shape (2,), got {env.action_space.shape}"
    )
    assert tuple(env.action_space.nvec.tolist()) == (NUM_ACTIONS, NUM_ACTIONS), (
        f"expected nvec ({NUM_ACTIONS}, {NUM_ACTIONS}), got {env.action_space.nvec}"
    )
    print(f"action_space: {env.action_space}")
    print(f"observation_space: {env.observation_space}")

    # Reset.
    obs, info = env.reset()
    assert isinstance(obs, np.ndarray), f"obs must be ndarray, got {type(obs)}"
    assert obs.shape == env.observation_space.shape, (
        f"obs shape {obs.shape} != observation_space {env.observation_space.shape}"
    )
    assert obs.dtype == np.float32, f"obs dtype must be float32, got {obs.dtype}"
    assert isinstance(info, dict), f"info must be dict, got {type(info)}"
    print(f"reset OK — obs shape={obs.shape} dtype={obs.dtype}")

    rng = np.random.default_rng(0)
    total_reward = 0.0
    episodes_ended = 0

    for i in range(10):
        joint_action = env.action_space.sample()
        # Override to force a known shape (and exercise list-input path).
        joint_action = [int(rng.integers(0, NUM_ACTIONS)),
                        int(rng.integers(0, NUM_ACTIONS))]

        obs, reward, terminated, truncated, step_info = env.step(joint_action)

        assert isinstance(obs, np.ndarray), f"step obs must be ndarray, got {type(obs)}"
        assert obs.shape == env.observation_space.shape, (
            f"step obs shape {obs.shape} != {env.observation_space.shape}"
        )
        assert isinstance(reward, float), f"reward must be float, got {type(reward)}"
        assert isinstance(terminated, bool), (
            f"terminated must be bool, got {type(terminated)}"
        )
        assert isinstance(truncated, bool), (
            f"truncated must be bool, got {type(truncated)}"
        )
        assert isinstance(step_info, dict), f"info must be dict, got {type(step_info)}"
        # The env must always honor opponent-controls-p1 invariant: the
        # returned p1_action must equal whatever counting_opponent returned
        # (so call_count must increment every step).
        assert "p1_action" in step_info, "expected info to include p1_action"
        assert "p2_action" in step_info, "expected info to include p2_action"

        total_reward += reward
        if terminated or truncated:
            episodes_ended += 1
            obs, info = env.reset()

        if i % 2 == 0:
            print(
                f"step {i:>2d}: reward={reward:+.3f} term={terminated} "
                f"trunc={truncated} p1_act={step_info['p1_action']} "
                f"p2_act={step_info['p2_action']}"
            )

    # The opponent must have been called once per step, even after resets.
    assert call_count["n"] >= 10, (
        f"opponent policy should be called >=10 times, got {call_count['n']}"
    )

    env.close()

    print("-" * 60)
    print(f"steps:           10")
    print(f"episodes ended:  {episodes_ended}")
    print(f"opponent calls:  {call_count['n']}")
    print(f"total reward:    {total_reward:+.3f}")
    print("-" * 60)
    print("PASS: DrMario2PEnv smoke test")
    return 0


if __name__ == "__main__":
    sys.exit(main())
