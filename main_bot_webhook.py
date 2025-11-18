import os
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup

# Токен твоего бота
TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
bot = Bot(token=TOKEN)

# Ссылка на группу (тебе нужно её использовать в кнопке)
GROUP_URL = "https://t.me/tribute/app?startapp=svnh"

# file_id нового видео
FILE_ID = "BAACAgUAAxkBAAIB2Gkcf0DOXbRrzMHBCZKu7KE7mS6hAAIWHwACGh_gVGkJijD4_dr6NgQ"

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id if update.message else None
    if chat_id:
        bot.send_video(chat_id=chat_id, video=FILE_ID)
        bot.send_message(
            chat_id=chat_id,
            text="Нажми кнопку чтобы перейти в группу",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Перейти в группу", url=GROUP_URL)]]
            )
        )
    return "ok"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
