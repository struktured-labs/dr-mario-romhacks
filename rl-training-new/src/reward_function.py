"""
Dr. Mario Reward Function

Dense reward shaping for RL training.

Reward Components:
1. **Color matches (DENSE):**
   - 2 consecutive same-color: +0.5 (setup potential)
   - 3 consecutive same-color: +2.0 (one away from clear)
   - 4+ consecutive same-color: +10.0 (actual clear)
   - Virus bonus: +3.0 extra if match contains virus

2. Virus clearing: +20 per virus cleared (main goal)
3. Height penalty: -0.5 per row from top
4. Game over penalty: -100 (avoid topping out)
5. Win bonus: +200 (all viruses cleared)

Philosophy:
- DENSE rewards from color matching (every step can earn reward)
- Favor virus-containing matches over pill-only matches
- Encourage downstacking via height penalty
- Heavy penalty for game over
"""

import numpy as np
from typing import List, Tuple
from memory_map import (
    get_tile_color, is_virus, is_empty,
    PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT
)


class RewardCalculator:
    """Calculate dense rewards for Dr. Mario RL training"""

    def __init__(self, match_reward_scale: float = 1.0):
        """
        Args:
            match_reward_scale: Damping factor for match rewards (0.0-1.0)
                                Start at 1.0, decay to 0.1 as agent improves
        """
        # Match rewards (DENSE - awarded every step)
        # Base values (scaled by match_reward_scale)
        self.MATCH_2_BASE = 0.5      # 2 in a row
        self.MATCH_3_BASE = 2.0      # 3 in a row (one away!)
        self.MATCH_4_BASE = 10.0     # 4+ in a row (actual clear)
        self.VIRUS_MATCH_BONUS_BASE = 3.0   # Extra if match contains virus

        # Sparse rewards (NEVER dampened - these are the real objectives)
        self.VIRUS_CLEAR_REWARD = 20.0
        self.HEIGHT_PENALTY_PER_ROW = -0.5
        self.GAME_OVER_PENALTY = -100.0
        self.WIN_BONUS = 200.0

        # Curriculum learning: dampen match rewards as agent improves
        self.match_reward_scale = match_reward_scale

        # State tracking
        self.prev_virus_count = None
        self.prev_max_height = None
        self.episode_reward = 0.0
        self.total_viruses_cleared = 0  # Lifetime tracking for curriculum

    def reset(self):
        """Reset state tracking for new episode"""
        self.prev_virus_count = None
        self.prev_max_height = None
        self.episode_reward = 0.0

    def _find_consecutive_matches(
        self,
        playfield: np.ndarray
    ) -> List[Tuple[int, bool]]:
        """
        Find all consecutive same-color sequences in playfield.

        Args:
            playfield: 16x8 numpy array of tile values

        Returns:
            List of (length, has_virus) tuples for each match found
        """
        matches = []

        # Horizontal matches (row-wise)
        for row in range(PLAYFIELD_HEIGHT):
            col = 0
            while col < PLAYFIELD_WIDTH:
                tile = playfield[row, col]
                color = get_tile_color(tile)

                if color == -1:  # Empty or unknown
                    col += 1
                    continue

                # Count consecutive same color
                length = 1
                has_virus = is_virus(tile)

                for next_col in range(col + 1, PLAYFIELD_WIDTH):
                    next_tile = playfield[row, next_col]
                    next_color = get_tile_color(next_tile)

                    if next_color != color:
                        break

                    length += 1
                    if is_virus(next_tile):
                        has_virus = True

                # Record match if 2+
                if length >= 2:
                    matches.append((length, has_virus))

                col += length

        # Vertical matches (column-wise)
        for col in range(PLAYFIELD_WIDTH):
            row = 0
            while row < PLAYFIELD_HEIGHT:
                tile = playfield[row, col]
                color = get_tile_color(tile)

                if color == -1:  # Empty or unknown
                    row += 1
                    continue

                # Count consecutive same color
                length = 1
                has_virus = is_virus(tile)

                for next_row in range(row + 1, PLAYFIELD_HEIGHT):
                    next_tile = playfield[next_row, col]
                    next_color = get_tile_color(next_tile)

                    if next_color != color:
                        break

                    length += 1
                    if is_virus(next_tile):
                        has_virus = True

                # Record match if 2+
                if length >= 2:
                    matches.append((length, has_virus))

                row += length

        return matches

    def _calculate_match_rewards(self, playfield: np.ndarray) -> float:
        """
        Calculate dense rewards from color matching.

        Args:
            playfield: 16x8 numpy array of tile values

        Returns:
            Total match reward for this state
        """
        matches = self._find_consecutive_matches(playfield)
        total_reward = 0.0

        for length, has_virus in matches:
            # Base reward by length (scaled by curriculum factor)
            if length == 2:
                reward = self.MATCH_2_BASE * self.match_reward_scale
            elif length == 3:
                reward = self.MATCH_3_BASE * self.match_reward_scale
            elif length >= 4:
                reward = self.MATCH_4_BASE * self.match_reward_scale
            else:
                continue  # Shouldn't happen

            # Virus bonus (also scaled)
            if has_virus:
                reward += self.VIRUS_MATCH_BONUS_BASE * self.match_reward_scale

            total_reward += reward

        return total_reward

    def calculate(
        self,
        playfield: np.ndarray,
        virus_count: int,
        max_height: int,
        game_over: bool,
        all_viruses_cleared: bool,
    ) -> float:
        """
        Calculate reward for current step

        Args:
            playfield: 16x8 numpy array of tile values
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

        # 1. DENSE: Color matching rewards (every step)
        match_reward = self._calculate_match_rewards(playfield)
        reward += match_reward
        if match_reward > 0:
            print(f"  [REWARD] Color matches: +{match_reward:.2f}")

        # 2. Virus clearing reward (sparse, NEVER dampened)
        viruses_cleared = self.prev_virus_count - virus_count
        if viruses_cleared > 0:
            clear_reward = self.VIRUS_CLEAR_REWARD * viruses_cleared
            reward += clear_reward
            self.total_viruses_cleared += viruses_cleared
            print(f"  [REWARD] Cleared {viruses_cleared} viruses: +{clear_reward} (lifetime: {self.total_viruses_cleared})")

        # 3. Height penalty (encourage low stacks)
        if max_height < 16:
            rows_from_top = max_height
            height_penalty = self.HEIGHT_PENALTY_PER_ROW * rows_from_top
            reward += height_penalty

        # 4. Game over penalty
        if game_over:
            reward += self.GAME_OVER_PENALTY
            print(f"  [REWARD] Game over: {self.GAME_OVER_PENALTY}")

        # 5. Win bonus
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

    def update_curriculum(self, viruses_cleared_milestone: int):
        """
        Update match reward scaling based on agent progress.

        Curriculum schedule:
        - 0-100 viruses: scale = 1.0 (full match rewards)
        - 100-500 viruses: scale = 0.5 (half match rewards)
        - 500+ viruses: scale = 0.1 (minimal match rewards)

        Args:
            viruses_cleared_milestone: Total viruses cleared (e.g., from checkpoints)
        """
        old_scale = self.match_reward_scale

        if viruses_cleared_milestone < 100:
            self.match_reward_scale = 1.0
        elif viruses_cleared_milestone < 500:
            # Linear decay from 1.0 to 0.5
            progress = (viruses_cleared_milestone - 100) / 400
            self.match_reward_scale = 1.0 - (0.5 * progress)
        elif viruses_cleared_milestone < 1000:
            # Linear decay from 0.5 to 0.1
            progress = (viruses_cleared_milestone - 500) / 500
            self.match_reward_scale = 0.5 - (0.4 * progress)
        else:
            self.match_reward_scale = 0.1  # Minimum

        if abs(old_scale - self.match_reward_scale) > 0.01:
            print(f"\n[CURRICULUM] Match reward scale: {old_scale:.2f} → {self.match_reward_scale:.2f} (viruses cleared: {viruses_cleared_milestone})\n")

    def get_curriculum_info(self) -> dict:
        """Get curriculum learning state"""
        return {
            'match_reward_scale': self.match_reward_scale,
            'total_viruses_cleared': self.total_viruses_cleared,
        }


if __name__ == "__main__":
    # Test reward function
    print("Testing dense reward function...")
    import numpy as np

    calc = RewardCalculator()
    calc.reset()

    # Create test playfield with some matches
    playfield = np.full((16, 8), 0xFF, dtype=np.uint8)  # Empty

    # Add virus match (3 red viruses in a row)
    playfield[10, 0] = 0xD1  # Red virus
    playfield[10, 1] = 0xD1  # Red virus
    playfield[10, 2] = 0xD1  # Red virus

    # Add pill match (2 blue pills vertical)
    playfield[12, 5] = 0x68  # Blue pill
    playfield[13, 5] = 0x68  # Blue pill

    print("\nScenario 1: 3 virus match + 2 pill match")
    r = calc.calculate(
        playfield=playfield,
        virus_count=10,
        max_height=10,
        game_over=False,
        all_viruses_cleared=False
    )
    print(f"Total reward: {r:.2f}")
    print(f"Expected: ~{calc.MATCH_3_REWARD + calc.VIRUS_MATCH_BONUS + calc.MATCH_2_REWARD:.2f}")

    print("\nDense reward function ready!")
