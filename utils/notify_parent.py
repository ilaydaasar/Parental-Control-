from plyer import notification
import smtplib
from email.message import EmailMessage
from utils.limits import load_limits

def notify_parent(context, app):
    print(f"[notify_parent] Fonksiyon çağrıldı - Context: {context}, App: {app}")

    # Bildirim göster
    try:
        notification.notify(
            title="⏰ Süre Limiti Aşıldı",
            message=f"{context.upper()} kategorisinde ({app}) kullanım limiti aşıldı!",
            timeout=10
        )
        print("🔔 Bildirim gösterildi.")
    except Exception as e:
        print(f"❌ Bildirim gösterilemedi: {e}")

    # E-posta gönder
    try:
        limits = load_limits()
        recipient = limits.get("parent_email", None)

        if not recipient:
            print("📭 Ebeveyn e-posta adresi tanımlı değil, e-posta gönderilmeyecek.")
            return

        email = EmailMessage()
        email["From"] = "mustafa8yildiz@gmail.com"
        email["To"] = recipient
        email["Subject"] = f"[Uyarı] Süre Limiti Aşıldı - {context.upper()}"

        email.set_content(f"""
Merhaba,

Çocuğunuz {context.upper()} kategorisindeki ({app}) uygulamasını izin verilen sürenin üzerinde kullandı.

Lütfen kontrol ediniz.

Parental Control Sistemi
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("mustafa8yildiz@gmail.com", "miiq bodi ldps iruo")
            smtp.send_message(email)

        print("📧 E-posta gönderildi.")
    except Exception as e:
        print(f"❌ E-posta gönderilemedi: {e}")
