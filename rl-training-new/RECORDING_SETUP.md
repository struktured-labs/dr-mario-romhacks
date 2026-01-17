# Recording Training Sessions

## Motivation
Capture the learning process to visualize agent improvement over time.

**User request**: "I'm kind of sad we didn't capture a recording of it learning"

## What to Record

### 1. TensorBoard Metrics (Already Happening!)
**Location**: `logs/tensorboard/`

**Metrics captured**:
- `rollout/ep_rew_mean` - Average episode reward
- `rollout/ep_len_mean` - Average episode length
- `train/value_loss` - Value function loss
- `train/policy_loss` - Policy gradient loss
- `train/entropy` - Policy entropy (exploration)
- `train/approx_kl` - KL divergence
- `train/clip_fraction` - Clipping frequency

**View live**:
```bash
tensorboard --logdir=logs/tensorboard --host=0.0.0.0 --port=6006
# Open: http://localhost:6006
```

### 2. Video Recordings of Gameplay (TODO - Next Session)

**Option A: FFmpeg Screen Recording**
Record Mednafen window directly:
```bash
# Start Mednafen with display
mednafen drmario_vs_cpu.nes

# In another terminal, record window
ffmpeg -video_size 256x240 -framerate 60 -f x11grab -i :0.0+100,100 \
  -c:v libx264 -preset ultrafast -crf 18 \
  training_session_$(date +%Y%m%d_%H%M%S).mp4
```

**Option B: Mednafen Built-in Recording**
Mednafen has AVI recording:
```bash
# Press Shift+F5 during gameplay to start/stop recording
# Saves to: ~/.mednafen/mcs/<rom_name>-<timestamp>.avi
```

**Option C: Custom Gymnasium VideoRecorder**
Add to training script:
```python
from gymnasium.wrappers import RecordVideo

env = RecordVideo(
    env,
    video_folder="logs/videos",
    episode_trigger=lambda ep: ep % 100 == 0,  # Record every 100th episode
    name_prefix="drmario_training"
)
```

### 3. Custom Metrics Logging (TODO - Next Session)

Track Dr. Mario specific metrics:
```python
# In drmario_env.py, log to CSV
import csv
from datetime import datetime

class MetricsLogger:
    def __init__(self, filepath="logs/training_metrics.csv"):
        self.filepath = filepath
        self.file = open(filepath, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow([
            'timestamp', 'episode', 'timestep',
            'viruses_cleared', 'max_combo', 'topped_out',
            'episode_length', 'total_reward'
        ])

    def log(self, episode, timestep, viruses_cleared, max_combo,
            topped_out, episode_length, total_reward):
        self.writer.writerow([
            datetime.now().isoformat(),
            episode, timestep, viruses_cleared, max_combo,
            topped_out, episode_length, total_reward
        ])
        self.file.flush()
```

### 4. Periodic Checkpoint Evaluation (TODO - Next Session)

Create `scripts/evaluate_checkpoint.py`:
```python
#!/usr/bin/env python3
"""
Evaluate a checkpoint on 100 episodes and record video.

Usage:
    python scripts/evaluate_checkpoint.py models/checkpoints/ppo_drmario_100000_steps.zip
"""

def evaluate_checkpoint(model_path, n_episodes=100, record_video=True):
    model = PPO.load(model_path)
    env = DrMarioEnv(player_id=2)

    if record_video:
        env = RecordVideo(env, f"logs/eval_videos/{model_path.stem}")

    stats = {
        'wins': 0,
        'losses': 0,
        'viruses_cleared': [],
        'episode_lengths': []
    }

    for ep in range(n_episodes):
        obs, _ = env.reset()
        done = False
        ep_length = 0

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            ep_length += 1

        stats['episode_lengths'].append(ep_length)
        if info.get('won'):
            stats['wins'] += 1
        else:
            stats['losses'] += 1

    print(f"Checkpoint: {model_path}")
    print(f"Win rate: {stats['wins']}/{n_episodes} ({100*stats['wins']/n_episodes:.1f}%)")
    print(f"Avg episode length: {sum(stats['episode_lengths'])/len(stats['episode_lengths']):.1f}")
```

Run after every checkpoint:
```bash
# Evaluate latest checkpoint
python scripts/evaluate_checkpoint.py models/checkpoints/ppo_drmario_100000_steps.zip
```

### 5. Time-lapse Video Creation (Post-Training)

Compile evaluation videos into time-lapse:
```bash
# After training, create time-lapse showing improvement
ffmpeg -framerate 30 -pattern_type glob -i 'logs/eval_videos/*/episode-*.mp4' \
  -c:v libx264 -pix_fmt yuv420p \
  training_timelapse_$(date +%Y%m%d).mp4
```

## Next Training Session Checklist

Before starting training:

- [ ] Clear old logs: `rm -rf logs/*` (or archive them)
- [ ] Start TensorBoard in background: `tensorboard --logdir=logs/tensorboard --host=0.0.0.0 &`
- [ ] Enable video recording wrapper in `drmario_env.py`
- [ ] Add custom metrics logger
- [ ] Create evaluation script
- [ ] Set up periodic checkpoint evaluation (cron job or training callback)

**During training**:
- [ ] Monitor TensorBoard live
- [ ] Run evaluation every 50K steps
- [ ] Take screenshots of interesting moments

**After training**:
- [ ] Create time-lapse video
- [ ] Generate final report with metrics
- [ ] Archive all recordings to permanent storage

## Storage Estimate

For 1M timestep training:
- TensorBoard logs: ~50-100 MB
- Video recordings (every 100 episodes): ~5-10 GB
- Checkpoint evaluations (20 checkpoints × 100 episodes): ~2-5 GB
- Custom metrics CSV: ~10-50 MB

**Total**: ~7-15 GB for full recording

## Current Session (150K steps)

**What we have**:
- ✅ TensorBoard logs in `logs/tensorboard/`
- ✅ Text logs in `logs/training.log`
- ✅ 15 checkpoints in `models/checkpoints/`

**What we're missing**:
- ❌ No video recordings
- ❌ No custom metrics tracking (virus clears, combos, etc.)
- ❌ No periodic evaluations

**Note**: We can still evaluate existing checkpoints after training completes!

## Quick Start for Next Session

**Option 1: Full Recording** (recommended for milestone runs)
```bash
# Start everything
tensorboard --logdir=logs/tensorboard --host=0.0.0.0 --port=6006 &
python scripts/train.py --timesteps 1000000 --device cuda --record-video

# In another terminal, monitor
watch -n 60 'python scripts/evaluate_checkpoint.py models/checkpoints/ppo_drmario_*.zip | tail -20'
```

**Option 2: Minimal Overhead** (for quick experiments)
```bash
# Just TensorBoard + text logs (current setup)
python scripts/train.py --timesteps 1000000 --device cuda
```

---

**Created**: 2026-01-17 during first successful 2P training run
**Status**: Prepared for next session
