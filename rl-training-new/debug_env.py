#!/usr/bin/env python3
"""
Debug Dr. Mario Environment
Check if observations, actions, and state changes are working correctly.
"""

import sys
sys.path.insert(0, 'src')

import numpy as np
from drmario_env import DrMarioEnv

print("="*60)
print("Dr. Mario Environment Debug")
print("="*60)
print()

# Create environment
env = DrMarioEnv(
    mesen_host="localhost",
    mesen_port=8000,
    player_id=2,
    max_episode_steps=100,
    frame_skip=1,
    opponent_policy="random",
)

print("1. Connecting to Mednafen...")
if not env.connect(timeout=10):
    print("   ✗ Failed to connect!")
    sys.exit(1)
print("   ✓ Connected")
print()

print("2. Resetting environment...")
obs, info = env.reset()
print(f"   Observation shape: {obs.shape}")
print(f"   Observation dtype: {obs.dtype}")
print(f"   Observation range: [{obs.min():.3f}, {obs.max():.3f}]")
print(f"   Non-zero elements: {np.count_nonzero(obs)} / {obs.size}")
print(f"   Info: {info}")
print()

# Check if observation is meaningful
if obs.max() == 0:
    print("   ⚠️  WARNING: Observation is all zeros!")
elif np.count_nonzero(obs) < 10:
    print("   ⚠️  WARNING: Observation is mostly zeros!")
else:
    print("   ✓ Observation looks reasonable")
print()

print("3. Checking observation channels...")
for channel in range(obs.shape[2]):
    channel_data = obs[:, :, channel]
    nonzero = np.count_nonzero(channel_data)
    print(f"   Channel {channel}: {nonzero} non-zero pixels (range: [{channel_data.min():.2f}, {channel_data.max():.2f}])")
print()

print("4. Taking actions and checking state changes...")
prev_obs = obs.copy()

for step in range(10):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

    obs_changed = not np.array_equal(obs, prev_obs)

    print(f"   Step {step+1}:")
    print(f"      Action: {action} ({['NOOP', 'LEFT', 'RIGHT', 'DOWN', 'A', 'B', 'LEFT+DOWN', 'RIGHT+DOWN', 'LEFT+A'][action]})")
    print(f"      Reward: {reward:.2f}")
    print(f"      Observation changed: {obs_changed}")
    print(f"      Virus count: {info['virus_count']}")
    print(f"      Max height: {info['max_height']}")
    print(f"      Terminated: {terminated}")

    if terminated or truncated:
        print(f"      Episode ended at step {step+1}")
        break

    prev_obs = obs.copy()

print()
print("5. Summary:")
print(f"   Episode lasted: {step+1} steps")

if step < 2:
    print("   ❌ PROBLEM: Episode too short!")
    print("      Agent is dying immediately - game over condition triggered")
else:
    print("   ✓ Episode lasted multiple steps")

env.close()
print()
print("Debug complete!")
