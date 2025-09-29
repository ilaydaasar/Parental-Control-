
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
import sqlite3

class LogsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📁 Risk Logları"))
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["ID", "Zaman", "Resim", "Uygulama", "Bağlam", "Risk", "Silah", "Şiddet", "Küfür"])
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("parental_control.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM risk_log ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, item in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
        conn.close()
