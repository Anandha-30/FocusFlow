# activity_monitor.py — polls OS to gather active window, keyboard/mouse activity
import time
import platform
import psutil
from datetime import datetime
from logger import append_row
import uuid

try:
    import pygetwindow as gw
except Exception:
    gw = None

SESSION_ID = str(uuid.uuid4())[:8]

def get_active_window_info():
    title = ""
    app = ""

    if gw:
        try:
            win = gw.getActiveWindow()
            if win is not None:
                title = win.title
                app = win.__class__.__module__
        except Exception:
            pass

    try:
        procs = sorted(
            psutil.process_iter(['name', 'cpu_percent']),
            key=lambda p: p.info['cpu_percent'] or 0,
            reverse=True
        )
        if procs:
            app = procs[0].info.get('name', app)
    except Exception:
        pass

    return app, title

def poll_loop(poll_interval=5):
    last_input_time = time.time()

    print("Starting Activity Monitor. Press Ctrl+C to stop.")

    while True:
        try:
            app, title = get_active_window_info()
            idle = max(0, int(time.time() - last_input_time))

            append_row(
                active_app=app or "",
                idle_time=idle,
                action_taken="",
                reward="",
                user_feedback=""
            )

            time.sleep(poll_interval)

        except KeyboardInterrupt:
            print("Monitor stopped.")
            break

        except Exception as e:
            print("Monitor error:", e)
            time.sleep(poll_interval)

if __name__ == "__main__":
    poll_loop()
