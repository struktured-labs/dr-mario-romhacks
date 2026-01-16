#!/usr/bin/env python3
"""
Train Dr. Mario PPO Agent

Uses Stable-Baselines3 with custom Gymnasium environment.

Usage:
    python scripts/train.py --timesteps 1000000 --device cuda

Requirements:
    - HTTP MCP server running (mednafen_mcp_server.py)
    - Mednafen launched via /launch endpoint (Option 2)
    - VS CPU ROM loaded and auto-navigated to gameplay
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import torch
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor

from drmario_env import DrMarioEnv


def make_env():
    """Create and wrap environment"""
    env = DrMarioEnv(
        mesen_host="localhost",
        mesen_port=8000,  # HTTP MCP server
        player_id=2,
        max_episode_steps=10000,
        frame_skip=1,
    )
    return Monitor(env)


def train(args):
    """Train PPO agent"""
    print("="*60)
    print("Dr. Mario PPO Training")
    print("="*60)
    print(f"Device: {args.device}")
    print(f"Total timesteps: {args.timesteps:,}")
    print(f"Learning rate: {args.learning_rate}")
    print(f"Batch size: {args.batch_size}")
    print(f"Save every: {args.save_freq:,} steps")
    print("="*60)
    print()

    # Create directories
    log_dir = Path("logs/tensorboard")
    log_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_dir = Path("models/checkpoints")
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    # Create environment
    print("Creating environment...")
    env = DummyVecEnv([make_env])

    # Check CUDA availability
    if args.device == "cuda" and not torch.cuda.is_available():
        print("⚠️  CUDA requested but not available. Falling back to CPU.")
        args.device = "cpu"

    if args.device == "cuda":
        device_info = torch.cuda.get_device_name(0)
        print(f"✓ Using GPU: {device_info}")
    else:
        print("✓ Using CPU")

    print()

    # Create or load model
    if args.resume:
        print(f"Loading model from {args.resume}...")
        model = PPO.load(
            args.resume,
            env=env,
            device=args.device,
            tensorboard_log=str(log_dir),
        )
        print("✓ Model loaded")
    else:
        print("Creating new PPO model...")
        model = PPO(
            policy="CnnPolicy",
            env=env,
            learning_rate=args.learning_rate,
            n_steps=args.n_steps,
            batch_size=args.batch_size,
            n_epochs=args.n_epochs,
            gamma=0.99,
            gae_lambda=0.95,
            clip_range=0.2,
            ent_coef=0.01,
            vf_coef=0.5,
            max_grad_norm=0.5,
            verbose=1,
            device=args.device,
            tensorboard_log=str(log_dir),
        )
        print("✓ Model created")

    print()
    print("Model architecture:")
    print(model.policy)
    print()

    # Callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=args.save_freq,
        save_path=str(checkpoint_dir),
        name_prefix="ppo_drmario",
        save_replay_buffer=False,
        save_vecnormalize=False,
    )

    callbacks = [checkpoint_callback]

    # Train
    print("Starting training...")
    print("Monitor progress with: tensorboard --logdir logs/tensorboard")
    print("Press Ctrl+C to stop training and save model")
    print()

    try:
        model.learn(
            total_timesteps=args.timesteps,
            callback=callbacks,
            progress_bar=True,
        )

        # Save final model
        final_path = "models/ppo_drmario_final.zip"
        model.save(final_path)
        print(f"\n✓ Training complete! Model saved to {final_path}")

    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user")
        interrupt_path = "models/ppo_drmario_interrupted.zip"
        model.save(interrupt_path)
        print(f"✓ Model saved to {interrupt_path}")

    finally:
        env.close()


def main():
    parser = argparse.ArgumentParser(description="Train Dr. Mario PPO agent")

    # Training parameters
    parser.add_argument(
        "--timesteps",
        type=int,
        default=1000000,
        help="Total timesteps to train (default: 1M)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        choices=["cuda", "cpu"],
        help="Device to use for training",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=3e-4,
        help="Learning rate (default: 3e-4)",
    )
    parser.add_argument(
        "--n-steps",
        type=int,
        default=2048,
        help="Number of steps per update (default: 2048)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Minibatch size (default: 64)",
    )
    parser.add_argument(
        "--n-epochs",
        type=int,
        default=10,
        help="Number of epochs per update (default: 10)",
    )
    parser.add_argument(
        "--save-freq",
        type=int,
        default=10000,
        help="Save checkpoint every N steps (default: 10000)",
    )
    parser.add_argument(
        "--resume",
        type=str,
        default=None,
        help="Path to model checkpoint to resume from",
    )

    args = parser.parse_args()

    # Validate
    if args.timesteps <= 0:
        print("Error: --timesteps must be positive")
        sys.exit(1)

    # Run training
    train(args)


if __name__ == "__main__":
    main()
