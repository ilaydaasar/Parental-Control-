import os
import time
import datetime
import cv2
import numpy as np
import torch
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor

from utils.capture_screen import capture_screen, get_active_window_process_name, get_app_category, get_friendly_app_name
from models import yolo_model, violence_model, nlp_tokenizer, nlp_model, ocr_reader
from database import initialize_database, insert_log, insert_app_usage
from utils.limits import get_total_usage, is_time_exceeded
from utils.notify_parent import notify_parent

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

DANGEROUS_CLASSES = ["gun","knife"]
BAD_WORDS = ["piç", "amk", "yarrak", "sik", "göt", "orospu", "ananı", "siktir", "puşt", "mal", "gerizekalı", "salak", "aptal", "bok", "sikik"]
WHITELISTED_APPS = ["code.exe", "pycharm.exe", "sublime_text.exe", "windowsterminal.exe", "explorer.exe","winword.exe"]

# === VIOLENCE MODEL INPUT DETECTION ===
VIOLENCE_INPUT_SHAPE = violence_model.input_shape
if len(VIOLENCE_INPUT_SHAPE) == 5 and VIOLENCE_INPUT_SHAPE[-1] == 3:
    MAX_FRAMES = VIOLENCE_INPUT_SHAPE[1]
else:
    raise Exception("Beklenmeyen violence model input shape (sadece RAW frame destekleniyor)")

violence_window = []
THRESHOLD = 0.7  # <--- FIGHT ORANI BU DEĞERDEN YÜKSEKSE "VIOLENCE" DİYECEK

def detect_weapon(img, result):
    try:
        if img is None:
            print("❌ Weapon - Görüntü okunamadı.")
            result["weapon"] = False
            return
        with torch.no_grad():
            res = yolo_model(img)
        names = yolo_model.names
        found = False
        for r in res:
            for box in r.boxes:
                class_name = names[int(box.cls[0])].lower()
                conf_score = float(box.conf[0])
                print(f"Detected: {class_name} with conf={conf_score:.2f}")
                if any(d in class_name for d in DANGEROUS_CLASSES) and conf_score > 0.5:
                    found = True
        result["weapon"] = found
    except Exception as e:
        print("❌ Weapon detection error:", e)
        result["weapon"] = False            

def detect_violence(img, result):
    global violence_window
    try:
        if img is None:
            print("❌ Violence - Görüntü okunamadı.")
            result["violence"] = False
            return

        resized = cv2.resize(img, (224, 224)).astype(np.float32) / 255.0
        violence_window.append(resized)

        print(f"[DEBUG] Violence Window Length: {len(violence_window)} / {MAX_FRAMES}")
        frame_debug_dir = "violence_debug_frames"
        os.makedirs(frame_debug_dir, exist_ok=True)
        cv2.imwrite(os.path.join(frame_debug_dir, f"frame_{len(violence_window)}.png"), (resized * 255).astype(np.uint8))

        if len(violence_window) == MAX_FRAMES:
            clip = np.expand_dims(np.array(violence_window), axis=0)
            prediction = violence_model.predict(clip)
            print("Prediction array:", prediction[0])
            print("NO FIGHT (0):", prediction[0][0])
            print("FIGHT   (1):", prediction[0][1])

            fight_prob = prediction[0][1]
            print(f"[DEBUG] Violence Fight Score: {fight_prob:.4f}")
            # Farklı threshold aralıklarında sonucu yazdır
            for thresh in [0.2, 0.4, 0.6, 0.8]:
                durum = "YES" if fight_prob > thresh else "no"
                print(f"    > Threshold {thresh:.2f}: {durum}")
            result["violence"] = fight_prob > THRESHOLD
            violence_window.pop(0)
        else:
            result["violence"] = False
    except Exception as e:
        print("❌ Violence detection error:", e)
        result["violence"] = False

def detect_toxic_text(img, result):
    try:
        if img is None:
            print("❌ ToxicText - Görüntü okunamadı.")
            result["toxic"] = False
            return
        text = " ".join(ocr_reader.readtext(img, detail=0)).lower()
        print("📄 OCR sonucu:", text)
        found = [w for w in BAD_WORDS if w in text]
        inputs = nlp_tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
        nlp_model.eval()
        with torch.no_grad():
            outputs = nlp_model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        is_toxic = probs[0][1] > 0.85
        print("Toxic probs:", probs.tolist())
        print("Toxic skoru:", probs[0][1])
        print("🧠 NLP tahmini:", probs.tolist(), "| Toxic:", is_toxic)
        print("🧨 Bad words bulunanlar:", found)
        result["toxic"] = is_toxic or bool(found)
    except Exception as e:
        print("❌ Toxic text detection error:", e)
        result["toxic"] = False

def blur_and_save(img, image_path):
    if img is not None:
        blurred = cv2.GaussianBlur(img, (99, 99), 30)
        os.makedirs("flagged", exist_ok=True)
        fname = os.path.basename(image_path)
        save_path = f"flagged/blurred_{fname}"
        cv2.imwrite(save_path, blurred)

def run_analysis():
    initialize_database()

    process_name, window_title = get_active_window_process_name()
    friendly_app_name = get_friendly_app_name(process_name, window_title)
    current_context = get_app_category(process_name, window_title)
    current_app = friendly_app_name
    start_time = datetime.datetime.now()

    frame_count = 0

    while True:
        try:
            process_name, window_title = get_active_window_process_name()
            if process_name.lower() in WHITELISTED_APPS:
                print(f"⛔ Beyaz listedeki uygulama açık ({process_name}), analiz yapılmadı.")
                violence_window.clear()
                time.sleep(3)
                continue

            path = capture_screen()
            img = cv2.imread(path)
            result_dict = {}

            context = get_app_category(process_name, window_title)
            run_ocr = (context == "chat") or (frame_count % 10 == 0)

            with ThreadPoolExecutor() as executor:
                fut_weapon = executor.submit(detect_weapon, img, result_dict)
                fut_violence = executor.submit(detect_violence, img, result_dict)
                if run_ocr:
                    fut_toxic = executor.submit(detect_toxic_text, img, result_dict)
                else:
                    result_dict["toxic"] = False

                fut_weapon.result()
                fut_violence.result()
                if run_ocr:
                    fut_toxic.result()

            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            friendly_app_name = get_friendly_app_name(process_name, window_title)
            context = get_app_category(process_name, window_title)

            score = 0
            if result_dict["weapon"]: score += 1 if context == "game" else 3
            if result_dict["violence"]: score += 3
            if result_dict["toxic"]: score += 3 if context == "chat" else 1

            print(f"\n🕵️ {now} | App: {friendly_app_name} | Context: {context} | "
                  f"Risk: {score} | Silah: {result_dict['weapon']} | Şiddet: {result_dict['violence']} | Küfür: {result_dict['toxic']}")
            sys.stdout.flush()

            if score >= 3:
                blur_and_save(img, path)
                print("⚠️ Tehlikeli içerik bulundu, sansür uygulandı.")
            else:
                print("✅ Güvenli içerik.")

            insert_log(now, path, friendly_app_name, context, score,
                       result_dict["weapon"], result_dict["violence"], result_dict["toxic"])

            now_time = datetime.datetime.now()
            duration = (now_time - start_time).total_seconds()

            if friendly_app_name != current_app or context != current_context or duration >= 60:
                insert_app_usage(current_app, current_context,
                                 start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                 now_time.strftime('%Y-%m-%d %H:%M:%S'),
                                 int(duration))
                start_time = now_time
                current_app = friendly_app_name
                current_context = context

            total_used = get_total_usage(context)
            exceeded, action = is_time_exceeded(context, total_used)
            print(f"[LİMİT TESTİ] Kullanım: {total_used}s | Kategori: {context}")

            if exceeded:
                print(f"[LİMİT AŞILDI] Bildirim gönderiliyor ({action})")
                notify_parent(context, friendly_app_name)

            frame_count += 1
            time.sleep(1)

        except Exception as e:
            print(f"❌ Genel hata: {e}")
            traceback.print_exc()
            sys.stdout.flush()
