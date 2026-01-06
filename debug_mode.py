#!/usr/bin/env python3
"""Debug script to discover actual Mode ($0046) values during different game states."""

import sys
import time
sys.path.insert(0, 'mednafen-mcp')
from mcp_server import MednafenMCP

# NES Controller button values for $F5
BTN_RIGHT  = 0x01
BTN_LEFT   = 0x02
BTN_DOWN   = 0x04
BTN_UP     = 0x08
BTN_START  = 0x10
BTN_SELECT = 0x20
BTN_B      = 0x40
BTN_A      = 0x80

def print_state(mcp, label=""):
    """Print current game state."""
    state = mcp.get_game_state()
    if "error" in state:
        print(f"Error: {state['error']}")
        return None

    mode = state.get('game_mode', '?')
    frame = state.get('frame', '?')
    p1_viruses = state['player1'].get('virus_count', 0)
    p2_viruses = state['player2'].get('virus_count', 0)
    p2_x = state['player2'].get('x_pos', 0)
    p2_y = state['player2'].get('y_pos', 0)
    num_players = state.get('num_players', 0)

    # Also read our custom flags
    flag_04 = mcp.read_nes_ram(0x04, 1)
    flag_02 = mcp.read_nes_ram(0x02, 1)

    vs_cpu_flag = flag_04.get('values', [0])[0] if 'values' in flag_04 else 0
    ai_ran_flag = flag_02.get('values', [0])[0] if 'values' in flag_02 else 0

    if label:
        print(f"[{label}]")
    print(f"  Frame {frame:3d}: Mode={mode:3d}, Players={num_players}, "
          f"P1 viruses={p1_viruses:2d}, P2 viruses={p2_viruses:2d}, "
          f"P2 pos=({p2_x},{p2_y}), VS_CPU=${vs_cpu_flag:02X}, AI_RAN=${ai_ran_flag:02X}")
    return state

def press_button(mcp, button, frames=5):
    """Press a button for specified frames then release."""
    # Press
    mcp.write_nes_ram(0xF5, [button])
    mcp.write_nes_ram(0xF7, [button])
    time.sleep(frames * 0.017)  # ~60fps
    # Release
    mcp.write_nes_ram(0xF5, [0])
    mcp.write_nes_ram(0xF7, [0])
    time.sleep(0.05)

def wait_frames(mcp, n):
    """Wait for approximately n frames."""
    time.sleep(n * 0.017)

def main():
    mcp = MednafenMCP()

    print("=" * 60)
    print("Dr. Mario Mode Value Debug")
    print("=" * 60)

    # Launch with virtual framebuffer (xvfb) instead of dummy SDL
    print("\nLaunching Mednafen with xvfb...")
    result = mcp.launch(headless=False, mode="vs_cpu")  # We'll run via xvfb-run
    print(f"Launch result: {result}")

    if "error" in result:
        print(f"ERROR: {result['error']}")
        return

    # Wait for game to initialize
    time.sleep(2.0)
    print_state(mcp, "After boot")

    # Navigate through title screen
    print("\n--- Navigating to VS CPU mode ---")

    # Press Start at title
    print("Pressing START at title...")
    press_button(mcp, BTN_START, 10)
    wait_frames(mcp, 30)
    print_state(mcp, "After title START")

    # Now at mode select: 1 PLAYER / 2 PLAYER / VS CPU
    # Press Down twice to get to VS CPU
    print("Navigating to VS CPU...")
    press_button(mcp, BTN_DOWN, 5)
    wait_frames(mcp, 10)
    press_button(mcp, BTN_DOWN, 5)
    wait_frames(mcp, 10)
    print_state(mcp, "At VS CPU option")

    # Select VS CPU
    print("Selecting VS CPU...")
    press_button(mcp, BTN_START, 10)
    wait_frames(mcp, 30)
    print_state(mcp, "After VS CPU select - should be level select")

    # We should now be at level select
    # Monitor Mode values here
    print("\n--- Level Select Screen ---")
    for i in range(10):
        print_state(mcp, f"Level select {i}")
        time.sleep(0.2)

    # Press Start to begin gameplay
    print("\nStarting gameplay...")
    press_button(mcp, BTN_START, 10)
    wait_frames(mcp, 60)  # Wait for Dr. Mario animation

    print("\n--- Gameplay Screen ---")
    for i in range(20):
        print_state(mcp, f"Gameplay {i}")
        time.sleep(0.3)

    print("\n" + "=" * 60)
    print("Mode value summary:")
    print("  - If Mode differs between level select and gameplay,")
    print("    we can use it for detection!")
    print("=" * 60)

    print("\nShutting down...")
    mcp.shutdown()
    print("Done.")

if __name__ == "__main__":
    main()
