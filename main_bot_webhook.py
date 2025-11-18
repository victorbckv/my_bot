import os
from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import TelegramError

app = Flask(__name__)

# ---------------------------------------
# 🔧 Настройки
# ---------------------------------------

TOKEN = os.getenv("TELEGRAM_TOKEN", "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM")
GROUP_LINK = os.getenv("GROUP_LINK", "https://t.me/+y6d1Q11HWGg5OWI6")
VIDEO_FILE_ID = os.getenv(
    "VIDEO_FILE_ID",
    "BAACAgUAAxkBAAIB2Gkcf0DOXbRrzMHBCZKu7KE7mS6hAAIWHwACGh_gVGkJijD4_dr6NgQ"
)

bot = Bot(TOKEN)


# ---------------------------------------
# 📌 Webhook endpoint
# ---------------------------------------
@app.route(f"/bot", methods=["POST"])
def bot_webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    try:
        if update.message:
            handle_message(update.message)

        if update.callback_query:
            handle_callback(update.callback_query)

    except TelegramError as e:
        print("Ошибка Telegram:", e)
    except Exception as e:
        print("Ошибка сервера:", e)

    return "OK", 200


# ---------------------------------------
# 📨 Обработка входящих сообщений
# ---------------------------------------
def handle_message(message):
    chat_id = message.chat_id

    # Сразу отправляем видео
    bot.send_video(
        chat_id=chat_id,
        video=VIDEO_FILE_ID,
        caption="🎥 Посмотри короткое 4-минутное видео, чтобы понять, что тебя ждёт в студии!"
    )

    # Следом отправляем кнопку "Войти в студию"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🧘‍♂️ Войти в СТУДИЮ", url=GROUP_LINK)]]
    )

    bot.send_message(
        chat_id=chat_id,
        text="Готов начать? Жми ниже 👇",
        reply_markup=keyboard
    )


# ---------------------------------------
# 🔘 Обработка callback-кнопок (если будут)
# ---------------------------------------
def handle_callback(callback):
    callback.answer()


# ---------------------------------------
# 🚀 Проверка
# ---------------------------------------
@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200


# ---------------------------------------
# ▶️ Запуск
# ---------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
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
