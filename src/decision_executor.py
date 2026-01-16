# decision_executor.py — safe, non-destructive executor for agent actions
import platform
from plyer import notification
import time
import psutil
import os

def notify(title, message):
    try:
        notification.notify(title=title, message=message, timeout=4)
    except Exception:
        print("NOTIFY:", title, message)

def bring_app_forward(app_hint=None):
    # best-effort placeholder: prints instruction for user to focus app
    print("Bring to front:", app_hint)
    notify("FocusFlow", f"Try focusing {app_hint or 'your primary app'}")

def apply_action(action, active_app):
    # action mapping must match env
    if action == 0:
        # do nothing
        return "do_nothing"
    elif action == 1:
        notify("FocusFlow Suggestion", "Consider taking a short break (5 minutes).")
        return "suggest_break"
    elif action == 2:
        bring_app_forward(active_app)
        return "soft_focus"
    elif action == 3:
        notify("FocusFlow Warning", "You're switching to a distracting app — stay focused!")
        return "warning"
    return "unknown"
