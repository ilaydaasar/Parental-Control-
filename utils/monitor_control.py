import os

FLAG_FILE = "monitoring.flag"

def start_monitoring():
    with open(FLAG_FILE, "w") as f:
        f.write("active")

def stop_monitoring():
    if os.path.exists(FLAG_FILE):
        os.remove(FLAG_FILE)

def is_monitoring_active():
    return os.path.exists(FLAG_FILE)
