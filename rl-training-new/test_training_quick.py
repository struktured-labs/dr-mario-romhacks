#!/usr/bin/env python3
"""
Quick training test - 100 steps to verify the loop works.

This is NOT actual training, just a smoke test to verify:
- Environment connects
- Observations are valid
- Actions work
- Rewards calculate
- Episode logic works
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from drmario_env import DrMarioEnv
import numpy as np


def main():
    print("="*60)
    print("Quick Training Test (100 steps)")
    print("="*60)
    print()
    print("This verifies the training loop works end-to-end.")
    print("NOT actual training - just a smoke test.")
    print()

    # Create environment
    print("Creating environment...")
    env = DrMarioEnv(player_id=2, max_episode_steps=100)

    # Connect
    print("Connecting to MCP server...")
    if not env.connect(timeout=10):
        print("✗ Failed to connect!")
        return 1

    print("✓ Connected!")
    print()

    # Run one episode
    print("Starting episode...")
    obs, info = env.reset()
    print(f"✓ Reset successful")
    print(f"  Initial viruses: {info['virus_count']}")
    print(f"  Observation shape: {obs.shape}")
    print(f"  Observation range: [{obs.min():.3f}, {obs.max():.3f}]")
    print()

    # Take 100 random actions
    print("Taking 100 random actions...")
    total_reward = 0
    episode_count = 0

    for step in range(100):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)

        total_reward += reward

        if step % 20 == 0:
            print(f"  Step {step:3d}: viruses={info['virus_count']:2d}, "
                  f"height={info.get('max_height', 0):2d}, reward={reward:6.2f}")

        if terminated or truncated:
            episode_count += 1
            print(f"\n  Episode ended at step {step}")
            print(f"  Final viruses: {info['virus_count']}")
            print(f"  Episode reward: {total_reward:.2f}")
            print(f"  Reason: {'win' if terminated and info['virus_count'] == 0 else 'game over' if terminated else 'truncated'}")

            # Reset for next episode
            if step < 95:  # Don't reset if we're almost done
                print(f"\n  Starting new episode {episode_count + 1}...")
                obs, info = env.reset()
                total_reward = 0

    print()
    print("="*60)
    print("Test Summary")
    print("="*60)
    print(f"✓ Completed 100 steps")
    print(f"✓ Episodes: {episode_count + 1}")
    print(f"✓ Final total reward: {total_reward:.2f}")
    print()
    print("✓ Training loop works! Ready for actual training.")
    print()

    env.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
