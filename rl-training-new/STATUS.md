# Dr. Mario RL Training - Project Status

**Last Updated**: 2026-01-11
**Current Phase**: Phase 2 Setup Complete ✅ - Ready to Train!

---

## Overview

Building a reinforcement learning system to train an AI for Dr. Mario, then distill it to a decision tree (~500 bytes) that fits in NES ROM.

**Goal**: Create AI that clears viruses with pathfinding, rotation, and height awareness.

---

## ✅ Phase 0: Mesen Integration (COMPLETE)

**Status**: Operational
**Duration**: ~2 days
**Commit**: `12aed93`, `39ba52a`

### What We Built

1. **Mesen2 Emulator**
   - Compiled from source (git submodule)
   - .NET 8 SDK integration
   - Most accurate NES emulator
   - Wrapper script: `../run_mesen.sh`

2. **Lua Bridge** (`lua/mesen_bridge.lua`)
   - TCP socket server (port 8765)
   - Commands: READ, WRITE, STEP, GET_STATE, QUIT
   - Runs inside Mesen's Lua environment
   - Non-blocking with frame callbacks

3. **Python Client** (`src/mesen_interface.py`)
   - Clean API for RL training
   - Memory read/write
   - Frame stepping
   - Full game state extraction

4. **Integration Test** (`tests/test_mesen_integration.py`)
   - Validates memory operations
   - Tests controller input
   - Verifies frame stepping

### Architecture

```
Python RL Trainer ←→ Lua Bridge (TCP:8765) ←→ Mesen Core (Lua API)
```

### Why Mesen > Mednafen

| Feature | Mesen | Mednafen |
|---------|-------|----------|
| API Documentation | ✅ Excellent | ❌ None |
| Debugger | ✅ Built-in | ❌ None |
| Accuracy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Lua Scripting | ✅ Yes | ❌ No |
| Implementation Time | 1-2 days | Weeks (reverse engineering) |

---

## ✅ Phase 1: Python AI (Oracle) (COMPLETE)

**Status**: Operational
**Duration**: ~1 day
**Commit**: `b58a323`

### What We Built

1. **Heuristics Module** (`src/heuristics.py`)
   - **Column height analysis**: Prefers lower placements
   - **Virus clearing potential**: +100 points per adjacent virus cleared
   - **Match potential**: Bonus for 2-3 consecutive colors (setup for future clears)
   - **Top row avoidance**: -200 penalty for stacking near top (partition risk)
   - **Height penalty**: -5 per row (encourages downstacking)
   - **Column balance**: Bonus for reducing max height

2. **Main AI** (`src/python_ai.py`)
   - State machine: WAITING → DECIDING → ROTATING → MOVING → DROPPING
   - Evaluates all (column, rotation) combinations
   - Picks best move using heuristics
   - Controls capsule via Mesen interface
   - Tracks viruses cleared and progress

3. **Runner Script** (`run_ai.sh`)
   - Checks for Mesen connection
   - Provides setup instructions
   - Launches AI with clean interface

4. **Quick Start Guide** (`QUICKSTART.md`)
   - 5-minute setup instructions
   - Troubleshooting tips
   - Advanced usage examples

### AI Features

- ✅ **Full playfield analysis** (8x16 grid)
- ✅ **4-way rotation** (horizontal, vertical L/R)
- ✅ **All column evaluation** (8 columns × 4 rotations = 32 options)
- ✅ **Virus priority targeting**
- ✅ **Height management**
- ✅ **No ROM constraints** (unlimited computation)

### Heuristic Weights

| Heuristic | Weight | Purpose |
|-----------|--------|---------|
| Virus clearing | +100 per virus | Prioritize goal |
| Immediate clear | +50 | Bonus for 4+ match |
| Match potential (3) | +15 | Setup chains |
| Match potential (2) | +5 | Build toward clears |
| Height reduction | +10 | Maintain low stack |
| Height penalty | -5 per row | Prefer lower |
| Height increase | -30 | Avoid stacking |
| Top row risk | -200 | Prevent partition |

### Usage

```bash
# Terminal 1: Launch Mesen
./run_mesen.sh drmario_vs_cpu.nes

# In Mesen: Tools → Script Window → Load lua/mesen_bridge.lua
# Start game, select VS CPU mode (P2)

# Terminal 2: Run AI
cd rl-training-new
./run_ai.sh
```

### Sample Output

```
[DECISION] Frame 42
  Capsule at (3, 1), colors: L=0 R=1
  Column heights: [16, 16, 16, 14, 14, 16, 16, 16]
  Viruses remaining: 20
  Decision: column=4, rotation=0
  [MOVE] Right (3 → 4)
  [DROP] At column 4
  ✓ Cleared 2 viruses! (18 remaining)
```

---

## ✅ Phase 2: RL Training Setup (COMPLETE)

**Status**: Setup complete, ready to train!
**Duration**: ~1 day
**Commit**: `c6a69e3`

### What We Built

1. **Memory Map** (`src/memory_map.py`)
   - NES memory addresses and constants
   - Helper functions for tile/color conversion
   - Playfield dimensions and layout

2. **Reward Function** (`src/reward_function.py`)
   - Based on Python AI insights from Phase 1
   - **+10 per virus cleared** (main objective)
   - **+5 for height reduction** (encourage downstacking)
   - **-0.5 per row of height** (discourage tall stacks)
   - **-0.1 per frame** (encourage speed)
   - **-100 for game over** (survival critical)
   - **+200 for win** (all viruses cleared)

3. **State Encoder** (`src/state_encoder.py`)
   - Converts game state → multi-channel CNN observation
   - **12 channels**: P2 (empty, yellow, red, blue, capsule, next) + P1 (same 6)
   - Output shape: **(12, 16, 8)** for spatial CNN
   - Normalized float32 values (0.0-1.0)

4. **Gymnasium Environment** (`src/drmario_env.py`)
   - Wraps Mesen interface for RL training
   - **Action space**: Discrete(9) - move, rotate, combos
   - **Observation space**: Box(12, 16, 8) - multi-channel CNN input
   - Handles reset, step, termination, rewards
   - Integrates state encoder and reward calculator

5. **Training Script** (`scripts/train.py`)
   - PPO training with Stable-Baselines3
   - **GPU support** (CUDA/CPU auto-detection)
   - **TensorBoard logging**
   - **Checkpoint saving** every 10K steps
   - **Resume training** from checkpoint
   - Configurable hyperparameters (learning rate, batch size, etc.)

6. **Evaluation Script** (`scripts/watch.py`)
   - Load trained model
   - Play N episodes
   - Show step-by-step progress
   - Report win/loss statistics

7. **Training Guide** (`TRAINING_GUIDE.md`)
   - Complete setup instructions
   - Training parameters explained
   - TensorBoard monitoring guide
   - Troubleshooting tips
   - Expected performance curves
   - Hardware requirements

8. **Validation Tests** (`tests/`)
   - **test_env_validation.py**: 5 automated tests (memory, controller, encoding, rewards, episode)
   - **visualize_observation.py**: ASCII visualization of agent's view
   - **README.md**: Complete troubleshooting guide with common issues
   - **CRITICAL**: Must pass before starting 4-day training run!

### Architecture

```
┌──────────────┐   Gymnasium   ┌─────────────┐   Mesen     ┌───────┐
│  PPO Agent   │◄─────────────►│ DrMarioEnv  │◄───────────►│ Mesen │
│ (CNN Policy) │   obs/reward  │  (wrapper)  │  read/write │  Core │
└──────────────┘               └─────────────┘             └───────┘
       ▲                              ▲                         ▲
       │                              │                         │
       └──── Learns from ─────────────┴─────── State from ─────┘
```

### Validation Before Training!

**IMPORTANT**: Run validation tests FIRST to verify everything works:

```bash
cd rl-training-new

# Terminal 1: Launch Mesen
cd ..
./run_mesen.sh drmario_vs_cpu.nes
# In Mesen: Tools → Script Window → Load lua/mesen_bridge.lua
# Start game, select VS CPU mode (P2), reach gameplay

# Terminal 2: Run validation
cd rl-training-new
python tests/test_env_validation.py
```

**All 5 tests must pass:**
1. ✅ Memory reading (game state, virus count, capsule position)
2. ✅ Controller input (pressing RIGHT moves capsule)
3. ✅ State encoding (12-channel observation valid)
4. ✅ Reward calculation (virus clears, height, terminal states)
5. ✅ Full episode (reset/step/termination works)

### Start Training (After Validation Passes)

```bash
cd rl-training-new
uv pip install -r requirements.txt
python scripts/train.py --timesteps 1000000 --device cuda
```

**Monitor**:
```bash
tensorboard --logdir logs/tensorboard
```

**Expected Training Time**: 1-4 days on 3090 GPU for 1M timesteps

### Training Target

Once training completes:
- **Win rate target**: 60-80%
- **Avg viruses cleared**: 15-20 (out of 20)
- **Qualitative**: Deliberate virus clearing, height management, rotation usage

---

## 📋 Phase 3: Decision Tree Distillation (TODO)

**Status**: Not started
**Estimated Duration**: 1-2 days

### Plan

1. **Collect policy samples**:
   - Load best PPO checkpoint
   - Run 100K steps
   - Record (state, action) pairs
   - Save to pickle

2. **Train decision tree**:
   ```python
   from sklearn.tree import DecisionTreeClassifier
   tree = DecisionTreeClassifier(max_depth=6)
   tree.fit(states, actions)
   ```

3. **Evaluate accuracy**: Target 70-80% match with NN policy

4. **Export tree structure** for assembly generation

### Expected Results

- Decision tree with depth ≤ 6
- ~64 nodes max (2^6)
- ~500 bytes when compiled to 6502
- 70-80% of NN performance

---

## 🔧 Phase 4: Compile to 6502 Assembly (TODO)

**Status**: Not started
**Estimated Duration**: 2-3 days

### Plan

1. **Write tree→assembly compiler** (`tools/tree_to_asm.py`)
2. **Generate 6502 code**:
   - Internal nodes: `LDA feature; CMP threshold; BCC left`
   - Leaf nodes: `LDA action; RTS`
3. **Assemble to binary** (ca65 or custom)
4. **Verify size ≤ 500 bytes**

---

## 💾 Phase 5: ROM Expansion & Embedding (TODO)

**Status**: Not started
**Estimated Duration**: 2-4 days

### Plan

1. **Find ROM space**:
   - Option A: Unused regions (scan for 0xFF)
   - Option B: CHR-ROM banking
   - Option C: Upgrade to MMC3 mapper

2. **Embed decision tree**
3. **Update controller hook** (0x37CF → new AI)
4. **Test in Mesen** and on real hardware

---

## Timeline

| Phase | Status | Duration | Dates |
|-------|--------|----------|-------|
| 0: Mesen Integration | ✅ Complete | 1-2 days | Jan 11 |
| 1: Python AI (Oracle) | ✅ Complete | 1 day | Jan 11 |
| 2: RL Training Setup | ✅ Complete | 1 day | Jan 11 |
| 2: RL Training (Actual) | 🔄 Next | 1-4 days | TBD |
| 3: Distillation | ⏳ Pending | 1-2 days | TBD |
| 4: Compile to ASM | ⏳ Pending | 2-3 days | TBD |
| 5: ROM Embedding | ⏳ Pending | 2-4 days | TBD |
| **TOTAL** | | **8-17 days** | **~1-3 weeks** |

---

## Resources

- **Documentation**: `README.md`, `QUICKSTART.md`
- **Plan Files**: `../.claude/plans/typed-beaming-blossom.md`
- **Emulator Research**: `../.claude/plans/emulator-research.md`
- **Implementation Plan**: `../.claude/plans/revised-implementation.md`

---

## Hardware

- **Machine**: blackmage (Ubuntu, 3090 GPU available)
- **Mesen**: Compiled in `../mesen2/`
- **ROM**: `../drmario_vs_cpu.nes`

---

## Next Steps

**Immediate**: Start Phase 2 - RL Training
1. Merge RL branch
2. Update for Mesen interface
3. Design reward function using Python AI insights
4. Train PPO agent on 3090 GPU

**Questions**:
- Which reward function design? (virus clears + height + time?)
- How many training episodes? (500K-1M suggested)
- Early stopping criteria? (convergence + 80% win rate)
