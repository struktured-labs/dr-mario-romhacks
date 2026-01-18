"""
Dr. Mario NES Memory Map
Derived from VS_CPU_PLAN.md and Data Crystal wiki
"""

# =============================================================================
# Player 1 Memory Addresses
# =============================================================================

# Playfield (8 columns × 16 rows = 128 bytes)
P1_PLAYFIELD_START = 0x0400
P1_PLAYFIELD_END = 0x047F
P1_PLAYFIELD_SIZE = 128

# Current Falling Capsule
P1_CAPSULE_LEFT_COLOR = 0x0301   # 0=Yellow, 1=Red, 2=Blue
P1_CAPSULE_RIGHT_COLOR = 0x0302
P1_CAPSULE_X = 0x0305            # 0-7 (column)
P1_CAPSULE_Y = 0x0306            # 0-15 (row)
P1_CAPSULE_ROTATION = 0x00A5     # 0-3
P1_DROP_TIMER = 0x0312           # Frames until auto-drop

# Next Capsule Preview
P1_NEXT_LEFT_COLOR = 0x031A
P1_NEXT_RIGHT_COLOR = 0x031B

# Virus Count
P1_VIRUS_COUNT = 0x0324

# =============================================================================
# Player 2 Memory Addresses
# =============================================================================

# Playfield (NOTE: +$100 offset, not +$80!)
P2_PLAYFIELD_START = 0x0500
P2_PLAYFIELD_END = 0x057F
P2_PLAYFIELD_SIZE = 128

# Current Falling Capsule (mostly +$80 offset from P1)
P2_CAPSULE_LEFT_COLOR = 0x0381
P2_CAPSULE_RIGHT_COLOR = 0x0382
P2_CAPSULE_X = 0x0385
P2_CAPSULE_Y = 0x0386
P2_CAPSULE_ROTATION = 0x0125     # Inferred, needs verification
P2_DROP_TIMER = 0x0392           # Inferred

# Next Capsule Preview
P2_NEXT_LEFT_COLOR = 0x039A
P2_NEXT_RIGHT_COLOR = 0x039B

# Virus Count
P2_VIRUS_COUNT = 0x03A4

# =============================================================================
# Controller Input Addresses
# =============================================================================

P1_CONTROLLER = 0xF5  # Player 1 button state
P2_CONTROLLER = 0xF6  # Player 2 button state

# Dr. Mario uses NON-STANDARD button mapping!
# Bit mapping for $F5 and $F6:
BTN_RIGHT = 0x01
BTN_LEFT = 0x02
BTN_SELECT = 0x04
BTN_START = 0x08
BTN_DOWN = 0x10      # Needs verification (could be 0x20)
BTN_A_ROTATE_CW = 0x40   # Rotate clockwise
BTN_B_ROTATE_CCW = 0x80  # Rotate counter-clockwise

# =============================================================================
# Game State
# =============================================================================

FRAME_COUNTER = 0x0043
GAME_MODE = 0x0046
PLAYER_COUNT = 0x0727

# =============================================================================
# Tile/Cell Values
# =============================================================================

TILE_EMPTY = 0xFF

# Viruses
TILE_VIRUS_YELLOW = 0xD0
TILE_VIRUS_RED = 0xD1
TILE_VIRUS_BLUE = 0xD2

# Pill halves (64-114, various orientations and colors)
TILE_PILL_MIN = 0x40
TILE_PILL_MAX = 0x72

# Pellets (isolated pill pieces after matching)
TILE_PELLET_YELLOW = 0x80
TILE_PELLET_RED = 0x81
TILE_PELLET_BLUE = 0x82

# =============================================================================
# Playfield Dimensions
# =============================================================================

PLAYFIELD_WIDTH = 8
PLAYFIELD_HEIGHT = 16

# =============================================================================
# Color Encoding
# =============================================================================

COLOR_YELLOW = 0
COLOR_RED = 1
COLOR_BLUE = 2
NUM_COLORS = 3

# =============================================================================
# Helper Functions
# =============================================================================

def is_virus(tile_value: int) -> bool:
    """Check if tile is a virus"""
    return tile_value in (TILE_VIRUS_YELLOW, TILE_VIRUS_RED, TILE_VIRUS_BLUE)


def is_pill(tile_value: int) -> bool:
    """Check if tile is a pill piece"""
    return TILE_PILL_MIN <= tile_value <= TILE_PILL_MAX


def is_pellet(tile_value: int) -> bool:
    """Check if tile is a pellet"""
    return tile_value in (TILE_PELLET_YELLOW, TILE_PELLET_RED, TILE_PELLET_BLUE)


def is_empty(tile_value: int) -> bool:
    """Check if tile is empty"""
    return tile_value == TILE_EMPTY


def get_tile_color(tile_value: int) -> int:
    """
    Extract color from tile value (0=Yellow, 1=Red, 2=Blue)

    Returns -1 for empty tiles or unknown values.
    """
    if is_empty(tile_value):
        return -1
    elif is_virus(tile_value):
        return tile_value - TILE_VIRUS_YELLOW
    elif is_pellet(tile_value):
        return tile_value - TILE_PELLET_YELLOW
    elif is_pill(tile_value):
        # Pills encoded in ranges: 0x40-0x5B (yellow), 0x5C-0x67 (red), 0x68-0x72 (blue)
        # Approximation based on observed ranges
        if tile_value < 0x5C:
            return COLOR_YELLOW
        elif tile_value < 0x68:
            return COLOR_RED
        else:
            return COLOR_BLUE
    return -1


def playfield_to_2d(playfield_bytes: bytes) -> list:
    """
    Convert flat 128-byte playfield to 2D array [row][col]

    Args:
        playfield_bytes: 128 bytes from memory

    Returns:
        16x8 2D list (row-major order)
    """
    grid = []
    for row in range(PLAYFIELD_HEIGHT):
        row_data = []
        for col in range(PLAYFIELD_WIDTH):
            idx = row * PLAYFIELD_WIDTH + col
            row_data.append(playfield_bytes[idx])
        grid.append(row_data)
    return grid
