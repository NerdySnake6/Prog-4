# -*- coding: utf-8 -*-

class AlchemistViolation:
    """
    Класс нарушает принцип единственной ответственности (SRP).
    Он совмещает логику приготовления, логику сохранения рецепта и расчет стоимости.
    """
    def __init__(self, name: str):
        self.name = name

    def brew_potion(self, potion_name: str, ingredients: list) -> dict:
        # Ответственность 1: Приготовление зелья
        print(f"[Алхимик {self.name}]: Приготовление зелья '{potion_name}'...")
        print(f"[Алхимик {self.name}]: Добавлены ингредиенты: {', '.join(ingredients)}")
        potion = {
            "name": potion_name,
            "ingredients": ingredients
        }
        print(f"[Алхимик {self.name}]: Зелье '{potion_name}' успешно приготовлено.\n")
        return potion

    def save_recipe(self, potion: dict):
        # Ответственность 2: Сохранение данных в файл
        file_name = "grimoire.txt"
        print(f"[Алхимик {self.name}]: Сохранение рецепта '{potion['name']}' в файл {file_name}...")
        try:
            with open(file_name, "a", encoding="utf-8") as f:
                f.write(f"Рецепт: {potion['name']} | Ингредиенты: {', '.join(potion['ingredients'])}\n")
            print("Успешно сохранено.\n")
        except Exception as e:
            print(f"Ошибка сохранения: {e}\n")

    def calculate_price(self, potion: dict) -> float:
        # Ответственность 3: Расчет стоимости
        base_price = len(potion['ingredients']) * 10
        tax_rate = 0.15
        total_price = base_price * (1 + tax_rate)
        
        print(f"[Алхимик {self.name}]: Расчет стоимости...")
        print(f"   Базовая стоимость: {base_price}")
        print(f"   Налог (15%): {base_price * tax_rate}")
        print(f"   Итоговая цена: {total_price}\n")
        return total_price

if __name__ == "__main__":
    print("=== Демонстрация нарушения SRP ===\n")
    alchemist = AlchemistViolation("Мерлин")
    potion = alchemist.brew_potion("Зелье невидимости", ["Слеза дракона", "Пыльца феи"])
    alchemist.save_recipe(potion)
    alchemist.calculate_price(potion)
