from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
import os
import asyncio

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
VIDEO_ID = "BAACAgUAAxkBAAICCGkeKi_UN9CKIgPEpEgIiLA3gjHmAAKUFg"
CHANNEL_URL = "https://t.me/tribute/app?startapp=svnh"

bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "No data", 400
    update = Update.de_json(data, bot)
    chat_id = update.message.chat.id if update.message else None
    if chat_id:
        text = (
            "Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое СТУДИЯ и что от неё ждать 🙂\n\n"
            "СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.\n"
            "В ней удобная навигация по контенту и великолепное качество самих видео.\n"
            "Все тренировки содержат в себе подробные инструкции и пояснения, а названия асан отмечены субтитрами."
        )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Вступить в СТУДИЮ", url=CHANNEL_URL)]])
        asyncio.run(bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard))
        asyncio.run(bot.send_video(chat_id=chat_id, video=VIDEO_ID))
    return "OK", 200

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
