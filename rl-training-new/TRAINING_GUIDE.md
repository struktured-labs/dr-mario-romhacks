# Dr. Mario RL Training Guide

Complete guide for training a PPO agent to play Dr. Mario.

## Prerequisites

1. **Mesen running** with Dr. Mario ROM
2. **Lua bridge loaded** (`lua/mesen_bridge.lua`)
3. **Game started** in VS CPU mode (P2)
4. **Python dependencies** installed

## Setup

### 1. Install Dependencies

```bash
cd rl-training-new

# Using uv (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

### 2. Verify GPU (Optional but Recommended)

```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
```

Expected output on blackmage:
```
CUDA available: True
GPU: NVIDIA GeForce RTX 3090
```

### 3. Test Environment

```bash
python src/drmario_env.py
```

This will:
- Connect to Mesen
- Reset environment
- Take 100 random actions
- Print rewards and state

If this works, you're ready to train!

## Training

### Basic Training (1M timesteps, ~1-4 days on 3090)

```bash
python scripts/train.py --timesteps 1000000 --device cuda
```

### Quick Test (10K timesteps, ~10 minutes)

```bash
python scripts/train.py --timesteps 10000 --device cuda --save-freq 2000
```

### Resume Training

```bash
python scripts/train.py --timesteps 1000000 --device cuda --resume models/checkpoints/ppo_drmario_10000_steps.zip
```

### Training Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--timesteps` | 1000000 | Total training steps |
| `--device` | cuda (if available) | cpu or cuda |
| `--learning-rate` | 3e-4 | PPO learning rate |
| `--n-steps` | 2048 | Steps per update |
| `--batch-size` | 64 | Minibatch size |
| `--n-epochs` | 10 | Epochs per update |
| `--save-freq` | 10000 | Checkpoint frequency |
| `--resume` | None | Path to checkpoint to resume |

## Monitoring

### TensorBoard

Launch TensorBoard to monitor training:

```bash
tensorboard --logdir logs/tensorboard
```

Open browser: http://localhost:6006

**Key metrics to watch:**
- **rollout/ep_rew_mean**: Average episode reward (should increase)
- **rollout/ep_len_mean**: Average episode length
- **train/loss**: Training loss (should decrease)
- **train/explained_variance**: How well value function predicts returns (0-1)

### Console Output

Training prints progress every N steps:
```
-------------------------------------
| rollout/                |         |
|    ep_len_mean          | 1.2e+03 |
|    ep_rew_mean          | -15.3   |
| time/                   |         |
|    fps                  | 847     |
|    iterations           | 100     |
|    time_elapsed         | 241     |
|    total_timesteps      | 204800  |
| train/                  |         |
|    entropy_loss         | -2.15   |
|    explained_variance   | 0.423   |
|    learning_rate        | 0.0003  |
|    loss                 | 12.4    |
|    policy_gradient_loss | -0.0156 |
|    value_loss           | 45.3    |
-------------------------------------
```

## Evaluation

### Watch Trained Agent

```bash
python scripts/watch.py models/ppo_drmario_final.zip --episodes 5
```

This will:
- Load the trained model
- Play 5 episodes
- Print progress every 100 steps
- Show final results (WIN/LOSS)

### Compare to Baseline

Compare RL agent to Python AI (oracle) baseline:

1. **Run Python AI for 10 games**, record win rate
2. **Run RL agent for 10 games**, record win rate
3. **Compare**:
   - RL should eventually beat Python AI (70-80% of oracle performance is target)
   - If RL < Python AI, train longer or tune hyperparameters

## Troubleshooting

### "Connection refused"

**Problem**: Can't connect to Mesen

**Solution**:
- Make sure Mesen is running
- Load Lua bridge script: Tools → Script Window → Load `lua/mesen_bridge.lua`
- Start game in VS CPU mode

### "CUDA out of memory"

**Problem**: GPU runs out of memory

**Solution**:
- Reduce `--batch-size` (try 32 or 16)
- Reduce `--n-steps` (try 1024)
- Use CPU instead: `--device cpu`

### Training is slow

**Problem**: < 100 FPS

**Solution**:
- Check GPU utilization: `nvidia-smi`
- If GPU not used, check: `torch.cuda.is_available()`
- Increase `frame_skip` in environment (trade accuracy for speed)

### Agent not learning

**Problem**: Episode reward not increasing after 100K steps

**Solution**:
- Check reward function (are rewards too sparse?)
- Verify environment is working (test with `python src/drmario_env.py`)
- Try different hyperparameters:
  - Increase `--learning-rate` (try 1e-3)
  - Decrease `--n-steps` (try 1024)
- Check TensorBoard for exploding/vanishing gradients

### Rewards are all negative

**Problem**: Episode rewards stay around -1000

**Solution**:
- This is normal early in training (agent is learning)
- Time penalty accumulates: -0.1 × 10000 steps = -1000
- Once agent starts clearing viruses, rewards will increase
- Give it 50K-100K steps to learn basics

## Expected Results

### Training Curve

**0-50K steps**: Random exploration, lots of game overs
- Reward: -500 to -1000
- Win rate: 0%

**50K-200K steps**: Learning basics (movement, rotation)
- Reward: -200 to -500
- Win rate: 0-10%

**200K-500K steps**: Starting to clear viruses
- Reward: -100 to +50
- Win rate: 10-30%

**500K-1M steps**: Consistent play, occasional wins
- Reward: +50 to +150
- Win rate: 30-60%

**1M+ steps**: Near-optimal play
- Reward: +100 to +200
- Win rate: 60-80%

### Final Performance Target

- **Win rate**: 60-80% (on Level 0, Speed Low)
- **Average viruses cleared**: 15-20 (out of 20)
- **Qualitative**:
  - Clears viruses deliberately (not random)
  - Manages height (doesn't top out often)
  - Uses rotation effectively
  - Avoids obvious mistakes

## Next Steps After Training

Once you have a trained model with good performance:

1. **Phase 3**: Distill to decision tree
   - Collect 100K (state, action) pairs from trained model
   - Train sklearn DecisionTreeClassifier (max_depth=6)
   - Target: 70-80% accuracy vs neural network

2. **Phase 4**: Compile to 6502 assembly
   - Generate assembly code from decision tree
   - Verify size ≤ 500 bytes

3. **Phase 5**: Embed in ROM
   - Find/create ROM space
   - Patch controller hook
   - Test on real hardware

## Tips for Success

1. **Start small**: Train for 10K steps first to verify everything works
2. **Monitor closely**: Check TensorBoard every hour for first few hours
3. **Be patient**: Good performance takes 500K-1M steps (1-4 days on 3090)
4. **Save often**: Checkpoints every 10K steps (don't lose progress!)
5. **Compare to baseline**: Python AI is your benchmark
6. **Iterate**: If not learning, tune hyperparameters and retry

## Hardware Performance

**3090 GPU** (blackmage):
- Expected FPS: 500-1000
- 1M timesteps: 1-4 days
- VRAM usage: ~4-6 GB

**CPU only**:
- Expected FPS: 50-100
- 1M timesteps: 1-2 weeks
- RAM usage: ~2-4 GB

Good luck training! 🎮🤖
