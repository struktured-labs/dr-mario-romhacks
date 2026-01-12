#!/usr/bin/env python3
"""
Visualize what the RL agent sees

Shows the 12-channel observation as ASCII art so you can verify
the state encoding is working correctly.
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mesen_interface import MesenInterface
from state_encoder import StateEncoder
from memory_map import TILE_EMPTY


def visualize_playfield(playfield_bytes, title="Playfield"):
    """Visualize playfield as ASCII"""
    print(f"\n{title}:")
    print("  " + "".join([str(i) for i in range(8)]))
    print("  " + "="*8)

    playfield = np.array(playfield_bytes).reshape(16, 8)

    for row in range(16):
        row_str = f"{row:2d}|"
        for col in range(8):
            tile = playfield[row, col]
            if tile == TILE_EMPTY:
                row_str += "."
            elif 0xD0 <= tile <= 0xD2:  # Virus
                row_str += "V"
            else:  # Capsule/pill
                row_str += "o"
        print(row_str)


def visualize_channel(channel, channel_name):
    """Visualize a single observation channel"""
    print(f"\n{channel_name}:")
    print("  " + "".join([str(i) for i in range(8)]))
    print("  " + "="*8)

    for row in range(16):
        row_str = f"{row:2d}|"
        for col in range(8):
            val = channel[row, col]
            if val > 0.9:
                row_str += "#"
            elif val > 0.5:
                row_str += "+"
            elif val > 0.1:
                row_str += "."
            else:
                row_str += " "
        row_str += f" |{channel[row].max():.2f}"
        print(row_str)


def main():
    """Main visualization"""
    print("="*60)
    print("Observation Visualization")
    print("="*60)
    print()
    print("This shows what the RL agent actually sees.")
    print("Verify that:")
    print("  1. Playfield is correct (viruses shown as V)")
    print("  2. Empty channel matches empty tiles")
    print("  3. Color channels match actual colors")
    print("  4. Capsule position is marked")
    print()
    input("Press ENTER when Mesen is ready...")

    # Connect
    interface = MesenInterface()
    if not interface.connect(timeout=10):
        print("✗ Failed to connect to Mesen")
        return 1

    try:
        # Get state
        state = interface.get_game_state()

        print("\nRAW GAME STATE:")
        print(f"  Mode: {state['mode']}")
        print(f"  Viruses: {state['virus_count']}")
        print(f"  Capsule: ({state['capsule_x']}, {state['capsule_y']})")
        print(f"  Colors: L={state['left_color']}, R={state['right_color']}")

        # Show raw playfield
        visualize_playfield(state['playfield'], "Raw Playfield (P2)")

        # Encode observation
        encoder = StateEncoder(player_id=2)
        obs = encoder.encode(state)

        print("\n" + "="*60)
        print("ENCODED OBSERVATION (12 channels)")
        print("="*60)

        # Show each channel
        channel_names = [
            "Ch 0: Empty (P2)",
            "Ch 1: Yellow (P2)",
            "Ch 2: Red (P2)",
            "Ch 3: Blue (P2)",
            "Ch 4: Capsule (P2)",
            "Ch 5: Next Capsule (P2)",
            "Ch 6: Empty (P1)",
            "Ch 7: Yellow (P1)",
            "Ch 8: Red (P1)",
            "Ch 9: Blue (P1)",
            "Ch 10: Capsule (P1)",
            "Ch 11: Next Capsule (P1)",
        ]

        for i, name in enumerate(channel_names):
            if i == 6:
                if np.all(obs[i] == 0):
                    print("\n[P1 channels all zero - single player mode]")
                    break

            visualize_channel(obs[i], name)

            # Channel statistics
            nonzero = np.count_nonzero(obs[i])
            total = obs[i].sum()
            max_val = obs[i].max()
            print(f"  Stats: {nonzero} nonzero tiles, sum={total:.2f}, max={max_val:.2f}")

        print("\n" + "="*60)
        print("VERIFICATION CHECKLIST:")
        print("="*60)

        # Automated checks
        checks = []

        # Check 1: Empty channel should have ~100+ empty tiles
        empty_count = np.count_nonzero(obs[0])
        checks.append(("Empty channel has many tiles", empty_count > 50, f"{empty_count} tiles"))

        # Check 2: At least one color channel should have viruses
        color_counts = [np.count_nonzero(obs[i]) for i in [1, 2, 3]]
        has_colors = sum(color_counts) > 0
        checks.append(("Color channels have tiles", has_colors, f"{sum(color_counts)} colored tiles"))

        # Check 3: Capsule channel should mark current capsule
        capsule_count = np.count_nonzero(obs[4])
        checks.append(("Capsule position marked", capsule_count > 0, f"{capsule_count} markers"))

        # Check 4: Observation in valid range
        in_range = (obs.min() >= 0 and obs.max() <= 1)
        checks.append(("Values in range [0, 1]", in_range, f"[{obs.min():.3f}, {obs.max():.3f}]"))

        # Print checks
        for check_name, passed, detail in checks:
            status = "✓" if passed else "✗"
            print(f"{status} {check_name}: {detail}")

        if all(passed for _, passed, _ in checks):
            print("\n✓ All checks passed! Observation looks correct.")
            return 0
        else:
            print("\n⚠️  Some checks failed. Review output above.")
            return 1

    finally:
        interface.disconnect()


if __name__ == "__main__":
    sys.exit(main())
