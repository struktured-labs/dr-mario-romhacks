#!/usr/bin/env python3
"""
Mednafen Process Manager

Handles spawning, managing, and auto-navigating Mednafen for RL training.
Solves the process ownership problem by launching Mednafen as a child.
"""

import subprocess
import time
import signal
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Add mednafen-mcp to path
sys.path.insert(0, str(Path(__file__).parent.parent / "mednafen-mcp"))
from mcp_server import MednafenMCP, find_mednafen_pid

logger = logging.getLogger(__name__)


class MednafenManager:
    """
    Manages Mednafen process lifecycle for RL training.

    Features:
    - Spawns Mednafen as child process (ensures parent-child for ptrace)
    - Auto-discovers NES RAM
    - Auto-navigates to VS CPU gameplay
    - Health monitoring and auto-restart
    - Headless or windowed mode
    """

    def __init__(
        self,
        rom_path: str,
        headless: bool = True,
        display: str = ":0",
    ):
        """
        Initialize manager.

        Args:
            rom_path: Path to Dr. Mario ROM
            headless: Run with xvfb (headless) or real display
            display: X display to use (for windowed mode)
        """
        self.rom_path = Path(rom_path)
        self.headless = headless
        self.display = display

        self.process: Optional[subprocess.Popen] = None
        self.mcp: Optional[MednafenMCP] = None
        self.pid: Optional[int] = None
        self.nes_ram_base: Optional[int] = None

        if not self.rom_path.exists():
            raise FileNotFoundError(f"ROM not found: {rom_path}")

    def launch(self) -> Dict[str, Any]:
        """
        Launch Mednafen and prepare for training.

        Returns:
            Status dict with PID, RAM base, etc.
        """
        logger.info("Launching Mednafen...")

        # Build command
        if self.headless:
            cmd = ["xvfb-run", "-a", "mednafen", str(self.rom_path)]
        else:
            cmd = ["mednafen", str(self.rom_path)]
            env = os.environ.copy()
            env["DISPLAY"] = self.display

        # Launch process
        try:
            if self.headless:
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            else:
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=env,
                )

            logger.info(f"Mednafen launched (PID {self.process.pid})")

            # Wait for Mednafen to fully start and initialize
            logger.info("Waiting for Mednafen initialization...")
            time.sleep(5)

            # Find actual Mednafen PID (may differ from Popen PID if xvfb-run used)
            self.pid = find_mednafen_pid()
            if not self.pid:
                raise RuntimeError("Mednafen process not found after launch")

            logger.info(f"Found Mednafen PID: {self.pid}")

            # Create MCP controller
            self.mcp = MednafenMCP()
            self.mcp.pid = self.pid

            # Discover NES RAM
            logger.info("Discovering NES RAM...")
            ram_result = self.mcp._discover_nes_ram()

            if self.mcp.nes_ram_base:
                self.nes_ram_base = self.mcp.nes_ram_base
                logger.info(f"NES RAM discovered at {hex(self.nes_ram_base)}")
            else:
                logger.warning("NES RAM not discovered yet (may need gameplay state)")

            # Auto-navigate to VS CPU gameplay
            logger.info("Auto-navigating to VS CPU gameplay...")
            nav_result = self._navigate_to_gameplay()

            return {
                "success": True,
                "pid": self.pid,
                "nes_ram_base": hex(self.nes_ram_base) if self.nes_ram_base else None,
                "game_mode": nav_result.get("game_mode", 0),
                "in_gameplay": nav_result.get("in_gameplay", False),
                "message": "Mednafen launched and ready for training"
            }

        except Exception as e:
            logger.error(f"Failed to launch Mednafen: {e}", exc_info=True)
            self.shutdown()
            return {
                "success": False,
                "error": str(e)
            }

    def _navigate_to_gameplay(self, max_attempts: int = 5) -> Dict[str, Any]:
        """
        Auto-navigate menu to VS CPU gameplay.

        Args:
            max_attempts: Number of navigation attempts

        Returns:
            Status dict with game mode
        """
        if not self.mcp:
            return {"error": "MCP not initialized"}

        def press_button(button_code, hold_frames=10, release_frames=5):
            """Press a button with proper timing - write to multiple addresses."""
            for _ in range(hold_frames):
                # Write to both controller RAM locations
                self.mcp.write_nes_ram(0xF5, [button_code])  # P1 new input
                self.mcp.write_nes_ram(0xF7, [button_code])  # P1 held input
                self.mcp.write_nes_ram(0x5B, [button_code])  # Processed input
                time.sleep(0.020)  # Slightly longer than 1 frame
            for _ in range(release_frames):
                self.mcp.write_nes_ram(0xF5, [0x00])
                self.mcp.write_nes_ram(0xF7, [0x00])
                self.mcp.write_nes_ram(0x5B, [0x00])
                time.sleep(0.020)

        for attempt in range(max_attempts):
            logger.info(f"Navigation attempt {attempt + 1}/{max_attempts}")

            try:
                # Read current game mode
                mode_result = self.mcp.read_nes_ram(0x46, 1)
                current_mode = mode_result.get('values', [0])[0] if 'values' in mode_result else 0

                logger.info(f"Current game mode: {current_mode}")

                # If already in gameplay (mode >= 4), we're done
                if current_mode >= 4:
                    logger.info("Already in gameplay!")
                    return {"in_gameplay": True, "game_mode": current_mode}

                # Step 1: Leave title screen with START
                logger.info("Step 1: Pressing START to leave title screen...")
                for _ in range(20):
                    press_button(0x10)  # START
                time.sleep(1.0)

                # Check state
                mode_result = self.mcp.read_nes_ram(0x46, 1)
                current_mode = mode_result.get('values', [0])[0] if 'values' in mode_result else 0
                logger.info(f"After START: mode={current_mode}")

                # Step 2: Press SELECT twice to reach VS CPU mode
                logger.info("Step 2: Pressing SELECT to reach VS CPU...")
                for _ in range(2):
                    for _ in range(10):
                        press_button(0x20)  # SELECT
                    time.sleep(0.5)

                # Check state
                mode_result = self.mcp.read_nes_ram(0x46, 1)
                current_mode = mode_result.get('values', [0])[0] if 'values' in mode_result else 0
                logger.info(f"After SELECT: mode={current_mode}")

                # Step 3: Press START to enter level select
                logger.info("Step 3: Pressing START for level select...")
                for _ in range(20):
                    press_button(0x10)  # START
                time.sleep(1.0)

                # Check state
                mode_result = self.mcp.read_nes_ram(0x46, 1)
                current_mode = mode_result.get('values', [0])[0] if 'values' in mode_result else 0
                logger.info(f"After level select: mode={current_mode}")

                # Step 4: Press START to begin game
                logger.info("Step 4: Pressing START to begin game...")
                for _ in range(20):
                    press_button(0x10)  # START
                time.sleep(2.0)  # Wait for virus intro

                # Final check
                mode_result = self.mcp.read_nes_ram(0x46, 1)
                final_mode = mode_result.get('values', [0])[0] if 'values' in mode_result else 0

                logger.info(f"Final game mode: {final_mode}")

                if final_mode >= 4:
                    logger.info("✓ Successfully navigated to gameplay!")

                    # Re-discover RAM now that we're in gameplay (more reliable)
                    if not self.nes_ram_base:
                        logger.info("Re-discovering RAM in gameplay state...")
                        self.mcp._discover_nes_ram()
                        self.nes_ram_base = self.mcp.nes_ram_base
                        if self.nes_ram_base:
                            logger.info(f"RAM discovered: {hex(self.nes_ram_base)}")

                    return {"in_gameplay": True, "game_mode": final_mode}

                logger.warning(f"Still in menu (mode {final_mode}), retrying...")
                time.sleep(2)

            except Exception as e:
                logger.error(f"Navigation error: {e}", exc_info=True)

        return {"in_gameplay": False, "game_mode": 0, "error": "Failed to reach gameplay"}

    def is_alive(self) -> bool:
        """Check if Mednafen process is still running."""
        if not self.process:
            return False
        return self.process.poll() is None

    def get_mcp(self) -> Optional[MednafenMCP]:
        """Get the MCP controller instance."""
        return self.mcp

    def shutdown(self):
        """Shutdown Mednafen process."""
        if self.process:
            logger.info(f"Shutting down Mednafen (PID {self.process.pid})...")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning("Mednafen didn't terminate, killing...")
                self.process.kill()
                self.process.wait()

            self.process = None
            self.pid = None
            self.mcp = None
            logger.info("Mednafen shutdown complete")

    def restart(self) -> Dict[str, Any]:
        """Restart Mednafen."""
        logger.info("Restarting Mednafen...")
        self.shutdown()
        time.sleep(2)
        return self.launch()

    def __enter__(self):
        """Context manager entry."""
        self.launch()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.shutdown()


if __name__ == "__main__":
    # Test the manager
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    rom_path = "/home/struktured/projects/dr-mario-mods/drmario_vs_cpu.nes"

    print("Testing MednafenManager...")
    print()

    with MednafenManager(rom_path, headless=False) as manager:
        result = manager.launch()

        if result["success"]:
            print(f"\n✓ Mednafen launched successfully!")
            print(f"  PID: {result['pid']}")
            print(f"  RAM base: {result['nes_ram_base']}")
            print(f"  Game mode: {result['game_mode']}")
            print(f"  In gameplay: {result['in_gameplay']}")
            print()
            print("Press ENTER to shutdown...")
            input()
        else:
            print(f"\n✗ Launch failed: {result.get('error')}")
