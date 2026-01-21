#!/bin/bash
# Start Mesen with Dr. Mario ROM and Lua bridge for RL training

# ROM path
ROM="../drmario_vs_cpu.nes"

# Lua bridge script
LUA_SCRIPT="lua/mesen_bridge.lua"

# Mesen executable (via pixi for .NET)
MESEN="../mesen2/bin/linux-x64/Release/Mesen"

# Start Mesen with ROM and Lua script
# Note: Mesen will load the Lua script automatically if placed in scripts folder
# or we can use --lua flag if supported

echo "Starting Mesen with Dr. Mario ROM..."
echo "  ROM: $ROM"
echo "  Lua Bridge: $LUA_SCRIPT"
echo ""

cd "$(dirname "$0")"

# Run via pixi to get .NET 8.0 runtime
pixi run "$MESEN" "$ROM" --lua "$LUA_SCRIPT" "$@"
