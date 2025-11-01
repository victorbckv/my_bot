import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import telebot
from telebot import types

# 🔹 Берём данные из переменных среды
TOKEN = os.environ["TOKEN"]
VIDEO_ID = os.environ["FILE_ID"]
GROUP_LINK = os.environ["GROUP_LINK"]

bot = telebot.TeleBot(TOKEN)

# --- Telegram bot ---
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

# Запускаем бота в отдельном потоке
threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()

# --- Минималистичный HTTP сервер ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

server = HTTPServer(("0.0.0.0", 10000), SimpleHandler)
server.serve_forever()
