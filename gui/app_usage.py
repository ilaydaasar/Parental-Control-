import os
import sqlite3
from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex, QVariant

APP_NAME_ROLE = Qt.UserRole + 1
DURATION_ROLE = Qt.UserRole + 2
START_TIME_ROLE = Qt.UserRole + 3
END_TIME_ROLE = Qt.UserRole + 4
CONTEXT_ROLE = Qt.UserRole + 5

class AppUsageModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.usage_data = []
        self.loadData()

    def rowCount(self, parent=QModelIndex()):
        return len(self.usage_data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.usage_data):
            return QVariant()
        item = self.usage_data[index.row()]
        if role == APP_NAME_ROLE:
            return item["app_name"]
        elif role == DURATION_ROLE:
            return item["duration_seconds"]
        elif role == START_TIME_ROLE:
            return item["start_time"]
        elif role == END_TIME_ROLE:
            return item["end_time"]
        elif role == CONTEXT_ROLE:
            return item["context"]
        return QVariant()

    def roleNames(self):
        return {
            APP_NAME_ROLE: b"app_name",
            DURATION_ROLE: b"duration_seconds",
            START_TIME_ROLE: b"start_time",
            END_TIME_ROLE: b"end_time",
            CONTEXT_ROLE: b"context"
        }

    def loadData(self):
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "parental_control.db"))
        if not os.path.exists(db_path):
            print("Veritabanı bulunamadı.")
            return

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                DATE(start_time) as usage_date,
                app_name,
                context,
                MIN(start_time) as first_seen,
                MAX(end_time) as last_seen,
                SUM(duration_seconds) as total_duration
            FROM app_usage
            GROUP BY usage_date, app_name, context
            ORDER BY usage_date DESC, total_duration DESC
        """)

        rows = cursor.fetchall()
        self.usage_data.clear()
        for row in rows:
            self.usage_data.append({
                "app_name": f"{row[1]} ({row[0]})",  # app_name (tarih)
                "context": row[2],
                "start_time": row[3],
                "end_time": row[4],
                "duration_seconds": row[5]
            })

        conn.close()
        self.layoutChanged.emit()

