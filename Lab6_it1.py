import requests
import sys
from typing import List, Dict, Optional

def get_currencies(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Optional[Dict[str, float]]:
    """
    Получает курсы валют из API ЦБ РФ.
    
    Args:
        currency_codes: Список кодов валют (например, ['USD', 'EUR'])
        url: URL API ЦБ РФ
    
    Returns:
        Словарь с курсами валют или None в случае ошибки
    """
    try:
        # Выполняем запрос к API
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        # Проверяем наличие ключа 'Valute' в ответе
        if 'Valute' not in data:
            print(f"Ошибка: в ответе API отсутствует ключ 'Valute'", file=sys.stdout)
            return None
        
        valutes = data['Valute']
        result = {}
        
        # Собираем курсы для запрошенных валют
        for code in currency_codes:
            if code not in valutes:
                print(f"Ошибка: валюта '{code}' не найдена в ответе API", file=sys.stdout)
                return None
            
            # Получаем курс валюты
            currency_data = valutes[code]
            result[code] = currency_data['Value']
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API: {e}", file=sys.stdout)
        return None
    except KeyError as e:
        print(f"Ошибка структуры данных: отсутствует ключ {e}", file=sys.stdout)
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stdout)
        return None

# Пример использования
if __name__ == "__main__":
    currencies = get_currencies(['USD', 'EUR', 'GBP'])
    print(f"Результат: {currencies}")