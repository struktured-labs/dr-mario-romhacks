"""
State Encoder: Convert raw NES memory to neural network input

Implements multi-channel image-like representation for CNN policies.
"""

import numpy as np
from .memory_map import *


def encode_state(state: dict) -> np.ndarray:
    """
    Encode raw game state as 12-channel image for CNN

    Channels:
      0-3: Own playfield (empty, yellow, red, blue)
      4-5: Own current capsule (position, orientation)
      6-9: Opponent playfield (empty, yellow, red, blue)
      10-11: Opponent capsule

    Args:
        state: Dict with keys:
            - playfield: bytes (128 bytes)
            - capsule_x, capsule_y, rotation
            - capsule_left_color, capsule_right_color
            - opponent_playfield: bytes (128 bytes)
            - (opponent capsule data if available)

    Returns:
        np.ndarray of shape (12, 16, 8) with values in [0, 1]
    """
    channels = np.zeros((12, PLAYFIELD_HEIGHT, PLAYFIELD_WIDTH), dtype=np.float32)

    # Encode own playfield (channels 0-3)
    playfield_2d = playfield_to_2d(state['playfield'])
    for row in range(PLAYFIELD_HEIGHT):
        for col in range(PLAYFIELD_WIDTH):
            tile = playfield_2d[row][col]

            if is_empty(tile):
                channels[0, row, col] = 1.0
            elif is_virus(tile) or is_pill(tile) or is_pellet(tile):
                color = get_tile_color(tile)
                if color == COLOR_YELLOW:
                    channels[1, row, col] = 1.0
                elif color == COLOR_RED:
                    channels[2, row, col] = 1.0
                elif color == COLOR_BLUE:
                    channels[3, row, col] = 1.0

    # Encode own capsule (channels 4-5)
    capsule_x = state.get('capsule_x', 0)
    capsule_y = state.get('capsule_y', 0)
    rotation = state.get('rotation', 0)

    if capsule_y < PLAYFIELD_HEIGHT and capsule_x < PLAYFIELD_WIDTH:
        # Channel 4: capsule position (binary mask)
        channels[4, capsule_y, capsule_x] = 1.0

        # Channel 5: rotation encoding (normalized 0-3 → 0-1)
        channels[5, capsule_y, capsule_x] = rotation / 3.0

    # Encode opponent playfield (channels 6-9)
    if 'opponent_playfield' in state:
        opp_playfield_2d = playfield_to_2d(state['opponent_playfield'])
        for row in range(PLAYFIELD_HEIGHT):
            for col in range(PLAYFIELD_WIDTH):
                tile = opp_playfield_2d[row][col]

                if is_empty(tile):
                    channels[6, row, col] = 1.0
                elif is_virus(tile) or is_pill(tile) or is_pellet(tile):
                    color = get_tile_color(tile)
                    if color == COLOR_YELLOW:
                        channels[7, row, col] = 1.0
                    elif color == COLOR_RED:
                        channels[8, row, col] = 1.0
                    elif color == COLOR_BLUE:
                        channels[9, row, col] = 1.0

    # Encode opponent capsule (channels 10-11) - if available
    # TODO: Read opponent capsule position from memory
    # For now, leave as zeros

    return channels


def encode_state_flat(state: dict) -> np.ndarray:
    """
    Alternative encoding: flat vector for MLP

    Returns:
        np.ndarray of shape (1050,) with normalized values
    """
    features = []

    # Flatten playfield (128 * 4 one-hot encoding)
    playfield_2d = playfield_to_2d(state['playfield'])
    for row in range(PLAYFIELD_HEIGHT):
        for col in range(PLAYFIELD_WIDTH):
            tile = playfield_2d[row][col]
            # One-hot: [empty, yellow, red, blue]
            one_hot = [0.0, 0.0, 0.0, 0.0]
            if is_empty(tile):
                one_hot[0] = 1.0
            else:
                color = get_tile_color(tile)
                if color >= 0:
                    one_hot[color + 1] = 1.0
            features.extend(one_hot)

    # Add capsule features
    features.append(state.get('capsule_x', 0) / PLAYFIELD_WIDTH)
    features.append(state.get('capsule_y', 0) / PLAYFIELD_HEIGHT)
    features.append(state.get('rotation', 0) / 3.0)

    # Add virus count
    features.append(state.get('virus_count', 0) / 100.0)  # Normalize

    # Opponent playfield (if available)
    if 'opponent_playfield' in state:
        opp_playfield_2d = playfield_to_2d(state['opponent_playfield'])
        for row in range(PLAYFIELD_HEIGHT):
            for col in range(PLAYFIELD_WIDTH):
                tile = opp_playfield_2d[row][col]
                one_hot = [0.0, 0.0, 0.0, 0.0]
                if is_empty(tile):
                    one_hot[0] = 1.0
                else:
                    color = get_tile_color(tile)
                    if color >= 0:
                        one_hot[color + 1] = 1.0
                features.extend(one_hot)

        features.append(state.get('opponent_virus_count', 0) / 100.0)

    return np.array(features, dtype=np.float32)
