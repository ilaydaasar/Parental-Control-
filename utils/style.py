import os 
def apply_stylesheet(app, path="style.qss"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            style = f.read()
            app.setStyleSheet(style)
            print("✅ Stil başarıyla yüklendi.")
    except FileNotFoundError:
        print("⚠️ style.qss dosyası bulunamadı. Varsayılan stil kullanılacak.")
