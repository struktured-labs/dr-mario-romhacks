# Dr. Mario RL Training with Mesen

This directory contains the infrastructure for training a reinforcement learning agent to play Dr. Mario, then distilling it to a decision tree that fits in NES ROM.

## Architecture

```
┌─────────────┐    Socket    ┌──────────────┐    Lua API    ┌───────┐
│   Python    │◄────────────►│  Lua Script  │◄─────────────►│ Mesen │
│  RL Trainer │              │  (Bridge)    │               │  Core │
└─────────────┘              └──────────────┘               └───────┘
```

## Components

### 1. Mesen Emulator (`../mesen2/`)
- Multi-system emulator with excellent NES accuracy
- Built from source as git submodule
- Lua API for memory access and control

### 2. Lua Bridge (`lua/mesen_bridge.lua`)
Socket server that exposes Mesen's Lua API via TCP:
- **READ <addr> <size>**: Read NES memory
- **WRITE <addr> <hex>**: Write NES memory
- **STEP <frames>**: Step forward N frames
- **GET_STATE**: Get full Dr. Mario game state
- **QUIT**: Close connection

Runs inside Mesen's Lua script environment.

### 3. Python Client (`src/mesen_interface.py`)
Python interface to the Lua bridge:
```python
from mesen_interface import MesenInterface

with MesenInterface() as interface:
    # Read memory
    virus_count = interface.read_memory(0x03A4, 1)[0]

    # Write controller input
    interface.write_memory(0x00F6, [0x01])  # Press RIGHT

    # Step frames
    interface.step_frame()

    # Get full game state
    state = interface.get_game_state()
    print(f"Capsule at ({state['capsule_x']}, {state['capsule_y']})")
```

## Setup

### Prerequisites
- Mesen2 compiled (see `../mesen2/`)
- Dr. Mario ROM (`drmario_vs_cpu.nes`)
- Python 3.8+
- uv (for Python package management)

### Installation

1. **Compile Mesen** (if not already done):
   ```bash
   cd ../mesen2
   export PATH="$HOME/.dotnet:$PATH"
   make -j$(nproc)
   ```

2. **Install Python dependencies**:
   ```bash
   cd rl-training-new
   uv pip install -r requirements.txt
   ```

3. **Run integration test**:
   ```bash
   ./tests/test_mesen_integration.py
   ```

## Testing

### Manual Test

1. Launch Mesen with Dr. Mario ROM:
   ```bash
   ../run_mesen.sh ../drmario_vs_cpu.nes
   ```

2. In Mesen:
   - Tools → Script Window
   - Load Script → `lua/mesen_bridge.lua`
   - Start game (F11)

3. In another terminal, run Python test:
   ```python
   python src/mesen_interface.py
   ```

### Automated Test

```bash
./tests/test_mesen_integration.py
```

## Next Steps

### Phase 1: MCP Python AI (Oracle)
Build the "oracle" AI with unlimited computation:
- Full heuristics (pathfinding, rotation, height awareness)
- No ROM constraints
- Used for reward function design and baseline performance

**Status**: TODO

### Phase 2: RL Training (PPO on 3090 GPU)
Train reinforcement learning agent:
- Stable-Baselines3 PPO
- 12-channel CNN observation encoding
- Reward: virus clears + height penalty - time
- Train for ~1M episodes on 3090 GPU (1-4 days)

**Status**: TODO

### Phase 3: Distillation to Decision Tree
Compress trained policy:
- Collect 100K (state, action) pairs from trained model
- Train sklearn DecisionTreeClassifier (max_depth=6)
- Target: ~500 bytes, 70-80% of NN performance

**Status**: TODO

### Phase 4: Compile to 6502 Assembly
Generate NES-compatible code:
- Parse decision tree structure
- Generate CMP + branch instructions
- Calculate branch offsets

**Status**: TODO

### Phase 5: Embed in ROM
Expand Dr. Mario ROM and embed decision tree:
- Find unused ROM space OR use CHR-ROM banking OR upgrade mapper
- Hook controller input to decision tree routine
- Test in emulator and on real hardware

**Status**: TODO

## Memory Map (Dr. Mario)

| Address | Description |
|---------|-------------|
| `$00F5` | P1 controller input (new) |
| `$00F6` | P2 controller input (new) |
| `$0046` | Game mode (< 4 = menu, >= 4 = gameplay) |
| `$0381` | P2 left capsule color (0=yellow, 1=red, 2=blue) |
| `$0382` | P2 right capsule color |
| `$0385` | P2 capsule X position (0-7) |
| `$0386` | P2 capsule Y position (0-15) |
| `$03A4` | P2 virus count |
| `$0400-$047F` | P1 playfield (8×16 = 128 bytes) |
| `$0500-$057F` | P2 playfield (8×16 = 128 bytes) |

Tile values:
- `$FF`: Empty
- `$D0`: Yellow virus
- `$D1`: Red virus
- `$D2`: Blue virus
- `$4C-$5B`: Capsule halves

## Troubleshooting

### "Connection refused" when running Python client
- Make sure Mesen is running
- Make sure Lua script is loaded (Tools → Script Window)
- Make sure game is started (F11)
- Check Lua script output in Script Window for errors

### "Client disconnected" in Lua script
- Python client may have crashed
- Check Python traceback for errors
- Ensure memory addresses are valid

### Mesen crashes on startup
- May need display (GUI mode)
- Try running with Xvfb for headless: `xvfb-run -a ./run_mesen.sh ROM.nes`

## Resources

- [Mesen Documentation](https://www.mesen.ca/docs/)
- [Mesen Lua API Reference](https://www.mesen.ca/docs/apireference.html)
- [Plan File](../.claude/plans/typed-beaming-blossom.md)
- [Emulator Research](../.claude/plans/emulator-research.md)
- [Implementation Plan](../.claude/plans/revised-implementation.md)
