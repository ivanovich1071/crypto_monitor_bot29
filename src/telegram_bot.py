import logging
from telegram.ext import Application
from src.config import TELEGRAM_BOT_TOKEN

# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)

# Инициализация Application
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

def send_telegram_message(chat_id, message):
    """
    Отправляет сообщение пользователю в Telegram.

    :param chat_id: ID чата пользователя
    :param message: Текст сообщения
    """
    try:
        application.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения пользователю {chat_id}: {e}")
