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

# Путь для сохранения JSON-файла
JSON_FILE_PATH = 'poloniex_ticker_data.json'

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(RequestException),
    reraise=True
)
async def fetch_ticker_data():
    """
    Выполняет запрос к публичному API Poloniex для получения данных тикеров.
    :return: JSON-ответ от API
    :raises: RequestException, ValueError
    """
    url = POLONIEX_API_URL
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    response = requests.get(url, headers=headers, timeout=300)
    response.raise_for_status()
    return response.json()

async def get_ticker_data():
    """
    Получает данные о тикерах с Poloniex API с обработкой ошибок и повторными попытками.
    Сохраняет результат в JSON файл.
    :return: Словарь с данными тикеров или пустой словарь при ошибке.
    """
    try:
        data = await fetch_ticker_data()
        logger.info("Успешно получены данные тикеров с Poloniex.")

        # Сохранение JSON-ответа в файл
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Данные сохранены в файл {JSON_FILE_PATH}")

        return data
    except RequestException as e:
        logger.error(f"Ошибка при запросе к Poloniex API: {e}")
    except ValueError as e:
        logger.error(f"Ошибка декодирования JSON от Poloniex API: {e}")
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")

    return {}

def print_saved_ticker_data():
    """
    Чтение сохраненного JSON-файла и вывод содержимого в консоль.
    """
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("Содержимое JSON-ответа из файла:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
    except FileNotFoundError:
        logger.error(f"Файл {JSON_FILE_PATH} не найден.")
    except json.JSONDecodeError:
        logger.error(f"Ошибка при чтении или декодировании данных из файла {JSON_FILE_PATH}.")
    except Exception as e:
        logger.error(f"Неизвестная ошибка при чтении файла {JSON_FILE_PATH}: {e}")
