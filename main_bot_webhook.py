from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
import asyncio
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(TOKEN)

VIDEO_ID = "BAACAgIAAxkBAAMJZ1y9YuYg3-b0q87Um1nfTeplcN2bAAIeMwACwOAASvQw7rYAIH9wNQQ"  
BUTTON_URL = "https://t.me/tribute/app?startapp=svnh"

app = Flask(__name__)


# Главная страница — отвечает 200 и на GET, и на HEAD
@app.route("/", methods=["GET", "HEAD"])
def index():
    return "OK", 200


# Webhook обработчик
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return "no data", 200

    update = Update.de_json(data, bot)

    if update.message:
        chat_id = update.message.chat_id

        asyncio.run(bot.send_message(
            chat_id=chat_id,
            text=(
                "Привет! Посмотри это 3х минутное ознакомительное видео, "
                "чтобы узнать что такое СТУДИЯ и что от неё ждать 🙂\n\n"
                "СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.\n"
                "В ней удобная навигация по контенту и великолепное качество самих видео.\n"
                "Все тренировки содержат в себе подробные инструкции и пояснения, "
                "а названия асан отмечены субтитрами."
            ),
            parse_mode=ParseMode.HTML
        ))

        asyncio.run(bot.send_video(chat_id=chat_id, video=VIDEO_ID))

        keyboard = [[InlineKeyboardButton("ВСТУПИТЬ В СТУДИЮ", url=BUTTON_URL)]]
        markup = InlineKeyboardMarkup(keyboard)

        asyncio.run(bot.send_message(chat_id=chat_id, text="Нажми, чтобы перейти 👇", reply_markup=markup))

    return "ok", 200


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
