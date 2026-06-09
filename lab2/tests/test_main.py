"""Тесты лабораторной работы 2."""

from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import CsvDecorator, CurrencyJsonComponent, YamlDecorator


class FakeResponse:
    """Простой объект вместо ответа urlopen."""

    def __init__(self, data: bytes) -> None:
        """Сохранить тестовые XML-данные."""
        self.data = data

    def __enter__(self) -> "FakeResponse":
        """Вернуть объект для with."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Ничего не делать при выходе из with."""

    def read(self) -> bytes:
        """Вернуть XML-данные."""
        return self.data


def sample_data() -> list[dict[str, object]]:
    """Вернуть тестовые валюты."""
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


class CurrencyJsonComponentTests(unittest.TestCase):
    """Проверяет базовый JSON-компонент."""

    def test_operation_returns_json(self) -> None:
        """Компонент должен возвращать JSON-строку."""
        component = CurrencyJsonComponent(source_data=sample_data())

        result = json.loads(component.operation())

        self.assertEqual(result[0]["char_code"], "USD")
        self.assertEqual(result[1]["value"], 91.5)

    def test_operation_loads_cbr_xml(self) -> None:
        """Компонент должен уметь разобрать XML Центробанка."""
        xml_data = """
        <ValCurs>
            <Valute ID="R01235">
                <NumCode>840</NumCode>
                <CharCode>USD</CharCode>
                <Nominal>1</Nominal>
                <Name>Доллар США</Name>
                <Value>90,0000</Value>
            </Valute>
        </ValCurs>
        """.encode("utf-8")

        with patch("main.urlopen", return_value=FakeResponse(xml_data)):
            component = CurrencyJsonComponent()
            result = json.loads(component.operation())

        self.assertEqual(result[0]["name"], "Доллар США")
        self.assertEqual(result[0]["value"], 90.0)


class YamlDecoratorTests(unittest.TestCase):
    """Проверяет YAML-декоратор."""

    def test_operation_returns_yaml(self) -> None:
        """YAML-декоратор должен возвращать YAML-строку."""
        component = CurrencyJsonComponent(source_data=sample_data())
        decorator = YamlDecorator(component)

        result = yaml.safe_load(decorator.operation())

        self.assertEqual(result[0]["char_code"], "USD")
        self.assertEqual(result[1]["name"], "Евро")

    def test_save_to_file(self) -> None:
        """YAML-декоратор должен сохранять данные в файл."""
        component = CurrencyJsonComponent(source_data=sample_data())
        decorator = YamlDecorator(component)

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "currencies.yaml"
            saved_path = decorator.save_to_file(file_path)
            result = yaml.safe_load(saved_path.read_text(encoding="utf-8"))

        self.assertEqual(saved_path.name, "currencies.yaml")
        self.assertEqual(result[0]["num_code"], "840")


class CsvDecoratorTests(unittest.TestCase):
    """Проверяет CSV-декоратор."""

    def test_operation_returns_csv(self) -> None:
        """CSV-декоратор должен возвращать CSV-строку."""
        component = CurrencyJsonComponent(source_data=sample_data())
        decorator = CsvDecorator(component)

        reader = csv.DictReader(io.StringIO(decorator.operation()))
        rows = list(reader)

        self.assertEqual(rows[0]["char_code"], "USD")
        self.assertEqual(rows[1]["name"], "Евро")

    def test_save_to_file(self) -> None:
        """CSV-декоратор должен сохранять данные в файл."""
        component = CurrencyJsonComponent(source_data=sample_data())
        decorator = CsvDecorator(component)

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "currencies.csv"
            saved_path = decorator.save_to_file(file_path)
            reader = csv.DictReader(io.StringIO(saved_path.read_text()))
            rows = list(reader)

        self.assertEqual(saved_path.name, "currencies.csv")
        self.assertEqual(rows[0]["value"], "90.0")


if __name__ == "__main__":
    unittest.main()
