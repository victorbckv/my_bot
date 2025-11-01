import telebot
from telebot import types

TOKEN = "8323792625:AAE-Z7cgncANZOQUlRBCx_qpqkBmJl8GuWM"

VIDEO_ID = "BAACAgUAAxkBAAIBbmkBsRPJsuENuJzxe38VTqAROoc5AALEGAACWSUQVPEi6bmpcyh1NgQ"

GROUP_LINK = "https://t.me/tribute/app?startapp=svnh"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_video(message):
    # Создаём кнопки
    markup = types.InlineKeyboardMarkup()
    join_btn = types.InlineKeyboardButton("💬 Перейти в группу", url=GROUP_LINK)
    markup.add(join_btn)

    # Отправляем видео
    bot.send_video(
        chat_id=message.chat.id,
        video=VIDEO_ID,
        caption="🎥 Посмотри видео и присоединяйся к нашей группе!",
        reply_markup=markup
    )

print("✅ Бот запущен. Ждём пользователей...")
bot.infinity_polling()
