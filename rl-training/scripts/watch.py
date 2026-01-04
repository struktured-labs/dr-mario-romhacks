#!/usr/bin/env python3
"""
Watch a trained Dr. Mario agent play

Loads a trained model and visualizes gameplay.
"""

import sys
from pathlib import Path
import argparse

sys.path.insert(0, str(Path(__file__).parent.parent))

from stable_baselines3 import PPO
from src.drmario_env import DrMarioEnv


def watch(model_path: str, rom_path: str, episodes: int = 10):
    """
    Watch trained agent play

    Args:
        model_path: Path to saved model (.zip)
        rom_path: Path to ROM file
        episodes: Number of episodes to watch
    """
    print(f"Loading model from {model_path}...")
    model = PPO.load(model_path)

    print(f"Creating environment with ROM {rom_path}...")
    env = DrMarioEnv(rom_path=rom_path, headless=False)  # Enable rendering

    for episode in range(episodes):
        print(f"\n{'='*60}")
        print(f"Episode {episode + 1}/{episodes}")
        print(f"{'='*60}")

        obs, info = env.reset()
        total_reward = 0
        steps = 0
        done = False

        while not done:
            # Predict action (deterministic for evaluation)
            action, _states = model.predict(obs, deterministic=True)

            # Step environment
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            total_reward += reward
            steps += 1

            # Print status every 60 frames
            if steps % 60 == 0:
                print(f"  Frame {steps}, Viruses: {info.get('virus_count', '?')}, "
                      f"Reward: {total_reward:.1f}")

        print(f"\nEpisode finished!")
        print(f"  Total steps: {steps}")
        print(f"  Total reward: {total_reward:.1f}")
        print(f"  Viruses remaining: {info.get('virus_count', '?')}")

    env.close()
    print("\nDone!")


def main():
    parser = argparse.ArgumentParser(description="Watch trained Dr. Mario agent")
    parser.add_argument(
        "model",
        type=str,
        help="Path to trained model (.zip file)"
    )
    parser.add_argument(
        "--rom",
        type=str,
        default="../drmario.nes",
        help="Path to Dr. Mario ROM"
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=10,
        help="Number of episodes to watch"
    )

    args = parser.parse_args()

    watch(
        model_path=args.model,
        rom_path=args.rom,
        episodes=args.episodes
    )


if __name__ == "__main__":
    main()
