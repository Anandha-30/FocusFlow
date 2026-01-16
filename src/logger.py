# logger.py
# Responsible ONLY for logging data (NO RL code here)

import csv
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "activity_log.csv")

HEADERS = [
    "timestamp",
    "active_app",
    "idle_time",
    "action_taken",
    "reward",
    "user_feedback"
]

# Create logs folder if not exists
os.makedirs(LOG_DIR, exist_ok=True)

def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def append_row(active_app, idle_time, action_taken="", reward="", user_feedback=""):
    init_log()
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            active_app,
            idle_time,
            action_taken,
            reward,
            user_feedback

        ])
