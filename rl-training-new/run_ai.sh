#!/bin/bash
# Runner script for Dr. Mario Python AI

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Dr. Mario Python AI (Oracle)"
echo "=========================================="
echo ""

# Check if Mesen is running by trying to connect to port 8765
if ! nc -z localhost 8765 2>/dev/null; then
    echo "⚠️  Mesen bridge not detected (port 8765)"
    echo ""
    echo "Manual setup required:"
    echo "  1. Launch Mesen with Dr. Mario ROM:"
    echo "     cd .. && ./run_mesen.sh drmario_vs_cpu.nes"
    echo ""
    echo "  2. In Mesen, load Lua script:"
    echo "     Tools → Script Window → Load Script"
    echo "     Select: $SCRIPT_DIR/lua/mesen_bridge.lua"
    echo ""
    echo "  3. Start game and select VS CPU mode (P2)"
    echo ""
    echo "  4. Run this script again"
    echo ""
    exit 1
fi

echo "✓ Mesen bridge detected"
echo ""
echo "Starting AI..."
echo ""

# Run the AI
python3 src/python_ai.py
