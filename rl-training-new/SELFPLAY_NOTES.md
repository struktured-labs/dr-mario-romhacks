# Dr. Mario 2P Self-Play — Implementation Notes

Scaffolding for two-player self-play training on top of the existing single
agent stack. The goal is for a PPO learner to play P2 against an evolving
opponent (P1) that is drawn from a pool of frozen earlier snapshots of
itself.

## Files

- `src/drmario_2p_env.py` — `DrMario2PEnv`, a single-agent Gymnasium env
  wrapping a 2P match. Reuses `StateEncoder` (12-channel obs covering both
  playfields) and `RewardCalculator` (per player). Provides a
  `mock_mode=True` ctor flag that swaps the Mednafen HTTP interface for a
  synthetic state generator, so tests + CI run without the emulator.
- `scripts/train_selfplay.py` — Self-play training loop (PPO + snapshot
  pool + curriculum). All `model.learn()` calls are gated behind
  `if __name__ == "__main__"`.
- `scripts/test_2p_env.py` — Smoke test (mock mode). Runs in <1 s.

## Self-play loop

```
for iteration in 0..M-1:
    level = level_for_iteration(iteration)        # curriculum
    env   = build_env(opponent_policy, level, ...)
    if model is None: model = build_model(env)    # iter 0: random opponent
    else:             model.set_env(env)          # reuse learner
    model.learn(timesteps_per_iter)
    snapshot_path = save model to disk
    pool.add(snapshot_path)                       # evicts oldest if > K
    opponent_policy = pool.make_opponent_policy() # samples 1 snapshot
```

Defaults: `M=10` iterations, `N=200_000` timesteps per iter, `K=5`
snapshot pool capacity.

### Opponent semantics

`DrMario2PEnv` exposes `action_space = MultiDiscrete([9, 9])` (a joint
action over the two players). On every step the env **overwrites** the
P1 slot with the opponent policy's choice — so even if the learner's
network produces a meaningful P1 action it has no effect. The single
scalar reward returned to PPO is the P2 reward (with a small +/-10 bonus
when P1/P2 tops out, to give the agent a competitive shaping signal on
top of the within-board dense reward). Per-player rewards plus action
indices are exposed via `info`.

### Snapshot pool

`SnapshotPool` keeps a bounded FIFO of paths to saved PPO models.
`make_opponent_policy()` samples one uniformly, loads it onto CPU
(`PPO.load(..., device="cpu")`) so the GPU stays dedicated to the
learner, and exposes a `(obs) -> int` callable. Because the snapshot was
trained with the same `MultiDiscrete([9, 9])` head, we grab index 1
(P2 slot) from the predicted joint action. Loaded snapshots are cached
per-path to avoid reloading the same `.zip` every step.

### Curriculum

| iteration | virus level |
| --------- | ----------- |
| 0         | 5           |
| 1         | 10          |
| 2         | 15          |
| 3         | 20          |
| 4+        | uniform sample from {5, 10, 15, 20} |

Advances by iteration index (not by timesteps), per project spec. The
`level` value is plumbed through to `DrMario2PEnv.level`, which the env
exposes for downstream save-state selection.

## Running the smoke test

```bash
cd /home/struktured/projects/dr-mario-mods
.venv/bin/python rl-training-new/scripts/test_2p_env.py
```

Exits 0 in <1 s. No emulator required.

## Starting actual training

```bash
cd /home/struktured/projects/dr-mario-mods
.venv/bin/python rl-training-new/scripts/train_selfplay.py \
    --iterations 10 \
    --timesteps-per-iter 200000 \
    --snapshot-capacity 5 \
    --snapshot-dir rl-training-new/models/selfplay \
    --tensorboard-log rl-training-new/logs/tensorboard_selfplay \
    --device auto
```

For a plumbing dry-run **without** Mednafen, add `--mock`:

```bash
.venv/bin/python rl-training-new/scripts/train_selfplay.py \
    --iterations 2 --timesteps-per-iter 1024 --mock
```

(Mock mode is for verifying the loop runs end-to-end, not for producing
a useful policy — the synthetic states are random noise.)

Monitor with:

```bash
tensorboard --logdir rl-training-new/logs/tensorboard_selfplay
```

## Known limitations / gotchas

1. **Mednafen bridge not yet wired for 2P-controlled-by-RL.** The
   existing `mednafen_interface_http` exposes `write_memory(0xF5/0xF6,
   ...)` for controller bytes and `get_game_state()` for both players,
   but `MULTI_AGENT_PLAN.md` notes "auto-navigation not working (RAM
   writes don't affect controller input)" at the time of writing. Non-mock
   training will only work once the controller-injection regression is
   resolved (or a save-state loader skipping the menu is in place per the
   plan doc).

2. **Save states + virus-level curriculum.** The plan calls for
   `save_states/level_{05,10,15,20}.mcs` selected on reset. The current
   env stores `level` but does not yet trigger a `load_save_state(...)`
   call on `reset()`. The hook is in place — once `MednafenInterface`
   gains a `load_save_state()` method, hook it into
   `DrMario2PEnv.reset()` keyed on `self.level`. Mock mode is unaffected.

3. **No vectorisation across emulators.** The training loop uses
   `DummyVecEnv` with a single env because we have one shared emulator.
   When multiple Mednafen instances become available, switch to
   `SubprocVecEnv` with multiple `mesen_port` values — the env constructor
   already takes `mesen_host` / `mesen_port` per instance.

4. **Opponent picked once per `learn()` call.** The opponent snapshot is
   sampled when we build the per-iteration opponent policy callable, so
   the entire 200K-step training iteration sees the same opponent. For
   richer self-play you may want to resample per-episode — the cleanest
   place is to add a `gymnasium.Wrapper` that calls
   `env.set_opponent_policy(pool.make_opponent_policy())` inside its
   `reset()`. Deliberately left as a follow-up so the first version stays
   easy to reason about.

5. **No symmetric training for P1.** This is a P2-only learner; we
   freeze P1 every iteration. The reasoning is (a) self-play with frozen
   past-self is the standard recipe (AlphaGo-style) and (b) it keeps
   sb3's single-agent assumptions intact. If we later want P1 to also
   improve in real time, the simplest path is to alternate which player
   index the learner controls per iteration — the env supports this with
   minimal change (swap which slot is the policy's vs. the opponent's).

6. **Reward shaping side-effects.** `RewardCalculator` prints
   diagnostics to stdout on virus clears / matches. That's fine for
   smoke tests but will be noisy during real training; consider
   silencing those prints (or routing them through `logging`) when you
   start a long run.

## Design deviations from MULTI_AGENT_PLAN.md

- The plan proposes a dict observation + dict reward keyed by agent.
  We use a single scalar reward (P2's) and a single tensor observation
  because **stable-baselines3 does not support multi-agent envs**. The
  joint action space (MultiDiscrete([9, 9])) preserves both players'
  action transcript in info; PPO only optimises the P2 component because
  the env always overrides P1.
- The plan suggests RLlib (`PPOTrainer` w/ multiagent config). We stay
  on sb3 PPO to keep the dependency surface aligned with the existing
  single-agent training scripts.
- Curriculum advances by **iteration** index instead of timestep count,
  per explicit project request.
