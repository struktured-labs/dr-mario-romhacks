#!/usr/bin/env python3
"""
HTTP server wrapper around Mednafen MCP tools.

This maintains a persistent MednafenMCP instance that was initialized
by the MCP launch tool. Python clients make HTTP requests instead of
creating their own MCP instances.

Usage:
    python3 mednafen_mcp_server.py

Then from Python:
    import requests
    state = requests.get('http://localhost:8000/game_state').json()
"""

import sys
import os
from pathlib import Path
from flask import Flask, jsonify, request
import logging

# Add mednafen-mcp to path
sys.path.insert(0, str(Path(__file__).parent.parent / "mednafen-mcp"))

from mcp_server import MednafenMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Global MCP instance (persistent across requests)
mcp = None


def get_mcp():
    """Get or initialize the MCP controller."""
    global mcp
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


if __name__ == '__main__':
    logger.info("Starting Mednafen MCP HTTP Server...")
    logger.info("Endpoints:")
    logger.info("  GET  /health - Health check")
    logger.info("  GET  /game_state - Get full game state")
    logger.info("  POST /read_memory - Read NES RAM")
    logger.info("  POST /write_memory - Write NES RAM")
    logger.info("  GET  /playfield?player=2 - ASCII playfield")
    logger.info("  POST /connect - Connect/reconnect to Mednafen")
    logger.info("")
    logger.info("Server running on http://localhost:8000")

    app.run(host='0.0.0.0', port=8000, debug=False)
