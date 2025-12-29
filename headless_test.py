#!/usr/bin/env python3
"""
Headless Dr. Mario CPU vs CPU using nes-py
No GUI - runs in terminal
"""

from nes_py import NESEnv
import numpy as np
import os

# Button constants for NES
BUTTON_A = 0
BUTTON_B = 1
BUTTON_SELECT = 2
BUTTON_START = 3
BUTTON_UP = 4
BUTTON_DOWN = 5
BUTTON_LEFT = 6
BUTTON_RIGHT = 7

ROM_PATH = "drmario.nes"

def main():
    print("Starting headless Dr. Mario...")

    # Create environment
    env = NESEnv(ROM_PATH)
    env.reset()

    frame = 0
    game_started = False

    print("Running CPU vs CPU...")

    try:
        while True:
            frame += 1

            # Build action (8 buttons)
            action = [0] * 8

            if frame < 120:
                # Wait for title screen
                pass
            elif frame < 150:
                # Press Start to exit title
                action[BUTTON_START] = 1
            elif frame < 180:
                # Wait
                pass
            elif frame < 210:
                # Press Right to select 2P
                action[BUTTON_RIGHT] = 1
            elif frame < 240:
                # Wait
                pass
            elif frame < 270:
                # Press Start to confirm 2P
                action[BUTTON_START] = 1
            elif frame < 400:
                # On level select, press Up to increase level
                if (frame % 10) < 5:
                    action[BUTTON_UP] = 1
            elif frame < 430:
                # Press Right for High speed
                action[BUTTON_RIGHT] = 1
            elif frame < 460:
                # Wait
                pass
            elif frame < 490:
                # Press Start to begin
                action[BUTTON_START] = 1
                game_started = True
            else:
                # Random gameplay
                if frame % 4 == 0:
                    # Random D-pad and A/B for P1
                    rand = np.random.randint(0, 256)
                    action[BUTTON_A] = (rand >> 0) & 1
                    action[BUTTON_B] = (rand >> 1) & 1
                    action[BUTTON_UP] = (rand >> 4) & 1
                    action[BUTTON_DOWN] = (rand >> 5) & 1
                    action[BUTTON_LEFT] = (rand >> 6) & 1
                    action[BUTTON_RIGHT] = (rand >> 7) & 1

            # Step the emulator
            # nes-py takes a single integer action, need to convert
            action_int = sum(a << i for i, a in enumerate(action))
            obs, reward, done, info = env.step(action_int)

            # Print status every 60 frames
            if frame % 60 == 0:
                print(f"Frame {frame}, game_started={game_started}")

            # Read some memory to check game state
            if frame % 300 == 0 and game_started:
                # Try to read player count at $0727
                try:
                    player_count = env.ram[0x0727]
                    p1_capsule_x = env.ram[0x0305]
                    p2_capsule_x = env.ram[0x0385]
                    print(f"  RAM: players={player_count}, P1_X={p1_capsule_x}, P2_X={p2_capsule_x}")
                except Exception as e:
                    print(f"  RAM read error: {e}")

            if frame > 3600:  # Run for ~1 minute at 60fps
                print("Test complete!")
                break

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        env.close()

if __name__ == "__main__":
    main()
