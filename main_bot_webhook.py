from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
VIDEO_ID = "ВАШ_ВИДЕО_ID"  # <-- вставь сюда ID видео
TEXT = """Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое СТУДИЯ и что от неё ждать 🙂

СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.
В ней удобная навигация по контенту и великолепное качество самих видео.
Все тренировки содержат в себе подробные инструкции и пояснения, а названия асан отмечены субтитрами."""

# Кнопка
keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Вступить в СТУДИЮ", url="https://t.me/tribute/app?startapp=svnh")]]
)

app = Flask(__name__)
bot = Bot(TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id

    # Отправляем сообщение с кнопкой
    bot.send_message(chat_id=chat_id, text=TEXT, reply_markup=keyboard)

    # Отправляем видео
    bot.send_video(chat_id=chat_id, video=VIDEO_ID)
    return "OK"

if __name__ == "__main__":
    PORT = 10000
    app.run(host="0.0.0.0", port=PORT)
