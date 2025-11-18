from flask import Flask, request
from telegram import Bot, Update
import telegram
import os

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
VIDEO_ID = "BAACAgUAAxkBAAIB2Gkcf0DOXbRrzMHBCZKu7KE7mS6hAAIWHwACGh_gVGkJijD4_dr6NgQ"  # твой видео ID

bot = Bot(TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message:
        chat_id = update.message.chat.id
        bot.send_video(chat_id=chat_id, video=VIDEO_ID)
    return "ok"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
