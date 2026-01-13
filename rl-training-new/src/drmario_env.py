"""
Dr. Mario Gymnasium Environment

Wraps Mednafen emulator for RL training with Stable-Baselines3.
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Optional, Tuple, Dict, Any
import time

from mednafen_interface_http import MednafenInterface as MesenInterface
from memory_map import *
from state_encoder import StateEncoder
from reward_function import RewardCalculator


class DrMarioEnv(gym.Env):
    """
    Gymnasium environment for Dr. Mario

    Observation Space:
        Multi-channel spatial representation (12, 16, 8)
        - Channels 0-5: P2 playfield (empty, yellow, red, blue, capsule, next)
        - Channels 6-11: P1 playfield (for 2-player mode)

    Action Space:
        Discrete(9): 9 possible actions
        0: NOOP
        1: LEFT
        2: RIGHT
        3: DOWN (soft drop)
        4: A (rotate)
        5: B (rotate opposite)
        6: LEFT + DOWN
        7: RIGHT + DOWN
        8: LEFT + A (move + rotate)
    """

    metadata = {'render_modes': []}

    # Action mapping to controller bytes
    ACTIONS = [
        0x00,                    # 0: NOOP
        BTN_LEFT,                # 1: LEFT
        BTN_RIGHT,               # 2: RIGHT
        BTN_DOWN,                # 3: DOWN
        BTN_A_ROTATE_CW,         # 4: A (rotate)
        BTN_B_ROTATE_CCW,        # 5: B (rotate opposite)
        BTN_LEFT | BTN_DOWN,     # 6: LEFT + DOWN
        BTN_RIGHT | BTN_DOWN,    # 7: RIGHT + DOWN
        BTN_LEFT | BTN_A_ROTATE_CW,  # 8: LEFT + A
    ]

    def __init__(
        self,
        mesen_host: str = "localhost",
        mesen_port: int = 8000,
        player_id: int = 2,
        max_episode_steps: int = 10000,
        frame_skip: int = 1,
    ):
        """
        Args:
            mesen_host: HTTP MCP server host
            mesen_port: HTTP MCP server port (default: 8000)
            player_id: Which player this agent controls (1 or 2)
            max_episode_steps: Maximum frames per episode
            frame_skip: Number of frames to repeat each action
        """
        super().__init__()

        self.mesen_host = mesen_host
        self.mesen_port = mesen_port
        self.player_id = player_id
        self.max_episode_steps = max_episode_steps
        self.frame_skip = frame_skip

        # Initialize HTTP interface
        self.mesen = MesenInterface(host=mesen_host, port=mesen_port)
        self.connected = False

        # State encoder and reward calculator
        self.encoder = StateEncoder(player_id=player_id)
        self.reward_calc = RewardCalculator()

        # Define action and observation spaces
        self.action_space = spaces.Discrete(len(self.ACTIONS))
        self.observation_space = self.encoder.get_observation_space()

        # Episode tracking
        self.current_step = 0
        self.episode_count = 0
        self.prev_state = None

        print(f"[DrMarioEnv] Initialized for Player {player_id}")
        print(f"  Action space: {self.action_space}")
        print(f"  Observation space: {self.observation_space.shape}")

    def connect(self, timeout: float = 30.0) -> bool:
        """
        Connect to Mesen

        Args:
            timeout: Connection timeout in seconds

        Returns:
            True if connected successfully
        """
        if self.connected:
            return True

        print(f"[DrMarioEnv] Connecting to MCP server at {self.mesen_host}:{self.mesen_port}...")
        if self.mesen.connect(timeout=timeout):
            self.connected = True
            print("[DrMarioEnv] ✓ Connected!")
            return True
        else:
            print("[DrMarioEnv] ✗ Connection failed")
            return False

    def disconnect(self):
        """Disconnect from Mesen"""
        if self.connected:
            self.mesen.disconnect()
            self.connected = False
            print("[DrMarioEnv] Disconnected from Mesen")

    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Reset environment for new episode

        Returns:
            (observation, info)
        """
        super().reset(seed=seed)

        if not self.connected:
            if not self.connect():
                raise ConnectionError("Failed to connect to Mesen")

        # Reset tracking
        self.current_step = 0
        self.episode_count += 1
        self.reward_calc.reset()

        # Get initial state
        state = self.mesen.get_game_state()
        self.prev_state = state

        # Encode observation
        obs = self.encoder.encode(state)

        info = {
            'episode': self.episode_count,
            'virus_count': state['virus_count'],
            'game_mode': state['mode'],
        }

        print(f"\n[DrMarioEnv] Episode {self.episode_count} started")
        print(f"  Viruses: {state['virus_count']}")

        return obs, info

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        Take action in environment

        Args:
            action: Action index (0-8)

        Returns:
            (observation, reward, terminated, truncated, info)
        """
        if not self.connected:
            raise RuntimeError("Not connected to Mesen. Call reset() first.")

        # Map action to controller input
        controller_input = self.ACTIONS[action]

        # Write controller input and step frames
        controller_addr = P2_CONTROLLER if self.player_id == 2 else P1_CONTROLLER

        for _ in range(self.frame_skip):
            self.mesen.write_memory(controller_addr, [controller_input])
            self.mesen.step_frame()

        self.current_step += self.frame_skip

        # Read new state
        state = self.mesen.get_game_state()

        # Calculate max height (lowest occupied row)
        playfield = np.array(state['playfield']).reshape(16, 8)
        max_height = 16  # Start at bottom
        for row in range(16):
            if np.any(playfield[row, :] != TILE_EMPTY):
                max_height = row
                break

        # Calculate reward
        reward = self.reward_calc.calculate(
            virus_count=state['virus_count'],
            max_height=max_height,
            game_over=False,  # TODO: Detect game over
            all_viruses_cleared=(state['virus_count'] == 0),
        )

        # Check termination conditions
        terminated = False
        truncated = False

        # Win condition
        if state['virus_count'] == 0:
            terminated = True
            print(f"[DrMarioEnv] ✓ Episode {self.episode_count} WON!")

        # Game over (topped out - simplistic check)
        if max_height <= 2:  # Stacked to near-top
            terminated = True
            reward += self.reward_calc.GAME_OVER_PENALTY
            print(f"[DrMarioEnv] ✗ Episode {self.episode_count} GAME OVER (topped out)")

        # Max steps reached
        if self.current_step >= self.max_episode_steps:
            truncated = True
            print(f"[DrMarioEnv] Episode {self.episode_count} truncated (max steps)")

        # Encode observation
        obs = self.encoder.encode(state)

        # Update prev state
        self.prev_state = state

        info = {
            'episode': self.episode_count,
            'step': self.current_step,
            'virus_count': state['virus_count'],
            'max_height': max_height,
            'episode_reward': self.reward_calc.get_episode_reward(),
        }

        return obs, reward, terminated, truncated, info

    def close(self):
        """Clean up environment"""
        self.disconnect()

    def __enter__(self):
        """Context manager support"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        self.close()


if __name__ == "__main__":
    # Test environment
    print("Testing Dr. Mario Gymnasium environment...")
    print()
    print("Prerequisites:")
    print("  1. Mesen running with Dr. Mario ROM")
    print("  2. Lua bridge loaded (mesen_bridge.lua)")
    print("  3. Game started in VS CPU mode")
    print()

    # Create environment
    env = DrMarioEnv(player_id=2)

    try:
        # Connect
        if not env.connect(timeout=10):
            print("Failed to connect. Exiting.")
            exit(1)

        # Run one episode
        obs, info = env.reset()
        print(f"\nInitial observation shape: {obs.shape}")
        print(f"Initial info: {info}")

        # Take random actions for 100 steps
        for i in range(100):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)

            if i % 10 == 0:
                print(f"Step {i}: reward={reward:.2f}, viruses={info['virus_count']}, height={info['max_height']}")

            if terminated or truncated:
                print(f"\nEpisode ended at step {i}")
                print(f"Final reward: {info['episode_reward']:.2f}")
                break

        print("\n✓ Environment test complete!")

    finally:
        env.close()
