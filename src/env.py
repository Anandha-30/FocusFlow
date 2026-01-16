# env.py — Stable-Baselines3 compatible environment
import gymnasium as gym
from gymnasium import spaces

import numpy as np
import os
import csv

SIM_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "simulated_sessions")

FOCUS_APPS = ["VSCode", "PyCharm", "LibreOffice"]
DISTRACT_APPS = ["YouTube", "Reddit", "Twitter", "Chrome"]
ALL_APPS = FOCUS_APPS + DISTRACT_APPS + ["Other"]


def app_to_onehot(app):
    arr = np.zeros(len(ALL_APPS), dtype=np.float32)
    try:
        idx = ALL_APPS.index(app)
    except ValueError:
        idx = len(ALL_APPS) - 1
    arr[idx] = 1.0
    return arr


class FocusEnv(gym.Env):
    """
    SB3-compatible environment (OLD Gym API)

    reset() returns: obs
    step() returns: obs, reward, done, info
    """

    metadata = {"render.modes": ["human"]}

    def __init__(self, sim_csv=None):
        super(FocusEnv, self).__init__()

        # load session data
        self.sim_csv = sim_csv
        self.rows = []
        if sim_csv:
            path = os.path.join(SIM_DIR, sim_csv)
            with open(path, newline="", encoding="utf-8") as f:
                self.rows = list(csv.DictReader(f))

        self.pos = 0
        self.streak = 0.0

        obs_len = len(ALL_APPS) + 4
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(obs_len,), dtype=np.float32
        )

        self.action_space = spaces.Discrete(4)

    # FIXED RESET
  
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)   # important for SB3 compatibility
        self.pos = 0
        self.streak = 0.0
        return self._get_obs()


    # build obs vector
    def _get_obs(self):
        if self.pos >= len(self.rows):
            app_vec = np.zeros(len(ALL_APPS), dtype=np.float32)
            return np.concatenate([app_vec, np.array([0, 0, self.streak / 60.0, 0])])

        r = self.rows[self.pos]
        app = r["active_app"]
        app_vec = app_to_onehot(app)

        kb = float(r.get("keyboard_count", 0))
        idle = float(r.get("idle_seconds", 0))

        kb_norm = min(1.0, kb / 50.0)
        idle_norm = min(1.0, idle / 300.0)
        streak_norm = min(1.0, self.streak / 60.0)
        time_norm = 0.5  # mock

        return np.concatenate(
            [app_vec, np.array([kb_norm, idle_norm, streak_norm, time_norm])]
        ).astype(np.float32)

    # FIXED STEP (SB3 expects 4 returns)

    def step(self, action):
        if self.pos >= len(self.rows):
            return self._get_obs(), 0.0, True, {}

        r = self.rows[self.pos]
        app = r["active_app"]
        is_focus = 1 if app in FOCUS_APPS else 0

        reward = 0.0

        # base reward logic
        if is_focus:
            reward += 1.0
            self.streak += 1.0
        else:
            reward -= 2.0
            self.streak = 0.0

        # action effects
        if action == 1:  # suggest break
            reward -= 0.1

        elif action == 2:  # bring forward (soft focus)
            if not is_focus and np.random.rand() < 0.3:
                reward += 1.0
                self.streak += 1.0

        elif action == 3:  # warning
            if not is_focus and np.random.rand() < 0.2:
                reward += 0.5

        self.pos += 1
        done = self.pos >= len(self.rows)
        return self._get_obs(), reward, done, {}

    def render(self, mode="human"):
        print(f"[pos={self.pos}] streak={self.streak}")
