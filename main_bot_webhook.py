import os
import telebot
from flask import Flask, request

# Загружаем переменные среды
TOKEN = os.environ.get("TOKEN")
VIDEO_ID = os.environ.get("FILE_ID")
GROUP_LINK = os.environ.get("GROUP_LINK")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🎬 Смотреть видео", callback_data="watch"))
    bot.send_message(message.chat.id, "Привет! 👋 Нажми, чтобы посмотреть видео:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "watch")
def send_video(call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("💬 Перейти в группу", url=GROUP_LINK))
    bot.send_video(call.message.chat.id, VIDEO_ID, caption="Видео доступно прямо здесь 👇", reply_markup=markup)

@app.route('/')
def home():
    return "✅ Bot is running!", 200

if __name__ == "__main__":
    # Настраиваем webhook при запуске
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
    bot.remove_webhook()
    if WEBHOOK_URL:
        bot.set_webhook(url=WEBHOOK_URL)
        print(f"Webhook установлен: {WEBHOOK_URL}")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
