import os
from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
VIDEO_FILE_ID = "BAACAgUAAxkBAAIB2Gkcf0DOXbRrzMHBCZKu7KE7mS6hAAIWHwACGh_gVGkJijD4_dr6NgQ"

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Проверка сервера
@app.route('/', methods=['GET'])
def index():
    return "Bot is running"

# Webhook для Telegram
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    if update.message:
        chat_id = update.message.chat.id
        # Отправляем видео с кнопкой
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Смотреть снова", callback_data="watch")]])
        bot.send_video(chat_id=chat_id, video=VIDEO_FILE_ID, reply_markup=keyboard)
    
    if update.callback_query:
        chat_id = update.callback_query.message.chat.id
        bot.send_message(chat_id=chat_id, text="Спасибо за просмотр!")

    return "OK", 200

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
