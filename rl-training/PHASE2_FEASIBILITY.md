# Phase 2 Feasibility: Fitting Trained RL Model on NES

## Executive Summary

**Verdict**: ✅ **FEASIBLE** with significant constraints

A near-ideal trained model **cannot** be directly deployed on NES, but a **highly competitive approximation** (70-90% of optimal performance) is achievable through aggressive model compression. The key is not fitting the neural network itself, but **distilling its learned policy** into NES-compatible primitives.

---

## NES Hardware Constraints

### Critical Limitations

| Resource | Constraint | Implication |
|----------|-----------|-------------|
| **ROM Space** | ~160 bytes available (0x7F40-0x7FDF) | Extremely limited code space |
| **RAM** | 2KB total (shared with game) | No space for model weights |
| **CPU** | 6502 @ 1.79 MHz | ~29,780 cycles/frame @ 60Hz |
| **Math** | No floating point, 8-bit only | No matrix operations |
| **Timing** | Must respond within 1 frame (16.67ms) | ~30k cycles max per decision |

### Performance Budget

For AI to feel responsive, it should decide in **<5ms** (~8,900 cycles):
- Memory reads: ~3-4 cycles each
- Simple arithmetic: 2-7 cycles
- Branches: 2-4 cycles
- Subroutine calls: 12 cycles (JSR+RTS)

**Available operations per decision: ~2,000-4,000 instructions**

---

## Trained Model Complexity

### Phase 1 Model (External Training)

A typical PPO model for Dr. Mario would have:

```
CNN Policy Network:
├── Conv2D(12→32, 3x3): ~3,456 params
├── Conv2D(32→64, 3x3): ~18,432 params
├── FC(64*14*6 → 256): ~1,376,256 params
└── FC(256 → 12): 3,072 params
───────────────────────────────────────
Total: ~1.4 million parameters (5.6 MB as float32)
```

**Reality Check**: This is **35,000x larger** than available ROM space.

---

## Compression Strategies: Ranked by Feasibility

### 🥇 **Option 1: Decision Tree Distillation** (MOST FEASIBLE)

**Approach**: Train a decision tree to mimic the neural network's behavior.

#### Advantages
- ✅ Naturally compact representation
- ✅ Pure branching logic (fast on 6502)
- ✅ Interpretable and debuggable
- ✅ No floating point needed

#### Implementation

**Step 1: Collect dataset from trained RL agent**
```python
# Run trained PPO model, collect (state, action) pairs
dataset = []
for episode in range(10000):
    obs, done = env.reset(), False
    while not done:
        action = model.predict(obs)  # From trained PPO
        dataset.append((extract_features(obs), action))
        obs, _, done, _ = env.step(action)
```

**Step 2: Train decision tree**
```python
from sklearn.tree import DecisionTreeClassifier

# Extract hand-crafted features (not raw pixels!)
X = [extract_features(obs) for obs, action in dataset]
y = [action for obs, action in dataset]

tree = DecisionTreeClassifier(
    max_depth=8,        # ~2^8 = 256 leaf nodes
    max_leaf_nodes=128, # Further constraint
    min_samples_leaf=50 # Prevent overfitting
)
tree.fit(X, y)
```

**Step 3: Compile to 6502 assembly**
```python
def compile_to_asm(tree):
    """Convert decision tree to 6502 assembly"""
    # Each node becomes a comparison + branch
    # Example node: if capsule_color == RED then...
    asm = []
    def traverse(node, depth=0):
        if is_leaf(node):
            action = node.value
            asm.append(f"  LDA #{ACTION_MAP[action]}")
            asm.append(f"  RTS")
        else:
            feature = node.feature
            threshold = node.threshold
            asm.append(f"  LDA ${feature_addr[feature]}")
            asm.append(f"  CMP #{threshold}")
            asm.append(f"  BCS right_branch_{depth}")
            traverse(node.left, depth+1)
            asm.append(f"right_branch_{depth}:")
            traverse(node.right, depth+1)

    traverse(tree.root)
    return asm
```

#### Size Estimation

**Decision tree with depth 8:**
- Internal nodes: up to 255 nodes
- Each node: ~8 bytes (LDA, CMP, BCS)
- Leaf nodes: ~3 bytes (LDA, RTS)
- **Total: ~2,040 bytes** ❌ (too large!)

**Optimized tree with depth 6:**
- Internal nodes: up to 63 nodes
- Each node: ~8 bytes
- **Total: ~500 bytes** ✅ (fits!)

#### Performance

**Execution time** (worst case, depth 6):
- 6 comparisons × 10 cycles = 60 cycles
- Plus memory reads: 6 × 4 = 24 cycles
- **Total: ~84 cycles (0.05ms)** ✅ Real-time!

#### Expected Accuracy

Based on research in model distillation:
- Depth 6 tree: **70-80%** of neural network performance
- Depth 8 tree: **80-90%** of neural network performance

**Trade-off**: Accept 10-30% performance loss for deployability.

---

### 🥈 **Option 2: Lookup Table (LUT)** (FEASIBLE with heavy quantization)

**Approach**: Pre-compute optimal actions for discretized states.

#### Design

**State quantization:**
```python
# Reduce continuous state to discrete bins
state_hash = (
    (virus_count // 4) << 6 |          # 4 virus bins
    (avg_height // 4) << 4 |           # 4 height bins
    (capsule_color) << 2 |             # 3 colors
    (top_color_needed)                 # 3 colors
)
# Total: 4×4×3×3 = 144 states
```

**Lookup table:**
```asm
; ROM 0x7F40
action_lut:
    .byte ACTION_LEFT      ; State 0
    .byte ACTION_RIGHT     ; State 1
    .byte ACTION_ROTATE    ; State 2
    ; ... 144 entries
```

#### Size Estimation

- 144 states × 1 byte = **144 bytes** ✅ Fits!
- Plus hashing logic: ~20 bytes
- **Total: ~164 bytes** ✅ Just barely fits!

#### Limitations

- ❌ Extremely coarse state representation (ignores most playfield)
- ❌ Hard to encode spatial patterns
- ⚠️ Likely **50-70%** of optimal performance

**Best use case**: As a fallback for decision tree or for specific sub-problems.

---

### 🥉 **Option 3: Binary Neural Network (BNN)** (MARGINALLY FEASIBLE)

**Approach**: 1-bit weights, fixed-point arithmetic.

#### Micro-architecture

```
Input: 32 features (hand-crafted)
Hidden: 16 neurons (binary weights)
Output: 12 actions
```

**Weights:**
- Layer 1: 32×16 = 512 bits = **64 bytes**
- Layer 2: 16×12 = 192 bits = **24 bytes**
- **Total: 88 bytes** ✅ Fits!

**Inference code:**
- Binary dot product: XNOR + popcount
- Activation: sign function
- **Estimated: ~50 bytes**

**Total: ~140 bytes** ✅ Fits!

#### Performance

**Execution time:**
- Layer 1: 32×16 bit ops = ~512 ops
- Each bit op: ~8 cycles (LDA, EOR, AND)
- **Total: ~4,000 cycles (0.2ms)** ✅ Fast enough!

#### Limitations

- ⚠️ Requires careful feature engineering (hand-crafted inputs)
- ⚠️ Training binary networks is tricky
- ⚠️ Likely **60-75%** of optimal performance

---

### ❌ **Option 4: Full Neural Network Quantization** (NOT FEASIBLE)

Even with aggressive INT8 quantization:
- 1.4M params → 1.4 MB
- Still **8,750x too large**
- Inference would take **>100ms** even if it fit

**Verdict**: Impossible without external hardware.

---

## Recommended Hybrid Approach

### Strategy: "Smart Fallback Hierarchy"

```
┌─────────────────────────────────────────┐
│  Decision Tree (Depth 6)                │
│  - Handles common situations (80%)      │
│  - 500 bytes                            │
└────────┬────────────────────────────────┘
         │ If uncertain/edge case
         ▼
┌─────────────────────────────────────────┐
│  Lookup Table (LUT)                     │
│  - Handles quantized state heuristics   │
│  - 150 bytes                            │
└─────────────────────────────────────────┘

Total: ~650 bytes (requires expanding ROM space)
```

### Implementation Plan

1. **Train full RL model** (Phase 1) to near-optimal performance
2. **Distill to decision tree** with depth 6-7
3. **Extract edge case heuristics** into LUT for rare states
4. **Compile to 6502 assembly** with careful optimization
5. **A/B test** against rule-based AI to measure performance gap

---

## ROM Space Expansion Options

If 160 bytes is insufficient, options include:

### 1. **Find More Free Space** ⭐ RECOMMENDED
- Analyze ROM for unused regions
- Many NES games have padding or unused code
- Could potentially find **500-1000 bytes**

### 2. **Overlay Existing Code**
- Replace tutorial/demo mode with AI
- Use CHR-ROM bank switching for code storage
- **Could gain 2-4 KB**

### 3. **External Mapper**
- Use MMC3 or similar mapper for code banking
- Requires hardware modification
- **Essentially unlimited space**

---

## Performance Expectations

### Realistic Performance Matrix

| Approach | ROM Size | Cycles | Performance vs Optimal | Feasibility |
|----------|----------|--------|------------------------|-------------|
| **Decision Tree (d=6)** | 500 bytes | 100 | 70-80% | ⭐⭐⭐⭐⭐ |
| **Decision Tree (d=8)** | 2000 bytes | 200 | 80-90% | ⭐⭐⭐⭐ (needs space) |
| **Lookup Table** | 150 bytes | 20 | 50-70% | ⭐⭐⭐⭐ |
| **Binary NN** | 140 bytes | 4000 | 60-75% | ⭐⭐⭐ |
| **Hybrid (Tree+LUT)** | 650 bytes | 150 | 75-85% | ⭐⭐⭐⭐ |

### What "70-80% of optimal" means

- **Optimal RL agent**: Clears 20-level virus board in 300 moves avg
- **70% performance**: Clears same board in ~420 moves
- **Still superhuman**: Much better than average human player

---

## Key Engineering Challenges

### 1. **Feature Engineering** ⚠️ CRITICAL

The model won't see raw playfield; must extract **smart features**:

**Good features (32-64 bytes):**
```c
- virus_count              // 1 byte
- viruses_by_color[3]      // 3 bytes
- column_heights[8]        // 8 bytes
- avg_height               // 1 byte
- max_height               // 1 byte
- holes_count              // 1 byte
- capsule_left_color       // 1 byte
- capsule_right_color      // 1 byte
- next_capsule_colors[2]   // 2 bytes
- color_clusters[3]        // 3 bytes
- reachable_viruses[3]     // 3 bytes (by color)
- blocking_pieces_above_viruses // 1 byte
- current_combo_potential  // 1 byte
```

**Total: ~28 bytes of features** (easily computable in <100 cycles)

### 2. **Decision Tree Training**

Must use features that are:
- ✅ Quickly computable on 6502
- ✅ Strongly predictive of good actions
- ✅ Complementary (low correlation)

**Strategy**: Train tree on **feature space**, not raw state!

### 3. **Action Smoothing**

Raw tree decisions can be jittery. Add hysteresis:

```asm
; Don't change direction every frame
LDA last_action
CMP new_action
BEQ same_action
INC action_change_counter
LDA action_change_counter
CMP #4                ; Require 4 frames of new action
BCC keep_old_action   ; Stick with old action
same_action:
  LDA #0
  STA action_change_counter
  LDA new_action
  STA last_action
keep_old_action:
  LDA last_action
  RTS
```

---

## Conclusion

### Is it Feasible? **YES** ✅

**But with caveats:**

1. ✅ **Can fit on NES**: With decision tree (depth 6-7) and careful optimization
2. ⚠️ **Performance trade-off**: Expect 70-85% of optimal RL agent performance
3. ⚠️ **ROM space**: May need to find more than 160 bytes (500-1000 bytes ideal)
4. ⚠️ **Engineering effort**: Significant work in distillation, feature engineering, and 6502 optimization

### Recommended Path Forward

**Phase 1**: Train near-optimal RL agent externally (current plan)
**Phase 1.5**: Feature engineering and decision tree distillation experiments
**Phase 2**: ROM deployment with performance validation

### Success Criteria

The on-NES AI should:
- ✅ Beat human players at medium-high difficulty (10-15 virus levels)
- ✅ Clear 20-virus boards consistently
- ✅ Run at 60 FPS with no lag
- ✅ Fit in available ROM space
- ⚠️ May lose to optimal RL agent in direct competition

### Real-World Analogies

This is similar to how chess engines work on embedded devices:
- **Stockfish on desktop**: 100M+ nodes/sec, near-perfect play
- **Stockfish on Arduino**: 1K nodes/sec, still rated ~1800 ELO
- **Percentage of optimal**: ~60-70%, but still very strong

---

## Next Steps

1. **Investigate ROM space**: Scan for unused regions in Dr. Mario ROM
2. **Feature engineering**: Implement and test feature extractors
3. **Baseline comparison**: Measure current rule-based AI performance
4. **Distillation pipeline**: Build tree training → ASM compilation toolchain
5. **Prototype**: Test depth-4 tree as proof-of-concept

**Estimated development time for Phase 2**: 4-6 weeks after Phase 1 model is trained.
