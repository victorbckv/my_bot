from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, request

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
VIDEO_ID = "BAACAgUAAxkBAAIB2Gkcf0DOXbRrzMHBCZKu7KE7mS6hAAIWHwACGh_gVGkJijD4_dr6NgQ"

WELCOME_TEXT = (
    "Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое "
    "СТУДИЯ и что от неё ждать 🙂\n\n"
    "СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.\n"
    "В ней удобная навигация по контенту и великолепное качество самих видео.\n"
    "Все тренировки содержат в себе подробные инструкции и пояснения, а названия асан "
    "отмечены субтитрами."
)

BUTTON_TEXT = "Вступить в СТУДИЮ"
BUTTON_URL = "https://t.me/+9Y-8uO2B24w1ZjRi"  # ← сюда вставь нужную ссылку

app = Flask(__name__)
bot = Bot(token=TOKEN)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    async def handle():
        chat_id = update.effective_chat.id

        # Кнопка
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(BUTTON_TEXT, url=BUTTON_URL)]
        ])

        # Сначала текст
        await bot.send_message(chat_id=chat_id, text=WELCOME_TEXT)

        # Потом видео + кнопка
        await bot.send_video(chat_id=chat_id, video=VIDEO_ID, reply_markup=keyboard)

    import asyncio
    asyncio.run(handle())
    return "OK"


if __name__ == "__main__":
    import os
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
