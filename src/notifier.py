import logging
from src.database import get_all_users
from src.poloniex_api import get_ticker_data
from src.data_processing import find_significant_drops
from src.telegram_bot import send_telegram_message

logger = logging.getLogger(__name__)

async def job():
    """
    Задача проверки тикеров каждый час.
    """
    logger.info("Запуск задачи проверки монет.")
    ticker_data = await get_ticker_data()
    if not ticker_data:
        logger.warning("Нет данных тикеров для обработки.")
        return

    users = get_all_users()
    for user in users:
        chat_id = user['chat_id']
        thresholds = user['thresholds']
        if not thresholds:
            continue

        new_drops, recovered_coins = await find_significant_drops(ticker_data, thresholds, chat_id)

        if new_drops:
            message = "📉 Найдены монеты с резким падением:\n"
            for threshold, coins in new_drops.items():
                message += f"\n🔹 Изменение более чем на {threshold}%:\n"
                for coin in coins:
                    message += f"• {coin['name']} - Объем торгов: {coin['volume']}\n"
            await send_telegram_message(chat_id, message)

        if recovered_coins:
            message = "📈 Монеты восстановились до исходного уровня или выше:\n"
            for coin in recovered_coins:
                message += f"• {coin}\n"
            await send_telegram_message(chat_id, message)
