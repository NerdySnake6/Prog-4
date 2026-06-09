# -*- coding: utf-8 -*-

# ==============================================================================
# ПРИМЕР С СОБЛЮДЕНИЕМ SRP (Single Responsibility Principle)
# ==============================================================================
# Мы разделили обязанности на три независимых класса. Каждая сущность теперь
# занимается строго своим делом и имеет ровно одну причину для изменения.

class Potion:
    """Сущность Зелья. Хранит данные о названии и ингредиентах."""
    def __init__(self, name: str, ingredients: list):
        self.name = name
        self.ingredients = ingredients


class Alchemist:
    """Класс отвечает ТОЛЬКО за процесс варки зелий."""
    def __init__(self, name: str):
        self.name = name

    def brew_potion(self, name: str, ingredients: list) -> Potion:
        print(f"🧙‍♂️ [Алхимик {self.name}]: Начинаю смешивать реактивы...")
        print(f"🧪 [Алхимик {self.name}]: Добавляю в котел: {', '.join(ingredients)}")
        print(f"✨ [Алхимик {self.name}]: Зелье '{name}' успешно сварено!\n")
        return Potion(name, ingredients)


class GrimoireRepository:
    """Класс отвечает ТОЛЬКО за сохранение рецептов зелий."""
    def __init__(self, file_path: str = "grimoire.txt"):
        self.file_path = file_path

    def save_recipe(self, potion: Potion):
        print(f"📖 [Гримуар]: Записываю рецепт '{potion.name}' в файл {self.file_path}...")
        try:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(f"Рецепт: {potion.name} | Ингредиенты: {', '.join(potion.ingredients)}\n")
            print("💾 Успешно сохранено на пергаменте.\n")
        except Exception as e:
            print(f"⚠️ Ошибка при записи в гримуар: {e}\n")


class PotionPricingCalculator:
    """Класс отвечает ТОЛЬКО за финансовые расчеты стоимости зелья."""
    def __init__(self, tax_rate: float = 0.15):
        self.tax_rate = tax_rate

    def calculate_price(self, potion: Potion) -> float:
        base_price = len(potion.ingredients) * 10  # 10 золотых за каждый ингредиент
        total_price = base_price * (1 + self.tax_rate)
        
        print(f"💰 [Калькулятор цен]: Считаю цену для '{potion.name}'...")
        print(f"   Базовая стоимость: {base_price} золотых.")
        print(f"   Налог королевства ({self.tax_rate * 100:.0f}%): {base_price * self.tax_rate:.2f} золотых.")
        print(f"   Итоговая цена: {total_price:.2f} золотых.\n")
        return total_price


if __name__ == "__main__":
    print("--- ЗАПУСК ПРИМЕРА С ИСПРАВЛЕННЫМ SRP ---\n")
    
    # 1. Создаем необходимые службы
    merlin = Alchemist("Мерлин")
    grimoire = GrimoireRepository("grimoire.txt")
    pricing_service = PotionPricingCalculator(tax_rate=0.15)
    
    # 2. Алхимик варит зелье (не думая о деньгах и записи файлов)
    potion = merlin.brew_potion("Зелье невидимости", ["Слеза дракона", "Пыльца феи", "Корень мандрагоры"])
    
    # 3. Гримуар сохраняет рецепт зелья
    grimoire.save_recipe(potion)
    
    # 4. Калькулятор рассчитывает стоимость зелья
    pricing_service.calculate_price(potion)
    
    print("-----------------------------------------")
