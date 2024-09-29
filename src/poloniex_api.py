import requests
import logging
from src.config import POLONIEX_API_URL
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

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
    Выполняет запрос к Poloniex API для получения данных тикеров.
    :return: JSON-ответ от API
    :raises: RequestException, ValueError
    """
    url = f"{POLONIEX_API_URL}?command=returnTicker"
    response = requests.get(url, timeout=10)
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
        return data
    except RequestException as e:
        logger.error(f"Ошибка при запросе к Poloniex API после повторных попыток: {e}")
    except ValueError as e:
        logger.error(f"Ошибка декодирования JSON от Poloniex API: {e}")
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")

    # Возврат пустого словаря в случае ошибки
    return {}
