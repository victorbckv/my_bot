from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
import asyncio
import os

# ======== НАСТРОЙКИ (уже подставлены) ========
TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
VIDEO_ID = "BAACAgUAAxkBAAIB2Gkcf0DOXbRrzMHBCZKu7KE7mS6hAAIWHwACGh_gVGkJijD4_dr6NgQ"
GROUP_URL = "https://t.me/tribute/app?startapp=svnh"
# =============================================

WELCOME_TEXT = (
    "Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое "
    "СТУДИЯ и что от неё ждать 🙂\n\n"
    "СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.\n"
    "В ней удобная навигация по контенту и великолепное качество самих видео.\n"
    "Все тренировки содержат в себе подробные инструкции и пояснения, а названия асан "
    "отмечены субтитрами."
)

BUTTON_TEXT = "Вступить в СТУДИЮ"

app = Flask(__name__)
bot = Bot(token=TOKEN)

# --- отвечает на GET и HEAD для пинга (UptimeRobot / Render) ---
@app.route("/", methods=["GET", "HEAD"])
def home():
    # для HEAD тело пустое, вернём 200
    if request.method == "HEAD":
        return "", 200
    # для GET можно вернуть короткий текст
    return "Bot is running", 200

# --- webhook на путь /<TOKEN> ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)

    async def handle_update(upd: Update):
        # если пришло сообщение (например /start)
        if upd.message:
            chat_id = upd.message.chat.id
            # отправляем сначала текст
            await bot.send_message(chat_id=chat_id, text=WELCOME_TEXT)
            # затем видео с кнопкой
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(BUTTON_TEXT, url=GROUP_URL)]])
            await bot.send_video(chat_id=chat_id, video=VIDEO_ID, reply_markup=keyboard)
        # если пришёл callback_query (если понадобятся)
        elif upd.callback_query:
            cid = upd.callback_query.message.chat.id
            await bot.send_message(chat_id=cid, text="Спасибо!")

    # запускаем асинхронную обработку синхронно
    try:
        asyncio.run(handle_update(update))
    except RuntimeError:
        # если asyncio.run не может запуститься (редкие окружения), используем альтернативу
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(handle_update(update))
        finally:
            loop.close()

    return "OK", 200

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
