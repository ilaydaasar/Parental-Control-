import datetime
import os
from mss import mss
import win32gui
import win32process
import psutil

def capture_screen():
    os.makedirs("screenshots", exist_ok=True)
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    path = f"screenshots/{now}.png"
    with mss() as sct:
        sct.shot(output=path)
    return path

def get_active_window_process_name():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process_name = psutil.Process(pid).name().lower()
        window_title = win32gui.GetWindowText(hwnd).lower()
        return process_name, window_title
    except Exception:
        return "unknown", ""

def get_app_category(app_name, window_title=None):
    app_name = (app_name or "").lower()
    window_title = (window_title or "").lower()

    if any(w in app_name for w in ["csgo", "valorant", "steam"]) or \
       any(w in window_title for w in ["csgo", "valorant", "steam"]):
        return "game"
    elif any(w in app_name for w in ["chrome", "edge", "firefox"]) or \
         any(w in window_title for w in ["google", "browser", "site", ".com"]):
        # özel durumlar: YouTube, Netflix vs.
        if "youtube" in window_title or "netflix" in window_title:
            return "video"
        elif "whatsapp" in window_title or "telegram" in window_title or "discord" in window_title:
            return "chat"
        else:
            return "web"
    elif any(w in app_name for w in ["whatsapp", "telegram", "discord"]) or \
         any(w in window_title for w in ["whatsapp", "telegram", "discord"]):
        return "chat"
    elif any(w in app_name for w in ["vlc", "netflix", "youtube"]) or \
         any(w in window_title for w in ["vlc", "netflix", "youtube"]):
        return "video"
    return "other"

def get_friendly_app_name(process_name, window_title):
    process_name = (process_name or "").lower()
    window_title = (window_title or "").lower()

    # Web tabanlı tanımalar (chrome için)
    if "youtube" in window_title:
        return "YouTube"
    elif "whatsapp" in window_title:
        return "WhatsApp Web"
    elif "telegram" in window_title:
        return "Telegram Web"
    elif "discord" in window_title:
        return "Discord Web"

    # Masaüstü uygulamaları
    elif "whatsapp" in window_title:
        return "WhatsApp"
    elif "telegram" in window_title:
        return "Telegram"
    elif "discord" in window_title:
        return "Discord"
    elif "netflix" in window_title:
        return "Netflix"
    elif "vlc" in window_title:
        return "VLC Player"

    # Hiçbiri eşleşmezse exe adı döner
    return process_name
