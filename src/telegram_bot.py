import logging
from telegram.ext import Updater
from src.config import TELEGRAM_BOT_TOKEN
from telegram import Bot
from telegram.ext import Updater, Queue
# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)

# Инициализация Updater
#updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
update_queue = Queue()
updater = Updater(bot=bot)

def send_telegram_message(chat_id, message):
    """
    Отправляет сообщение пользователю в Telegram.

    :param chat_id: ID чата пользователя
    :param message: Текст сообщения
    """
    try:
        updater.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения пользователю {chat_id}: {e}")
