import os
from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

# -----------------------------
# ЗАМЕНИ СВОЙ ТОКЕН И FILE_ID
TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
GROUP_URL = "https://t.me/tribute/app?startapp=svnh"
VIDEO_FILE_ID = "BAACAgUAAxkBAAIB2Gkcf0DOXbRrzMHBCZKu7KE7mS6hAAIWHwACGh_gVGkJijD4_dr6NgQ"
# -----------------------------

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

# -----------------------------
# Команды бота
def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("Перейти в группу", url=GROUP_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_video(VIDEO_FILE_ID, reply_markup=reply_markup)

# Регистрация обработчика
dispatcher.add_handler(CommandHandler("start", start))

# -----------------------------
# Webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# -----------------------------
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
