# Mednafen Setup for RL Training

## Quick Start

The RL training uses Mednafen via MCP tools for memory access and control.

### 1. Launch Mednafen (use MCP tools in Claude Code)

In Claude Code, use the MCP launch tool:
```
Launch Mednafen with vs_cpu mode headless
```

Or manually:
```bash
xvfb-run -a mednafen /path/to/drmario_vs_cpu.nes &
```

### 2. Verify Connection

Check that Mednafen is running and MCP can connect:
```bash
pgrep mednafen  # Should show PID
```

In Claude Code, test MCP connection:
```
Connect to Mednafen and get game state
```

### 3. Run Validation

```bash
cd rl-training-new
uv run python tests/test_env_validation.py
```

### 4. Start Training

```bash
uv run python scripts/train.py --timesteps 1000000 --device cuda
```

## Architecture

```
PPO Agent (Python)
    ↓
DrMarioEnv (Gymnasium)
    ↓
MednafenInterface (mednafen_interface_mcp.py)
    ↓
MednafenMCP Controller (mednafen-mcp/mcp_server.py)
    ↓
/proc/PID/mem (Direct Memory Access)
    ↓
Mednafen Process (NES Emulator)
```

## Known Issues

### Issue: "NES RAM not found"

**Cause**: RAM discovery looks for virus patterns in memory. At title screen, no viruses exist.

**Solution 1** (via Claude Code MCP):
- Use MCP `launch` tool with `mode=vs_cpu`
- Automatically discovers RAM during launch

**Solution 2** (manual):
1. Start Mednafen: `xvfb-run -a mednafen ROM &`
2. Wait 5 seconds for initialization
3. Use MCP `find_ram` tool to discover RAM
4. If not found, game might need to be in active gameplay

**Solution 3** (controller inputs):
```bash
# Send START, SELECT SELECT, START to navigate to VS CPU gameplay
python3 scripts/start_game.py
```

### Issue: Interface creates new MCP controller

**Cause**: Each `MednafenInterface()` creates a NEW `MednafenMCP()` object without shared RAM base.

**Workaround**: Use MCP launch tool first, which sets up persistent RAM discovery.

**Better fix** (TODO): Make `MednafenInterface` use singleton MCP controller or accept it as parameter.

## Testing RAM Discovery

```python
# In Claude Code, use MCP tools:
from mcp__mednafen import connect, find_ram, game_state

# Connect
result = connect()
print(result)  # Should show PID and RAM base

# Get state
state = game_state()
print(state['player2']['virus_count'])  # Should show viruses if in gameplay
```

## Headless Operation

Mednafen headless modes:

1. **Xvfb** (WORKS): `xvfb-run -a mednafen ROM`
   - Virtual framebuffer
   - Full emulation
   - RAM discovery works

2. **SDL dummy** (DOESN'T WORK): `SDL_VIDEODRIVER=dummy mednafen ROM`
   - Frame counter stays at 0
   - Game doesn't progress
   - Don't use for training!

Always use **Xvfb** for headless training.

## Training Workflow

```bash
# Terminal 1: Monitor logs
tail -f logs/training.log

# Terminal 2: TensorBoard
tensorboard --logdir logs/tensorboard

# Terminal 3: Training (via Claude Code or manually)
# 1. Launch Mednafen via MCP
# 2. Run validation
# 3. Start training
```
