#!/usr/bin/env python3
"""
HTTP server wrapper around Mednafen MCP tools.

Option 2 Implementation: Server spawns and manages Mednafen process.

Features:
- Spawns Mednafen as child process (solves ptrace ownership)
- Auto-navigates to VS CPU gameplay
- Health monitoring and auto-restart
- Full lifecycle management

Usage:
    python3 mednafen_mcp_server.py

Then from Python:
    import requests
    # Launch Mednafen
    requests.post('http://localhost:8000/launch', json={'rom_path': '/path/to/rom.nes'})
    # Use as normal
    state = requests.get('http://localhost:8000/game_state').json()
"""

import sys
import os
from pathlib import Path
from flask import Flask, jsonify, request
import logging

# Add mednafen-mcp to path
sys.path.insert(0, str(Path(__file__).parent.parent / "mednafen-mcp"))

from mcp_server import MednafenMCP, find_mednafen_pid
from mednafen_manager import MednafenManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Global instances
mcp = None  # MCP controller (backwards compatibility)
manager = None  # Mednafen manager (Option 2)


def get_mcp():
    """Get or initialize the MCP controller."""
    global mcp, manager

    # If using managed Mednafen, return manager's MCP
    if manager and manager.get_mcp():
        return manager.get_mcp()

    # Otherwise, create standalone MCP (backwards compatibility)
    if mcp is None:
        logger.info("Initializing MednafenMCP instance...")
        mcp = MednafenMCP()
        # Connect to existing Mednafen process
        mcp.connect()
        logger.info(f"Connected to Mednafen PID {mcp.pid}, RAM base {hex(mcp.nes_ram_base) if mcp.nes_ram_base else 'not set'}")
    return mcp


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'pid': mcp.pid if mcp else None,
        'nes_ram_base': hex(mcp.nes_ram_base) if (mcp and mcp.nes_ram_base) else None,
    })


@app.route('/game_state', methods=['GET'])
def game_state():
    """Get full game state (both players)."""
    try:
        controller = get_mcp()
        logger.info(f"Getting game state (PID={controller.pid}, RAM={hex(controller.nes_ram_base) if controller.nes_ram_base else 'None'})")
        result = controller.get_game_state()
        logger.info(f"Game state result keys: {list(result.keys())}")
        if 'error' in result:
            logger.error(f"Game state returned error: {result['error']}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Exception getting game state: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/read_memory', methods=['POST'])
def read_memory():
    """
    Read NES RAM.

    Request JSON:
        {
            "address": 0x0046,
            "size": 1
        }

    Response JSON:
        {
            "values": [0x01, 0x02, ...]
        }
    """
    try:
        controller = get_mcp()
        data = request.get_json()
        address = data.get('address')
        size = data.get('size', 1)

        if address is None:
            return jsonify({'error': 'Missing address'}), 400

        result = controller.read_nes_ram(address, size)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error reading memory: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/write_memory', methods=['POST'])
def write_memory():
    """
    Write NES RAM.

    Request JSON:
        {
            "address": 0x00F6,
            "data": [0x01, 0x02, ...]
        }

    Response JSON:
        {
            "status": "ok",
            "bytes_written": 2
        }
    """
    try:
        controller = get_mcp()
        data = request.get_json()
        address = data.get('address')
        bytes_data = data.get('data')

        if address is None or bytes_data is None:
            return jsonify({'error': 'Missing address or data'}), 400

        result = controller.write_nes_ram(address, bytes_data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error writing memory: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/playfield', methods=['GET'])
def playfield():
    """
    Get ASCII art visualization of playfield.

    Query params:
        player: 1 or 2 (default: 2)
    """
    try:
        controller = get_mcp()
        player = int(request.args.get('player', 2))
        result = controller.get_playfield_ascii(player)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting playfield: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/connect', methods=['POST'])
def connect():
    """
    Connect to Mednafen (or reconnect).

    Request JSON (optional):
        {
            "nes_ram_base": "0x18c6290"  // Manually set RAM base
        }

    This will search for Mednafen process and discover NES RAM.
    If nes_ram_base is provided, it will skip discovery.
    """
    try:
        controller = get_mcp()

        # Check if RAM base is provided
        data = request.get_json() or {}
        manual_ram_base = data.get('nes_ram_base')

        if manual_ram_base:
            # Manually set RAM base (skip discovery)
            if isinstance(manual_ram_base, str):
                controller.nes_ram_base = int(manual_ram_base, 16)
            else:
                controller.nes_ram_base = int(manual_ram_base)
            logger.info(f"Manually set NES RAM base to {hex(controller.nes_ram_base)}")

            # Still need to find PID
            if controller.pid is None:
                from mcp_server import find_mednafen_pid
                controller.pid = find_mednafen_pid()
                if controller.pid is None:
                    return jsonify({'error': 'Mednafen not running'}), 500

            return jsonify({
                'status': 'connected',
                'pid': controller.pid,
                'nes_ram_base': hex(controller.nes_ram_base),
                'manual': True
            })

        # Normal connection with auto-discovery
        success = controller.connect()
        if success:
            return jsonify({
                'status': 'connected',
                'pid': controller.pid,
                'nes_ram_base': hex(controller.nes_ram_base) if controller.nes_ram_base else None,
                'manual': False
            })
        else:
            return jsonify({'error': 'Failed to connect'}), 500
    except Exception as e:
        logger.error(f"Error connecting: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/launch', methods=['POST'])
def launch():
    """
    Launch Mednafen with auto-navigation (Option 2).

    Request JSON:
        {
            "rom_path": "/path/to/drmario.nes",  // Required
            "headless": true,  // Optional, default true
            "display": ":0"  // Optional, for windowed mode
        }

    Returns:
        {
            "success": true,
            "pid": 12345,
            "nes_ram_base": "0x18c6290",
            "game_mode": 4,
            "in_gameplay": true
        }
    """
    global manager

    try:
        data = request.get_json() or {}
        rom_path = data.get('rom_path')

        if not rom_path:
            # Try default paths
            rom_path = "/home/struktured/projects/dr-mario-mods/drmario_vs_cpu.nes"
            if not Path(rom_path).exists():
                return jsonify({'error': 'ROM path required and default not found'}), 400

        headless = data.get('headless', True)
        display = data.get('display', ':0')

        logger.info(f"Launching Mednafen with ROM: {rom_path}")
        logger.info(f"  Headless: {headless}")

        # Shutdown existing manager if any
        if manager:
            logger.info("Shutting down existing Mednafen...")
            manager.shutdown()

        # Create and launch new manager
        manager = MednafenManager(rom_path, headless=headless, display=display)
        result = manager.launch()

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error launching Mednafen: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """
    Shutdown managed Mednafen instance.

    Returns:
        {
            "success": true,
            "message": "Mednafen shutdown"
        }
    """
    global manager

    try:
        if manager:
            logger.info("Shutting down Mednafen...")
            manager.shutdown()
            manager = None
            return jsonify({'success': True, 'message': 'Mednafen shutdown'})
        else:
            return jsonify({'success': False, 'message': 'No managed Mednafen running'})

    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/status', methods=['GET'])
def status():
    """
    Get status of managed Mednafen instance.

    Returns:
        {
            "managed": true,  // Using Option 2
            "alive": true,
            "pid": 12345,
            "nes_ram_base": "0x18c6290",
            "game_mode": 4
        }
    """
    global manager

    try:
        if manager:
            mcp_instance = manager.get_mcp()
            game_mode = None

            if mcp_instance and mcp_instance.nes_ram_base:
                try:
                    mode_result = mcp_instance.read_nes_ram(0x46, 1)
                    game_mode = mode_result.get('values', [0])[0] if 'values' in mode_result else None
                except:
                    pass

            return jsonify({
                'managed': True,
                'alive': manager.is_alive(),
                'pid': manager.pid,
                'nes_ram_base': hex(manager.nes_ram_base) if manager.nes_ram_base else None,
                'game_mode': game_mode
            })
        else:
            # Check for standalone MCP
            if mcp and mcp.pid:
                return jsonify({
                    'managed': False,
                    'pid': mcp.pid,
                    'nes_ram_base': hex(mcp.nes_ram_base) if mcp.nes_ram_base else None
                })
            else:
                return jsonify({
                    'managed': False,
                    'connected': False
                })

    except Exception as e:
        logger.error(f"Error getting status: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logger.info("Starting Mednafen MCP HTTP Server (Option 2)...")
    logger.info("")
    logger.info("Core Endpoints:")
    logger.info("  POST /launch - Launch Mednafen with auto-navigation (Option 2)")
    logger.info("  POST /shutdown - Shutdown managed Mednafen")
    logger.info("  GET  /status - Get Mednafen status")
    logger.info("")
    logger.info("Game Endpoints:")
    logger.info("  GET  /game_state - Get full game state")
    logger.info("  POST /read_memory - Read NES RAM")
    logger.info("  POST /write_memory - Write NES RAM")
    logger.info("  GET  /playfield?player=2 - ASCII playfield")
    logger.info("")
    logger.info("Legacy Endpoints:")
    logger.info("  GET  /health - Health check")
    logger.info("  POST /connect - Connect to existing Mednafen")
    logger.info("")
    logger.info("Server running on http://localhost:8000")
    logger.info("")
    logger.info("Quick start:")
    logger.info("  curl -X POST http://localhost:8000/launch")
    logger.info("  curl http://localhost:8000/game_state")
    logger.info("")

    app.run(host='0.0.0.0', port=8000, debug=False)
