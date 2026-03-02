from functools import wraps
from typing import Callable, Dict, Any, Optional
import logging
from abstract_base import DataSerializer
from serializers import JSONSerializer, YAMLSerializer, CSVSerializer

# Словарь доступных сериализаторов
_SERIALIZERS = {
    'json': JSONSerializer(),
    'yaml': YAMLSerializer(),
    'csv': CSVSerializer()
}

def get_serializer(format_name: str) -> Optional[DataSerializer]:
    """
    Фабрика для получения сериализатора по имени формата.
    
    Args:
        format_name: Название формата (json, yaml, csv)
        
    Returns:
        Экземпляр сериализатора или None, если формат не поддерживается
    """
    return _SERIALIZERS.get(format_name.lower())

def serialize_output(format_name: str = 'json'):
    """
    Декоратор для сериализации результата функции в указанный формат.
    
    Args:
        format_name: Формат сериализации (json, yaml, csv)
    
    Returns:
        Декорированная функция
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем результат исходной функции
            result = func(*args, **kwargs)
            
            # Если результат None (ошибка), возвращаем как есть
            if result is None:
                return None
            
            # Получаем сериализатор
            serializer = get_serializer(format_name)
            if serializer is None:
                logging.error(f"Неподдерживаемый формат сериализации: {format_name}")
                return result
            
            try:
                # Сериализуем результат
                serialized = serializer.serialize(result)
                logging.info(f"Данные сериализованы в формат {serializer.get_format_name()}")
                return serialized
            except Exception as e:
                logging.error(f"Ошибка при сериализации в {format_name}: {e}")
                return result
        
        return wrapper
    return decorator