from flask import Flask, request
import telebot
import os
import json

TOKEN = os.environ.get("TOKEN")
VIDEO_FILE_ID = os.environ.get("VIDEO_FILE_ID")
GROUP_LINK = os.environ.get("GROUP_LINK")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Устанавливаем webhook
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)
print(f"Webhook установлен: {WEBHOOK_URL}")

@app.route("/bot", methods=["POST"])
def webhook():
    # Принимаем апдейты от Telegram
    try:
        update_data = request.stream.read().decode("utf-8")
        update_dict = json.loads(update_data)
        update = telebot.types.Update.de_json(update_dict)
        bot.process_new_updates([update])
    except Exception as e:
        print(f"Ошибка при обработке апдейта: {e}")
    return "OK", 200

@bot.message_handler(commands=["start"])
def send_welcome(message):
    try:
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton("🎧 Войти в студию", url=GROUP_LINK)
        markup.add(btn)

        bot.send_video(
            message.chat.id,
            VIDEO_FILE_ID,
            caption="Привет! 👋 Добро пожаловать в студию 🎬\n\nНажми кнопку ниже, чтобы войти 👇",
            reply_markup=markup
        )
    except Exception as e:
        print(f"Ошибка при отправке видео: {e}")

@app.route("/", methods=["GET"])
def index():
    return "Бот работает через Render!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
