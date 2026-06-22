"""
Dr. Mario Two-Player Gymnasium Environment for Self-Play

This module defines DrMario2PEnv, a SINGLE-agent Gymnasium env wrapping a
2-player Dr. Mario match. It is designed for self-play with stable-baselines3
(which does not natively support multi-agent envs):

  - The trained ("learning") agent always controls Player 2.
  - The opponent controls Player 1 via an injectable callable
    `opponent_policy(observation) -> int` (action in [0, 9)).
  - The action space is a JOINT MultiDiscrete([9, 9]) (p1, p2). The env
    overrides the p1 entry on every step with the opponent's choice, so a
    learned policy that "thinks" it controls both indices is fine — only the
    p2 entry is honored by the policy in practice. We expose MultiDiscrete
    rather than Discrete(9) so the env transcript transparently records the
    joint action that was actually executed (useful for replay / debugging).
  - The reward is a single scalar — the P2 reward. The plan doc proposes a
    dict reward keyed by agent, but sb3 cannot consume that; condensing to
    p2_reward is the standard self-play workaround.
  - The observation is the existing 12-channel (16, 8, 12) tensor produced
    by StateEncoder, which already encodes both playfields (channels 0-5
    for P2, 6-11 for P1). No duplication needed.

`mock_mode=True` short-circuits the Mednafen connection and generates
synthetic game states. This lets us smoke-test the env, the action plumbing,
and (eventually) the training loop without an emulator.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

import gymnasium as gym
import numpy as np
from gymnasium import spaces

# Make sibling modules importable whether this file is run directly or as
# part of the `src` package.
_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from memory_map import (  # noqa: E402  (sys.path mutated above)
    BTN_A_ROTATE_CW,
    BTN_B_ROTATE_CCW,
    BTN_DOWN,
    BTN_LEFT,
    BTN_RIGHT,
    P1_CONTROLLER,
    P2_CONTROLLER,
    PLAYFIELD_HEIGHT,
    PLAYFIELD_WIDTH,
    TILE_EMPTY,
    TILE_VIRUS_BLUE,
    TILE_VIRUS_RED,
    TILE_VIRUS_YELLOW,
)
from reward_function import RewardCalculator  # noqa: E402
from state_encoder import StateEncoder  # noqa: E402


# Reuse the same 9-action discrete space as the single-agent env, so action
# semantics stay consistent across envs and policies are interchangeable.
ACTIONS = (
    0x00,                              # 0: NOOP
    BTN_LEFT,                          # 1: LEFT
    BTN_RIGHT,                         # 2: RIGHT
    BTN_DOWN,                          # 3: DOWN (soft drop)
    BTN_A_ROTATE_CW,                   # 4: A (rotate CW)
    BTN_B_ROTATE_CCW,                  # 5: B (rotate CCW)
    BTN_LEFT | BTN_DOWN,               # 6: LEFT + DOWN
    BTN_RIGHT | BTN_DOWN,              # 7: RIGHT + DOWN
    BTN_LEFT | BTN_A_ROTATE_CW,        # 8: LEFT + A
)
NUM_ACTIONS = len(ACTIONS)


OpponentPolicy = Callable[[np.ndarray], int]


def random_opponent_policy(_observation: np.ndarray) -> int:
    """Default opponent: uniform random action over the 9-action space.

    The observation argument is accepted (and ignored) so this signature
    matches a fully-fledged policy callable.
    """
    return int(np.random.randint(0, NUM_ACTIONS))


class DrMario2PEnv(gym.Env):
    """Two-player Dr. Mario env exposed as a single-agent Gymnasium env.

    Trained agent controls Player 2. Player 1 is driven by `opponent_policy`,
    which the training loop can swap out (e.g. for a frozen self-play
    snapshot) by calling `set_opponent_policy()`.

    Args:
        mesen_host: HTTP MCP host (only used when `mock_mode=False`).
        mesen_port: HTTP MCP port.
        opponent_policy: callable mapping observation -> p1 action index.
            Defaults to uniform-random.
        level: virus level (curriculum hook). Used by the training loop to
            select the appropriate save state on reset; the env stores it
            verbatim for downstream consumers.
        max_episode_steps: hard cap on env steps per episode.
        frame_skip: number of emulator frames to advance per env step.
        mock_mode: if True, do not connect to Mednafen — generate synthetic
            game states instead. For tests + CI.
        seed: RNG seed for mock-mode state generation.
    """

    metadata = {"render_modes": []}

    def __init__(
        self,
        mesen_host: str = "localhost",
        mesen_port: int = 8000,
        opponent_policy: Optional[OpponentPolicy] = None,
        level: int = 5,
        max_episode_steps: int = 10_000,
        frame_skip: int = 1,
        mock_mode: bool = False,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__()

        self.mesen_host = mesen_host
        self.mesen_port = mesen_port
        self.level = int(level)
        self.max_episode_steps = int(max_episode_steps)
        self.frame_skip = int(frame_skip)
        self.mock_mode = bool(mock_mode)

        self._opponent_policy: OpponentPolicy = (
            opponent_policy if opponent_policy is not None else random_opponent_policy
        )

        # Action space: JOINT (p1, p2). Only the p2 component is consulted
        # from the learning policy in practice — the env overwrites the p1
        # slot with the opponent's choice every step.
        self.action_space = spaces.MultiDiscrete([NUM_ACTIONS, NUM_ACTIONS])

        # Observation = the existing 12-channel encoding (already covers
        # both playfields, channels 0-5 = P2, 6-11 = P1).
        self._encoder = StateEncoder(player_id=2)
        self.observation_space = self._encoder.get_observation_space()

        # Reward calculators per player. We report only P2's reward as the
        # env reward, but compute both so info dict + future variants can use
        # them (and so reward shaping internal state advances correctly per
        # player).
        self._reward_p2 = RewardCalculator()
        self._reward_p1 = RewardCalculator()

        # Lazily-connected Mednafen interface (only when not in mock mode).
        self._mesen = None
        self._connected = False

        # Episode tracking.
        self._step_count = 0
        self._episode_count = 0
        self._last_state: Optional[Dict[str, Any]] = None
        self._last_obs: Optional[np.ndarray] = None

        # Mock-state RNG. Use the seeded np.random.Generator so tests are
        # deterministic when a seed is provided.
        self._rng = np.random.default_rng(seed)

    # ------------------------------------------------------------------
    # Public configuration knobs used by the self-play training loop
    # ------------------------------------------------------------------

    def set_opponent_policy(self, policy: OpponentPolicy) -> None:
        """Swap the opponent in. Safe to call between episodes."""
        if policy is None:
            policy = random_opponent_policy
        self._opponent_policy = policy

    def set_level(self, level: int) -> None:
        """Update the curriculum level used for the NEXT episode."""
        self.level = int(level)

    # ------------------------------------------------------------------
    # Gymnasium interface
    # ------------------------------------------------------------------

    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        super().reset(seed=seed)
        if seed is not None:
            self._rng = np.random.default_rng(seed)

        self._step_count = 0
        self._episode_count += 1
        self._reward_p2.reset()
        self._reward_p1.reset()

        state = self._fetch_state(initial=True)
        self._last_state = state
        obs = self._encoder.encode(state)
        self._last_obs = obs

        info = {
            "episode": self._episode_count,
            "level": self.level,
            "mock_mode": self.mock_mode,
            "p2_virus_count": state.get("virus_count", 0),
            "p1_virus_count": state.get("p1_virus_count", 0),
        }
        return obs, info

    def step(
        self,
        action: np.ndarray,
    ) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        # Coerce the joint action into (p1, p2) ints. We accept either a
        # MultiDiscrete sample (np.ndarray of shape (2,)) or a tuple/list
        # for flexibility.
        action = np.asarray(action).reshape(-1)
        if action.size != 2:
            raise ValueError(
                f"DrMario2PEnv expects a joint action of length 2, got "
                f"{action.size}: {action!r}"
            )
        # The learning policy controls p2. p1's slot is always overridden by
        # the opponent — this guarantees self-play behavior even if a future
        # policy class accidentally outputs a meaningful p1 action.
        p2_action = int(action[1]) % NUM_ACTIONS
        try:
            opponent_obs = self._last_obs if self._last_obs is not None else np.zeros(
                self.observation_space.shape, dtype=np.float32
            )
            p1_action = int(self._opponent_policy(opponent_obs)) % NUM_ACTIONS
        except Exception:  # noqa: BLE001 — opponent must never crash training
            p1_action = random_opponent_policy(self._last_obs)

        self._apply_actions(p1_action, p2_action)

        self._step_count += self.frame_skip
        state = self._fetch_state(initial=False)
        self._last_state = state

        # Compute per-player rewards from each playfield. The shared
        # RewardCalculator API takes a 16x8 playfield; we feed P2's
        # playfield for the agent reward and P1's for the opponent reward.
        p2_playfield = np.array(state["playfield"], dtype=np.uint8).reshape(
            PLAYFIELD_HEIGHT, PLAYFIELD_WIDTH
        )
        p1_playfield = np.array(state.get("p1_playfield", [TILE_EMPTY] * 128),
                                dtype=np.uint8).reshape(PLAYFIELD_HEIGHT,
                                                       PLAYFIELD_WIDTH)

        p2_max_height = _max_height(p2_playfield)
        p1_max_height = _max_height(p1_playfield)

        p2_virus = int(state.get("virus_count", 0))
        p1_virus = int(state.get("p1_virus_count", 0))

        p2_won = (p2_virus == 0)
        p1_won = (p1_virus == 0)
        p2_topped = (p2_max_height == 0)
        p1_topped = (p1_max_height == 0)

        reward_p2 = self._reward_p2.calculate(
            playfield=p2_playfield,
            virus_count=p2_virus,
            max_height=p2_max_height,
            game_over=p2_topped,
            all_viruses_cleared=p2_won,
        )
        # Compute opponent reward too — informational only, surfaced via info.
        reward_p1 = self._reward_p1.calculate(
            playfield=p1_playfield,
            virus_count=p1_virus,
            max_height=p1_max_height,
            game_over=p1_topped,
            all_viruses_cleared=p1_won,
        )

        # Versus-mode framing: P2 also wins if P1 tops out, and loses if P2
        # tops out before P1. Apply small competitive shaping on top of the
        # within-board reward.
        if p1_topped and not p2_topped:
            reward_p2 += 10.0  # opponent KO
        if p2_topped and not p1_topped:
            reward_p2 -= 10.0  # self KO

        terminated = bool(p2_won or p1_won or p2_topped or p1_topped)
        truncated = bool(self._step_count >= self.max_episode_steps)

        obs = self._encoder.encode(state)
        self._last_obs = obs

        info = {
            "episode": self._episode_count,
            "step": self._step_count,
            "level": self.level,
            "p1_action": p1_action,
            "p2_action": p2_action,
            "p1_reward": float(reward_p1),
            "p2_reward": float(reward_p2),
            "p1_virus_count": p1_virus,
            "p2_virus_count": p2_virus,
            "p1_topped_out": p1_topped,
            "p2_topped_out": p2_topped,
            "p2_won": p2_won,
            "p1_won": p1_won,
        }

        return obs, float(reward_p2), terminated, truncated, info

    def close(self) -> None:
        if self._mesen is not None and self._connected:
            try:
                self._mesen.disconnect()
            finally:
                self._connected = False
                self._mesen = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_connected(self) -> None:
        if self.mock_mode:
            return
        if self._connected:
            return
        # Import lazily so mock-mode tests don't require the HTTP stack.
        from mednafen_interface_http import MednafenInterface  # noqa: WPS433

        self._mesen = MednafenInterface(host=self.mesen_host, port=self.mesen_port)
        if not self._mesen.connect(timeout=30):
            raise ConnectionError(
                f"DrMario2PEnv: failed to connect to MCP at "
                f"{self.mesen_host}:{self.mesen_port}"
            )
        self._connected = True

    def _apply_actions(self, p1_action_idx: int, p2_action_idx: int) -> None:
        if self.mock_mode:
            # Stash actions on the RNG so mock state can mildly react. Not
            # really needed for shape/type smoke tests, but keeps the mock
            # state evolving instead of frozen.
            self._last_mock_actions = (p1_action_idx, p2_action_idx)
            return

        self._ensure_connected()
        p1_byte = ACTIONS[p1_action_idx]
        p2_byte = ACTIONS[p2_action_idx]
        for _ in range(self.frame_skip):
            self._mesen.write_memory(P1_CONTROLLER, [p1_byte])
            self._mesen.write_memory(P2_CONTROLLER, [p2_byte])
            self._mesen.step_frame()

    def _fetch_state(self, initial: bool) -> Dict[str, Any]:
        if self.mock_mode:
            return self._mock_state(initial=initial)

        self._ensure_connected()
        return self._mesen.get_game_state()

    def _mock_state(self, initial: bool) -> Dict[str, Any]:
        """Generate a plausible-but-fake game state.

        We sprinkle a handful of viruses + a couple of capsule pieces onto
        each playfield. The exact contents do not matter for the smoke test;
        what matters is that all downstream consumers
        (StateEncoder / RewardCalculator) receive shapes/dtypes they accept.
        """
        rng = self._rng

        def _make_playfield() -> list:
            field = np.full(PLAYFIELD_HEIGHT * PLAYFIELD_WIDTH, TILE_EMPTY, dtype=np.uint8)
            # Drop ~6 viruses + ~4 pill cells in random low rows.
            num_viruses = int(rng.integers(2, 8))
            virus_choices = [TILE_VIRUS_YELLOW, TILE_VIRUS_RED, TILE_VIRUS_BLUE]
            for _ in range(num_viruses):
                row = int(rng.integers(8, PLAYFIELD_HEIGHT))
                col = int(rng.integers(0, PLAYFIELD_WIDTH))
                field[row * PLAYFIELD_WIDTH + col] = rng.choice(virus_choices)
            num_pills = int(rng.integers(0, 5))
            pill_choices = [0x40, 0x5C, 0x68]  # yellow / red / blue pill heads
            for _ in range(num_pills):
                row = int(rng.integers(4, PLAYFIELD_HEIGHT))
                col = int(rng.integers(0, PLAYFIELD_WIDTH))
                field[row * PLAYFIELD_WIDTH + col] = rng.choice(pill_choices)
            return field.tolist()

        return {
            "mode": 4,  # arbitrary "in-game" mode value
            "virus_count": int(rng.integers(0, max(1, self.level) + 1)),
            "capsule_x": int(rng.integers(0, PLAYFIELD_WIDTH)),
            "capsule_y": int(rng.integers(0, PLAYFIELD_HEIGHT)),
            "left_color": int(rng.integers(0, 3)),
            "right_color": int(rng.integers(0, 3)),
            "next_left_color": int(rng.integers(0, 3)),
            "next_right_color": int(rng.integers(0, 3)),
            "playfield": _make_playfield(),
            "p1_playfield": _make_playfield(),
            "p1_virus_count": int(rng.integers(0, max(1, self.level) + 1)),
            "p1_capsule_x": int(rng.integers(0, PLAYFIELD_WIDTH)),
            "p1_capsule_y": int(rng.integers(0, PLAYFIELD_HEIGHT)),
            "p1_next_left_color": int(rng.integers(0, 3)),
        }


def _max_height(playfield: np.ndarray) -> int:
    """Return the row index of the topmost non-empty tile (0 = very top).

    Matches the convention used by RewardCalculator: 0 means stack reaches
    the ceiling (i.e. topped out). 16 means the board is empty.
    """
    for row in range(PLAYFIELD_HEIGHT):
        if np.any(playfield[row, :] != TILE_EMPTY):
            return row
    return PLAYFIELD_HEIGHT


if __name__ == "__main__":  # pragma: no cover — manual smoke run
    env = DrMario2PEnv(mock_mode=True, seed=0)
    obs, info = env.reset()
    print("obs shape:", obs.shape, "dtype:", obs.dtype)
    print("info:", info)
    for _ in range(5):
        joint = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(joint)
        print(f"step reward={reward:+.3f} term={terminated} trunc={truncated}")
        if terminated or truncated:
            obs, info = env.reset()
    env.close()
