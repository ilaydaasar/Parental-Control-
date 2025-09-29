import json
import os
import datetime
import sqlite3

LIMITS_FILE = "limits.json"
DB_FILE = "parental_control.db"

def load_limits():
    if os.path.exists(LIMITS_FILE):
        with open(LIMITS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_limits(limits):
    with open(LIMITS_FILE, "w", encoding="utf-8") as f:
        json.dump(limits, f, indent=4, ensure_ascii=False)

def get_total_usage(context):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        cursor.execute("""
            SELECT duration_seconds FROM app_usage 
            WHERE context = ? AND start_time LIKE ?
        """, (context, f"{today}%"))
        records = cursor.fetchall()
    except Exception as e:
        print(f"[get_total_usage HATA] {e}")
        return 0
    finally:
        conn.close()

    total = sum(r[0] for r in records if r[0] is not None)
    return int(total)

def is_time_exceeded(app_type, total_seconds):
    limits = load_limits()
    app_limits = limits.get(app_type, {})
    max_minutes = app_limits.get("duration", 0)
    action = app_limits.get("action", "none")
    if max_minutes > 0 and total_seconds > max_minutes * 60:
        return True, action
    return False, action
