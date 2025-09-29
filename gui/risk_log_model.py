import os
import sqlite3
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex, QVariant, pyqtSlot

# Rol sabitleri
TIMESTAMP_ROLE = Qt.UserRole + 1
RISK_TYPE_ROLE = Qt.UserRole + 2
SOURCE_APP_ROLE = Qt.UserRole + 3
SCREENSHOT_ROLE = Qt.UserRole + 4

class RiskLogModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.logs = []
        self.filtered_logs = []
        self.search_keyword = ""
        self.type_filter = "Tümü"
        self.loadLogs()

    def rowCount(self, parent=QModelIndex()):
        return len(self.filtered_logs)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.filtered_logs):
            return QVariant()

        log = self.filtered_logs[index.row()]

        if role == TIMESTAMP_ROLE:
            return log["timestamp"]
        elif role == RISK_TYPE_ROLE:
            return log["risk_type"]
        elif role == SOURCE_APP_ROLE:
            return log["app_name"]
        elif role == SCREENSHOT_ROLE:
            return log["image_path"]

        return QVariant()

    def roleNames(self):
        return {
            TIMESTAMP_ROLE: b"timestamp",
            RISK_TYPE_ROLE: b"risk_type",
            SOURCE_APP_ROLE: b"app_name",
            SCREENSHOT_ROLE: b"image_path"
        }

    def loadLogs(self):
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "parental_control.db"))
        self.logs.clear()

        if not os.path.exists(db_path):
            print("❌ Veritabanı bulunamadı:", db_path)
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
            SELECT timestamp, risk_score, app_name, image_path, weapon_detected, violence_detected, toxic_detected 
            FROM risk_log 
            WHERE risk_score >= 3
            ORDER BY timestamp DESC
        """)
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                timestamp, risk_score, app_name, image_path, weapon, violence, toxic = row
                risk_type = self.getRiskType(weapon, violence, toxic)

                absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", image_path)).replace("\\", "/")
                if not absolute_path.startswith("file:///"):
                    absolute_path = "file:///" + absolute_path
                self.logs.append({
                    "timestamp": timestamp,
                    "risk_type": risk_type,
                    "app_name": app_name,
                    "image_path": absolute_path
                })

            print(f"📦 Toplam kayıt yüklendi: {len(self.logs)}")
            self.applyFilters()
        except Exception as e:
            print(f"Veritabanı hatası: {e}")

    def getRiskType(self, weapon, violence, toxic):
        types = []
        if weapon:
            types.append("Silah")
        if violence:
            types.append("Şiddet")
        if toxic:
            types.append("Küfür")
        if not types:
            return "Diğer"
        return ", ".join(types)

    def applyFilters(self):
        self.filtered_logs = []
        keyword = self.search_keyword.lower().strip()

        for log in self.logs:
            log_risk_types = [rt.strip().lower() for rt in log["risk_type"].split(",")]
            matches_search = keyword in log["app_name"].lower() or keyword in log["risk_type"].lower()

            matches_type = (
                self.type_filter == "Tümü" or
                self.type_filter.lower() in log_risk_types
            )

            if matches_search and matches_type:
                self.filtered_logs.append(log)

        print(f"🔍 Filtre sonucu: {len(self.filtered_logs)} kayıt gösteriliyor")
        self.layoutChanged.emit()

    @pyqtSlot(str)
    def setFilter(self, keyword):
        self.search_keyword = keyword
        self.applyFilters()

    @pyqtSlot(str)
    def setTypeFilter(self, risk_type):
        self.type_filter = risk_type
        self.applyFilters()
