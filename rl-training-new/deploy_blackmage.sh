#!/bin/bash
#
# Deploy Dr. Mario RL Training to blackmage (3090 GPU)
#
# Usage:
#   ./deploy_blackmage.sh
#
# This script:
#   1. Syncs code to blackmage
#   2. Sets up Python environment
#   3. Verifies ptrace permissions
#   4. Provides instructions for starting training

set -e

REMOTE_USER="${BLACKMAGE_USER:-struktured}"
REMOTE_HOST="blackmage"
REMOTE_DIR="~/rl-training"
LOCAL_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=================================================="
echo "Dr. Mario RL Training - Deploy to blackmage"
echo "=================================================="
echo ""

# Check if blackmage is reachable
echo "[1/5] Checking connection to blackmage..."
if ! ssh -q "${REMOTE_USER}@${REMOTE_HOST}" exit; then
    echo "❌ Cannot connect to ${REMOTE_USER}@${REMOTE_HOST}"
    echo "   Make sure SSH is configured and you have access"
    exit 1
fi
echo "✓ Connection OK"
echo ""

# Sync code
echo "[2/5] Syncing code to blackmage..."
rsync -av --delete \
    --exclude '.git' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.pytest_cache' \
    --exclude 'logs' \
    --exclude 'models' \
    --exclude 'tmp' \
    "${LOCAL_DIR}/" \
    "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/"
echo "✓ Code synced"
echo ""

# Check mednafen-mcp submodule
echo "[3/5] Syncing mednafen-mcp submodule..."
PARENT_DIR="$(dirname "$LOCAL_DIR")"
rsync -av --delete \
    --exclude '.git' \
    --exclude '__pycache__' \
    "${PARENT_DIR}/mednafen-mcp/" \
    "${REMOTE_USER}@${REMOTE_HOST}:~/dr-mario-mods/mednafen-mcp/"
echo "✓ Submodule synced"
echo ""

# Install dependencies
echo "[4/5] Installing Python dependencies..."
ssh "${REMOTE_USER}@${REMOTE_HOST}" "cd ${REMOTE_DIR} && uv pip install -r requirements.txt"
echo "✓ Dependencies installed"
echo ""

# Check ptrace permissions
echo "[5/5] Checking ptrace permissions..."
PTRACE_SCOPE=$(ssh "${REMOTE_USER}@${REMOTE_HOST}" "cat /proc/sys/kernel/yama/ptrace_scope")
echo "   Current ptrace_scope: ${PTRACE_SCOPE}"

if [ "$PTRACE_SCOPE" != "0" ]; then
    echo ""
    echo "⚠️  WARNING: ptrace_scope is not 0"
    echo "   Option 2 (server-spawned Mednafen) should work with any ptrace_scope"
    echo "   If you encounter issues, run on blackmage:"
    echo "      echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope"
    echo ""
fi
echo ""

# Success
echo "=================================================="
echo "✓ Deployment complete!"
echo "=================================================="
echo ""
echo "Next steps on blackmage:"
echo ""
echo "1. Start HTTP MCP server:"
echo "   ssh ${REMOTE_USER}@${REMOTE_HOST}"
echo "   cd ${REMOTE_DIR}"
echo "   nohup python mednafen_mcp_server.py > mcp_server.log 2>&1 &"
echo ""
echo "2. Launch Mednafen (Option 2 - autonomous):"
echo "   curl -X POST http://localhost:8000/launch"
echo ""
echo "3. Verify status:"
echo "   curl http://localhost:8000/status"
echo ""
echo "4. Start training (1M timesteps on 3090):"
echo "   python scripts/train.py --timesteps 1000000 --device cuda"
echo ""
echo "5. Monitor progress:"
echo "   # In another terminal:"
echo "   ssh ${REMOTE_USER}@${REMOTE_HOST}"
echo "   cd ${REMOTE_DIR}"
echo "   tensorboard --logdir=logs/tensorboard --host=0.0.0.0"
echo "   # Then open http://blackmage:6006 in browser"
echo ""
echo "=================================================="
