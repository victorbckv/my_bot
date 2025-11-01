import os
from flask import Flask, request
import telebot
from telebot import types

# Переменные среды
TOKEN = os.environ["TOKEN"]
VIDEO_ID = os.environ["FILE_ID"]
GROUP_LINK = os.environ["GROUP_LINK"]

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

# --- Webhook route ---
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

# --- Set webhook when service starts ---
@app.before_first_request
def setup_webhook():
    url = os.environ["WEBHOOK_URL"]  # например: https://my-bot2-iw21.onrender.com/bot
    bot.remove_webhook()
    bot.set_webhook(url=url)

# --- Run Flask ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
