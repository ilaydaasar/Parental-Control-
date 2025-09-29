from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty,pyqtSlot
import sqlite3
import os
import random
from datetime import datetime

class DashboardData(QObject):
    totalRisksChanged = pyqtSignal()
    screenTimeChanged = pyqtSignal()
    mostUsedAppChanged = pyqtSignal()
    activeUsersChanged = pyqtSignal()
    pieDataChanged = pyqtSignal()
    riskTimeDataChanged = pyqtSignal()
    riskImagesChanged = pyqtSignal()

    def __init__(self):
        super().__init__()

        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "parental_control.db"))
        print(f"📌 Dashboard için veritabanı yolu: {db_path}")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self._totalRisks = self.get_total_risks()
        self._screenTime = self.get_screen_time()
        self._mostUsedApp = self.get_most_used_app()
        self._activeUsers = 1
        self._pieData = self.get_pie_data()
        self._riskTimeData = self.get_risk_time_data()
        self._riskImages = self.load_risk_images()

    def get_total_risks(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM risk_log WHERE DATE(timestamp) = DATE('now')")
            return self.cursor.fetchone()[0]
        except Exception as e:
            print("⛔ Total Risks hatası:", e)
            return 0

    def get_screen_time(self):
        try:
        # Tüm aralıkları çek
            self.cursor.execute("""
            SELECT start_time, end_time FROM app_usage
            WHERE DATE(start_time) = DATE('now') AND end_time IS NOT NULL
            """)
            rows = self.cursor.fetchall()

            from datetime import datetime

            def parse_time(ts):
            # Tarih formatını gerektiği gibi ayarla (örnek: "2025-06-23 16:00:00")
                return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")

        # Aralıkları hazırla
            intervals = []
            for start, end in rows:
                if start and end:
                    intervals.append((parse_time(start), parse_time(end)))

        # Sırala ve birleştir
            intervals.sort(key=lambda x: x[0])
            merged = []
            for start, end in intervals:
                if not merged:
                    merged.append([start, end])
                else:
                    last_start, last_end = merged[-1]
                    if start <= last_end:  # Çakışıyorsa
                        merged[-1][1] = max(last_end, end)
                    else:
                        merged.append([start, end])

        # Toplam süreyi hesapla
            total_seconds = sum((end - start).total_seconds() for start, end in merged)
            hours, minutes = divmod(int(total_seconds // 60), 60)
            return f"{hours} sa. {minutes} dk."
        except Exception as e:
            print("⛔ Ekran süresi hatası:", e)
            return "0 sa. 0 dk."


    def get_most_used_app(self):
        try:
            self.cursor.execute("""
                SELECT app_name FROM app_usage
                WHERE DATE(start_time) = DATE('now')
                GROUP BY app_name
                ORDER BY SUM(duration_seconds) DESC
                LIMIT 1
            """)
            row = self.cursor.fetchone()
            return row[0] if row else "Yok"
        except Exception as e:
            print("⛔ En çok kullanılan uygulama hatası:", e)
            return "Yok"

    def get_pie_data(self):
        try:
            self.cursor.execute("""
                SELECT 
                    SUM(CASE WHEN violence_detected = 1 THEN 1 ELSE 0 END),
                    SUM(CASE WHEN weapon_detected = 1 THEN 1 ELSE 0 END),
                    SUM(CASE WHEN toxic_detected = 1 THEN 1 ELSE 0 END)
                FROM risk_log
                WHERE DATE(timestamp) = DATE('now')
            """)
            row = self.cursor.fetchone()
            return list(row) if row else [0, 0, 0]
        except Exception as e:
            print("⛔ PieData hatası:", e)
            return [0, 0, 0]
    
    def get_risk_time_data(self):
            try:
                self.cursor.execute("""
                    SELECT strftime('%H', timestamp), COUNT(*) 
                    FROM risk_log 
                    WHERE DATE(timestamp) = DATE('now')
                    GROUP BY strftime('%H', timestamp)
                """)
                return [{'hour': int(h), 'value': v} for h, v in self.cursor.fetchall()]
            except Exception as e:
                print("⛔ Risk Zaman Grafiği hatası:", e)
                return []
    def load_risk_images(self):
        flagged_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'flagged'))
        print("📂 [Dashboard] Flagged klasörü:", flagged_folder)

        if not os.path.exists(flagged_folder):
            return []

        images = [
            'file:///' + os.path.join(flagged_folder, f).replace("\\", "/")
            for f in os.listdir(flagged_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg')) and f.startswith('blurred_')
        ]

        return random.sample(images, min(5, len(images)))

    @pyqtProperty(int, notify=totalRisksChanged)
    def totalRisks(self):
        return self._totalRisks

    @pyqtProperty(str, notify=screenTimeChanged)
    def screenTime(self):
        return self._screenTime

    @pyqtProperty(str, notify=mostUsedAppChanged)
    def mostUsedApp(self):
        return self._mostUsedApp

    @pyqtProperty(int, notify=activeUsersChanged)
    def activeUsers(self):
        return self._activeUsers

    @pyqtProperty('QVariantList', notify=pieDataChanged)
    def pieData(self):
         print("🎯 pieData:", self._pieData)
         print("📈 riskTimeData:", self._riskTimeData)
         return self._pieData
       
    @pyqtProperty('QVariantList', notify=riskTimeDataChanged)
    def riskTimeData(self):
        return self._riskTimeData

    @pyqtProperty('QStringList', notify=riskImagesChanged)
    def riskImages(self):
        return self._riskImages
    
    @pyqtSlot(result='QStringList')
    def refreshRiskImages(self):
        return self.load_risk_images()

