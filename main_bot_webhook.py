import os
import time
from flask import Flask, request
import telebot

TOKEN = os.environ.get("TOKEN")
VIDEO_FILE_ID = "BAACAgUAAxkBAAIBbmkBsRPJsuENuJzxe38VTqAROoc5AALEGAACWSUQVPEi6bmpcyh1NgQ"
GROUP_LINK = "https://t.me/tribute/app?startapp=svnh"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === Команда /start ===
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    # 1️⃣ Отправляем видео с подписью
    bot.send_video(
        chat_id,
        VIDEO_FILE_ID,
        caption="🎥 Посмотри это короткое 4-минутное видео, чтобы понять, что тебя ждёт в студии!"
    )

    # 2️⃣ Небольшая пауза, чтобы Telegram не проглотил второе сообщение
    time.sleep(0.7)

    # 3️⃣ Кнопка и текст под видео
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("Войти в СТУДИЮ 🧘‍♂️", url=GROUP_LINK)
    markup.add(btn)

    bot.send_message(chat_id, "Жми сюда, чтобы присоединиться 👇", reply_markup=markup)


# === Любое другое сообщение ===
@bot.message_handler(func=lambda msg: True)
def echo_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Чтобы начать, нажми /start 🔹")


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
