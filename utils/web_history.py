import os
import sqlite3
import shutil
import datetime
import tempfile
import time

def parse_history_sqlite(file_path, browser):
    import uuid
    results = []

    # Geçici kopya oluştur (kilitli dosya sorunu için)
    temp_dir = tempfile.gettempdir()
    temp_copy = os.path.join(temp_dir, f"history_copy_{uuid.uuid4().hex}.db")

    # Veritabanını kopyalamayı birkaç kez dene
    for attempt in range(3):
        try:
            shutil.copy2(file_path, temp_copy)
            break
        except PermissionError:
            print(f"⚠️ {file_path} kilitli. {attempt+1}. deneme...")
            time.sleep(1)
    else:
        print("❌ Veritabanı kopyalanamadı, işlem iptal.")
        return []

    try:
        conn = sqlite3.connect(temp_copy)
        cursor = conn.cursor()

        if browser in ["chrome", "edge"]:
            cursor.execute("""
                SELECT title, url, last_visit_time 
                FROM urls 
                ORDER BY last_visit_time DESC 
                LIMIT 100
            """)
            for title, url, timestamp in cursor.fetchall():
                visit_time = convert_chrome_time(timestamp)
                results.append((title, url, visit_time))

        elif browser == "firefox":
            cursor.execute("""
                SELECT moz_places.title, moz_places.url, moz_historyvisits.visit_date
                FROM moz_places
                JOIN moz_historyvisits ON moz_places.id = moz_historyvisits.place_id
                ORDER BY moz_historyvisits.visit_date DESC 
                LIMIT 100
            """)
            for title, url, timestamp in cursor.fetchall():
                visit_time = convert_firefox_time(timestamp)
                results.append((title or "No Title", url, visit_time))

    except Exception as e:
        print(f"❌ Geçmiş verisi okunamadı: {e}")
    finally:
        try:
            conn.close()
            if os.path.exists(temp_copy):
                os.remove(temp_copy)
        except:
            pass

    return results

def convert_chrome_time(timestamp):
    if not timestamp:
        return "N/A"
    try:
        epoch_start = datetime.datetime(1601, 1, 1)
        delta = datetime.timedelta(microseconds=int(timestamp))
        return (epoch_start + delta).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "Invalid Time"

def convert_firefox_time(timestamp):
    if not timestamp:
        return "N/A"
    try:
        return datetime.datetime.fromtimestamp(timestamp / 1_000_000).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "Invalid Time"
