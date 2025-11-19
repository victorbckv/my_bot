from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
VIDEO_ID = "BAACAgIAAxkBAAECc-VgkQ1u7UJh8sMIpzYjS5Tzqn-9QAACZAADVp29Ck-dNyWZqgVZKQQ"  # Вставлен твой видео ID
bot = Bot(TOKEN)

app = Flask(__name__)

# Текст и кнопка
TEXT = """Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое СТУДИЯ и что от неё ждать 🙂

СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.
В ней удобная навигация по контенту и великолепное качество самих видео.
Все тренировки содержат в себе подробные инструкции и пояснения, а названия асан отмечены субтитрами.
"""

BUTTON_TEXT = "Вступить в СТУДИЮ"
BUTTON_URL = "https://t.me/tribute/app?startapp=svnh"

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(BUTTON_TEXT, url=BUTTON_URL)]
])

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id

    # Отправка сообщения и видео
    bot.send_message(chat_id=chat_id, text=TEXT, reply_markup=keyboard)
    bot.send_video(chat_id=chat_id, video=VIDEO_ID)
    return "OK"

if __name__ == "__main__":
    PORT = 10000
    app.run(host="0.0.0.0", port=PORT)
