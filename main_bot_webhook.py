import telebot
from telebot import types
from flask import Flask, request

# -------------------------------
# Вставь сюда свои данные
# -------------------------------
TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"  # токен твоего бота
VIDEO_ID = "BAACAgUAAxkBAAIBbmkBsRPJsuENuJzxe38VTqAROoc5AALEGAACWSUQVPEi6bmpcyh1NgQ"  # file_id видео
GROUP_LINK = "https://t.me/tribute/app?startapp=svnh"
WEBHOOK_URL = "https://my-bot2-iw21.onrender.com/bot"  # для Render
PORT = 10000
# -------------------------------

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- Telegram bot handler ---
@bot.message_handler(commands=['start'])
def send_video(message):
    markup = types.InlineKeyboardMarkup()
    join_btn = types.InlineKeyboardButton("💬 Перейти в группу", url=GROUP_LINK)
    markup.add(join_btn)

    bot.send_video(
        chat_id=message.chat.id,
        video=VIDEO_ID,
        caption="🎥 Посмотри видео и присоединяйся к нашей группе!",
        reply_markup=markup
    )

# --- Webhook route (для Render) ---
@app.route(f"/bot", methods=['POST'])
def webhook():
    json_data = request.get_json()
    if json_data:
        bot.process_new_updates([telebot.types.Update.de_json(json_data)])
    return "!", 200

# --- Healthcheck ---
@app.route("/", methods=['GET'])
def index():
    return "Bot is running!", 200

# --- Устанавливаем webhook прямо перед запуском Flask ---
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

# --- Запуск Flask ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)