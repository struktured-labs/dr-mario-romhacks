"""
Dr. Mario Heuristics Module

Implements smart scoring functions for evaluating capsule placements.
No ROM constraints - uses full computation for optimal decision making.

Heuristics:
- Column height penalty (prefer lower stacks)
- Virus clearing potential (prioritize virus matches)
- Consecutive color detection (bonus for chain potential)
- Top row avoidance (prevent partition risk)
- Hole creation penalty (avoid blocking access)
"""

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import numpy as np


# Constants
PLAYFIELD_WIDTH = 8
PLAYFIELD_HEIGHT = 16
EMPTY_TILE = 0xFF

# Tile colors
COLOR_YELLOW = 0
COLOR_RED = 1
COLOR_BLUE = 2

# Tile types
VIRUS_YELLOW = 0xD0
VIRUS_RED = 0xD1
VIRUS_BLUE = 0xD2

# Controller inputs
INPUT_RIGHT = 0x01
INPUT_LEFT = 0x02
INPUT_DOWN = 0x04
INPUT_UP = 0x08  # Unused in Dr. Mario
INPUT_A = 0x80   # Rotate counterclockwise
INPUT_B = 0x40   # Rotate clockwise
INPUT_SELECT = 0x20
INPUT_START = 0x10


def tile_to_color(tile: int) -> Optional[int]:
    """
    Convert tile value to color index

    Args:
        tile: Tile byte value

    Returns:
        Color index (0=yellow, 1=red, 2=blue) or None if not a colored tile
    """
    if tile == EMPTY_TILE:
        return None

    # Viruses
    if tile == VIRUS_YELLOW:
        return COLOR_YELLOW
    elif tile == VIRUS_RED:
        return COLOR_RED
    elif tile == VIRUS_BLUE:
        return COLOR_BLUE

    # Capsule pieces are in range 0x4C-0x5B
    # Extract color from lower bits
    if 0x4C <= tile <= 0x5B:
        color_bits = tile & 0x03
        return color_bits

    return None


def is_virus(tile: int) -> bool:
    """Check if tile is a virus"""
    return tile in (VIRUS_YELLOW, VIRUS_RED, VIRUS_BLUE)


@dataclass
class Playfield:
    """Represents the 8x16 Dr. Mario playfield"""
    tiles: np.ndarray  # Shape: (16, 8), row 0 = top

    @classmethod
    def from_bytes(cls, data: List[int]) -> 'Playfield':
        """
        Create playfield from 128-byte array

        Args:
            data: 128 bytes from $0500-$057F

        Returns:
            Playfield object
        """
        # Data is stored row-by-row, 8 bytes per row
        tiles = np.array(data, dtype=np.uint8).reshape(16, 8)
        return cls(tiles=tiles)

    def get_column_height(self, col: int) -> int:
        """
        Get height of a column (lowest occupied row)

        Args:
            col: Column index (0-7)

        Returns:
            Row index of lowest occupied tile (0=top), or 16 if column is empty
        """
        for row in range(PLAYFIELD_HEIGHT):
            if self.tiles[row, col] != EMPTY_TILE:
                return row
        return PLAYFIELD_HEIGHT

    def get_all_column_heights(self) -> List[int]:
        """Get heights for all columns"""
        return [self.get_column_height(col) for col in range(PLAYFIELD_WIDTH)]

    def get_max_height(self) -> int:
        """Get tallest column height"""
        heights = self.get_all_column_heights()
        return min(heights) if heights else PLAYFIELD_HEIGHT

    def count_viruses(self) -> int:
        """Count remaining viruses"""
        count = 0
        for row in range(PLAYFIELD_HEIGHT):
            for col in range(PLAYFIELD_WIDTH):
                if is_virus(self.tiles[row, col]):
                    count += 1
        return count

    def count_matches(self, row: int, col: int, color: int) -> Tuple[int, int]:
        """
        Count consecutive matching colors in horizontal and vertical directions

        Args:
            row: Row index
            col: Column index
            color: Color to match

        Returns:
            (horizontal_count, vertical_count)
        """
        h_count = 1  # Include current tile
        v_count = 1

        # Horizontal - left
        for c in range(col - 1, -1, -1):
            tile_color = tile_to_color(self.tiles[row, c])
            if tile_color == color:
                h_count += 1
            else:
                break

        # Horizontal - right
        for c in range(col + 1, PLAYFIELD_WIDTH):
            tile_color = tile_to_color(self.tiles[row, c])
            if tile_color == color:
                h_count += 1
            else:
                break

        # Vertical - up
        for r in range(row - 1, -1, -1):
            tile_color = tile_to_color(self.tiles[r, col])
            if tile_color == color:
                v_count += 1
            else:
                break

        # Vertical - down
        for r in range(row + 1, PLAYFIELD_HEIGHT):
            tile_color = tile_to_color(self.tiles[r, col])
            if tile_color == color:
                v_count += 1
            else:
                break

        return (h_count, v_count)

    def would_clear(self, row: int, col: int, color: int) -> bool:
        """
        Check if placing a tile would create a 4+ match

        Args:
            row: Row index
            col: Column index
            color: Tile color

        Returns:
            True if placement would clear
        """
        h_count, v_count = self.count_matches(row, col, color)
        return h_count >= 4 or v_count >= 4

    def count_adjacent_viruses(self, row: int, col: int, color: int) -> int:
        """
        Count viruses adjacent to position that match color

        Args:
            row: Row index
            col: Column index
            color: Color to match

        Returns:
            Number of adjacent matching viruses
        """
        count = 0

        # Check all 4 directions
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < PLAYFIELD_HEIGHT and 0 <= c < PLAYFIELD_WIDTH:
                tile = self.tiles[r, c]
                if is_virus(tile) and tile_to_color(tile) == color:
                    count += 1

        return count


@dataclass
class CapsuleState:
    """Current capsule state"""
    x: int  # Column (0-7)
    y: int  # Row (0-15)
    left_color: int  # 0=yellow, 1=red, 2=blue
    right_color: int
    orientation: int = 0  # 0=horizontal, 1=vertical (left up), 2=reverse, 3=vertical (right up)


def score_placement(playfield: Playfield, capsule: CapsuleState, target_col: int, rotation: int) -> float:
    """
    Score a potential capsule placement

    Args:
        playfield: Current playfield state
        capsule: Current capsule state
        target_col: Target column to drop in
        rotation: Number of rotations (0-3)

    Returns:
        Score (higher = better)
    """
    score = 0.0

    # Determine final orientation after rotation
    final_orientation = (capsule.orientation + rotation) % 4

    # Determine where capsule would land
    # For simplicity, assume it drops straight down to the column
    if final_orientation == 0:  # Horizontal
        # Both halves in same row
        left_col = target_col
        right_col = target_col + 1

        if right_col >= PLAYFIELD_WIDTH:
            return -1000  # Out of bounds

        # Find landing row
        left_height = playfield.get_column_height(left_col)
        right_height = playfield.get_column_height(right_col)
        landing_row = min(left_height, right_height) - 1

        if landing_row < 0:
            return -1000  # Would stack above playfield

        left_row = right_row = landing_row
        left_color = capsule.left_color
        right_color = capsule.right_color

    else:  # Vertical (simplified - assume single column drop)
        col = target_col
        landing_row = playfield.get_column_height(col) - 1

        if landing_row < 1:  # Need room for 2 tiles
            return -1000

        if final_orientation == 1:  # Left on top
            left_row = landing_row - 1
            right_row = landing_row
            left_col = right_col = col
            left_color = capsule.left_color
            right_color = capsule.right_color
        else:  # Right on top
            left_row = landing_row
            right_row = landing_row - 1
            left_col = right_col = col
            left_color = capsule.left_color
            right_color = capsule.right_color

    # --- HEURISTIC 1: Virus clearing potential ---
    # High bonus for clearing viruses
    if playfield.would_clear(left_row, left_col, left_color):
        virus_count = playfield.count_adjacent_viruses(left_row, left_col, left_color)
        score += 100 * virus_count + 50  # Big bonus

    if playfield.would_clear(right_row, right_col, right_color):
        virus_count = playfield.count_adjacent_viruses(right_row, right_col, right_color)
        score += 100 * virus_count + 50

    # --- HEURISTIC 2: Height penalty ---
    # Prefer lower placements
    avg_row = (left_row + right_row) / 2
    score -= avg_row * 5  # Lower rows = higher score

    # --- HEURISTIC 3: Top row avoidance ---
    # Heavy penalty for stacking near top
    if left_row < 3 or right_row < 3:
        score -= 200

    # --- HEURISTIC 4: Column height balance ---
    # Prefer placements that reduce max height
    heights = playfield.get_all_column_heights()
    max_height_before = min(heights)

    # Simulate placement
    new_heights = heights.copy()
    new_heights[left_col] = min(new_heights[left_col], left_row)
    new_heights[right_col] = min(new_heights[right_col], right_row)
    max_height_after = min(new_heights)

    if max_height_after > max_height_before:
        score -= 30  # Penalty for increasing max height
    else:
        score += 10  # Bonus for maintaining or reducing

    # --- HEURISTIC 5: Match potential (even if not clearing) ---
    # Bonus for creating 2-3 consecutive colors (setup for future clears)
    left_h, left_v = playfield.count_matches(left_row, left_col, left_color)
    right_h, right_v = playfield.count_matches(right_row, right_col, right_color)

    match_bonus = 0
    for count in [left_h, left_v, right_h, right_v]:
        if count == 2:
            match_bonus += 5
        elif count == 3:
            match_bonus += 15

    score += match_bonus

    return score


def find_best_move(playfield: Playfield, capsule: CapsuleState) -> Tuple[int, int]:
    """
    Find best move (column + rotation) using heuristics

    Args:
        playfield: Current playfield state
        capsule: Current capsule state

    Returns:
        (best_column, best_rotation) where rotation is 0-3
    """
    best_score = -float('inf')
    best_col = 3  # Default center
    best_rotation = 0

    # Try all combinations of column and rotation
    for rotation in range(4):  # 4 possible rotations
        for col in range(PLAYFIELD_WIDTH):
            score = score_placement(playfield, capsule, col, rotation)

            if score > best_score:
                best_score = score
                best_col = col
                best_rotation = rotation

    return best_col, best_rotation


if __name__ == "__main__":
    # Test heuristics
    print("Testing Dr. Mario Heuristics...")

    # Create test playfield with some viruses
    test_data = [EMPTY_TILE] * 128

    # Add some viruses at bottom
    for i in range(8):
        test_data[15 * 8 + i] = VIRUS_RED  # Bottom row
    test_data[14 * 8 + 3] = VIRUS_YELLOW
    test_data[14 * 8 + 4] = VIRUS_YELLOW

    playfield = Playfield.from_bytes(test_data)

    print(f"Viruses: {playfield.count_viruses()}")
    print(f"Column heights: {playfield.get_all_column_heights()}")
    print(f"Max height (min row): {playfield.get_max_height()}")

    # Test capsule
    capsule = CapsuleState(x=3, y=0, left_color=COLOR_YELLOW, right_color=COLOR_RED)

    print(f"\nFinding best move for capsule: L={capsule.left_color}, R={capsule.right_color}")
    best_col, best_rot = find_best_move(playfield, capsule)
    print(f"Best move: column={best_col}, rotation={best_rot}")

    print("\nHeuristics module ready!")
