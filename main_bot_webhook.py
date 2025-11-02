import telebot
from flask import Flask, request
import os

TOKEN = os.environ.get("TOKEN", "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

WEBHOOK_URL = "https://my-bot-zw4o.onrender.com/bot"

# Устанавливаем вебхук
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)
print(f"Webhook установлен: {WEBHOOK_URL}")

# Обработка входящих апдейтов
@app.route("/bot", methods=["POST"])
def bot_webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    print(f"📩 Получено сообщение: {update.to_dict()}")  # <-- добавим лог
    bot.process_new_updates([update])
    return "OK", 200

# Реакция на /start
@bot.message_handler(commands=['start'])
def start_message(message):
    print(f"✅ Получен /start от {message.from_user.id}")
    bot.send_message(message.chat.id, "Привет! Бот работает ✅")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
