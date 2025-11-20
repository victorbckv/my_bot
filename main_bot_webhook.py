from flask import Flask, request
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"
CHAT_ID = 822726834
VIDEO_ID = "AAMCBQADGQEAAgULaR62dTjHWgABfeXUj5cJ6d0Hn_UNAAI_FwACT_T5VPMGD-Q3sxA7AQAHbQADNgQ"

app = Flask(__name__)
bot = Bot(TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Кнопка
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Вступить в СТУДИЮ", url="https://t.me/tribute/app?startapp=svnh")]])
    
    # Отправка видео
    bot.send_video(chat_id=CHAT_ID, video=VIDEO_ID)
    
    # Отправка сообщения с кнопкой
    bot.send_message(chat_id=CHAT_ID, text=(
        "Привет! Посмотри это 3х минутное ознакомительное видео, чтобы узнать что такое СТУДИЯ и что от неё ждать 🙂\n\n"
        "СТУДИЯ это онлайн платформа для практики йоги на базе ТЕЛЕГРАМ.\n"
        "В ней удобная навигация по контенту и великолепное качество самих видео.\n"
        "Все тренировки содержат в себе подробные инструкции и пояснения, а названия асан отмечены субтитрами."
    ), reply_markup=keyboard)
    
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
