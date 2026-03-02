import requests
import sys
from typing import List, Dict, Optional, Callable
from functools import wraps

def log_errors_to_stdout(func: Callable) -> Callable:
    """
    Декоратор для логирования ошибок в stdout.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к API: {e}", file=sys.stdout)
            return None
        except KeyError as e:
            if str(e) == "'Valute'":
                print(f"Ошибка: в ответе API отсутствует ключ 'Valute'", file=sys.stdout)
            else:
                currency_code = str(e).strip("'")
                print(f"Ошибка: валюта '{currency_code}' не найдена в ответе API", file=sys.stdout)
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}", file=sys.stdout)
            return None
    return wrapper

@log_errors_to_stdout
def get_currencies(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Optional[Dict[str, float]]:
    """
    Получает курсы валют из API ЦБ РФ.
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
    
    return result

# Пример использования
if __name__ == "__main__":
    currencies = get_currencies(['USD', 'EUR', 'GBP'])
    print(f"Результат: {currencies}")
