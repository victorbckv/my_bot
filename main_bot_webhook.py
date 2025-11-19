from telegram import Bot, Update
from flask import Flask, request

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
VIDEO_ID = "BAACAgUAAxkBAAIB2Gkcf0DOXbRrzMHBCZKu7KE7mS6hAAIWHwACGh_gVGkJijD4_dr6NgQ"

app = Flask(__name__)
bot = Bot(token=TOKEN)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    async def handle():
        chat_id = update.effective_chat.id
        await bot.send_video(chat_id=chat_id, video=VIDEO_ID)

    import asyncio
    asyncio.run(handle())
    return "OK"


if __name__ == "__main__":
    import os
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
