from flask import Flask, request
import requests
import os

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
VIDEO_ID = "BAACAgIAAxkBAAIBAWcoFBD6j8_7cYV4I5-hxvOz0wABHQACV-k4SvgwhMsuHizJxkUEAE"  # <-- твой видео айди
TG_API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": reply_markup
    }
    requests.post(f"{TG_API}/sendMessage", json=payload)

def send_video(chat_id, video):
    payload = {
        "chat_id": chat_id,
        "video": video
    }
    requests.post(f"{TG_API}/sendVideo", json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.json

    if "message" not in update:
        return "ok"

    chat_id = update["message"]["chat"]["id"]

    text = (
        "Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое "
        "СТУДИЯ и что от неё ждать 🙂\n\n"
        "СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.\n"
        "В ней удобная навигация по контенту и великолепное качество самих видео.\n"
        "Все тренировки содержат в себе подробные инструкции и пояснения, а названия "
        "асан отмечены субтитрами."
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Вступить в СТУДИЮ", "url": "https://t.me/tribute/app?startapp=svnh"}
            ]
        ]
    }

    send_message(chat_id, text, reply_markup=keyboard)
    send_video(chat_id, VIDEO_ID)

    return "ok"

@app.route("/")
def home():
    return "ok"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
