from flask import Flask, request
import telebot
import os
import json

# === Настройки из переменных окружения ===
TOKEN = os.environ.get("TOKEN")
VIDEO_FILE_ID = os.environ.get("VIDEO_FILE_ID")
GROUP_LINK = os.environ.get("GROUP_LINK")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === Устанавливаем webhook ===
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)
print(f"Webhook установлен: {WEBHOOK_URL}")

# === Обработка POST-запросов от Telegram ===
@app.route("/bot", methods=["POST"])
def webhook():
    try:
        json_string = request.get_data().decode("utf-8")
        print("Получен апдейт от Telegram:", json_string)  # логируем всё, что приходит
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
    except Exception as e:
        print(f"Ошибка при обработке апдейта: {e}")
    return "OK", 200

# === Обработка команды /start ===
@bot.message_handler(commands=["start"])
def start(message):
    try:
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton("🎧 Войти в студию", url=GROUP_LINK)
        markup.add(btn)

        bot.send_video(
            chat_id=message.chat.id,
            data=VIDEO_FILE_ID,
            caption="Привет! 👋 Добро пожаловать в студию 🎬\nНажми кнопку ниже, чтобы войти 👇",
            reply_markup=markup
        )
        print(f"Отправлено видео пользователю: {message.chat.id}")
    except Exception as e:
        print(f"Ошибка при отправке видео: {e}")

# === Проверка, что сервер жив ===
@app.route("/", methods=["GET"])
def index():
    return "Бот работает через Render!", 200

# === Запуск Flask ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
