# gui/history.py

import os
import winreg
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QFileDialog
)
from utils.web_history import parse_history_sqlite

def get_default_browser():
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice"
        ) as key:
            prog_id, _ = winreg.QueryValueEx(key, "ProgId")
            if "chrome" in prog_id.lower():
                return "chrome"
            elif "firefox" in prog_id.lower():
                return "firefox"
            elif "edge" in prog_id.lower():
                return "edge"
    except Exception as e:
        print("Tarayıcı algılanamadı:", e)
    return "chrome"

def find_chrome_history():
    base_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")
    for profile in os.listdir(base_path):
        hist_path = os.path.join(base_path, profile, "History")
        if os.path.exists(hist_path):
            return hist_path
    return None

class WebHistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.label = QLabel("🌐 Web Erişim Geçmişi")
        self.layout().addWidget(self.label)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Başlık veya URL ile ara...")
        self.search_bar.textChanged.connect(self.search)
        self.layout().addWidget(self.search_bar)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Başlık", "URL", "Zaman"])
        self.layout().addWidget(self.table)

        self.export_button = QPushButton("💾 Dışa Aktar")
        self.export_button.clicked.connect(self.export)
        self.layout().addWidget(self.export_button)
        self.table.setWordWrap(False)


        browser = get_default_browser()
        self.full_data = []

        history_file = ""
        if browser == "chrome":
            history_file = find_chrome_history()
        elif browser == "firefox":
            base_path = os.path.expanduser(r"~\AppData\Roaming\Mozilla\Firefox\Profiles")
            for folder in os.listdir(base_path):
                if folder.endswith(".default-release"):
                    history_file = os.path.join(base_path, folder, "places.sqlite")
                    break
        elif browser == "edge":
            history_file = os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\History")

        if history_file and os.path.exists(history_file):
            try:
                self.full_data = parse_history_sqlite(history_file, browser)
            except Exception as e:
                print("⚠️ Geçmiş verisi alınamadı:", e)
        else:
            print("⚠️ Geçmiş dosyası bulunamadı.")

        self.populate_table(self.full_data)

    def populate_table(self, data):
        self.table.setRowCount(0)
        for row_data in data:
            if len(row_data) != 3:
                continue  # Hatalı veya eksik satırları atla

            title = str(row_data[0]) if row_data[0] else "No Title"
            url = str(row_data[1]) if row_data[1] else "No URL"
            timestamp = str(row_data[2]) if row_data[2] else "Unknown"

            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(title))
            self.table.setItem(row, 1, QTableWidgetItem(url))
            self.table.setItem(row, 2, QTableWidgetItem(timestamp))


    def search(self):
        query = self.search_bar.text().lower()
        if not query:
            self.populate_table(self.full_data)
            return

        filtered = [
            row for row in self.full_data 
            if (row[0] and query in row[0].lower()) or (row[1] and query in row[1].lower())
        ]
        self.populate_table(filtered)


    def export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Web Geçmişini Kaydet", "", "CSV Files (*.csv)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("Başlık,URL,Zaman\n")
                for row in self.full_data:
                    f.write(f"{row[0]},{row[1]},{row[2]}\n")
