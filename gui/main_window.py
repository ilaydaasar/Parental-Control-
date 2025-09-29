from PyQt5.QtWidgets import QMainWindow, QTabWidget
from gui.dashboard import DashboardTab
from gui.logs import LogsTab
from gui.app_usage import AppUsageTab
from gui.settings import SettingsTab
from gui.history import WebHistoryTab
from gui.limits import LimitsTab
from gui.keylogs import KeylogsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parental Control Dashboard")
        self.setGeometry(100, 100, 1200, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Sekmeler
        self.tabs.addTab(DashboardTab(), "📊 Dashboard")
        self.tabs.addTab(KeylogsTab(), "🧾 Keylogs")
        self.tabs.addTab(WebHistoryTab(), "🌐 Web History")
        self.tabs.addTab(LogsTab(), "⚠️ Risk Logs")
        self.tabs.addTab(LimitsTab(), "⏱ Süre Limitleri")
        self.tabs.addTab(AppUsageTab(), "📱 App Usage")
       
