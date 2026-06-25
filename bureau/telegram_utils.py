import telebot
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)


def send_order_notification(order):
    urgency = "🔥 Так" if order.is_urgent else "Ні"
    message = (
        f"Нове замовлення!\n\n"
        f"Клієнт: {order.client.name}\n"
        f"Email: {order.client.email}\n"
        f"Телефон: {order.client.phone}\n"
        f"Послуга: {order.service.name}\n"
        # f"Мова оригіналу: {order.source_language.name}\n"
        # f"Мова перекладу: {order.target_language.name}\n"
        f"Термінове: {urgency}\n"
        f"Коментар: {order.comment or '—'}\n"
        f"Статус: {order.status}"
    )

    bot.send_message(CHAT_ID, message)