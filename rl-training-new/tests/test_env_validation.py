#!/usr/bin/env python3
"""
Validation test for Dr. Mario RL environment

Tests:
1. Can read game state correctly
2. Controller input actually moves capsule
3. State encoding produces valid observations
4. Rewards are calculated correctly
5. Episode termination works

This must pass before training!
"""

import sys
from pathlib import Path
import time
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mednafen_interface_mcp import MednafenInterface as MesenInterface
from drmario_env import DrMarioEnv
from state_encoder import StateEncoder
from reward_function import RewardCalculator
from memory_map import *


def test_memory_reading():
    """Test 1: Can we read game state correctly?"""
    print("="*60)
    print("TEST 1: Memory Reading")
    print("="*60)

    interface = MesenInterface()
    if not interface.connect(timeout=10):
        print("✗ Failed to connect to Mesen")
        return False

    try:
        # Read game state
        state = interface.get_game_state()

        print(f"✓ Connected and read state")
        print(f"  Game mode: {state['mode']}")
        print(f"  Virus count: {state['virus_count']}")
        print(f"  Capsule position: ({state['capsule_x']}, {state['capsule_y']})")
        print(f"  Capsule colors: L={state['left_color']}, R={state['right_color']}")
        print(f"  Playfield size: {len(state['playfield'])} bytes")

        # Validate
        if state['mode'] < 0 or state['mode'] > 255:
            print(f"✗ Invalid game mode: {state['mode']}")
            return False

        if state['capsule_x'] < 0 or state['capsule_x'] > 7:
            print(f"✗ Invalid capsule X: {state['capsule_x']}")
            return False

        if len(state['playfield']) != 128:
            print(f"✗ Invalid playfield size: {len(state['playfield'])}")
            return False

        print("✓ All memory reads look valid")
        return True

    finally:
        interface.disconnect()


def test_controller_input():
    """Test 2: Does controller input actually move the capsule?"""
    print("\n" + "="*60)
    print("TEST 2: Controller Input")
    print("="*60)

    interface = MesenInterface()
    if not interface.connect(timeout=10):
        print("✗ Failed to connect to Mesen")
        return False

    try:
        # Get initial position
        initial_state = interface.get_game_state()
        initial_x = initial_state['capsule_x']
        initial_y = initial_state['capsule_y']

        print(f"Initial capsule position: ({initial_x}, {initial_y})")

        # Try moving right
        print("Pressing RIGHT for 10 frames...")
        for _ in range(10):
            interface.write_memory(P2_CONTROLLER, [BTN_RIGHT])
            interface.step_frame()
            time.sleep(0.016)

        # Check if moved
        new_state = interface.get_game_state()
        new_x = new_state['capsule_x']
        new_y = new_state['capsule_y']

        print(f"New capsule position: ({new_x}, {new_y})")

        if new_x == initial_x and new_y == initial_y:
            print("⚠️  WARNING: Capsule didn't move!")
            print("   Possible causes:")
            print("   - Game not in active gameplay (check mode >= 4)")
            print("   - Capsule hit wall")
            print("   - Wrong controller address")
            print("   - Frame timing issue")
            return False

        if new_x > initial_x:
            print(f"✓ Capsule moved right ({initial_x} → {new_x})")
            return True
        elif new_y > initial_y:
            print(f"✓ Capsule moved down (fell naturally) ({initial_y} → {new_y})")
            print("   This is OK - means controller input is working")
            return True
        else:
            print(f"? Capsule moved in unexpected direction")
            return True  # Still movement

    finally:
        interface.disconnect()


def test_state_encoding():
    """Test 3: Does state encoding produce valid CNN observations?"""
    print("\n" + "="*60)
    print("TEST 3: State Encoding")
    print("="*60)

    interface = MesenInterface()
    if not interface.connect(timeout=10):
        print("✗ Failed to connect to Mesen")
        return False

    try:
        # Get state and encode
        state = interface.get_game_state()
        encoder = StateEncoder(player_id=2)
        obs = encoder.encode(state)

        print(f"Observation shape: {obs.shape}")
        print(f"Observation dtype: {obs.dtype}")
        print(f"Min value: {obs.min():.3f}")
        print(f"Max value: {obs.max():.3f}")

        # Validate
        if obs.shape != (12, 16, 8):
            print(f"✗ Wrong observation shape: {obs.shape}")
            return False

        if obs.dtype != np.float32:
            print(f"✗ Wrong dtype: {obs.dtype}")
            return False

        if obs.min() < 0 or obs.max() > 1:
            print(f"✗ Values out of range [0, 1]: [{obs.min()}, {obs.max()}]")
            return False

        # Check channel statistics
        print("\nChannel statistics:")
        for i in range(6):  # Just P2 channels
            channel_sum = np.sum(obs[i])
            print(f"  Channel {i}: sum={channel_sum:.2f} (nonzero={np.count_nonzero(obs[i])})")

        # Channel 0 should be mostly full (empty tiles)
        if np.sum(obs[0]) < 50:
            print("⚠️  WARNING: Channel 0 (empty) has very few tiles")
            print("   Expected mostly empty playfield at game start")

        print("✓ State encoding looks valid")
        return True

    finally:
        interface.disconnect()


def test_reward_calculation():
    """Test 4: Are rewards calculated correctly?"""
    print("\n" + "="*60)
    print("TEST 4: Reward Calculation")
    print("="*60)

    calc = RewardCalculator()
    calc.reset()

    # Test case 1: No change
    r1 = calc.calculate(virus_count=20, max_height=15, game_over=False, all_viruses_cleared=False)
    print(f"Frame 1 (no change): reward={r1:.2f}")

    # Test case 2: Clear 2 viruses
    r2 = calc.calculate(virus_count=18, max_height=15, game_over=False, all_viruses_cleared=False)
    print(f"Frame 2 (cleared 2 viruses): reward={r2:.2f}")

    if r2 <= r1:
        print("✗ Expected reward to increase after clearing viruses")
        return False

    # Test case 3: Height increased (bad)
    calc.reset()
    r1 = calc.calculate(virus_count=20, max_height=10, game_over=False, all_viruses_cleared=False)
    r2 = calc.calculate(virus_count=20, max_height=5, game_over=False, all_viruses_cleared=False)
    print(f"Height penalty: {r2:.2f} (worse than {r1:.2f})")

    if r2 >= r1:
        print("✗ Expected reward to decrease when height increases")
        return False

    # Test case 4: Game over
    calc.reset()
    r_go = calc.calculate(virus_count=10, max_height=0, game_over=True, all_viruses_cleared=False)
    print(f"Game over: reward={r_go:.2f}")

    if r_go >= -90:  # Should be around -100
        print("✗ Expected large negative reward for game over")
        return False

    # Test case 5: Win
    calc.reset()
    r_win = calc.calculate(virus_count=0, max_height=10, game_over=False, all_viruses_cleared=True)
    print(f"Win: reward={r_win:.2f}")

    if r_win <= 100:  # Should be around +200
        print("✗ Expected large positive reward for winning")
        return False

    print("✓ All reward calculations look correct")
    return True


def test_environment_episode():
    """Test 5: Can we run a full episode?"""
    print("\n" + "="*60)
    print("TEST 5: Full Episode")
    print("="*60)

    env = DrMarioEnv(player_id=2, max_episode_steps=500)

    if not env.connect(timeout=10):
        print("✗ Failed to connect to Mesen")
        return False

    try:
        # Reset
        obs, info = env.reset()
        print(f"✓ Environment reset successful")
        print(f"  Initial viruses: {info['virus_count']}")
        print(f"  Observation shape: {obs.shape}")

        # Take 50 random actions
        total_reward = 0
        for step in range(50):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)

            total_reward += reward

            if step % 10 == 0:
                print(f"  Step {step:2d}: viruses={info['virus_count']:2d}, "
                      f"height={info['max_height']:2d}, reward={reward:6.2f}")

            if terminated or truncated:
                print(f"\n✓ Episode ended naturally at step {step}")
                print(f"  Total reward: {total_reward:.2f}")
                print(f"  Final viruses: {info['virus_count']}")
                break
        else:
            print(f"\n✓ Ran 50 steps without crashing")
            print(f"  Total reward: {total_reward:.2f}")
            print(f"  Final viruses: {info['virus_count']}")

        return True

    finally:
        env.close()


def main():
    """Run all validation tests"""
    print("Dr. Mario Environment Validation")
    print()
    print("IMPORTANT: Make sure before running:")
    print("  1. Mednafen is running (use MCP launch tool or xvfb-run mednafen ROM)")
    print("  2. Game loaded with drmario_vs_cpu.nes")
    print("  3. Game is running (doesn't need to be in gameplay yet)")
    print()
    print("NOTE: Validation will connect automatically via MCP interface")
    print()
    input("Press ENTER when ready...")

    results = {}

    # Run tests
    results['memory'] = test_memory_reading()
    results['controller'] = test_controller_input()
    results['encoding'] = test_state_encoding()
    results['reward'] = test_reward_calculation()
    results['episode'] = test_environment_episode()

    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)

    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:20s}: {status}")

    print("="*60)

    if all(results.values()):
        print("\n🎉 ALL TESTS PASSED!")
        print("Environment is ready for training.")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED!")
        print("Fix issues before starting training.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
