from flask import Flask, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, ContextTypes, CommandHandler
import asyncio
import os

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
VIDEO_ID = "ВАШ_ВИДЕО_ID_СЮДА"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()
application.initialize()

async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = (
        "Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое СТУДИЯ и что от неё ждать 🙂\n\n"
        "СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.\n"
        "В ней удобная навигация по контенту и великолепное качество самих видео.\n"
        "Все тренировки содержат в себе подробные инструкции и пояснения, а названия асан отмечены субтитрами."
    )
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Вступить в СТУДИЮ", url="https://t.me/tribute/app?startapp=svnh")]]
    )
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
    await context.bot.send_video(chat_id=chat_id, video=VIDEO_ID)

application.add_handler(CommandHandler("start", send_welcome))

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        asyncio.create_task(application.process_update(update))
        return "OK"
    except Exception as e:
        print("Webhook error:", e)
        return "Error", 500

@app.route("/", methods=["GET", "HEAD"])
def index():
    return "Bot is running", 200

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
