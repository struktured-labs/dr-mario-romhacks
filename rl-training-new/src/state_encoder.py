"""
Dr. Mario State Encoder

Converts raw game state into multi-channel CNN-friendly representation.

Observation Space: (12, 16, 8) - 12 channels × 16 rows × 8 columns

Channels for P2 (what the agent sees):
  0: Empty tiles (1.0 = empty, 0.0 = occupied)
  1: Yellow pieces (viruses + capsules)
  2: Red pieces (viruses + capsules)
  3: Blue pieces (viruses + capsules)
  4: Current capsule position
  5: Next capsule preview (broadcast across field)

Channels for P1 (opponent, for context):
  6: Empty tiles
  7: Yellow pieces
  8: Red pieces
  9: Blue pieces
  10: P1 capsule position
  11: P1 next capsule (broadcast)

This encoding allows the CNN to learn:
- Spatial patterns (where are viruses clustered?)
- Color matching (which colors are where?)
- Capsule awareness (current and next)
- Opponent state (in 2-player mode)
"""

import numpy as np
from typing import Dict, Any, List

from memory_map import (
    PLAYFIELD_WIDTH,
    PLAYFIELD_HEIGHT,
    TILE_EMPTY,
    TILE_VIRUS_YELLOW,
    TILE_VIRUS_RED,
    TILE_VIRUS_BLUE,
    COLOR_YELLOW,
    COLOR_RED,
    COLOR_BLUE,
    is_empty,
    is_virus,
)


def tile_to_color(tile: int) -> int:
    """
    Extract color from tile value

    Args:
        tile: Tile byte value

    Returns:
        Color index (0=yellow, 1=red, 2=blue) or -1 if no color
    """
    if tile == TILE_EMPTY:
        return -1

    # Viruses
    if tile == TILE_VIRUS_YELLOW:
        return COLOR_YELLOW
    elif tile == TILE_VIRUS_RED:
        return COLOR_RED
    elif tile == TILE_VIRUS_BLUE:
        return COLOR_BLUE

    # Capsule/pill pieces (0x4C-0x72)
    # Extract color from lower 2 bits
    if 0x4C <= tile <= 0x72:
        return tile & 0x03

    # Pellets (isolated pieces)
    if 0x80 <= tile <= 0x82:
        return tile - 0x80

    return -1


class StateEncoder:
    """Encodes game state into multi-channel observation"""

    def __init__(self, player_id: int = 2):
        """
        Args:
            player_id: Which player this encoder is for (1 or 2)
        """
        self.player_id = player_id
        self.num_channels = 12
        self.obs_shape = (self.num_channels, PLAYFIELD_HEIGHT, PLAYFIELD_WIDTH)

    def encode(self, state: Dict[str, Any]) -> np.ndarray:
        """
        Encode game state into observation tensor

        Args:
            state: Game state dict with keys:
                - playfield: List[int] (128 bytes)
                - capsule_x: int
                - capsule_y: int
                - left_color: int
                - right_color: int
                - next_left_color: int (optional)
                - next_right_color: int (optional)
                - p1_playfield: List[int] (optional, for 2-player)
                - p1_capsule_x: int (optional)
                - p1_capsule_y: int (optional)

        Returns:
            Observation array of shape (12, 16, 8)
        """
        obs = np.zeros(self.obs_shape, dtype=np.float32)

        # Parse playfield into 2D grid
        playfield = np.array(state['playfield'], dtype=np.uint8).reshape(16, 8)

        # === CHANNELS 0-5: P2 (Agent's View) ===

        # Channel 0: Empty tiles
        obs[0] = (playfield == TILE_EMPTY).astype(np.float32)

        # Channels 1-3: Color channels (yellow, red, blue)
        for row in range(PLAYFIELD_HEIGHT):
            for col in range(PLAYFIELD_WIDTH):
                tile = playfield[row, col]
                color = tile_to_color(tile)

                if color >= 0:
                    obs[1 + color, row, col] = 1.0

        # Channel 4: Current capsule position
        capsule_x = state.get('capsule_x', -1)
        capsule_y = state.get('capsule_y', -1)

        if 0 <= capsule_x < 8 and 0 <= capsule_y < 16:
            obs[4, capsule_y, capsule_x] = 1.0

            # If horizontal capsule, mark both halves
            # (Simplified: assume horizontal, mark right tile too)
            if capsule_x + 1 < 8:
                obs[4, capsule_y, capsule_x + 1] = 0.5

        # Channel 5: Next capsule preview (broadcast as global feature)
        next_left = state.get('next_left_color', -1)
        next_right = state.get('next_right_color', -1)

        if next_left >= 0:
            # Broadcast next capsule info across field
            obs[5, :, :] = next_left / 3.0  # Normalize 0-2 → 0.0-0.67

        # === CHANNELS 6-11: P1 (Opponent's View) ===
        # (Only if 2-player mode and p1_playfield is provided)

        if 'p1_playfield' in state:
            p1_playfield = np.array(state['p1_playfield'], dtype=np.uint8).reshape(16, 8)

            # Channel 6: P1 empty tiles
            obs[6] = (p1_playfield == TILE_EMPTY).astype(np.float32)

            # Channels 7-9: P1 color channels
            for row in range(PLAYFIELD_HEIGHT):
                for col in range(PLAYFIELD_WIDTH):
                    tile = p1_playfield[row, col]
                    color = tile_to_color(tile)

                    if color >= 0:
                        obs[7 + color, row, col] = 1.0

            # Channel 10: P1 capsule position
            p1_x = state.get('p1_capsule_x', -1)
            p1_y = state.get('p1_capsule_y', -1)

            if 0 <= p1_x < 8 and 0 <= p1_y < 16:
                obs[10, p1_y, p1_x] = 1.0
                if p1_x + 1 < 8:
                    obs[10, p1_y, p1_x + 1] = 0.5

            # Channel 11: P1 next capsule (broadcast)
            p1_next = state.get('p1_next_left_color', -1)
            if p1_next >= 0:
                obs[11, :, :] = p1_next / 3.0

        return obs

    def get_observation_space(self):
        """Get Gymnasium observation space"""
        import gymnasium as gym
        return gym.spaces.Box(
            low=0.0,
            high=1.0,
            shape=self.obs_shape,
            dtype=np.float32
        )


def encode_state(state: Dict[str, Any], player_id: int = 2) -> np.ndarray:
    """
    Legacy function for compatibility

    Args:
        state: Game state dictionary
        player_id: Which player (1 or 2)

    Returns:
        Encoded observation array
    """
    encoder = StateEncoder(player_id=player_id)
    return encoder.encode(state)


if __name__ == "__main__":
    # Test state encoder
    print("Testing state encoder...")

    # Create test state
    test_state = {
        'playfield': [TILE_EMPTY] * 128,
        'capsule_x': 3,
        'capsule_y': 5,
        'left_color': COLOR_YELLOW,
        'right_color': COLOR_RED,
        'next_left_color': COLOR_BLUE,
        'next_right_color': COLOR_YELLOW,
    }

    # Add some viruses
    playfield = list(test_state['playfield'])
    # Bottom row with viruses
    for i in range(8):
        playfield[15 * 8 + i] = TILE_VIRUS_RED
    # Middle viruses
    playfield[10 * 8 + 3] = TILE_VIRUS_YELLOW
    playfield[10 * 8 + 4] = TILE_VIRUS_BLUE
    test_state['playfield'] = playfield

    # Encode
    encoder = StateEncoder(player_id=2)
    obs = encoder.encode(test_state)

    print(f"Observation shape: {obs.shape}")
    print(f"Observation dtype: {obs.dtype}")
    print(f"Min value: {obs.min()}")
    print(f"Max value: {obs.max()}")

    # Check channels
    print(f"\nChannel 0 (empty): {np.sum(obs[0])} empty tiles")
    print(f"Channel 1 (yellow): {np.sum(obs[1])} yellow tiles")
    print(f"Channel 2 (red): {np.sum(obs[2])} red tiles")
    print(f"Channel 3 (blue): {np.sum(obs[3])} blue tiles")
    print(f"Channel 4 (capsule): {np.sum(obs[4]):.2f} capsule markers")
    print(f"Channel 5 (next): {np.sum(obs[5]):.2f} next capsule broadcast")

    print("\nState encoder ready!")
