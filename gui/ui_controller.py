import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl

from login_handler import LoginHandler
from keylogs import KeylogData
from risk_log_model import RiskLogModel
from app_usage import AppUsageModel
from dashboard_data import DashboardData
from settings import SettingsHandler   # ✅ EKLE

# 🔧 QML için platform yolu (Anaconda fix)
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"C:\Users\sayca\anaconda3\envs\cuda-env\Library\plugins\platforms"

# ✅ Uygulama başlat
app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

# 🔗 Python backend sınıflarını QML'e bağla
login_handler = LoginHandler()
engine.rootContext().setContextProperty("LoginHandler", login_handler)

dashboard_data = DashboardData()
engine.rootContext().setContextProperty("dashboardData", dashboard_data)

keylog_model = KeylogData()
engine.rootContext().setContextProperty("keylogData", keylog_model)

risk_model = RiskLogModel()
engine.rootContext().setContextProperty("riskLogModel", risk_model)

app_model = AppUsageModel()
engine.rootContext().setContextProperty("appUsageModel", app_model)

settings_handler = SettingsHandler()                     # ✅ EKLE
engine.rootContext().setContextProperty("settingsHandler", settings_handler)  # ✅ EKLE

# ✅ QML dosyasını yükle
qml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "UntitledProject3Content", "App.qml"))
engine.load(QUrl.fromLocalFile(qml_path))

# ❌ Hata varsa çık
if not engine.rootObjects():
    print("❌ QML yüklenemedi.")
    sys.exit(-1)

# ▶️ Başlat
sys.exit(app.exec_())
