import requests
import logging
from typing import List, Dict, Optional, Callable
from functools import wraps

# Настройка логирования
def setup_logging():
    """Настройка конфигурации логирования."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Вывод в консоль
            logging.FileHandler('currency_rates.log', encoding='utf-8')  # Запись в файл
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
def get_currencies(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Optional[Dict[str, float]]:
    """
    Получает курсы валют из API ЦБ РФ.
    
    Args:
        currency_codes: Список кодов валют (например, ['USD', 'EUR'])
        url: URL API ЦБ РФ
    
    Returns:
        Словарь с курсами валют или None в случае ошибки
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
        
        # Получаем курс валюты
        currency_data = valutes[code]
        result[code] = currency_data['Value']
    
    logging.info(f"Успешно получены курсы для валют: {list(result.keys())}")
    return result

# Тестирование функций
def test_get_currencies():
    """Тестирование функции get_currencies."""
    setup_logging()
    
    print("=== Тестирование функции get_currencies ===")
    
    # Тест 1: Корректный запрос
    print("\n1. Корректный запрос:")
    result = get_currencies(['USD', 'EUR'])
    if result:
        print(f"Ключи: {list(result.keys())}")
        print(f"Значения: {result}")
        assert set(result.keys()) == {'USD', 'EUR'}, "Неверные ключи в результате"
        assert all(isinstance(v, float) for v in result.values()), "Значения должны быть float"
    
    # Тест 2: Несуществующая валюта
    print("\n2. Запрос несуществующей валюты:")
    result = get_currencies(['INVALID_CODE'])
    assert result is None, "Должен вернуть None для несуществующей валюты"
    
    # Тест 3: Неверный URL
    print("\n3. Запрос к неверному URL:")
    result = get_currencies(['USD'], 'https://invalid-url.example.com')
    assert result is None, "Должен вернуть None при ошибке запроса"
    
    # Тест 4: Пустой список валют
    print("\n4. Пустой список валют:")
    result = get_currencies([])
    assert result == {}, "Должен вернуть пустой словарь для пустого списка"
    
    print("\n=== Все тесты пройдены ===")

if __name__ == "__main__":
    test_get_currencies()
    
    # Демонстрация работы
    print("\n=== Демонстрация работы ===")
    setup_logging()
    currencies = get_currencies(['USD', 'EUR', 'GBP', 'JPY'])
    print(f"Текущие курсы: {currencies}") 
