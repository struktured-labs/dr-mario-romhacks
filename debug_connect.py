#!/usr/bin/env python3
"""Connect to running Mednafen and monitor game state."""

import sys
import time
sys.path.insert(0, 'mednafen-mcp')
from mcp_server import MednafenMCP

def main():
    mcp = MednafenMCP()

    print("Connecting to Mednafen...")
    result = mcp.connect()
    print(f"Connect result: {result}")

    if "error" in result:
        return

    print("\nMonitoring Mode values for 60 seconds...")
    print("Navigate through menus manually to see Mode changes.")
    print("-" * 70)

    start = time.time()
    last_mode = None
    while time.time() - start < 60:
        state = mcp.get_game_state()
        if "error" in state:
            print(f"Error: {state['error']}")
            time.sleep(1)
            continue

        mode = state.get('game_mode', '?')
        frame = state.get('frame', '?')
        p1_viruses = state['player1'].get('virus_count', 0)
        p2_viruses = state['player2'].get('virus_count', 0)
        p1_x = state['player1'].get('x_pos', 0)
        p1_y = state['player1'].get('y_pos', 0)
        p2_x = state['player2'].get('x_pos', 0)
        p2_y = state['player2'].get('y_pos', 0)
        num_players = state.get('num_players', 0)

        # Also read our custom flags
        flag_04 = mcp.read_nes_ram(0x04, 1)
        flag_02 = mcp.read_nes_ram(0x02, 1)
        input_f5 = mcp.read_nes_ram(0xF5, 1)
        input_5b = mcp.read_nes_ram(0x5B, 1)

        vs_cpu_flag = flag_04.get('values', [0])[0] if 'values' in flag_04 else 0
        ai_ran_flag = flag_02.get('values', [0])[0] if 'values' in flag_02 else 0
        p1_input = input_f5.get('values', [0])[0] if 'values' in input_f5 else 0
        p2_processed = input_5b.get('values', [0])[0] if 'values' in input_5b else 0

        # Only print when mode changes or every 30 frames
        if mode != last_mode or frame % 30 == 0:
            changed = " <-- MODE CHANGED!" if mode != last_mode else ""
            print(f"F{frame:3d} Mode={mode:2d} P={num_players} "
                  f"V1={p1_viruses:2d} V2={p2_viruses:2d} "
                  f"P1({p1_x},{p1_y:2d}) P2({p2_x},{p2_y:2d}) "
                  f"$04={vs_cpu_flag:02X} $02={ai_ran_flag:02X} "
                  f"$F5={p1_input:02X} $5B={p2_processed:02X}{changed}")
            last_mode = mode

        time.sleep(0.1)

    print("\nDone.")

if __name__ == "__main__":
    main()
