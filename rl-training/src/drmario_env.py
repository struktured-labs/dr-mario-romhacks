"""
Dr. Mario Gymnasium Environment

Wrapper around Mednafen emulator for RL training.
Implements OpenAI Gym interface for compatibility with Stable-Baselines3.
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Optional, Tuple, Dict, Any

from .mednafen_interface import create_mednafen_interface
from .memory_map import *
from .state_encoder import encode_state
from .reward_function import calculate_reward


class DrMarioEnv(gym.Env):
    """
    Gymnasium environment for Dr. Mario

    Observation Space:
        Multi-channel image-like representation (12, 16, 8)
        - Channels 0-5: Player 1 (playfield + capsule)
        - Channels 6-11: Player 2 (playfield + capsule)

    Action Space:
        Discrete(12): 12 possible actions
        0: NOOP
        1: LEFT
        2: RIGHT
        3: DOWN (soft drop)
        4: A (rotate CW)
        5: B (rotate CCW)
        6: LEFT + A
        7: RIGHT + A
        8: LEFT + B
        9: RIGHT + B
        10: DOWN + LEFT
        11: DOWN + RIGHT
    """

    metadata = {'render_modes': ['rgb_array', 'human']}

    # Action mapping
    ACTIONS = [
        0x00,                          # 0: NOOP
        BTN_LEFT,                      # 1: LEFT
        BTN_RIGHT,                     # 2: RIGHT
        BTN_DOWN,                      # 3: DOWN
        BTN_A_ROTATE_CW,               # 4: A
        BTN_B_ROTATE_CCW,              # 5: B
        BTN_LEFT | BTN_A_ROTATE_CW,    # 6: LEFT + A
        BTN_RIGHT | BTN_A_ROTATE_CW,   # 7: RIGHT + A
        BTN_LEFT | BTN_B_ROTATE_CCW,   # 8: LEFT + B
        BTN_RIGHT | BTN_B_ROTATE_CCW,  # 9: RIGHT + B
        BTN_DOWN | BTN_LEFT,           # 10: DOWN + LEFT
        BTN_DOWN | BTN_RIGHT,          # 11: DOWN + RIGHT
    ]

    def __init__(
        self,
        rom_path: str = "drmario.nes",
        player_id: int = 1,
        opponent: Optional['DrMarioAgent'] = None,
        max_episode_steps: int = 10000,
        headless: bool = True
    ):
        """
        Args:
            rom_path: Path to Dr. Mario ROM file
            player_id: Which player this agent controls (1 or 2)
            opponent: Optional opponent agent for self-play
            max_episode_steps: Maximum frames per episode
            headless: Run Mednafen without GUI
        """
        super().__init__()

        self.rom_path = rom_path
        self.player_id = player_id
        self.opponent = opponent
        self.max_episode_steps = max_episode_steps
        self.headless = headless

        # Initialize Mednafen interface
        self.mednafen = None

        # Define action and observation spaces
        self.action_space = spaces.Discrete(len(self.ACTIONS))

        # Observation: 12-channel image (16 rows × 8 columns)
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(12, PLAYFIELD_HEIGHT, PLAYFIELD_WIDTH),
            dtype=np.float32
        )

        # Episode tracking
        self.current_step = 0
        self.prev_state = None

    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Reset environment to initial state"""
        super().reset(seed=seed)

        # Start or reset Mednafen
        if self.mednafen is None:
            self.mednafen = create_mednafen_interface(
                self.rom_path,
                headless=self.headless
            )
        else:
            self.mednafen.reset()

        # Navigate menus to start 2-player game
        self._navigate_to_game()

        # Reset episode tracking
        self.current_step = 0
        self.prev_state = None

        # Get initial observation
        obs = self._get_observation()
        info = self._get_info()

        return obs, info

    def step(
        self,
        action: int
    ) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        Execute one environment step

        Args:
            action: Action index (0-11)

        Returns:
            observation, reward, terminated, truncated, info
        """
        self.current_step += 1

        # Store previous state for reward calculation
        self.prev_state = self._read_raw_state()

        # Convert action to button mask
        buttons = self.ACTIONS[action]

        # Get opponent action if present
        if self.opponent is not None:
            opp_obs = self._get_opponent_observation()
            opp_action = self.opponent.predict(opp_obs)
            opp_buttons = self.ACTIONS[opp_action]
        else:
            opp_buttons = 0x00  # No input

        # Inject controller inputs
        if self.player_id == 1:
            self.mednafen.write_memory(P1_CONTROLLER, buttons)
            self.mednafen.write_memory(P2_CONTROLLER, opp_buttons)
        else:
            self.mednafen.write_memory(P1_CONTROLLER, opp_buttons)
            self.mednafen.write_memory(P2_CONTROLLER, buttons)

        # Step emulator one frame
        self.mednafen.step_frame()

        # Read new state
        current_state = self._read_raw_state()

        # Calculate reward
        reward = calculate_reward(
            self.prev_state,
            current_state,
            player_id=self.player_id
        )

        # Check terminal conditions
        terminated = self._check_game_over(current_state)
        truncated = self.current_step >= self.max_episode_steps

        # Get observation and info
        obs = self._get_observation()
        info = self._get_info()

        return obs, reward, terminated, truncated, info

    def _navigate_to_game(self):
        """
        Auto-navigate menus to start 2-player game

        Sequence (from headless_test.py):
        1. Wait for title screen
        2. Press START
        3. Select 2P mode
        4. Set level/speed
        5. Start game
        """
        # Frame-by-frame menu navigation
        # TODO: Implement based on headless_test.py logic

        for frame in range(600):
            if frame < 120:
                # Wait for title
                action = 0x00
            elif frame == 130:
                # Press START to exit title
                action = BTN_START
            elif frame == 200:
                # Press RIGHT to select 2P
                action = BTN_RIGHT
            elif frame == 250:
                # Press START to confirm 2P
                action = BTN_START
            elif 300 <= frame < 400:
                # Increase level (optional)
                if frame % 20 == 0:
                    action = BTN_A_ROTATE_CW  # Increase level
                else:
                    action = 0x00
            elif frame == 450:
                # Press START to begin
                action = BTN_START
            else:
                action = 0x00

            # Apply input to both controllers (same for menu)
            self.mednafen.write_memory(P1_CONTROLLER, action)
            self.mednafen.write_memory(P2_CONTROLLER, action)
            self.mednafen.step_frame()

    def _read_raw_state(self) -> Dict[str, Any]:
        """Read raw game state from memory"""
        if self.player_id == 1:
            playfield = self.mednafen.read_memory(P1_PLAYFIELD_START, P1_PLAYFIELD_SIZE)
            capsule_x = self.mednafen.read_memory(P1_CAPSULE_X, 1)[0]
            capsule_y = self.mednafen.read_memory(P1_CAPSULE_Y, 1)[0]
            capsule_left_color = self.mednafen.read_memory(P1_CAPSULE_LEFT_COLOR, 1)[0]
            capsule_right_color = self.mednafen.read_memory(P1_CAPSULE_RIGHT_COLOR, 1)[0]
            rotation = self.mednafen.read_memory(P1_CAPSULE_ROTATION, 1)[0]
            virus_count = self.mednafen.read_memory(P1_VIRUS_COUNT, 1)[0]

            opp_playfield = self.mednafen.read_memory(P2_PLAYFIELD_START, P2_PLAYFIELD_SIZE)
            opp_virus_count = self.mednafen.read_memory(P2_VIRUS_COUNT, 1)[0]
        else:
            playfield = self.mednafen.read_memory(P2_PLAYFIELD_START, P2_PLAYFIELD_SIZE)
            capsule_x = self.mednafen.read_memory(P2_CAPSULE_X, 1)[0]
            capsule_y = self.mednafen.read_memory(P2_CAPSULE_Y, 1)[0]
            capsule_left_color = self.mednafen.read_memory(P2_CAPSULE_LEFT_COLOR, 1)[0]
            capsule_right_color = self.mednafen.read_memory(P2_CAPSULE_RIGHT_COLOR, 1)[0]
            rotation = self.mednafen.read_memory(P2_CAPSULE_ROTATION, 1)[0]
            virus_count = self.mednafen.read_memory(P2_VIRUS_COUNT, 1)[0]

            opp_playfield = self.mednafen.read_memory(P1_PLAYFIELD_START, P1_PLAYFIELD_SIZE)
            opp_virus_count = self.mednafen.read_memory(P1_VIRUS_COUNT, 1)[0]

        return {
            'playfield': playfield,
            'capsule_x': capsule_x,
            'capsule_y': capsule_y,
            'capsule_left_color': capsule_left_color,
            'capsule_right_color': capsule_right_color,
            'rotation': rotation,
            'virus_count': virus_count,
            'opponent_playfield': opp_playfield,
            'opponent_virus_count': opp_virus_count,
        }

    def _get_observation(self) -> np.ndarray:
        """Get encoded observation for neural network"""
        state = self._read_raw_state()
        return encode_state(state)

    def _get_opponent_observation(self) -> np.ndarray:
        """Get observation from opponent's perspective"""
        # Swap self/opponent data
        state = self._read_raw_state()
        opp_state = {
            'playfield': state['opponent_playfield'],
            'virus_count': state['opponent_virus_count'],
            'opponent_playfield': state['playfield'],
            'opponent_virus_count': state['virus_count'],
            # Opponent capsule data would need separate read
            # For now, use dummy data
            'capsule_x': 0,
            'capsule_y': 0,
            'capsule_left_color': 0,
            'capsule_right_color': 0,
            'rotation': 0,
        }
        return encode_state(opp_state)

    def _check_game_over(self, state: Dict[str, Any]) -> bool:
        """Check if game has ended"""
        # Game ends when either player wins or loses
        # TODO: Detect actual game over condition from memory
        # For now, check if all viruses cleared
        return state['virus_count'] == 0 or state['opponent_virus_count'] == 0

    def _get_info(self) -> Dict[str, Any]:
        """Get auxiliary information"""
        state = self._read_raw_state()
        return {
            'virus_count': state['virus_count'],
            'opponent_virus_count': state['opponent_virus_count'],
            'frame': self.current_step,
        }

    def render(self):
        """Render environment (optional)"""
        # Could enable Mednafen GUI or export screenshot
        pass

    def close(self):
        """Clean up resources"""
        if self.mednafen:
            self.mednafen.stop()
