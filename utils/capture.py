from mss import mss
from datetime import datetime
import win32gui
import win32process
import psutil

def capture_screen():
    with mss() as sct:
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = f"screenshots/{now}.png"
        sct.shot(output=path)
        return path

def get_active_window_process_name():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return psutil.Process(pid).name().lower()
    except Exception:
        return "unknown"
