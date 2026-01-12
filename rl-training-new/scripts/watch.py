#!/usr/bin/env python3
"""
Watch trained Dr. Mario agent play

Loads a trained model and plays Dr. Mario, showing decisions and rewards.

Usage:
    python scripts/watch.py models/ppo_drmario_final.zip
"""

import argparse
import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import torch
from stable_baselines3 import PPO

from drmario_env import DrMarioEnv


def watch(model_path: str, num_episodes: int = 3):
    """Watch agent play"""
    print("="*60)
    print("Dr. Mario Agent Evaluation")
    print("="*60)
    print(f"Model: {model_path}")
    print(f"Episodes: {num_episodes}")
    print("="*60)
    print()

    # Load model
    print(f"Loading model...")
    model = PPO.load(model_path)
    print("✓ Model loaded")
    print()

    # Create environment
    print("Creating environment...")
    env = DrMarioEnv(
        mesen_host="localhost",
        mesen_port=8765,
        player_id=2,
        max_episode_steps=10000,
    )

    if not env.connect(timeout=10):
        print("✗ Failed to connect to Mesen")
        print("Make sure:")
        print("  1. Mesen is running")
        print("  2. Lua bridge loaded")
        print("  3. Game started in VS CPU mode")
        return

    print("✓ Connected to Mesen")
    print()

    try:
        for episode in range(num_episodes):
            print(f"\n{'='*60}")
            print(f"Episode {episode + 1}/{num_episodes}")
            print(f"{'='*60}")

            obs, info = env.reset()
            episode_reward = 0
            step = 0

            while True:
                # Predict action
                action, _states = model.predict(obs, deterministic=True)

                # Take action
                obs, reward, terminated, truncated, info = env.step(action)

                episode_reward += reward
                step += 1

                # Print progress every 100 steps
                if step % 100 == 0:
                    print(f"  Step {step:4d}: viruses={info['virus_count']:2d}, "
                          f"height={info['max_height']:2d}, reward={reward:6.2f}")

                if terminated or truncated:
                    print(f"\nEpisode ended:")
                    print(f"  Steps: {step}")
                    print(f"  Final virus count: {info['virus_count']}")
                    print(f"  Episode reward: {episode_reward:.2f}")
                    print(f"  Result: {'WIN' if info['virus_count'] == 0 else 'LOSS'}")
                    break

                # Small delay for visibility
                time.sleep(0.01)

        print(f"\n{'='*60}")
        print("Evaluation complete!")
        print(f"{'='*60}")

    finally:
        env.close()


def main():
    parser = argparse.ArgumentParser(description="Watch trained Dr. Mario agent")
    parser.add_argument(
        "model_path",
        type=str,
        help="Path to trained model (.zip file)",
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=3,
        help="Number of episodes to watch (default: 3)",
    )

    args = parser.parse_args()

    # Validate model path
    if not Path(args.model_path).exists():
        print(f"Error: Model file not found: {args.model_path}")
        sys.exit(1)

    watch(args.model_path, args.episodes)


if __name__ == "__main__":
    main()
