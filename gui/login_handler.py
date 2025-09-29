from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
import sqlite3, os, re, random, string
from email.mime.text import MIMEText
import smtplib

class LoginHandler(QObject):
    loginSuccess = pyqtSignal()
    loginFailed = pyqtSignal(str)
    registerSuccess = pyqtSignal()
    registerFailed = pyqtSignal(str)
    resetSuccess = pyqtSignal()
    resetFailed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "users.db"))
        self.remember_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "remember.txt"))
        self._current_user_email = ""  # 🔐 Oturum açan kullanıcının email'i
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                email TEXT UNIQUE,
                password TEXT
            )
        """)
        conn.commit()
        conn.close()

    @pyqtProperty(str)
    def currentUserEmail(self):
        return self._current_user_email

    @pyqtSlot(str, str)
    def login(self, email, password):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                self._current_user_email = email  # ✅ Oturum bilgisini sakla
                self.loginSuccess.emit()
            else:
                self.loginFailed.emit("Email veya şifre yanlış.")
        except Exception as e:
            self.loginFailed.emit(f"Giriş hatası: {str(e)}")

    @pyqtSlot(str, str, str)
    def register(self, name, email, password):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            self.registerFailed.emit("Geçersiz e-posta adresi.")
            return

        if len(password) < 6 or password.isdigit() or password.isalpha():
            self.registerFailed.emit("Şifre en az 6 karakter olmalı, harf ve rakam içermelidir.")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            conn.close()
            self.registerSuccess.emit()
        except sqlite3.IntegrityError:
            self.registerFailed.emit("Bu email zaten kayıtlı.")
        except Exception as e:
            self.registerFailed.emit(f"Kayıt hatası: {str(e)}")

    @pyqtSlot(str)
    def send_reset_email(self, email):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            user = cursor.fetchone()
            conn.close()

            if not user:
                self.resetFailed.emit("Email sistemde kayıtlı değil.")
                return

            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
            conn.commit()
            conn.close()

            sender_email = "mustafa8yildiz@gmail.com"
            sender_password = "miiq bodi ldps iruo"
            msg = MIMEText(f"Yeni geçici şifreniz: {new_password}")
            msg["Subject"] = "KidShield Şifre Sıfırlama"
            msg["From"] = sender_email
            msg["To"] = email

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)

            self.resetSuccess.emit()

        except Exception as e:
            self.resetFailed.emit("E-posta gönderilemedi.")

    @pyqtSlot(str, str)
    def save_remember_me(self, email, remember):
        with open(self.remember_file, "w") as f:
            f.write(email if remember else "")

    @pyqtSlot(result=str)
    def load_remember_me(self):
        if os.path.exists(self.remember_file):
            with open(self.remember_file, "r") as f:
                return f.read().strip()
        return ""

    @pyqtSlot(str, str, str)
    def change_password(self, email, old_password, new_password):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE email=?", (email,))
            result = cursor.fetchone()

            if not result:
                self.resetFailed.emit("Kullanıcı bulunamadı.")
                return

            if result[0] != old_password:
                self.resetFailed.emit("Eski şifre yanlış.")
                return

            cursor.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
            conn.commit()
            conn.close()

            self.resetSuccess.emit()
        except Exception as e:
            self.resetFailed.emit("Şifre değiştirme hatası.")

    @pyqtSlot(str, str)
    def save_remember_me(self, email, remember):
        with open(self.remember_file, "w") as f:
            f.write(email if remember else "")

    @pyqtSlot(result=str)
    def load_remember_me(self):
        if os.path.exists(self.remember_file):
            with open(self.remember_file, "r") as f:
                return f.read().strip()
        return ""

