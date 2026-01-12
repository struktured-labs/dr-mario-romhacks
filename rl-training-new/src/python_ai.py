"""
Dr. Mario Python AI (Oracle)

Full-featured AI with unlimited computation.
Uses comprehensive heuristics for optimal play.

This "oracle" AI demonstrates what's possible without ROM constraints:
- Pathfinding and rotation
- Full column height analysis
- Virus clearing optimization
- Lookahead and planning

Used for:
- Reward function design and validation
- Baseline performance for RL agent
- Data collection for decision tree distillation
"""

import time
from enum import Enum
from typing import Optional, Tuple
from dataclasses import dataclass

from mesen_interface import MesenInterface
from heuristics import (
    Playfield, CapsuleState, find_best_move,
    INPUT_RIGHT, INPUT_LEFT, INPUT_DOWN, INPUT_A, INPUT_B
)


class AIState(Enum):
    """AI control state machine"""
    WAITING = "waiting"  # Waiting for gameplay to start
    DECIDING = "deciding"  # Deciding on next move
    ROTATING = "rotating"  # Rotating capsule
    MOVING = "moving"  # Moving to target column
    DROPPING = "dropping"  # Dropping capsule


@dataclass
class AIContext:
    """AI decision context"""
    target_column: int = 3
    target_rotation: int = 0
    current_rotation: int = 0
    state: AIState = AIState.WAITING
    frames_since_decision: int = 0
    last_capsule_y: int = 0


class DrMarioAI:
    """Python AI for Dr. Mario using Mesen interface"""

    def __init__(self, interface: MesenInterface):
        self.interface = interface
        self.context = AIContext()
        self.frame_count = 0
        self.viruses_cleared = 0
        self.initial_viruses = None

    def read_game_state(self) -> dict:
        """Read current game state from emulator"""
        return self.interface.get_game_state()

    def is_gameplay(self, state: dict) -> bool:
        """Check if game is in active gameplay mode"""
        return state['game_mode'] >= 4

    def make_decision(self, playfield: Playfield, capsule: CapsuleState):
        """
        Decide best move using heuristics

        Updates context with target column and rotation
        """
        print(f"\n[DECISION] Frame {self.frame_count}")
        print(f"  Capsule at ({capsule.x}, {capsule.y}), colors: L={capsule.left_color} R={capsule.right_color}")

        # Use heuristics to find best move
        target_col, target_rot = find_best_move(playfield, capsule)

        self.context.target_column = target_col
        self.context.target_rotation = target_rot
        self.context.current_rotation = 0  # Assume horizontal to start
        self.context.state = AIState.ROTATING
        self.context.frames_since_decision = 0

        print(f"  Decision: column={target_col}, rotation={target_rot}")

        # Print playfield info
        heights = playfield.get_all_column_heights()
        print(f"  Column heights: {heights}")
        print(f"  Viruses remaining: {playfield.count_viruses()}")

    def get_control_input(self, state: dict) -> int:
        """
        Get controller input based on current state

        Returns:
            Controller byte to write to $00F6
        """
        if not self.is_gameplay(state):
            self.context.state = AIState.WAITING
            return 0x00

        # Parse state into objects
        playfield = Playfield.from_bytes(state['playfield'])
        capsule = CapsuleState(
            x=state['capsule_x'],
            y=state['capsule_y'],
            left_color=state['left_color'],
            right_color=state['right_color']
        )

        # Track viruses cleared
        current_viruses = state['virus_count']
        if self.initial_viruses is None:
            self.initial_viruses = current_viruses
        if current_viruses < self.viruses_cleared:
            cleared = self.viruses_cleared - current_viruses
            print(f"  ✓ Cleared {cleared} viruses! ({current_viruses} remaining)")
        self.viruses_cleared = current_viruses

        # State machine for capsule control
        if self.context.state == AIState.WAITING:
            # Check if new capsule spawned
            if capsule.y < 2:  # Near top = new capsule
                self.context.state = AIState.DECIDING

        elif self.context.state == AIState.DECIDING:
            # Make decision
            self.make_decision(playfield, capsule)
            return 0x00  # No input while deciding

        elif self.context.state == AIState.ROTATING:
            # Rotate to target orientation
            rotations_needed = self.context.target_rotation - self.context.current_rotation

            if rotations_needed > 0:
                self.context.current_rotation += 1
                print(f"  [ROTATE] {self.context.current_rotation}/{self.context.target_rotation}")
                return INPUT_B  # Rotate clockwise
            else:
                # Done rotating
                self.context.state = AIState.MOVING
                return 0x00

        elif self.context.state == AIState.MOVING:
            # Move to target column
            if capsule.x < self.context.target_column:
                print(f"  [MOVE] Right ({capsule.x} → {self.context.target_column})")
                return INPUT_RIGHT
            elif capsule.x > self.context.target_column:
                print(f"  [MOVE] Left ({capsule.x} → {self.context.target_column})")
                return INPUT_LEFT
            else:
                # At target column, drop
                self.context.state = AIState.DROPPING
                print(f"  [DROP] At column {capsule.x}")
                return INPUT_DOWN

        elif self.context.state == AIState.DROPPING:
            # Keep pressing down until capsule locks
            if capsule.y > self.context.last_capsule_y:
                # Still falling
                self.context.last_capsule_y = capsule.y
                return INPUT_DOWN
            else:
                # Capsule locked or new capsule spawned
                if capsule.y < 2:
                    # New capsule
                    self.context.state = AIState.DECIDING
                return 0x00

        # Default: no input
        return 0x00

    def run_frame(self) -> bool:
        """
        Run one frame of AI

        Returns:
            True if game is active, False if game over or exited
        """
        self.frame_count += 1

        # Read game state
        state = self.read_game_state()

        # Check for game over
        if state['virus_count'] == 0:
            print("\n" + "="*60)
            print("🎉 GAME WON! All viruses cleared!")
            print("="*60)
            return False

        # Get control input
        input_byte = self.get_control_input(state)

        # Write to controller
        if input_byte != 0x00:
            self.interface.write_memory(0x00F6, [input_byte])

        # Step one frame
        self.interface.step_frame()

        return True

    def run(self, max_frames: Optional[int] = None):
        """
        Run AI main loop

        Args:
            max_frames: Maximum frames to run (None = infinite)
        """
        print("="*60)
        print("Dr. Mario Python AI Started")
        print("="*60)
        print("Oracle AI with full heuristics:")
        print("  - Virus clearing optimization")
        print("  - Height management")
        print("  - Column balance")
        print("  - Match potential scoring")
        print()
        print("Press Ctrl+C to stop")
        print("="*60)

        try:
            frame = 0
            while True:
                if max_frames and frame >= max_frames:
                    print(f"\nReached max frames ({max_frames})")
                    break

                # Run one frame
                if not self.run_frame():
                    break

                frame += 1

                # Throttle to ~60 FPS
                time.sleep(0.016)

        except KeyboardInterrupt:
            print("\n\nAI stopped by user")

        finally:
            print(f"\nFinal stats:")
            print(f"  Frames: {self.frame_count}")
            print(f"  Viruses remaining: {self.viruses_cleared}")
            if self.initial_viruses:
                cleared = self.initial_viruses - self.viruses_cleared
                print(f"  Viruses cleared: {cleared}/{self.initial_viruses}")


def main():
    """Main entry point"""
    import sys

    print("Dr. Mario Python AI (Oracle)")
    print()
    print("Prerequisites:")
    print("  1. Mesen running with Dr. Mario ROM")
    print("  2. Lua bridge script loaded (mesen_bridge.lua)")
    print("  3. Game started in VS CPU mode (P2)")
    print()

    # Connect to Mesen
    interface = MesenInterface()
    print("Connecting to Mesen...")

    if not interface.connect(timeout=10):
        print("ERROR: Failed to connect to Mesen")
        print("Make sure:")
        print("  - Mesen is running")
        print("  - Lua script is loaded (Tools → Script Window)")
        print("  - Game is started")
        sys.exit(1)

    print("✓ Connected!\n")

    try:
        # Create and run AI
        ai = DrMarioAI(interface)
        ai.run()

    finally:
        interface.disconnect()
        print("\nDisconnected from Mesen")


if __name__ == "__main__":
    main()
