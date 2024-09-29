import logging
from src.config import TELEGRAM_BOT_TOKEN
from src.handlers import setup_handlers
from src.database import init_db
from src.notifier import job
import schedule
import time

def main():
    # Настройка логирования
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    # Инициализация базы данных
    init_db()

    # Настройка бота
    from src.telegram_bot import updater
    setup_handlers(updater)

    # Запуск бота
    updater.start_polling()
    logger.info("Бот запущен.")

    # Настройка планировщика задач
    schedule.every(15).minutes.do(job)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        updater.stop()
        logger.info("Бот остановлен.")

if __name__ == "__main__":
    main()
