#!/usr/bin/env python3
"""
Dr. Mario RL Training Script

Main entry point for training agents via self-play.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor
import argparse

from src.drmario_env import DrMarioEnv


def make_env(rom_path: str, rank: int, seed: int = 0):
    """
    Create a single environment instance

    Args:
        rom_path: Path to ROM file
        rank: Unique ID for this environment
        seed: Random seed

    Returns:
        Function that creates environment
    """
    def _init():
        env = DrMarioEnv(rom_path=rom_path, player_id=1)
        env = Monitor(env)  # Wrap for logging
        env.reset(seed=seed + rank)
        return env
    return _init


def train(
    rom_path: str,
    total_timesteps: int = 1_000_000,
    num_envs: int = 4,
    learning_rate: float = 3e-4,
    save_freq: int = 10_000,
    log_dir: str = "./logs",
    model_dir: str = "./models"
):
    """
    Train PPO agent on Dr. Mario

    Args:
        rom_path: Path to Dr. Mario ROM
        total_timesteps: Total training steps
        num_envs: Number of parallel environments
        learning_rate: PPO learning rate
        save_freq: Save checkpoint every N steps
        log_dir: TensorBoard log directory
        model_dir: Model checkpoint directory
    """
    print("=" * 60)
    print("Dr. Mario Deep RL Training")
    print("=" * 60)
    print(f"ROM: {rom_path}")
    print(f"Total timesteps: {total_timesteps:,}")
    print(f"Parallel envs: {num_envs}")
    print(f"Learning rate: {learning_rate}")
    print("=" * 60)

    # Create vectorized environment
    if num_envs > 1:
        env = SubprocVecEnv([make_env(rom_path, i) for i in range(num_envs)])
    else:
        env = DummyVecEnv([make_env(rom_path, 0)])

    print(f"Created {num_envs} parallel environment(s)")

    # Create PPO model
    model = PPO(
        policy="CnnPolicy",  # CNN for image-like input
        env=env,
        learning_rate=learning_rate,
        n_steps=2048,        # Steps per rollout
        batch_size=64,       # Minibatch size
        n_epochs=10,         # Optimization epochs per rollout
        gamma=0.99,          # Discount factor
        gae_lambda=0.95,     # GAE parameter
        clip_range=0.2,      # PPO clip range
        ent_coef=0.01,       # Entropy coefficient (exploration)
        vf_coef=0.5,         # Value function coefficient
        max_grad_norm=0.5,   # Gradient clipping
        verbose=1,
        tensorboard_log=f"{log_dir}/tensorboard/"
    )

    print("Created PPO model")
    print(model.policy)

    # Setup callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=save_freq,
        save_path=f"{model_dir}/checkpoints/",
        name_prefix="drmario_ppo"
    )

    # Optional: evaluation callback (for testing against fixed opponent)
    # eval_env = DummyVecEnv([make_env(rom_path, 999)])
    # eval_callback = EvalCallback(
    #     eval_env,
    #     best_model_save_path=f"{model_dir}/best/",
    #     log_path=f"{log_dir}/eval/",
    #     eval_freq=10000,
    #     deterministic=True
    # )

    print("Starting training...")

    # Train!
    model.learn(
        total_timesteps=total_timesteps,
        callback=checkpoint_callback,
        log_interval=10,
        progress_bar=True
    )

    # Save final model
    final_path = f"{model_dir}/drmario_ppo_final.zip"
    model.save(final_path)
    print(f"Training complete! Model saved to {final_path}")

    env.close()


def main():
    parser = argparse.ArgumentParser(description="Train Dr. Mario RL agent")
    parser.add_argument(
        "--rom",
        type=str,
        default="../drmario.nes",
        help="Path to Dr. Mario ROM"
    )
    parser.add_argument(
        "--timesteps",
        type=int,
        default=1_000_000,
        help="Total training timesteps"
    )
    parser.add_argument(
        "--num-envs",
        type=int,
        default=4,
        help="Number of parallel environments"
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=3e-4,
        help="Learning rate"
    )
    parser.add_argument(
        "--save-freq",
        type=int,
        default=10_000,
        help="Save checkpoint every N steps"
    )

    args = parser.parse_args()

    train(
        rom_path=args.rom,
        total_timesteps=args.timesteps,
        num_envs=args.num_envs,
        learning_rate=args.lr,
        save_freq=args.save_freq
    )


if __name__ == "__main__":
    main()
