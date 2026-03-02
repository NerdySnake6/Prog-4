import requests
import logging
from typing import List, Dict, Optional, Callable
from functools import wraps
from decorators import serialize_output

# Настройка логирования
def setup_logging():
    """Настройка конфигурации логирования."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('currency_rates.log', encoding='utf-8')
        ]
    )

def log_errors(func: Callable) -> Callable:
    """
    Декоратор для логирования ошибок с использованием модуля logging.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка запроса к API: {e}")
            return None
        except KeyError as e:
            if str(e) == "'Valute'":
                logging.error("В ответе API отсутствует ключ 'Valute'")
            else:
                currency_code = str(e).strip("'")
                logging.error(f"Валюта '{currency_code}' не найдена в ответе API")
            return None
        except Exception as e:
            logging.error(f"Неожиданная ошибка: {e}", exc_info=True)
            return None
    return wrapper

@log_errors
@serialize_output(format_name='json')  # По умолчанию JSON
def get_currencies(
    currency_codes: List[str], 
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
    output_format: str = 'json'  # Можно переопределить при вызове
) -> Optional[Dict[str, float]]:
    """
    Получает курсы валют из API ЦБ РФ.
    
    Args:
        currency_codes: Список кодов валют (например, ['USD', 'EUR'])
        url: URL API ЦБ РФ
        output_format: Формат вывода (json, yaml, csv)
    
    Returns:
        Словарь с курсами валют, сериализованная строка или None в случае ошибки
    """
    # Выполняем запрос к API
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    # Проверяем наличие ключа 'Valute' в ответе
    if 'Valute' not in data:
        raise KeyError('Valute')
    
    valutes = data['Valute']
    result = {}
    
    # Собираем курсы для запрошенных валют
    for code in currency_codes:
        if code not in valutes:
            raise KeyError(code)
        
        # Получаем курс валюты с учетом номинала
        currency_data = valutes[code]
        result[code] = currency_data['Value'] / currency_data.get('Nominal', 1)
    
    logging.info(f"Успешно получены курсы для валют: {list(result.keys())}")
    return result

# Для переопределения формата при вызове можно сделать обертки
def get_currencies_as_json(*args, **kwargs):
    """Получить курсы в формате JSON."""
    kwargs['output_format'] = 'json'
    return get_currencies(*args, **kwargs)

def get_currencies_as_yaml(*args, **kwargs):
    """Получить курсы в формате YAML."""
    kwargs['output_format'] = 'yaml'
    return get_currencies(*args, **kwargs)

def get_currencies_as_csv(*args, **kwargs):
    """Получить курсы в формате CSV."""
    kwargs['output_format'] = 'csv'
    return get_currencies(*args, **kwargs)

if __name__ == "__main__":
    setup_logging()
    
    # Примеры использования
    print("=== JSON ===")
    print(get_currencies(['USD', 'EUR'], output_format='json'))
    
    print("\n=== YAML ===")
    print(get_currencies(['USD', 'EUR'], output_format='yaml'))
    
    print("\n=== CSV ===")
    print(get_currencies(['USD', 'EUR'], output_format='csv'))