from flask import Flask, request
import telebot
import os

# Токен из переменных окружения
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Твой file_id и ссылка
VIDEO_FILE_ID = os.environ.get("VIDEO_FILE_ID")
GROUP_LINK = os.environ.get("GROUP_LINK")

app = Flask(__name__)

# Устанавливаем webhook при запуске
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)
print(f"Webhook установлен: {WEBHOOK_URL}")

# Обработка запроса от Telegram
@app.route("/bot", methods=["POST"])
def webhook():
    update = request.get_json(force=True)
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

# Когда пользователь нажимает /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    # Создаём кнопку
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("🎧 Войти в студию", url=GROUP_LINK)
    markup.add(btn)

    # Отправляем видео и сообщение
    bot.send_video(
        message.chat.id,
        VIDEO_FILE_ID,
        caption="Добро пожаловать в студию 🎬\n\nНажми кнопку ниже, чтобы войти 👇",
        reply_markup=markup
    )

@app.route("/", methods=["GET"])
def index():
    return "Бот запущен и работает через Render!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
