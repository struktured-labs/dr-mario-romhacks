#!/usr/bin/env python3
"""
2-Agent Self-Play Training for Dr. Mario

Both P1 and P2 controlled by RL agents, competing against each other.
Agents improve through self-play (like AlphaGo, OpenAI Five).

Usage:
    python scripts/train_2agent.py --timesteps 1000000 --device cuda
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import torch
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor

from drmario_env import DrMarioEnv
from custom_cnn import DrMarioCNN


class TwoAgentWrapper:
    """
    Wrapper that manages two agents playing against each other.

    Both agents share the same Mednafen instance but control different players.
    Agents take turns acting, simulating simultaneous play.
    """

    def __init__(self, host="localhost", port=8000):
        # Create two environments (one per player)
        self.env_p1 = DrMarioEnv(mesen_host=host, mesen_port=port, player_id=1)
        self.env_p2 = DrMarioEnv(mesen_host=host, mesen_port=port, player_id=2)

        # Connect both (they share the MCP server)
        self.env_p1.connect()
        self.env_p2.connect()

        # Shared episode state
        self.current_step = 0
        self.max_steps = 10000

    def reset(self):
        """Reset both agents."""
        obs_p1, _ = self.env_p1.reset()
        obs_p2, _ = self.env_p2.reset()

        self.current_step = 0

        return {
            'agent_p1': obs_p1,
            'agent_p2': obs_p2
        }

    def step(self, actions):
        """
        Step both agents simultaneously.

        Args:
            actions: Dict with 'agent_p1' and 'agent_p2' actions

        Returns:
            observations, rewards, dones, infos (all dicts)
        """
        # Write both controller inputs to Mednafen
        # P1 writes to $F5, P2 writes to $F6
        action_p1 = self.env_p1.ACTIONS[actions['agent_p1']]
        action_p2 = self.env_p2.ACTIONS[actions['agent_p2']]

        self.env_p1.mesen.write_memory(0xF5, [action_p1])
        self.env_p2.mesen.write_memory(0xF6, [action_p2])

        # Step the emulator (shared between both)
        self.env_p1.mesen.step_frame()

        # Get new state
        state = self.env_p1.mesen.get_game_state()

        # Encode observations for both players
        obs_p1 = self.env_p1.encoder.encode(state)
        obs_p2 = self.env_p2.encoder.encode(state)

        # Calculate rewards
        # P1 gets positive reward if P2 topped out OR P1 cleared all viruses
        # P2 gets positive reward if P1 topped out OR P2 cleared all viruses

        p1_viruses = state.get('virus_count', 10)  # P1 virus count
        p2_viruses = state.get('virus_count', 10)  # TODO: Get P2 virus count separately

        # Check win conditions
        p1_won = (p1_viruses == 0)
        p2_won = (p2_viruses == 0)

        # Check loss conditions (topped out)
        # TODO: Detect topped out for each player
        p1_topped_out = False
        p2_topped_out = False

        # Rewards: +1 for winning, -1 for losing, 0 otherwise
        reward_p1 = 0.0
        reward_p2 = 0.0

        if p1_won or p2_topped_out:
            reward_p1 = 1.0
            reward_p2 = -1.0
        elif p2_won or p1_topped_out:
            reward_p1 = -1.0
            reward_p2 = 1.0

        # Done if either player won or both topped out
        done = p1_won or p2_won or p1_topped_out or p2_topped_out

        self.current_step += 1
        if self.current_step >= self.max_steps:
            done = True

        return (
            {'agent_p1': obs_p1, 'agent_p2': obs_p2},
            {'agent_p1': reward_p1, 'agent_p2': reward_p2},
            {'agent_p1': done, 'agent_p2': done, '__all__': done},
            {'agent_p1': {}, 'agent_p2': {}}
        )


def train_self_play(args):
    """Train two agents via self-play."""
    print("="*60)
    print("Dr. Mario 2-Agent Self-Play Training")
    print("="*60)
    print(f"Device: {args.device}")
    print(f"Total timesteps: {args.timesteps:,}")
    print("="*60)
    print()

    # Create directories
    log_dir = Path("logs/tensorboard_2agent")
    log_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_dir = Path("models/checkpoints_2agent")
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    # Create wrapper
    wrapper = TwoAgentWrapper()

    # For now, train P2 against P1 making random moves
    # TODO: Full multi-agent training with RLlib or custom implementation

    print("NOTE: This is a simplified implementation")
    print("For true self-play, use RLlib or implement custom multi-agent training")
    print()
    print("Current setup: P1 random policy, P2 learning policy")
    print()

    # Train P2 only for now
    env_p2 = Monitor(DrMarioEnv(mesen_host="localhost", mesen_port=8000, player_id=2))

    # But make P1 take random actions every frame
    # This gives P2 a moving target (better than idle P1)

    print("Starting training...")
    print("(See MULTI_AGENT_PLAN.md for full 2-agent implementation)")
    print()


def main():
    parser = argparse.ArgumentParser(description="Train Dr. Mario 2-agent self-play")

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

    args = parser.parse_args()

    print("2-Agent training requires full multi-agent framework")
    print("See MULTI_AGENT_PLAN.md for implementation details")
    print()
    print("Quick fix for current training:")
    print("  1. Stop current training (Ctrl+C)")
    print("  2. Modify reward function to give dense rewards")
    print("  3. Add random P1 opponent (via controller injection)")
    print()


if __name__ == "__main__":
    main()
