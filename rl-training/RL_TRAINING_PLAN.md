# Dr. Mario Deep RL Training System

## Overview
Train two RL agents to play Dr. Mario optimally through self-play using Mednafen headless mode. The trained models will run externally during training (Phase 1), with future work to fit them onto NES hardware (Phase 2).

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Training Controller                    │
│  - Manages self-play episodes                           │
│  - Coordinates both agents                              │
│  - Collects training data                               │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
        ┌──────▼──────┐           ┌──────▼──────┐
        │  RL Agent 1 │           │  RL Agent 2 │
        │  (Player 1) │           │  (Player 2) │
        └──────┬──────┘           └──────┬──────┘
               │                          │
               │  actions                 │  actions
               │  ┌───────────────────┐  │
               └──►  state ◄──┐       ├──┘
                  │           │       │
                  │  Mednafen │       │
                  │  Headless │       │
                  │  Debugger │       │
                  │  Interface│       │
                  └───────────┘       │
                         │            │
                    Dr. Mario ROM     │
                         └────────────┘
                         read memory
```

## Phase 1: External RL Training

### 1. Mednafen Integration

**Why Mednafen over nes-py:**
- Mednafen has powerful debugger capabilities
- Can inject memory writes via debugger interface
- Better accuracy and timing control
- Supports headless rendering

**Mednafen Debugger Interface:**
Mednafen supports a built-in debugger that can be accessed via:
- Command-line debugger (interactive mode)
- Remote debugger protocol (for automation)
- Memory read/write through debugger commands

**Options for Integration:**

1. **Mednafen Server Mode (Recommended)**
   - Use Mednafen's network debugger server
   - Python client connects via socket
   - Send memory read/write commands
   - Fast, low-latency communication

2. **Lua Scripting (Alternative)**
   - Check if Mednafen supports Lua hooks
   - Similar to FCEUX cpu_vs_cpu.lua approach
   - May have limited functionality

3. **Save State Manipulation**
   - Read save states as binary files
   - Parse memory state
   - Modify and reload
   - Slower but reliable fallback

**Implementation Strategy:**
Start with approach #1 (network debugger), fall back to #3 if needed.

### 2. State Representation

**Raw Memory State (from VS_CPU_PLAN.md):**

```python
# Player 1 State
P1_PLAYFIELD = 0x0400  # 8x16 grid = 128 bytes
P1_CAPSULE_LEFT_COLOR = 0x0301  # 0=Yellow, 1=Red, 2=Blue
P1_CAPSULE_RIGHT_COLOR = 0x0302
P1_CAPSULE_X = 0x0305  # 0-7
P1_CAPSULE_Y = 0x0306  # 0-15
P1_ROTATION = 0x00A5  # 0-3
P1_DROP_TIMER = 0x0312
P1_NEXT_COLORS = (0x031A, 0x031B)
P1_VIRUS_COUNT = 0x0324

# Player 2 State (+$80 or +$100 offset)
P2_PLAYFIELD = 0x0500  # 8x16 grid = 128 bytes
P2_CAPSULE_LEFT_COLOR = 0x0381
P2_CAPSULE_RIGHT_COLOR = 0x0382
P2_CAPSULE_X = 0x0385
P2_CAPSULE_Y = 0x0386
P2_ROTATION = 0x0125  # (inferred)
P2_NEXT_COLORS = (0x039A, 0x039B)
P2_VIRUS_COUNT = 0x03A4

# Tile encoding:
# 0xFF = Empty
# 0xD0-0xD2 = Virus (Yellow/Red/Blue)
# 0x40-0x72 = Pill half
# 0x80-0x82 = Pellet
```

**Neural Network Input Encoding:**

Option A: **Multi-channel Image-like Representation** (CNN-friendly)
```python
state_shape = (C, H, W) = (12, 16, 8)

Channels:
  P1 Playfield:
    0: Empty cells (binary)
    1: Yellow pieces (virus/pill)
    2: Red pieces
    3: Blue pieces
  P1 Current Capsule:
    4: Capsule position (binary mask)
    5: Capsule orientation encoding
  P2 Playfield:
    6: Empty cells
    7: Yellow pieces
    8: Red pieces
    9: Blue pieces
  P2 Current Capsule:
    10: Capsule position
    11: Capsule orientation

Additional features (vector):
  - P1/P2 virus counts (normalized)
  - Next capsule colors (one-hot)
  - Drop timer
  - Height metrics per column
```

Option B: **Compact Flat Representation** (MLP-friendly)
```python
# Flattened playfield + metadata
P1_playfield: 128 bytes (one-hot encoded → 128*4)
P2_playfield: 128 bytes (one-hot encoded → 128*4)
P1_capsule: [x, y, rot, color1, color2] → 9 dims
P2_capsule: [x, y, rot, color1, color2] → 9 dims
P1_next: 6 dims (one-hot colors)
P2_next: 6 dims
Virus_counts: 2 dims
Total: ~1050 dimensions
```

**Recommendation:** Start with Option A (CNN) as it preserves spatial structure.

### 3. Action Space

**Dr. Mario Button Mapping (from VS_CPU_PLAN.md):**
```python
# $F5 = Player 1, $F6 = Player 2
RIGHT = 0x01
LEFT = 0x02
SELECT = 0x04
START = 0x08
DOWN = 0x10  # (or 0x20, needs verification)
A_ROTATE_CW = 0x40
B_ROTATE_CCW = 0x80
```

**Discrete Action Space:**
```python
actions = [
    0: NOOP
    1: LEFT
    2: RIGHT
    3: DOWN (soft drop)
    4: A (rotate clockwise)
    5: B (rotate counter-clockwise)
    6: LEFT + A
    7: RIGHT + A
    8: LEFT + B
    9: RIGHT + B
    10: DOWN + LEFT
    11: DOWN + RIGHT
]
# Total: 12 discrete actions
```

**Alternative: Continuous/Multi-discrete:**
- Could use multi-discrete([3, 2, 2]) for [DPAD, Rotate, Drop]
- Start with discrete for simplicity

### 4. Reward Function

**Objective:** Maximize virus elimination while surviving longer than opponent.

```python
def calculate_reward(prev_state, current_state, done, winner):
    reward = 0.0

    # 1. Virus elimination (primary goal)
    virus_eliminated = prev_state.virus_count - current_state.virus_count
    reward += virus_eliminated * 100.0

    # 2. Survival bonus (per frame)
    reward += 0.1

    # 3. Height penalty (encourage keeping field low)
    avg_height = calculate_average_column_height(current_state.playfield)
    reward -= avg_height * 0.5

    # 4. Efficient placement (reward making matches)
    pills_cleared = count_cleared_pills(prev_state, current_state)
    reward += pills_cleared * 5.0

    # 5. Combo/chain bonus
    if current_state.combo_count > 1:
        reward += current_state.combo_count * 20.0

    # 6. Win/loss terminal rewards
    if done:
        if winner == "self":
            reward += 1000.0
        elif winner == "opponent":
            reward -= 500.0
        else:  # draw
            reward += 0.0

    # 7. Death penalty (topping out)
    if current_state.topped_out:
        reward -= 1000.0

    return reward
```

**Reward Shaping Considerations:**
- Tune coefficients through experimentation
- Consider opponent-relative rewards (virus differential)
- Add exploration bonuses early in training
- Curriculum learning: start with easy virus levels

### 5. RL Algorithm Selection

**Recommended: PPO (Proximal Policy Optimization)**

Pros:
- Stable training
- Works well with discrete actions
- Handles partial observability
- Industry standard for game AI

**Alternative Options:**
- DQN/Rainbow: Good for discrete actions, but less stable
- A3C/IMPALA: Distributed training, more complex
- MuZero: State-of-the-art but requires much more compute

**Implementation:**
Use Stable-Baselines3 (SB3) for PPO:
```python
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv

model = PPO(
    "CnnPolicy",  # or "MlpPolicy"
    env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    verbose=1,
    tensorboard_log="./logs/"
)
```

### 6. Self-Play Training Loop

**Self-Play Strategy:**

```python
class SelfPlayTraining:
    def __init__(self):
        self.agent_current = PPO(...)  # Current agent
        self.agent_opponent = None     # Historical opponent
        self.opponent_pool = []        # Pool of past agents

    def train_episode(self):
        # 1. Select opponent from pool (or use current agent)
        opponent = self.select_opponent()

        # 2. Run episode with both agents
        obs = env.reset()
        done = False

        while not done:
            # Agent 1 (current) chooses action
            action1 = self.agent_current.predict(obs[0])

            # Agent 2 (opponent) chooses action
            action2 = opponent.predict(obs[1])

            # Step environment
            obs, rewards, done, info = env.step([action1, action2])

            # Store transitions for both agents
            self.agent_current.store_transition(...)

        # 3. Update current agent
        self.agent_current.train()

        # 4. Periodically save to opponent pool
        if episode % 100 == 0:
            self.opponent_pool.append(self.agent_current.copy())

    def select_opponent(self):
        # Strategy: mix of current agent and historical agents
        if random.random() < 0.8:
            return self.agent_current  # Self-play
        else:
            return random.choice(self.opponent_pool)  # Past version
```

**Opponent Pool Strategy:**
- Keep snapshots every N episodes
- Optionally keep only "diverse" opponents (different playstyles)
- Prevents overfitting to current policy

### 7. Training Infrastructure

**File Structure:**
```
rl-training/
├── RL_TRAINING_PLAN.md          # This document
├── requirements.txt              # Python dependencies
├── config/
│   └── ppo_config.yaml          # Hyperparameters
├── src/
│   ├── __init__.py
│   ├── mednafen_interface.py    # Mednafen debugger client
│   ├── drmario_env.py           # Gym environment wrapper
│   ├── state_encoder.py         # Raw memory → NN input
│   ├── reward_function.py       # Reward calculation
│   ├── memory_map.py            # Memory address constants
│   └── self_play.py             # Self-play training loop
├── models/
│   └── checkpoints/             # Saved model weights
├── logs/
│   └── tensorboard/             # Training metrics
├── scripts/
│   ├── train.py                 # Main training script
│   ├── evaluate.py              # Evaluation/testing
│   └── watch.py                 # Render agent gameplay
└── tests/
    ├── test_mednafen.py         # Integration tests
    └── test_env.py              # Environment tests
```

**Dependencies:**
```txt
# requirements.txt
torch>=2.0.0
stable-baselines3>=2.0.0
gymnasium>=0.29.0
numpy>=1.24.0
tensorboard>=2.14.0
pyyaml>=6.0
```

### 8. Mednafen Headless Interface Design

**Core Interface Class:**
```python
class MednafenDebugger:
    """Interface to Mednafen headless emulator via debugger protocol"""

    def __init__(self, rom_path: str, headless: bool = True):
        self.rom_path = rom_path
        self.process = None
        self.socket = None

    def start(self):
        """Launch Mednafen in debugger mode"""
        # Launch: mednafen -debugger.autostart 1 -debugger.server 1 rom.nes
        pass

    def read_memory(self, address: int, length: int = 1) -> bytes:
        """Read NES CPU memory via debugger"""
        # Send: "read <address> <length>"
        pass

    def write_memory(self, address: int, value: int):
        """Write to NES CPU memory (for controller injection)"""
        # Send: "write <address> <value>"
        pass

    def step_frame(self):
        """Advance emulation by 1 frame"""
        pass

    def reset(self):
        """Reset emulator to initial state"""
        pass

    def save_state(self, slot: int = 0):
        """Save current state"""
        pass

    def load_state(self, slot: int = 0):
        """Load saved state"""
        pass
```

**Alternative: Process-based Control**
If network debugger is not available:
```python
class MednafenHeadless:
    """Control Mednafen via save state manipulation"""

    def step(self, action: int):
        # 1. Load current state
        state = self.load_state_file()

        # 2. Inject controller input ($F5 or $F6)
        state.memory[0xF5] = action  # P1

        # 3. Save modified state
        self.save_state_file(state)

        # 4. Run emulator for 1 frame
        subprocess.run(["mednafen", "--frames", "1", ...])

        # 5. Load new state and read memory
        new_state = self.load_state_file()
        return self.extract_observation(new_state)
```

### 9. Gym Environment Wrapper

```python
import gymnasium as gym
from gymnasium import spaces

class DrMarioEnv(gym.Env):
    """Gym environment for Dr. Mario via Mednafen"""

    metadata = {'render_modes': ['rgb_array', 'human']}

    def __init__(self, player_id: int = 1, opponent=None):
        super().__init__()

        self.mednafen = MednafenDebugger("drmario.nes")
        self.player_id = player_id
        self.opponent = opponent  # For self-play

        # Action space: 12 discrete actions
        self.action_space = spaces.Discrete(12)

        # Observation space: 12-channel 16x8 image
        self.observation_space = spaces.Box(
            low=0, high=1,
            shape=(12, 16, 8),
            dtype=np.float32
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Reset emulator
        self.mednafen.reset()

        # Navigate menus to 2P mode
        self._navigate_to_game()

        # Read initial state
        obs = self._get_observation()
        info = {}

        return obs, info

    def step(self, action):
        # 1. Convert action to button mask
        buttons = self._action_to_buttons(action)

        # 2. If opponent exists, get their action
        if self.opponent:
            opp_action = self.opponent.predict(self._get_opponent_obs())
            opp_buttons = self._action_to_buttons(opp_action)
        else:
            opp_buttons = 0x00  # No input

        # 3. Inject both controllers
        if self.player_id == 1:
            self.mednafen.write_memory(0xF5, buttons)
            self.mednafen.write_memory(0xF6, opp_buttons)
        else:
            self.mednafen.write_memory(0xF5, opp_buttons)
            self.mednafen.write_memory(0xF6, buttons)

        # 4. Step emulator
        self.mednafen.step_frame()

        # 5. Read new state
        obs = self._get_observation()
        reward = self._calculate_reward()
        terminated = self._check_game_over()
        truncated = False
        info = self._get_info()

        return obs, reward, terminated, truncated, info

    def _get_observation(self):
        """Read memory and encode as neural network input"""
        # Read playfield
        if self.player_id == 1:
            playfield_addr = 0x0400
            capsule_x_addr = 0x0305
            # ... etc
        else:
            playfield_addr = 0x0500
            capsule_x_addr = 0x0385

        playfield = self.mednafen.read_memory(playfield_addr, 128)
        # Encode to multi-channel representation
        return encode_state(playfield, ...)

    def _navigate_to_game(self):
        """Auto-navigate menus to start 2P game"""
        # Replicate headless_test.py menu navigation
        pass
```

### 10. Training Script

```python
# scripts/train.py

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from src.drmario_env import DrMarioEnv
from src.self_play import SelfPlayCallback

def make_env(rank):
    def _init():
        env = DrMarioEnv(player_id=1)
        return env
    return _init

if __name__ == "__main__":
    # Create vectorized environment (multiple parallel instances)
    num_envs = 4
    env = SubprocVecEnv([make_env(i) for i in range(num_envs)])

    # Create PPO agent
    model = PPO(
        "CnnPolicy",
        env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        verbose=1,
        tensorboard_log="./logs/tensorboard/"
    )

    # Self-play callback
    self_play_callback = SelfPlayCallback(
        save_freq=10000,
        opponent_pool_size=10
    )

    # Train
    model.learn(
        total_timesteps=10_000_000,
        callback=self_play_callback
    )

    # Save final model
    model.save("models/drmario_ppo_final")
```

### 11. Evaluation & Monitoring

**Metrics to Track:**
- Win rate (vs. random, vs. rule-based, vs. self)
- Average viruses cleared per game
- Average game length (survival time)
- Episode rewards
- Policy entropy (exploration)
- Value function loss

**TensorBoard Integration:**
```bash
# Automatically logged by SB3
uv run tensorboard --logdir ./logs/tensorboard/
```

**Watch Trained Agent:**
```python
# scripts/watch.py
from src.drmario_env import DrMarioEnv
from stable_baselines3 import PPO

model = PPO.load("models/drmario_ppo_final")
env = DrMarioEnv(player_id=1)

obs, _ = env.reset()
for _ in range(10000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    env.render()  # Optional: enable Mednafen GUI
    if done:
        obs, _ = env.reset()
```

## Next Steps (Implementation Order)

1. **Setup Infrastructure** (Week 1)
   - [ ] Create folder structure
   - [ ] Install dependencies
   - [ ] Test Mednafen headless mode manually

2. **Mednafen Integration** (Week 1-2)
   - [ ] Implement MednafenDebugger class
   - [ ] Test memory read/write
   - [ ] Verify controller injection works
   - [ ] Test menu navigation automation

3. **Environment Implementation** (Week 2-3)
   - [ ] Implement DrMarioEnv
   - [ ] Implement state encoder (memory → CNN input)
   - [ ] Implement action mapping
   - [ ] Test environment manually

4. **Reward Function** (Week 3)
   - [ ] Implement basic reward function
   - [ ] Test reward signal quality
   - [ ] Tune reward coefficients

5. **Training Setup** (Week 3-4)
   - [ ] Implement training script
   - [ ] Setup TensorBoard logging
   - [ ] Test with random policy
   - [ ] Debug any issues

6. **Initial Training** (Week 4-6)
   - [ ] Train baseline agent (vs. random opponent)
   - [ ] Evaluate performance
   - [ ] Iterate on hyperparameters

7. **Self-Play** (Week 6-8)
   - [ ] Implement self-play training loop
   - [ ] Implement opponent pool management
   - [ ] Train with self-play
   - [ ] Evaluate vs. rule-based AI

8. **Optimization** (Week 8+)
   - [ ] Hyperparameter tuning
   - [ ] Reward shaping refinement
   - [ ] Curriculum learning (easy → hard virus levels)
   - [ ] Multi-agent training strategies

## Phase 2: On-NES Deployment (Future)

**Challenges:**
- NES has 2KB RAM, minimal compute
- No floating point operations
- Must fit model in ROM space (~160 bytes available)

**Approaches:**
1. **Lookup Table Distillation**
   - Pre-compute optimal actions for common states
   - Use hash function to map state → action
   - Store in ROM lookup table

2. **Decision Tree Distillation**
   - Train decision tree to mimic neural network
   - Compile tree to 6502 assembly
   - Much smaller than full NN

3. **Extreme Quantization**
   - 1-bit weights (binary neural network)
   - Fixed-point arithmetic
   - Tiny MLP (8-16-8 architecture)

4. **Rule Extraction**
   - Analyze trained model behavior
   - Extract human-interpretable rules
   - Implement rules in assembly

**Recommendation:** Start with approach #2 (decision tree), as it's most feasible for NES constraints.

## Open Questions

1. **Mednafen Debugger Protocol:** Need to investigate if Mednafen supports network debugger or if we need save state approach
2. **P2 Memory Offsets:** Some addresses in VS_CPU_PLAN are marked "inferred" - need verification
3. **Down Button Mapping:** Still unclear which bit represents DOWN for soft-drop
4. **Combo Detection:** Need to understand how game tracks combos for reward function
5. **Starting Virus Configuration:** Should we train on fixed levels or randomize?

## References

- VS_CPU_PLAN.md: Memory addresses and button mappings
- headless_test.py: Example of nes-py integration (adapt for Mednafen)
- Mednafen Documentation: https://mednafen.github.io/documentation/
- Stable-Baselines3: https://stable-baselines3.readthedocs.io/
- OpenAI Gym: https://gymnasium.farama.org/

---

**Next immediate action:** Investigate Mednafen debugger capabilities and choose integration approach.
