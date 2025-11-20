from flask import Flask, request
import requests
import json

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
URL = f"https://api.telegram.org/bot{TOKEN}/"

VIDEO_ID = "AAMCBQADGQEAAgULaR62dTjHWgABfeXUj5cJ6d0Hn_UNAAI_FwACT_T5VPMGD-Q3sxA7AQAHbQADNgQ"

app = Flask(__name__)

def send_video(chat_id):
    text_after_video = (
        "Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое "
        "СТУДИЯ и что от неё ждать 🙂\n\n"
        "СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.\n"
        "В ней удобная навигация по контенту и великолепное качество самих видео.\n"
        "Все тренировки содержат в себе подробные инструкции и пояснения, а названия асан отмечены субтитрами."
    )

    button = {
        "inline_keyboard": [
            [
                {
                    "text": "Вступить в СТУДИЮ",
                    "url": "https://t.me/tribute/app?startapp=svnh"
                }
            ]
        ]
    }

    # 1) Отправляем видео (по file_id)
    requests.post(
        URL + "sendVideo",
        data={
            "chat_id": chat_id,
            "video": VIDEO_ID
        },
        timeout=30
    )

    # 2) Отправляем сообщение с кнопкой
    requests.post(
        URL + "sendMessage",
        data={
            "chat_id": chat_id,
            "text": text_after_video,
            "reply_markup": json.dumps(button)
        },
        timeout=15
    )

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    # проверяем, что это входящее сообщение с чатом
    if not data or "message" not in data or "chat" not in data["message"]:
        return "OK", 200

    # игнорируем сообщения, отправленные ботами
    from_user = data["message"].get("from", {})
    if from_user.get("is_bot"):
        return "OK", 200

    chat_id = data["message"]["chat"]["id"]
    send_video(chat_id)
    return "OK", 200

@app.route("/", methods=["GET", "HEAD"])
def index():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
