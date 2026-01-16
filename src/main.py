# main.py — run the monitor in suggestion-only mode with a pre-trained policy
import time
import os
from env import FocusEnv
from decision_executor import apply_action
from logger import append_row
from stable_baselines3 import PPO
import numpy as np
from datetime import datetime
import csv

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "focus_agent.zip")

def load_model():
    if os.path.exists(MODEL_PATH):
        model = PPO.load(MODEL_PATH)
        print("Model loaded.")
        return model
    print("Model not found. Run training first.")
    return None

def read_latest_state_from_logs():
    # read last row from logs
    logp = os.path.join(os.path.dirname(__file__), "..", "data", "logs.csv")
    if not os.path.exists(logp):
        return None
    with open(logp, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
        if not rows:
            return None
        last = rows[-1]
        return last
    return None

def state_to_obs(row):
    # produce dummy obs consistent with env._get_obs
    from env import ALL_APPS
    app = row.get("active_app","")
    onehot = np.zeros(len(ALL_APPS), dtype=np.float32)
    try:
        idx = ALL_APPS.index(app)
    except:
        idx = len(ALL_APPS)-1
    onehot[idx] = 1.0
    kb = float(row.get("keyboard_count") or 0)
    idle = float(row.get("idle_seconds") or 0)
    streak = 0.0
    tod = 0.5
    obs = np.concatenate([onehot, np.array([min(1,kb/50), min(1, idle/300), streak, tod], dtype=np.float32)])
    return obs

def run_suggestion_loop(poll_interval=10):
    model = load_model()
    if model is None:
        return

    print("Starting suggestion loop. Running in suggestion-only mode.")

    while True:
        try:
            row = read_latest_state_from_logs()
            if not row:
                time.sleep(poll_interval)
                continue

            obs = state_to_obs(row)
            action, _ = model.predict(obs, deterministic=False)
            action = int(action)

            action_name = apply_action(action, row.get("active_app"))

            print(f"[{datetime.now().strftime('%H:%M:%S')}] Suggested action: {action_name}")

            append_row(
                active_app=row.get("active_app", ""),
                idle_time=row.get("idle_seconds", 0),
                action_taken=action_name,
                reward="",
                user_feedback=""
            )

            time.sleep(poll_interval)

        except KeyboardInterrupt:
            print("Stopping loop.")
            break

        except Exception as e:
            print("Loop error:", e)
            time.sleep(poll_interval)

if __name__ == "__main__":
    run_suggestion_loop()
