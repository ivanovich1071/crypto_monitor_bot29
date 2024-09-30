import logging
import asyncio
from src.config import TELEGRAM_BOT_TOKEN
from src.handlers import setup_handlers
from src.database import init_db
from src.notifier import job
import schedule
from telegram.ext import Application

async def main():
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

    # Инициализация бота через Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Инициализация приложения (обязательный шаг в версии 21.x)
    await application.initialize()

    # Настройка обработчиков
    setup_handlers(application)

    # Запуск бота
    await application.start()
    logger.info("Бот запущен.")

    # Настройка планировщика задач
    schedule.every(15).minutes.do(job)

    try:
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await application.stop()
        logger.info("Бот остановлен.")

if __name__ == "__main__":
    asyncio.run(main())
