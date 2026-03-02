import json
import csv
import io
from typing import Dict, Any, List
import yaml
from abstract_base import DataSerializer

class JSONSerializer(DataSerializer):
    """Сериализатор в формат JSON."""
    
    def serialize(self, data: Dict[str, Any]) -> str:
        """
        Сериализует данные в JSON формат.
        
        Args:
            data: Словарь с данными
            
        Returns:
            JSON строка
        """
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def get_format_name(self) -> str:
        return "json"


class YAMLSerializer(DataSerializer):
    """Сериализатор в формат YAML."""
    
    def serialize(self, data: Dict[str, Any]) -> str:
        """
        Сериализует данные в YAML формат.
        
        Args:
            data: Словарь с данными
            
        Returns:
            YAML строка
        """
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)
    
    def get_format_name(self) -> str:
        return "yaml"


class CSVSerializer(DataSerializer):
    """Сериализатор в формат CSV."""
    
    def serialize(self, data: Dict[str, Any]) -> str:
        """
        Сериализует данные в CSV формат.
        
        Args:
            data: Словарь с данными в формате {'USD': 91.5, 'EUR': 99.2}
            
        Returns:
            CSV строка
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Заголовки
        writer.writerow(['Currency', 'Rate'])
        
        # Данные
        for currency, rate in data.items():
            writer.writerow([currency, rate])
        
        return output.getvalue()
    
    def get_format_name(self) -> str:
        return "csv"