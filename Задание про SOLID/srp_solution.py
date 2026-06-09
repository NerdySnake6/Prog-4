# -*- coding: utf-8 -*-

class Potion:
    """Класс-модель, содержащий данные о зелье."""
    def __init__(self, name: str, ingredients: list):
        self.name = name
        self.ingredients = ingredients


class Alchemist:
    """Отвечает исключительно за приготовление зелий."""
    def __init__(self, name: str):
        self.name = name

    def brew_potion(self, name: str, ingredients: list) -> Potion:
        print(f"[Алхимик {self.name}]: Приготовление зелья '{name}'...")
        print(f"[Алхимик {self.name}]: Добавлены ингредиенты: {', '.join(ingredients)}")
        print(f"[Алхимик {self.name}]: Зелье '{name}' успешно приготовлено.\n")
        return Potion(name, ingredients)


class GrimoireRepository:
    """Отвечает исключительно за сохранение данных."""
    def __init__(self, file_path: str = "grimoire.txt"):
        self.file_path = file_path

    def save_recipe(self, potion: Potion):
        print(f"[Гримуар]: Сохранение рецепта '{potion.name}' в файл {self.file_path}...")
        try:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(f"Рецепт: {potion.name} | Ингредиенты: {', '.join(potion.ingredients)}\n")
            print("Успешно сохранено.\n")
        except Exception as e:
            print(f"Ошибка сохранения: {e}\n")


class PotionPricingCalculator:
    """Отвечает исключительно за расчеты стоимости зелий."""
    def __init__(self, tax_rate: float = 0.15):
        self.tax_rate = tax_rate

    def calculate_price(self, potion: Potion) -> float:
        base_price = len(potion.ingredients) * 10
        total_price = base_price * (1 + self.tax_rate)
        
        print(f"[Калькулятор цен]: Расчет стоимости зелья '{potion.name}'...")
        print(f"   Базовая стоимость: {base_price}")
        print(f"   Налог ({self.tax_rate * 100:.0f}%): {base_price * self.tax_rate:.2f}")
        print(f"   Итоговая цена: {total_price:.2f}\n")
        return total_price


if __name__ == "__main__":
    print("=== Демонстрация решения по SRP ===\n")
    
    alchemist = Alchemist("Мерлин")
    repository = GrimoireRepository("grimoire.txt")
    pricing_service = PotionPricingCalculator(tax_rate=0.15)
    
    # 1. Приготовление зелья
    potion = alchemist.brew_potion("Зелье невидимости", ["Слеза дракона", "Пыльца феи"])
    
    # 2. Сохранение рецепта
    repository.save_recipe(potion)
    
    # 3. Расчет стоимости
    pricing_service.calculate_price(potion)
