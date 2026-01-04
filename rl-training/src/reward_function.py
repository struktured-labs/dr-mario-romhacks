"""
Reward Function for Dr. Mario RL Training

Defines the reward signal that guides learning.
"""

from typing import Dict, Any


def calculate_reward(
    prev_state: Dict[str, Any],
    current_state: Dict[str, Any],
    player_id: int = 1
) -> float:
    """
    Calculate reward for a single step

    Reward components:
    1. Virus elimination (primary goal)
    2. Survival bonus
    3. Height penalty (keep playfield low)
    4. Piece placement efficiency

    Args:
        prev_state: Previous game state
        current_state: Current game state
        player_id: Which player (1 or 2)

    Returns:
        Scalar reward value
    """
    if prev_state is None:
        return 0.0

    reward = 0.0

    # 1. Virus elimination reward (main objective)
    prev_viruses = prev_state.get('virus_count', 0)
    curr_viruses = current_state.get('virus_count', 0)
    viruses_eliminated = prev_viruses - curr_viruses

    if viruses_eliminated > 0:
        reward += viruses_eliminated * 100.0

    # 2. Small survival bonus (encourages staying alive)
    reward += 0.1

    # 3. Height penalty (punish stacking too high)
    avg_height = calculate_average_column_height(current_state['playfield'])
    reward -= avg_height * 0.5

    # 4. Opponent comparison (relative performance)
    opponent_viruses = current_state.get('opponent_virus_count', 100)
    virus_differential = opponent_viruses - curr_viruses
    reward += virus_differential * 0.1  # Bonus for being ahead

    # 5. Terminal rewards
    if is_game_over(current_state):
        if curr_viruses == 0:
            # Win: cleared all viruses
            reward += 1000.0
        else:
            # Loss: topped out
            reward -= 500.0

    return reward


def calculate_average_column_height(playfield: bytes) -> float:
    """
    Calculate average height of filled cells per column

    Args:
        playfield: 128-byte playfield data

    Returns:
        Average height (0-16)
    """
    from .memory_map import PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT, is_empty, playfield_to_2d

    grid = playfield_to_2d(playfield)
    heights = []

    for col in range(PLAYFIELD_WIDTH):
        height = 0
        for row in range(PLAYFIELD_HEIGHT):
            if not is_empty(grid[row][col]):
                height = PLAYFIELD_HEIGHT - row
                break
        heights.append(height)

    return sum(heights) / len(heights) if heights else 0.0


def is_game_over(state: Dict[str, Any]) -> bool:
    """
    Check if game has ended

    Game ends when:
    - All viruses cleared (win)
    - Playfield topped out (loss)
    """
    # Check if all viruses cleared
    if state.get('virus_count', 0) == 0:
        return True

    # Check if opponent won
    if state.get('opponent_virus_count', 100) == 0:
        return True

    # TODO: Detect top-out condition from memory
    # May need to check playfield top row or game state flag

    return False


def calculate_shaped_reward(
    prev_state: Dict[str, Any],
    current_state: Dict[str, Any],
    player_id: int = 1,
    curriculum_level: int = 0
) -> float:
    """
    Advanced reward function with curriculum learning

    As training progresses, shifts reward emphasis:
    - Early: reward any virus elimination
    - Mid: reward efficient clearing (combos)
    - Late: penalize mistakes more heavily

    Args:
        prev_state: Previous state
        current_state: Current state
        player_id: Player ID
        curriculum_level: Training stage (0-10)

    Returns:
        Shaped reward value
    """
    base_reward = calculate_reward(prev_state, current_state, player_id)

    # Curriculum adjustments
    if curriculum_level < 3:
        # Early training: encourage exploration
        base_reward += 0.5  # Extra survival bonus
    elif curriculum_level < 7:
        # Mid training: reward efficiency
        # TODO: Add combo detection and bonus
        pass
    else:
        # Late training: harsh penalties
        avg_height = calculate_average_column_height(current_state['playfield'])
        if avg_height > 12:  # Danger zone
            base_reward -= 10.0

    return base_reward
