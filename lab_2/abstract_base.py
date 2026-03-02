from abc import ABC, abstractmethod
from typing import Dict, Any

class DataSerializer(ABC):
    """Абстрактный базовый класс для сериализаторов данных."""
    
    @abstractmethod
    def serialize(self, data: Dict[str, Any]) -> str:
        """
        Сериализует словарь с данными в строку определенного формата.
        
        Args:
            data: Словарь с данными для сериализации
            
        Returns:
            Строка в соответствующем формате
        """
        pass
    
    @abstractmethod
    def get_format_name(self) -> str:
        """
        Возвращает название формата сериализации.
        
        Returns:
            Название формата (json, yaml, csv)
        """
        pass