# simulator.py — generates synthetic sessions for offline RL training
import random
from datetime import datetime, timedelta
import csv
import os

SIM_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "simulated_sessions")
os.makedirs(SIM_DIR, exist_ok=True)

FOCUS_APPS = ["VSCode", "PyCharm", "LibreOffice"]
DISTRACT_APPS = ["YouTube", "Reddit", "Twitter", "Chrome"]

def generate_session(filename, minutes=120, distract_prob=0.12):
    now = datetime.utcnow()
    rows = []
    for i in range(minutes):
        t = (now + timedelta(minutes=i)).isoformat()
        if random.random() < distract_prob:
            app = random.choice(DISTRACT_APPS)
            idle = random.randint(0, 30)
            keyboard = random.randint(0, 5)
        else:
            app = random.choice(FOCUS_APPS)
            idle = random.randint(0, 5)
            keyboard = random.randint(5, 40)
        rows.append([t, "sim", app, "", "", keyboard, 0, idle, "", "", ""])
    with open(os.path.join(SIM_DIR, filename), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp","session_id","active_app","active_title","active_url","keyboard_count","mouse_count","idle_seconds","action_taken","reward","user_feedback"])
        writer.writerows(rows)
    print("Generated", filename)

if __name__ == "__main__":
    generate_session("session1.csv", minutes=240, distract_prob=0.15)
