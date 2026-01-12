"""
Dr. Mario Reward Function

Designed based on Python AI (oracle) insights from Phase 1.

Reward Components:
1. Virus clearing: +10 per virus cleared (main goal)
2. Height reduction: +5 for lowering max column height
3. Height penalty: -0.1 per frame (encourage speed)
4. Game over penalty: -100 (avoid topping out)
5. Win bonus: +200 (all viruses cleared)

Philosophy:
- Reward immediate virus clears (sparse but high value)
- Encourage downstacking (height management)
- Penalize time (encourage efficiency)
- Heavy penalty for game over (survival is critical)
"""

from typing import Dict, Any


class RewardCalculator:
    """Calculate reward for Dr. Mario RL training"""

    def __init__(self):
        # Reward weights
        self.VIRUS_CLEAR_REWARD = 10.0
        self.HEIGHT_REDUCTION_REWARD = 5.0
        self.TIME_PENALTY = -0.1
        self.GAME_OVER_PENALTY = -100.0
        self.WIN_BONUS = 200.0
        self.HEIGHT_PENALTY_PER_ROW = -0.5

        # State tracking
        self.prev_virus_count = None
        self.prev_max_height = None
        self.episode_reward = 0.0

    def reset(self):
        """Reset state tracking for new episode"""
        self.prev_virus_count = None
        self.prev_max_height = None
        self.episode_reward = 0.0

    def calculate(
        self,
        virus_count: int,
        max_height: int,  # Lowest occupied row (0 = top)
        game_over: bool,
        all_viruses_cleared: bool,
    ) -> float:
        """
        Calculate reward for current step

        Args:
            virus_count: Current virus count
            max_height: Tallest column (lowest row number, 0=top)
            game_over: True if game ended (topped out)
            all_viruses_cleared: True if won (all viruses cleared)

        Returns:
            Reward value
        """
        reward = 0.0

        # Initialize tracking on first call
        if self.prev_virus_count is None:
            self.prev_virus_count = virus_count
            self.prev_max_height = max_height

        # 1. Virus clearing reward (main objective)
        viruses_cleared = self.prev_virus_count - virus_count
        if viruses_cleared > 0:
            reward += self.VIRUS_CLEAR_REWARD * viruses_cleared
            print(f"  [REWARD] Cleared {viruses_cleared} viruses: +{self.VIRUS_CLEAR_REWARD * viruses_cleared}")

        # 2. Height management reward
        height_reduced = self.prev_max_height - max_height
        if height_reduced > 0:
            reward += self.HEIGHT_REDUCTION_REWARD * height_reduced
            # print(f"  [REWARD] Height reduced: +{self.HEIGHT_REDUCTION_REWARD * height_reduced}")

        # 3. Height penalty (encourage low stacks)
        # Penalize based on how high the stack is
        if max_height < 16:  # Only if column has tiles
            rows_from_top = max_height
            height_penalty = self.HEIGHT_PENALTY_PER_ROW * rows_from_top
            reward += height_penalty
            # print(f"  [REWARD] Height penalty (row {max_height}): {height_penalty:.2f}")

        # 4. Time penalty (encourage speed)
        reward += self.TIME_PENALTY

        # 5. Game over penalty
        if game_over:
            reward += self.GAME_OVER_PENALTY
            print(f"  [REWARD] Game over: {self.GAME_OVER_PENALTY}")

        # 6. Win bonus
        if all_viruses_cleared:
            reward += self.WIN_BONUS
            print(f"  [REWARD] All viruses cleared! Bonus: +{self.WIN_BONUS}")

        # Update tracking
        self.prev_virus_count = virus_count
        self.prev_max_height = max_height
        self.episode_reward += reward

        return reward

    def get_episode_reward(self) -> float:
        """Get cumulative episode reward"""
        return self.episode_reward


def calculate_reward(
    prev_state: Dict[str, Any],
    current_state: Dict[str, Any],
    done: bool,
    info: Dict[str, Any]
) -> float:
    """
    Legacy interface for compatibility

    Args:
        prev_state: Previous game state
        current_state: Current game state
        done: Episode ended
        info: Additional info

    Returns:
        Reward value
    """
    # Extract relevant features
    prev_virus_count = prev_state.get('virus_count', 0)
    curr_virus_count = current_state.get('virus_count', 0)

    prev_max_height = prev_state.get('max_height', 16)
    curr_max_height = current_state.get('max_height', 16)

    game_over = info.get('game_over', False)
    all_cleared = curr_virus_count == 0

    # Calculate reward components
    reward = 0.0

    # Virus clearing
    viruses_cleared = prev_virus_count - curr_virus_count
    if viruses_cleared > 0:
        reward += 10.0 * viruses_cleared

    # Height reduction
    height_reduced = prev_max_height - curr_max_height
    if height_reduced > 0:
        reward += 5.0 * height_reduced

    # Height penalty
    if curr_max_height < 16:
        reward -= 0.5 * curr_max_height

    # Time penalty
    reward -= 0.1

    # Game over
    if game_over:
        reward -= 100.0

    # Win
    if all_cleared:
        reward += 200.0

    return reward


if __name__ == "__main__":
    # Test reward function
    print("Testing reward function...")

    calc = RewardCalculator()
    calc.reset()

    # Scenario 1: Clear 2 viruses
    print("\nScenario 1: Clear 2 viruses")
    r1 = calc.calculate(virus_count=18, max_height=14, game_over=False, all_viruses_cleared=False)
    r2 = calc.calculate(virus_count=16, max_height=14, game_over=False, all_viruses_cleared=False)
    print(f"Reward: {r2:.2f}")

    # Scenario 2: Reduce height
    print("\nScenario 2: Reduce max height by 2")
    calc.reset()
    r1 = calc.calculate(virus_count=10, max_height=10, game_over=False, all_viruses_cleared=False)
    r2 = calc.calculate(virus_count=10, max_height=8, game_over=False, all_viruses_cleared=False)
    print(f"Reward: {r2:.2f}")

    # Scenario 3: Game over
    print("\nScenario 3: Game over")
    calc.reset()
    r = calc.calculate(virus_count=5, max_height=0, game_over=True, all_viruses_cleared=False)
    print(f"Reward: {r:.2f}")

    # Scenario 4: Win
    print("\nScenario 4: Clear last virus and win")
    calc.reset()
    r1 = calc.calculate(virus_count=1, max_height=12, game_over=False, all_viruses_cleared=False)
    r2 = calc.calculate(virus_count=0, max_height=12, game_over=False, all_viruses_cleared=True)
    print(f"Reward: {r2:.2f}")

    print("\nReward function ready!")
