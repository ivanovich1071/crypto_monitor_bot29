import logging
from src.database import get_dropped_coins, add_dropped_coin, remove_dropped_coin
from src.telegram_bot import send_telegram_message  # Импортируем функцию отправки сообщений
from src.config import POLONIEX_API_URL

logger = logging.getLogger(__name__)


async def find_significant_drops(ticker_data, user_thresholds, chat_id):
    """
    Найти монеты с падением на заданные пороги и обнаружить их восстановление, с отправкой уведомлений.

    :param ticker_data: Данные тикера Poloniex
    :param user_thresholds: Список порогов (например, [50, 30, 10])
    :param chat_id: ID пользователя
    :return: два словаря: new_drops и recovered_coins
    """
    new_drops = {}  # {threshold: [coin1, coin2, ...]}
    recovered_coins = []  # [coin1, coin2, ...]

    # Получаем список ранее отслеживаемых упавших монет для пользователя
    dropped_coins = get_dropped_coins(chat_id)
    dropped_coins_dict = {coin.coin: coin.threshold for coin in dropped_coins}

    for coin, data in ticker_data.items():
        try:
            percent_change = float(data.get("percentChange", "0"))
            volume = data.get("baseVolume", "0")

            # Проверка на значительное падение
            for threshold in user_thresholds:
                if percent_change <= -threshold:
                    # Проверяем, отслеживается ли уже падение этого монеты на данном пороге
                    if coin not in dropped_coins_dict or dropped_coins_dict[coin] < threshold:
                        # Добавляем монету в отслеживаемые падения
                        add_dropped_coin(chat_id, coin, threshold)
                        # Добавляем в новые падения
                        new_drops.setdefault(threshold, []).append({
                            "name": coin,
                            "volume": volume
                        })
                        logger.info(f"Монета {coin} упала на {threshold}%, добавлена в отслеживаемые.")

                    # Отправляем уведомление о новом падении
                    message = f"📉 Монета {coin} упала более чем на {threshold}%.\nОбъем торгов: {volume}"
                    await send_telegram_message(chat_id, message)
                    logger.info(f"Отправлено уведомление о падении {coin} на {threshold}% для пользователя {chat_id}.")

                    break  # Если монета уже добавлена для более высокого порога, не добавляем для меньших

            # Проверка на восстановление
            if percent_change >= 0:
                if coin in dropped_coins_dict:
                    # Монета восстановилась
                    remove_dropped_coin(chat_id, coin)
                    recovered_coins.append(coin)
                    logger.info(f"Монета {coin} восстановилась до исходного уровня.")
        except ValueError:
            logger.error(f"Ошибка обработки данных для монеты {coin}.")
            continue

    # Возвращаем результаты
    return new_drops, recovered_coins
