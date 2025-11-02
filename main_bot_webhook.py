import os
from flask import Flask, request
import telebot

TOKEN = os.environ.get("TOKEN")
VIDEO_FILE_ID = "BAACAgUAAxkBAAIBbmkBsRPJsuENuJzxe38VTqAROoc5AALEGAACWSUQVPEi6bmpcyh1NgQ"
GROUP_LINK = "https://t.me/tribute/app?startapp=svnh"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === Обработка команды /start ===
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🎬 Привет! Сейчас отправлю тебе видео...")

    # Отправляем видео
    try:
        bot.send_video(chat_id, VIDEO_FILE_ID, caption="✨ Смотри видео и потом заходи в студию!")
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Ошибка при отправке видео: {e}")

    # Добавляем кнопку
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("🎧 Войти в студию", url=GROUP_LINK)
    markup.add(btn)

    bot.send_message(chat_id, "👇 Нажми, чтобы войти:", reply_markup=markup)


# === Webhook ===
@app.route("/bot", methods=["POST"])
def bot_webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200


@app.route("/")
def home():
    return "Бот работает", 200


if __name__ == "__main__":
    url = "https://my-bot-zw4o.onrender.com/bot"
    bot.remove_webhook()
    bot.set_webhook(url=url)
    print(f"Webhook установлен: {url}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
