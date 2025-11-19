import os
from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update

TOKEN = os.environ.get("BOT_TOKEN")
VIDEO_ID = "BAACAgUAAxkBAAIB2Gkcf0DOXbRrzMHBCZKu7KE7mS6hAAIWHwACGh_gVGkJijD4_dr6NgQ"

bot = Bot(TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = (
        "Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое СТУДИЯ и что от неё ждать 🙂\n\n"
        "СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.\n"
        "В ней удобная навигация по контенту и великолепное качество самих видео.\n"
        "Все тренировки содержат в себе подробные инструкции и пояснения, а названия асан отмечены субтитрами."
    )
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Вступить в СТУДИЮ", url="https://t.me/tribute/app?startapp=svnh")]])
    bot.send_message(chat_id=chat_id, text=message_text)
    bot.send_video(chat_id=chat_id, video=VIDEO_ID)
    bot.send_message(chat_id=chat_id, text=" ", reply_markup=keyboard)
    return "OK"

@app.route("/", methods=["GET", "HEAD"])
def index():
    return "OK"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
