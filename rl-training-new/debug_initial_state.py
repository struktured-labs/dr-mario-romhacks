#!/usr/bin/env python3
"""
Debug: Check initial game state after reset
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from drmario_env import DrMarioEnv
import numpy as np

print("=" * 60)
print("Debugging Initial Game State")
print("=" * 60)

# Create environment
env = DrMarioEnv(player_id=2, max_episode_steps=1000)

# Connect
print("\nConnecting to MCP server...")
if not env.connect(timeout=10):
    print("Failed to connect!")
    sys.exit(1)

print("Connected!")

# Reset and check initial state
print("\nResetting environment...")
obs, info = env.reset()

print(f"\nInitial state info:")
print(f"  Virus count: {info['virus_count']}")
print(f"  Episode: {info['episode']}")

# Get playfield state
state = env.mesen.get_game_state()
playfield = np.array(state['playfield'], dtype=np.uint8).reshape(16, 8)

print(f"\nPlayfield shape: {playfield.shape}")
print(f"  Empty tiles (0xFF): {np.sum(playfield == 0xFF)}")
print(f"  Non-empty tiles: {np.sum(playfield != 0xFF)}")

# Check each row for occupancy
print(f"\nRow occupancy (top to bottom):")
for row in range(16):
    occupied = np.sum(playfield[row, :] != 0xFF)
    print(f"  Row {row:2d}: {occupied} occupied tiles")
    if row == 0 and occupied > 0:
        print(f"    ⚠️  TOP ROW OCCUPIED! This triggers instant game over")
        print(f"    Tiles: {playfield[row, :]}")

# Calculate max height
max_height = 16
for row in range(16):
    if np.any(playfield[row, :] != 0xFF):
        max_height = row
        break

print(f"\nMax height (lowest occupied row): {max_height}")
if max_height == 0:
    print("  ⚠️  GAME OVER CONDITION MET ON RESET!")

# Take one step and check again
print("\n" + "=" * 60)
print("Taking one action (NOOP)...")
obs, reward, terminated, truncated, info = env.step(0)

print(f"\nAfter 1 step:")
print(f"  Reward: {reward:.2f}")
print(f"  Terminated: {terminated}")
print(f"  Truncated: {truncated}")
print(f"  Virus count: {info['virus_count']}")
print(f"  Max height: {info['max_height']}")

if terminated:
    print("\n⚠️  EPISODE TERMINATED AFTER 1 STEP!")
    print("This explains why training shows instant game overs.")

env.close()
