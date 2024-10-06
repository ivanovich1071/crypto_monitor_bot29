import requests
import logging
import json
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

POLONIEX_API_URL = os.getenv('POLONIEX_API_URL')

# Настройка логирования для этого модуля
logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(RequestException),
    reraise=True
)
def fetch_ticker_data():
    """
    Выполняет запрос к публичному API Poloniex для получения данных тикеров.
    :return: JSON-ответ от API
    :raises: RequestException, ValueError
    """
    url = POLONIEX_API_URL  # Используем URL для тикеров
    headers = {
        'User-Agent': 'Mozilla/5.0',  # Добавляем заголовок User-Agent
    }
    response = requests.get(url, headers=headers, timeout=300)
    response.raise_for_status()
    return response.json()

def get_ticker_data():
    """
    Получает данные о тикерах с Poloniex API с обработкой ошибок и повторными попытками.
    :return: Словарь с данными тикеров или пустой словарь при ошибке.
    """
    try:
        data = fetch_ticker_data()
        logger.info("Успешно получены данные тикеров с Poloniex.")

        # Выводим данные в консоль для проверки
        print("Содержимое JSON-ответа:")
        print(json.dumps(data, indent=4))  # Красивый вывод JSON с отступами

        return data
    except RequestException as e:
        logger.error(f"Ошибка при запросе к Poloniex API: {e}")
    except ValueError as e:
        logger.error(f"Ошибка декодирования JSON от Poloniex API: {e}")
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")

    # Возврат пустого словаря в случае ошибки
    return {}

if __name__ == "__main__":
    # Пример вызова функции для получения данных тикеров
    get_ticker_data()
