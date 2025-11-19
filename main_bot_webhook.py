from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Dispatcher, CommandHandler

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
VIDEO_ID = "BAACAgUAAxkBAAIB2Gkcf0DOXbRrzMHBCZKu7KE7mS6hAAIWHwACGh_gVGkJijD4_dr6NgQ"
bot = Bot(TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

def start(update: Update, context=None):
    chat_id = update.effective_chat.id
    text = (
        "Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое СТУДИЯ и что от неё ждать 🙂\n\n"
        "СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.\n"
        "В ней удобная навигация по контенту и великолепное качество самих видео.\n"
        "Все тренировки содержат в себе подробные инструкции и пояснения, а названия асан отмечены субтитрами."
    )
    button = InlineKeyboardButton("Вступить в СТУДИЮ", url="https://t.me/tribute/app?startapp=svnh")
    markup = InlineKeyboardMarkup([[button]])
    bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    bot.send_video(chat_id=chat_id, video=VIDEO_ID)

dispatcher.add_handler(CommandHandler("start", start))

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    import os
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
