# Dr. Mario RL Training - Project Status

**Last Updated**: 2026-01-11
**Current Phase**: Phase 1 Complete ✅

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

## 🔄 Phase 2: RL Training (NEXT)

**Status**: Not started
**Estimated Duration**: 3-7 days
**Goal**: Train PPO agent on 3090 GPU

### Plan

1. **Merge RL branch** from `origin/claude/rl-agents-mednafen-d84K3`
2. **Update for Mesen** (replace mednafen_interface.py → mesen_interface.py)
3. **Design reward function** based on Python AI insights:
   ```python
   reward = 0
   reward += 10 * viruses_cleared_this_step
   reward += 5 * height_reduced
   reward -= 100 if game_over else 0
   reward -= 1  # Time penalty (encourage speed)
   ```
4. **Install dependencies** (`stable-baselines3`, `gymnasium`, `torch`)
5. **Train on 3090 GPU** (~1M episodes, 1-4 days)
6. **Monitor with TensorBoard**
7. **Save best checkpoint**

### Expected Results

- Agent clears viruses in >80% of games
- Outperforms Python AI baseline
- Learns pathfinding and rotation implicitly
- Manages height without explicit penalty

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
| 2: RL Training | 🔄 Next | 3-7 days | TBD |
| 3: Distillation | ⏳ Pending | 1-2 days | TBD |
| 4: Compile to ASM | ⏳ Pending | 2-3 days | TBD |
| 5: ROM Embedding | ⏳ Pending | 2-4 days | TBD |
| **TOTAL** | | **11-21 days** | **~2-4 weeks** |

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
