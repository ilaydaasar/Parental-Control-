from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QVariant
import os
import json
import sqlite3
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import limits, notify_parent, monitor_control
from login_handler import LoginHandler
import subprocess
import psutil
import winreg


class SettingsHandler(QObject):
    monitoringChanged = pyqtSignal(bool)
    statusMessageChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.limits = limits.load_limits()

    @pyqtSlot(str, str, result=QVariant)
    def getLimit(self, app_type, key):
        return self.limits.get(app_type, {}).get(key, 0 if key == "duration" else "none")

    @pyqtSlot(str, str, QVariant)
    def setLimit(self, app_type, key, value):
        if app_type not in self.limits:
            self.limits[app_type] = {}
        self.limits[app_type][key] = value

    @pyqtSlot()
    def saveAll(self):
        try:
            limits.save_limits(self.limits)
            self.statusMessageChanged.emit("✅ Ayarlar başarıyla kaydedildi.")
        except Exception as e:
            self.statusMessageChanged.emit("❌ Ayarlar kaydedilemedi!")
    @pyqtSlot()
    def startMonitoring(self):
        try:
            py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "monitor_controller.py"))
            subprocess.Popen(["python", py_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.monitoringChanged.emit(True)
            self.statusMessageChanged.emit("✅ İzleme başlatıldı (Python).")
        except Exception as e:
            self.statusMessageChanged.emit(f"❌ İzleme başlatılamadı: {str(e)}")

    @pyqtSlot()
    def stopMonitoring(self):
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline and isinstance(cmdline, list) and any("monitor_controller.py" in part for part in cmdline):
                        proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            monitor_control.stop_monitoring()
            self.monitoringChanged.emit(False)
            self.statusMessageChanged.emit("🛑 İzleme durduruldu.")
        except Exception as e:
            self.statusMessageChanged.emit(f"❌ İzleme durdurulamadı: {str(e)}")


    @pyqtSlot(result=bool)
    def isMonitoring(self):
        return monitor_control.is_monitoring_active()

    # ✅ Otomatik Başlatmayı python ile ayarlayan sürüm
    @pyqtSlot(result=bool)
    def isAutoStartEnabled(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            val, _ = winreg.QueryValueEx(key, "ParentalControl")
            return "monitor_controller.py" in val
        except FileNotFoundError:
            return False

    @pyqtSlot(bool)
    def setAutoStartEnabled(self, enabled):
        try:
            python_path = sys.executable  # örn: C:\Users\kullanici\AppData\Local\Programs\Python\Python310\python.exe
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "monitor_controller.py"))
            run_value = f'"{python_path}" "{script_path}"'

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)

            if enabled:
                winreg.SetValueEx(key, "ParentalControl", 0, winreg.REG_SZ, run_value)
                self.statusMessageChanged.emit("✅ Başlangıçta otomatik başlatma etkinleştirildi.")
            else:
                try:
                    winreg.DeleteValue(key, "ParentalControl")
                except FileNotFoundError:
                    pass
                self.statusMessageChanged.emit("✅ Otomatik başlatma devre dışı bırakıldı.")
        except Exception as e:
            self.statusMessageChanged.emit(f"❌ Otomatik başlatma hatası: {str(e)}")

        # 🔑 Şifre Değiştirme
    @pyqtSlot(str, str, str)
    def change_password(self, email, old_password, new_password):
        try:
            conn = sqlite3.connect("users.db")
            cur = conn.cursor()
            cur.execute("SELECT password FROM users WHERE email = ?", (email,))
            row = cur.fetchone()
            if not row:
                self.statusMessageChanged.emit("❌ Kullanıcı bulunamadı.")
                return
            if row[0] != old_password:
                self.statusMessageChanged.emit("❌ Eski şifre hatalı.")
                return
            cur.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
            conn.commit()
            conn.close()
            self.statusMessageChanged.emit("✅ Şifre başarıyla değiştirildi.")
        except Exception as e:
            self.statusMessageChanged.emit(f"❌ Şifre değiştirilemedi: {str(e)}")
