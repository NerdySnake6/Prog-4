"""Лабораторная работа 2: паттерн «Декоратор» для курсов валют."""

from __future__ import annotations

import csv
import io
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from urllib.request import urlopen
from xml.etree import ElementTree

import yaml

CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"


class Component(ABC):
    """Базовый интерфейс компонента."""

    @abstractmethod
    def operation(self) -> str:
        """Вернуть данные в виде строки."""


class CurrencyJsonComponent(Component):
    """Получает курсы валют и возвращает их в JSON-формате."""

    def __init__(
        self,
        url: str = CBR_URL,
        source_data: list[dict[str, Any]] | None = None,
    ) -> None:
        """Создать компонент с адресом API или готовыми учебными данными."""
        self.url = url
        self.source_data = source_data

    def operation(self) -> str:
        """Вернуть валюты в формате JSON."""
        data = self.source_data
        if data is None:
            data = self._load_from_cbr()
        return json.dumps(data, ensure_ascii=False, indent=2)

    def _load_from_cbr(self) -> list[dict[str, Any]]:
        """Загрузить и разобрать XML с сайта Центробанка."""
        with urlopen(self.url, timeout=10) as response:
            xml_data = response.read()

        root = ElementTree.fromstring(xml_data)
        currencies: list[dict[str, Any]] = []

        for valute in root.findall("Valute"):
            value_text = self._text(valute, "Value").replace(",", ".")
            currencies.append(
                {
                    "num_code": self._text(valute, "NumCode"),
                    "char_code": self._text(valute, "CharCode"),
                    "nominal": int(self._text(valute, "Nominal")),
                    "name": self._text(valute, "Name"),
                    "value": float(value_text),
                }
            )

        return currencies

    def _text(self, element: ElementTree.Element, tag: str) -> str:
        """Вернуть текст тега из XML."""
        child = element.find(tag)
        if child is None or child.text is None:
            return ""
        return child.text.strip()


class Decorator(Component, ABC):
    """Базовый декоратор, который хранит оборачиваемый компонент."""

    def __init__(self, component: Component) -> None:
        """Сохранить компонент внутри декоратора."""
        self._component = component

    @property
    def component(self) -> Component:
        """Вернуть обернутый компонент."""
        return self._component


class YamlDecorator(Decorator):
    """Преобразует JSON-результат компонента в YAML."""

    def operation(self) -> str:
        """Вернуть данные в YAML-формате."""
        data = json.loads(self.component.operation())
        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)

    def save_to_file(self, file_path: str | Path) -> Path:
        """Сохранить YAML-результат в файл."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.operation(), encoding="utf-8")
        return path


class CsvDecorator(Decorator):
    """Преобразует JSON-результат компонента в CSV."""

    fieldnames = ["num_code", "char_code", "nominal", "name", "value"]

    def operation(self) -> str:
        """Вернуть данные в CSV-формате."""
        data = json.loads(self.component.operation())
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.fieldnames)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

    def save_to_file(self, file_path: str | Path) -> Path:
        """Сохранить CSV-результат в файл."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.operation(), encoding="utf-8", newline="")
        return path


def demo_data() -> list[dict[str, Any]]:
    """Вернуть маленький набор данных для демонстрации без интернета."""
    return [
        {
            "num_code": "840",
            "char_code": "USD",
            "nominal": 1,
            "name": "Доллар США",
            "value": 90.0,
        },
        {
            "num_code": "978",
            "char_code": "EUR",
            "nominal": 1,
            "name": "Евро",
            "value": 91.5,
        },
    ]


def client_code(component: Component) -> None:
    """Показать результат работы любого компонента."""
    print(component.operation())


def main() -> None:
    """Запустить простой пример работы декораторов."""
    component = CurrencyJsonComponent(source_data=demo_data())
    yaml_component = YamlDecorator(component)
    csv_component = CsvDecorator(component)

    print("JSON:")
    client_code(component)

    print("\nYAML:")
    client_code(yaml_component)

    print("\nCSV:")
    client_code(csv_component)

    yaml_component.save_to_file("output/currencies.yaml")
    csv_component.save_to_file("output/currencies.csv")


if __name__ == "__main__":
    main()
