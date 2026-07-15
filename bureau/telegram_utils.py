import logging
import os
from pathlib import Path

import telebot
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_order_notification(order) -> None:


    if not BOT_TOKEN or not CHAT_ID:
        logger.warning(
            "Telegram notification skipped: BOT_TOKEN or CHAT_ID is missing"
        )
        return

    bot = telebot.TeleBot(BOT_TOKEN)

    urgency = "🔥 Так" if order.is_urgent else "Ні"
    comment = order.comment or "—"

    status = (
        order.get_status_display()
        if hasattr(order, "get_status_display")
        else order.status
    )

    message = (
        f"🆕 Нове замовлення №{order.id}\n\n"
        f"👤 Клієнт: {order.client.name}\n"
        f"📧 Email: {order.client.email}\n"
        f"📞 Телефон: {order.client.phone}\n\n"
        f"📋 Послуга: {order.service.name}\n"
        f"⚡ Термінове: {urgency}\n"
        f"💬 Коментар: {comment}\n"
        f"📌 Статус: {status}"
    )

    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
        )
    except Exception:
        logger.exception(
            "Failed to send Telegram notification for order %s",
            order.id,
        )
        return


    if not getattr(order, "file", None):
        return

    try:
        file_path = Path(order.file.path)

        if not file_path.exists():
            logger.error(
                "File for order %s does not exist: %s",
                order.id,
                file_path,
            )
            return

        with file_path.open("rb") as uploaded_file:
            bot.send_document(
                chat_id=CHAT_ID,
                document=uploaded_file,
                caption=f"📎 Файл до замовлення №{order.id}",
                visible_file_name=file_path.name,
            )

    except Exception:
        logger.exception(
            "Failed to send file for order %s",
            order.id,
        )