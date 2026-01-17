# Multi-Agent Training Plan

## User Requirement
"btw remember u need 2 bots here one for both players. and they ideally would be training at different levels over time but most of the time at level 5 or higher"

## Current Status
- ❌ Auto-navigation not working (RAM writes don't affect controller input)
- ✅ Training infrastructure ready
- ✅ Custom CNN working
- ⏳ Need to implement 2-player multi-agent training

## Navigation Solution: Save State Approach

Since fully automated menu navigation requires controller injection (not available in MCP), use save states:

1. **One-time manual setup** (with display):
   - Launch Mednafen with display
   - Navigate to 2P VS mode
   - Select virus level (5-20)
   - Press START to begin game
   - Immediately save state: F5 key or Mednafen command
   - Copy save state file to training directory

2. **Automated training** (headless):
   - Mednafen loads from save state at launch
   - Starts directly in gameplay (both players at selected level)
   - No menu navigation needed

3. **Virus level variation**:
   - Create multiple save states (level 5, 10, 15, 20)
   - Training script randomly selects level on each episode reset
   - Curriculum learning: start at level 5, gradually increase

## Multi-Agent Architecture

### Option A: Single Environment, Two Agents (Recommended)

**Structure**:
```
DrMario2PEnv (Gymnasium)
    ├─ Observation space: Dict
    │   ├─ agent_p1: Box(16, 8, 12)  # P1 view
    │   └─ agent_p2: Box(16, 8, 12)  # P2 view
    ├─ Action space: Dict
    │   ├─ agent_p1: Discrete(9)
    │   └─ agent_p2: Discrete(9)
    └─ Reward: Dict
        ├─ agent_p1: float
        └─ agent_p2: float
```

**Training**:
- Use `MultiAgentEnv` wrapper or custom implementation
- Two PPO agents (P1 and P2) with separate networks
- Self-play: agents improve by competing against each other
- Shared replay buffer or separate buffers (configurable)

**Pros**:
- True competitive training (self-play)
- Agents learn to counter each other's strategies
- More realistic than vs CPU

**Cons**:
- More complex implementation
- Requires multi-agent RL library (RLlib or custom)

### Option B: Two Separate Environments (Simpler)

**Structure**:
```
DrMarioEnv(player_id=1)  # P1 agent
DrMarioEnv(player_id=2)  # P2 agent
```

**Training**:
- Two independent PPO agents
- Each sees only their own side
- Train sequentially or in parallel
- No direct interaction between agents

**Pros**:
- Simpler implementation (reuse existing code)
- Can train independently
- Easier to debug

**Cons**:
- No self-play (miss competitive dynamics)
- Not as efficient

### Recommendation: Start with Option B, Migrate to Option A

1. **Phase 1** (immediate): Get save state working, train single agent
2. **Phase 2** (after 1M timesteps): Duplicate env for P1 and P2
3. **Phase 3** (future): Implement full multi-agent with self-play

## Implementation Steps

### Step 1: Save State Setup (Manual, One-Time)

```bash
# On local machine with display
mednafen drmario_vs_cpu.nes

# In game:
# 1. Navigate to 2P VS mode
# 2. Select level 10, speed MED
# 3. Press START
# 4. Immediately press F5 (quick save)
# 5. Mednafen saves to ~/.mednafen/mcs/drmario_vs_cpu.nes.0.mc

# Copy save state to training dir
cp ~/.mednafen/mcs/drmario_vs_cpu.nes.0.mc rl-training-new/save_states/level_10.mcs
```

### Step 2: Modify MednafenManager to Load Save State

```python
def launch(self, save_state_path: Optional[str] = None):
    """Launch Mednafen, optionally from save state."""
    if save_state_path:
        cmd = ["xvfb-run", "-a", "mednafen",
               "-loadstate", save_state_path,
               str(self.rom_path)]
    else:
        cmd = ["xvfb-run", "-a", "mednafen", str(self.rom_path)]

    # ... rest of launch code
```

### Step 3: Create Multi-Agent Environment

**File**: `src/drmario_2p_env.py`

```python
class DrMario2PEnv(gym.Env):
    """
    2-player Dr. Mario environment for multi-agent training.

    Both P1 and P2 are controlled by RL agents.
    """

    def __init__(self, level: int = 10):
        self.level = level
        self.save_state_path = f"save_states/level_{level}.mcs"

        # Two agents
        self.observation_space = spaces.Dict({
            "agent_p1": spaces.Box(0, 1, (16, 8, 12), np.float32),
            "agent_p2": spaces.Box(0, 1, (16, 8, 12), np.float32),
        })

        self.action_space = spaces.Dict({
            "agent_p1": spaces.Discrete(9),
            "agent_p2": spaces.Discrete(9),
        })

    def reset(self):
        # Reload save state
        self.mesen.load_save_state(self.save_state_path)

        # Get initial observations
        state = self.mesen.get_game_state()
        obs = {
            "agent_p1": self.encoder_p1.encode(state),
            "agent_p2": self.encoder_p2.encode(state),
        }
        return obs

    def step(self, actions):
        # actions = {"agent_p1": 3, "agent_p2": 1}

        # Send both controller inputs
        self.mesen.write_memory(0xF5, [self.ACTIONS[actions["agent_p1"]]])
        self.mesen.write_memory(0xF6, [self.ACTIONS[actions["agent_p2"]]])

        # Step frame
        self.mesen.step_frame()

        # Get rewards for both
        state = self.mesen.get_game_state()
        rewards = {
            "agent_p1": self.reward_calc.calculate(state, player=1),
            "agent_p2": self.reward_calc.calculate(state, player=2),
        }

        # Check done
        done = {
            "agent_p1": state['p1_topped_out'],
            "agent_p2": state['p2_topped_out'],
            "__all__": state['game_over'],
        }

        obs = {
            "agent_p1": self.encoder_p1.encode(state),
            "agent_p2": self.encoder_p2.encode(state),
        }

        return obs, rewards, done, {}
```

### Step 4: Training Script for Multi-Agent

**File**: `scripts/train_2p.py`

```python
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.env.multi_agent_env import MultiAgentEnv

# Or use stable-baselines3 with custom wrapper

def train_multiagent():
    config = {
        "env": DrMario2PEnv,
        "multiagent": {
            "policies": {
                "agent_p1": (None, obs_space, act_space, {}),
                "agent_p2": (None, obs_space, act_space, {}),
            },
            "policy_mapping_fn": lambda agent_id: agent_id,
        },
    }

    trainer = PPOTrainer(config=config)

    for i in range(1000):
        result = trainer.train()
        print(f"Iteration {i}: P1 reward={result['policy_reward_mean']['agent_p1']}, "
              f"P2 reward={result['policy_reward_mean']['agent_p2']}")
```

## Next Steps

1. ✅ Document this plan
2. ⏳ Create save state (manual, one-time, with display)
3. ⏳ Implement save state loading in MednafenManager
4. ⏳ Test: launch from save state → should start in gameplay
5. ⏳ Train single agent (P2) to verify it works
6. ⏳ Implement multi-agent environment
7. ⏳ Train both agents with self-play

## Virus Level Curriculum

Start easy, gradually increase difficulty:

| Phase | Timesteps | Virus Level | Description |
|-------|-----------|-------------|-------------|
| 1 | 0-200K | 5 | Learn basic mechanics |
| 2 | 200K-400K | 10 | Increase difficulty |
| 3 | 400K-600K | 15 | Advanced patterns |
| 4 | 600K-1M | 20 | Expert level |
| 5 | 1M+ | Mix (5-20) | Generalization |

**Implementation**:
```python
def get_level_for_timestep(timestep):
    if timestep < 200000:
        return 5
    elif timestep < 400000:
        return 10
    elif timestep < 600000:
        return 15
    elif timestep < 1000000:
        return 20
    else:
        return random.choice([5, 10, 15, 20])  # Mix for robustness
```

## Save State File Management

```
save_states/
├── level_05.mcs  # 5 viruses, speed LOW
├── level_10.mcs  # 10 viruses, speed MED
├── level_15.mcs  # 15 viruses, speed MED
└── level_20.mcs  # 20 viruses, speed HI
```

Create all 4 during initial manual setup.

---

**Status**: Plan documented, ready to implement save state approach.
