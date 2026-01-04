# Dr. Mario Deep RL Training

Train reinforcement learning agents to play Dr. Mario optimally using self-play.

## Overview

This system trains two RL agents that play Dr. Mario against each other using Mednafen emulator in headless mode. The trained neural network models run externally during training, with future plans to compress them onto NES hardware.

## Architecture

- **Emulator**: Mednafen (headless mode via debugger interface)
- **RL Framework**: Stable-Baselines3 (PPO algorithm)
- **State Representation**: 12-channel image (8×16×12) for CNN policy
- **Action Space**: 12 discrete actions (movement + rotation combos)
- **Training Strategy**: Self-play with opponent pool

## Project Structure

```
rl-training/
├── README.md                    # This file
├── RL_TRAINING_PLAN.md          # Detailed design document
├── requirements.txt             # Python dependencies
├── config/                      # Configuration files
├── src/                         # Core library code
│   ├── memory_map.py           # NES memory addresses
│   ├── mednafen_interface.py   # Emulator control
│   ├── drmario_env.py          # Gymnasium environment
│   ├── state_encoder.py        # State → NN input encoding
│   └── reward_function.py      # Reward calculation
├── scripts/                     # Training scripts
│   ├── train.py                # Main training script
│   └── watch.py                # Visualize trained agent
├── models/                      # Saved model weights
│   └── checkpoints/            # Training checkpoints
├── logs/                        # Training logs
│   └── tensorboard/            # TensorBoard logs
└── tests/                       # Unit tests
```

## Installation

1. **Install Mednafen**:
   ```bash
   # Ubuntu/Debian
   sudo apt install mednafen

   # macOS
   brew install mednafen
   ```

2. **Install Python dependencies**:
   ```bash
   cd rl-training
   pip install -r requirements.txt
   ```

3. **Verify ROM file**:
   Ensure `drmario.nes` is in the parent directory.

## Quick Start

### 1. Train an Agent

```bash
python scripts/train.py --timesteps 1000000 --num-envs 4
```

Options:
- `--rom PATH`: Path to Dr. Mario ROM (default: `../drmario.nes`)
- `--timesteps N`: Total training steps (default: 1,000,000)
- `--num-envs N`: Parallel environments (default: 4)
- `--lr RATE`: Learning rate (default: 3e-4)
- `--save-freq N`: Save checkpoint every N steps (default: 10,000)

### 2. Watch Trained Agent

```bash
python scripts/watch.py models/drmario_ppo_final.zip --episodes 10
```

### 3. Monitor Training

```bash
tensorboard --logdir logs/tensorboard/
```

Open http://localhost:6006 in your browser.

## Implementation Status

**Phase 1: External RL Training** ⚠️ IN PROGRESS

- [x] Project structure created
- [x] Memory map defined
- [x] Skeleton code written
- [ ] Mednafen integration implemented
- [ ] Environment tested
- [ ] Initial training run
- [ ] Self-play implementation
- [ ] Hyperparameter tuning

**Phase 2: On-NES Deployment** 📅 PLANNED

- [ ] Model distillation to decision tree
- [ ] Compile to 6502 assembly
- [ ] Fit into ROM space (~160 bytes)

## Current Limitations

1. **Mednafen Interface**: Debugger protocol not yet implemented
   - Need to investigate Mednafen's actual debugger capabilities
   - May fall back to save state manipulation approach

2. **Memory Addresses**: Some P2 addresses are inferred and need verification
   - P2_CAPSULE_ROTATION (0x0125) - unverified
   - BTN_DOWN mapping - needs testing

3. **Reward Function**: Basic implementation, needs tuning
   - Combo detection not implemented
   - Top-out detection incomplete

## Next Steps

See `RL_TRAINING_PLAN.md` for detailed implementation roadmap.

**Immediate priorities**:
1. Implement Mednafen debugger interface
2. Test memory read/write functionality
3. Verify controller injection works
4. Run first training episode

## References

- [RL_TRAINING_PLAN.md](RL_TRAINING_PLAN.md) - Comprehensive design document
- [VS_CPU_PLAN.md](../VS_CPU_PLAN.md) - Memory mapping research
- [Stable-Baselines3 Docs](https://stable-baselines3.readthedocs.io/)
- [Mednafen Docs](https://mednafen.github.io/documentation/)

## Contributing

This is a research project for training optimal Dr. Mario strategies.

## License

Same as parent project.
