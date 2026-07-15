import os

import telebot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(func=lambda message: True)
def show_chat_id(message):
    print("CHAT_ID:", message.chat.id)

    bot.reply_to(
        message,
        f"Ваш Telegram ID: {message.chat.id}"
    )


print("bot started")
bot.infinity_polling()