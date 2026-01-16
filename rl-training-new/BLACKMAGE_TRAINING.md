# Dr. Mario RL Training on Blackmage (3090 GPU)

Quick reference for running training on the blackmage server.

## Prerequisites

- SSH access to blackmage
- 3090 GPU available
- CUDA toolkit installed
- Python 3.9+ with uv/pixi

## Deployment

From your local machine:

```bash
cd /home/struktured/projects/dr-mario-mods/rl-training-new
./deploy_blackmage.sh
```

This will:
- Sync all code to blackmage
- Install Python dependencies
- Check ptrace permissions
- Display next steps

## Running Training

### 1. SSH to blackmage

```bash
ssh blackmage
cd ~/rl-training
```

### 2. Start HTTP MCP Server (Background)

```bash
# Start server in background
nohup python mednafen_mcp_server.py > mcp_server.log 2>&1 &

# Save PID for later
echo $! > mcp_server.pid
```

### 3. Launch Mednafen (Option 2 - Autonomous)

```bash
# Launch with auto-navigation
curl -X POST http://localhost:8000/launch

# Check status
curl http://localhost:8000/status
```

Expected response:
```json
{
  "managed": true,
  "alive": true,
  "pid": 12345,
  "nes_ram_base": "0x18c6290",
  "game_mode": 4
}
```

### 4. Start PPO Training

```bash
# Train for 1M timesteps on 3090
python scripts/train.py --timesteps 1000000 --device cuda

# Or for longer training (5M timesteps)
python scripts/train.py --timesteps 5000000 --device cuda

# Resume from checkpoint
python scripts/train.py --timesteps 1000000 --device cuda --resume models/checkpoints/ppo_drmario_10000_steps.zip
```

### 5. Monitor Training

#### Option A: TensorBoard (Recommended)

In another terminal:
```bash
ssh blackmage
cd ~/rl-training
tensorboard --logdir=logs/tensorboard --host=0.0.0.0 --port=6006
```

Then open in browser: http://blackmage:6006

Metrics to watch:
- `rollout/ep_rew_mean` - Average episode reward (should increase)
- `rollout/ep_len_mean` - Average episode length
- `train/value_loss` - Value function loss (should decrease)
- `train/policy_loss` - Policy loss (should decrease)

#### Option B: Training Logs

```bash
# Watch training progress
tail -f logs/training.log

# Check GPU usage
watch -n 1 nvidia-smi
```

## Training Parameters

Default configuration (adjust in scripts/train.py):

| Parameter | Value | Description |
|-----------|-------|-------------|
| `--timesteps` | 1,000,000 | Total training steps |
| `--device` | cuda | Use GPU (3090) |
| `--learning-rate` | 3e-4 | PPO learning rate |
| `--n-steps` | 2048 | Steps per policy update |
| `--batch-size` | 64 | Minibatch size |
| `--n-epochs` | 10 | Gradient epochs per update |
| `--save-freq` | 10,000 | Save checkpoint every N steps |

## Expected Training Time

With 3090 GPU:
- 1M timesteps: ~2-6 hours (depending on episode length)
- 5M timesteps: ~10-30 hours

CPU would take 5-10x longer.

## Checkpoints

Training saves checkpoints to `models/checkpoints/`:
- `ppo_drmario_10000_steps.zip`
- `ppo_drmario_20000_steps.zip`
- ... (every 10K steps)

Final model: `models/ppo_drmario_final.zip`

## Stopping Training

### Graceful Stop (Recommended)

Press `Ctrl+C` in the training terminal. The script will:
1. Stop training
2. Save current model to `models/ppo_drmario_interrupted.zip`
3. Exit cleanly

### Kill Training

```bash
# Find training process
ps aux | grep train.py

# Kill it
kill <PID>

# Model will NOT be saved - resume from last checkpoint
```

## Shutdown

### 1. Stop Training

Press `Ctrl+C` or kill process

### 2. Shutdown Mednafen

```bash
curl -X POST http://localhost:8000/shutdown
```

### 3. Stop MCP Server

```bash
# If you saved the PID
kill $(cat mcp_server.pid)

# Or find it
ps aux | grep mednafen_mcp_server
kill <PID>
```

## Troubleshooting

### GPU Not Detected

```bash
# Check CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Should print: True

# Check GPU
nvidia-smi
```

If CUDA not available:
- Verify CUDA toolkit installed
- Check PyTorch installation: `python -c "import torch; print(torch.__version__)"`
- May need to reinstall PyTorch with CUDA support

### Mednafen Not Launching

Check MCP server logs:
```bash
tail -f mcp_server.log
```

Common issues:
- ROM path incorrect (default: `/home/struktured/projects/dr-mario-mods/drmario_vs_cpu.nes`)
- xvfb-run not installed: `sudo apt install xvfb`
- Mednafen not installed: `sudo apt install mednafen`

### Training Crashes

1. Check logs: `tail -f logs/training.log`
2. Verify Mednafen still alive: `curl http://localhost:8000/status`
3. If Mednafen crashed, restart it: `curl -X POST http://localhost:8000/launch`
4. Resume training from checkpoint: `--resume models/checkpoints/ppo_drmario_<steps>_steps.zip`

### Connection Refused

If training can't connect to HTTP server:
- Check server running: `ps aux | grep mednafen_mcp_server`
- Check port: `curl http://localhost:8000/health`
- Restart server if needed

## After Training

Once training completes (or reaches good performance):

### 1. Evaluate Model

```bash
# TODO: Add evaluation script
python scripts/evaluate.py --model models/ppo_drmario_final.zip
```

### 2. Copy Model Back to Local

```bash
# From local machine
rsync -av blackmage:~/rl-training/models/ ./models/
```

### 3. Distill to Decision Tree

Next phase: Convert trained neural network to decision tree (~500 bytes for ROM).

See: [PHASE2_FEASIBILITY.md](../plan/PHASE2_FEASIBILITY.md) (if exists in plan)

---

## Quick Reference Commands

```bash
# Deploy from local
./deploy_blackmage.sh

# On blackmage - full startup
nohup python mednafen_mcp_server.py > mcp_server.log 2>&1 &
curl -X POST http://localhost:8000/launch
python scripts/train.py --timesteps 1000000 --device cuda

# Monitor
curl http://localhost:8000/status
tail -f logs/training.log
tensorboard --logdir=logs/tensorboard --host=0.0.0.0

# Shutdown
curl -X POST http://localhost:8000/shutdown
kill $(cat mcp_server.pid)
```

---

**Training target**: 500K-1M episodes until agent consistently clears viruses and manages height.

**Success criteria**:
- Episode reward > 50 consistently
- Virus clear rate > 80%
- Rarely tops out (good height management)
