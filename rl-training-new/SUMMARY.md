# Dr. Mario RL Training - Session Summary

**Date**: 2026-01-11
**Duration**: ~8 hours
**Status**: Phase 2 Setup Complete ✅ - Ready to Train!

---

## 🎉 What We Built Today

### Phase 0: Mesen Integration (Commits: `12aed93`, `39ba52a`)

Switched from Mednafen to Mesen2 for superior RL training infrastructure.

**Built:**
- Compiled Mesen2 from source (git submodule)
- Created Lua bridge socket server (TCP:8765)
- Built Python client (`mesen_interface.py`)
- Integration tests

**Why Mesen?**
- Well-documented Lua API (vs Mednafen: none)
- Most accurate NES emulator
- 1-2 days to implement (vs weeks of reverse engineering)

---

### Phase 1: Python AI "Oracle" (Commit: `b58a323`)

Built full-featured AI with unlimited computation to demonstrate optimal play.

**Heuristics:**
- ✅ Column height analysis
- ✅ Virus clearing potential (+100 per virus)
- ✅ Match potential (2-3 color chains)
- ✅ Top row avoidance (-200 partition penalty)
- ✅ Height management (-5 per row)
- ✅ Column balance

**Purpose:**
- Baseline performance target for RL agent
- Reward function design validation
- Debugging tool (compare RL vs heuristic decisions)

---

### Phase 2: RL Training System (Commit: `c6a69e3`)

Complete infrastructure for training PPO agent with Stable-Baselines3.

**Components:**

1. **Memory Map** (`src/memory_map.py`)
   - NES addresses, constants, helpers

2. **Reward Function** (`src/reward_function.py`)
   - +10 per virus cleared
   - +5 for height reduction
   - -0.5 per row of height
   - -0.1 per frame
   - -100 for game over
   - +200 for win

3. **State Encoder** (`src/state_encoder.py`)
   - 12-channel CNN observation
   - Shape: (12, 16, 8)
   - Channels: empty, yellow, red, blue, capsule, next (×2 for both players)

4. **Gymnasium Environment** (`src/drmario_env.py`)
   - Wraps Mesen interface
   - Action space: Discrete(9)
   - Observation space: Box(12, 16, 8)
   - Handles reset/step/rewards

5. **Training Script** (`scripts/train.py`)
   - PPO with Stable-Baselines3
   - GPU support (CUDA/CPU)
   - TensorBoard logging
   - Checkpoint saving (every 10K steps)
   - Resume training

6. **Evaluation Script** (`scripts/watch.py`)
   - Load trained model
   - Play N episodes
   - Show progress and stats

7. **Documentation**
   - `TRAINING_GUIDE.md` (complete training manual)
   - `requirements.txt` (Python dependencies)
   - `STATUS.md` (project tracker)

---

## 📊 Architecture

```
┌──────────────┐   Gymnasium   ┌─────────────┐   Socket    ┌────────┐
│  PPO Agent   │◄─────────────►│ DrMarioEnv  │◄───────────►│  Lua   │
│ (CNN Policy) │   obs/reward  │  (wrapper)  │  TCP:8765   │ Bridge │
└──────────────┘               └─────────────┘             └────────┘
       ▲                              ▲                         ▲
       │                              │                         │
  Learns from                   Converts state             Read/Write
  experience                    to CNN format              NES memory
       │                              │                         │
       └──────────────────────────────┴─────────────────────────┘
                            Mesen Core (Lua API)
```

---

## 🚀 Ready to Train!

### Quick Start

```bash
# 1. Terminal 1: Launch Mesen
cd /home/struktured/projects/dr-mario-mods
./run_mesen.sh drmario_vs_cpu.nes

# In Mesen:
# - Tools → Script Window → Load lua/mesen_bridge.lua
# - Start game, select VS CPU mode (P2)

# 2. Terminal 2: Install dependencies
cd rl-training-new
uv pip install -r requirements.txt

# 3. Verify GPU
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

# 4. Test environment
python src/drmario_env.py

# 5. Start training!
python scripts/train.py --timesteps 1000000 --device cuda

# 6. Monitor (optional)
tensorboard --logdir logs/tensorboard
```

### Expected Training Time

**On 3090 GPU (blackmage):**
- **1M timesteps**: 1-4 days
- **FPS**: 500-1000
- **VRAM**: ~4-6 GB

---

## 📈 Expected Results

### Training Progression

| Steps | Reward | Win Rate | What's Happening |
|-------|--------|----------|------------------|
| 0-50K | -500 to -1000 | 0% | Random exploration, learning basics |
| 50K-200K | -200 to -500 | 0-10% | Learning movement and rotation |
| 200K-500K | -100 to +50 | 10-30% | Starting to clear viruses |
| 500K-1M | +50 to +150 | 30-60% | Consistent play, occasional wins |
| 1M+ | +100 to +200 | 60-80% | Near-optimal play |

### Final Performance Target

- **Win rate**: 60-80% (Level 0, Speed Low)
- **Avg viruses cleared**: 15-20 (out of 20)
- **Qualitative**:
  - Deliberate virus clearing (not random)
  - Height management (avoids topping out)
  - Effective rotation usage
  - Learns pathfinding implicitly

---

## 📁 File Structure

```
rl-training-new/
├── lua/
│   └── mesen_bridge.lua          # Socket server in Mesen
├── src/
│   ├── __init__.py
│   ├── mesen_interface.py        # Python client for Mesen
│   ├── memory_map.py             # NES memory addresses
│   ├── reward_function.py        # Reward calculator
│   ├── state_encoder.py          # Game state → CNN observation
│   ├── drmario_env.py            # Gymnasium environment
│   ├── heuristics.py             # Python AI heuristics
│   └── python_ai.py              # Python AI (oracle)
├── scripts/
│   ├── train.py                  # PPO training script
│   └── watch.py                  # Evaluation script
├── tests/
│   └── test_mesen_integration.py # Integration tests
├── logs/
│   └── tensorboard/              # TensorBoard logs
├── models/
│   └── checkpoints/              # Saved model checkpoints
├── requirements.txt              # Python dependencies
├── TRAINING_GUIDE.md             # Complete training manual
├── QUICKSTART.md                 # 5-minute setup guide
├── README.md                     # Project overview
├── STATUS.md                     # Project status tracker
└── run_ai.sh                     # Run Python AI oracle
```

---

## 🎯 Next Steps

### Immediate: Start Training

1. **Install dependencies**:
   ```bash
   cd rl-training-new
   uv pip install -r requirements.txt
   ```

2. **Test environment**:
   ```bash
   python src/drmario_env.py
   ```

3. **Start training**:
   ```bash
   python scripts/train.py --timesteps 1000000 --device cuda
   ```

4. **Monitor progress**:
   ```bash
   tensorboard --logdir logs/tensorboard
   # Open: http://localhost:6006
   ```

### After Training (Phase 3-5)

Once you have a trained model with 60-80% win rate:

**Phase 3: Distillation** (1-2 days)
- Collect 100K (state, action) pairs from trained model
- Train sklearn DecisionTreeClassifier (max_depth=6)
- Target: 70-80% accuracy vs neural network

**Phase 4: Compile to Assembly** (2-3 days)
- Write tree→assembly compiler
- Generate 6502 code from decision tree
- Verify size ≤ 500 bytes

**Phase 5: Embed in ROM** (2-4 days)
- Find/create ROM space (MMC3 mapper or CHR-ROM banking)
- Patch controller hook
- Test on real hardware

---

## 📊 Progress Summary

| Phase | Status | Files Created | Lines of Code |
|-------|--------|---------------|---------------|
| 0: Mesen Integration | ✅ | 5 | ~500 |
| 1: Python AI (Oracle) | ✅ | 4 | ~900 |
| 2: RL Training Setup | ✅ | 9 | ~1600 |
| **TOTAL** | **3/5 Complete** | **18 files** | **~3000 LOC** |

**Time invested**: ~8 hours
**Time remaining**: 8-17 days (mostly training time)

---

## 💡 Key Insights

1. **Mesen > Mednafen**: Well-documented API saved weeks of work
2. **Python AI crucial**: Provides baseline and validates reward function
3. **Reward design matters**: Based on Phase 1 heuristics (virus clearing, height, time)
4. **12-channel CNN**: Spatial representation lets agent learn patterns
5. **Phase 2 is infrastructure**: Setup fast (~1 day), training slow (1-4 days)

---

## 🎮 Try It Now!

### Option 1: Watch Python AI (No Training Required)

```bash
cd rl-training-new
./run_ai.sh
```

This shows what "optimal" play looks like (the oracle baseline).

### Option 2: Start RL Training

```bash
cd rl-training-new
python scripts/train.py --timesteps 10000 --device cuda  # Quick test
```

Start small (10K steps) to verify everything works, then scale to 1M.

---

## 📚 Documentation

- **`QUICKSTART.md`**: 5-minute setup
- **`TRAINING_GUIDE.md`**: Complete training manual
- **`STATUS.md`**: Project status and timeline
- **`README.md`**: Project overview
- **Plan files**: `../.claude/plans/`

---

## 🏆 Achievement Unlocked

You now have a **complete RL training system** for Dr. Mario!

- ✅ Emulator integration (Mesen + Lua)
- ✅ Oracle AI (baseline performance)
- ✅ Reward function (virus clearing + height management)
- ✅ CNN observation encoding (12-channel spatial)
- ✅ Gymnasium environment (standard RL interface)
- ✅ PPO training (Stable-Baselines3)
- ✅ GPU support (3090 ready!)
- ✅ Monitoring (TensorBoard)
- ✅ Evaluation (watch.py)
- ✅ Documentation (comprehensive guides)

**Ready to train and distill to ROM!** 🚀🤖🎮
