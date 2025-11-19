from flask import Flask, request
import requests
import os

# --- ВАЖНО: токен бота (вставлен) ---
TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
TG_API = f"https://api.telegram.org/bot{TOKEN}"

# --- ВАЖНО: вставь сюда твой рабочий VIDEO_ID, если другой --- 
VIDEO_ID = "BAACAgIAAxkBAAIC3mdY1f-Tp5e1r-Py4-U_Yyq8ptLsAAL2RAACN0rRSd9Ps6Wl2jjVNgQ"

app = Flask(__name__)

TEXT = (
    "Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое СТУДИЯ и что от неё ждать 🙂\n\n"
    "СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.\n"
    "В ней удобная навигация по контенту и великолепное качество самих видео.\n"
    "Все тренировки содержат в себе подробные инструкции и пояснения, а названия асан отмечены субтитрами."
)

BUTTON = {
    "inline_keyboard": [
        [
            {"text": "Вступить в СТУДИЮ", "url": "https://t.me/tribute/app?startapp=svnh"}
        ]
    ]
}

def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup is not None:
        payload["reply_markup"] = reply_markup
    # timeout чтобы не вешаться
    requests.post(f"{TG_API}/sendMessage", json=payload, timeout=15)

def send_video(chat_id, video_id):
    payload = {"chat_id": chat_id, "video": video_id}
    requests.post(f"{TG_API}/sendVideo", json=payload, timeout=30)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    if not data:
        return "ok"
    # только для простых сообщений
    if "message" not in data:
        return "ok"
    try:
        chat_id = data["message"]["chat"]["id"]
    except Exception:
        return "ok"
    # Отправляем текст + кнопку и видео
    send_message(chat_id, TEXT, reply_markup=BUTTON)
    send_video(chat_id, VIDEO_ID)
    return "ok"

@app.route("/", methods=["GET", "HEAD"])
def index():
    return "ok", 200

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
