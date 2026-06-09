# -*- coding: utf-8 -*-

# ==============================================================================
# ПРИМЕР С НАРУШЕНИЕМ SRP (Single Responsibility Principle)
# ==============================================================================
# Класс AlchemistViolation нарушает принцип единственной ответственности, 
# выполняя сразу три разные роли: мага, архивариуса и бухгалтера.

class AlchemistViolation:
    def __init__(self, name: str):
        self.name = name

    def brew_potion(self, potion_name: str, ingredients: list) -> dict:
        # 1. Основная логика: варка зелья
        print(f"🧙‍♂️ [Алхимик {self.name}]: Начинаю смешивать реактивы...")
        print(f"🧪 [Алхимик {self.name}]: Добавляю в котел: {', '.join(ingredients)}")
        potion = {
            "name": potion_name,
            "ingredients": ingredients
        }
        print(f"✨ [Алхимик {self.name}]: Зелье '{potion_name}' успешно сварено!\n")
        return potion

    def save_recipe_to_grimoire(self, potion: dict):
        # 2. Побочная логика: работа с сохранением данных (файловая система)
        # Если изменится формат файла (например, на JSON) или путь — придется менять этот класс!
        file_name = "grimoire.txt"
        print(f"📖 [Алхимик {self.name}]: Записываю рецепт '{potion['name']}' в файл {file_name}...")
        try:
            with open(file_name, "a", encoding="utf-8") as f:
                f.write(f"Рецепт: {potion['name']} | Ингредиенты: {', '.join(potion['ingredients'])}\n")
            print("💾 Успешно сохранено на пергаменте.\n")
        except Exception as e:
            print(f"⚠️ Ошибка при записи в гримуар: {e}\n")

    def calculate_price_in_gold(self, potion: dict) -> float:
        # 3. Побочная логика: бухгалтерия и расчет налогов королевства
        # Если казначейство изменит налог или формулу расчета, нам снова придется менять этот класс.
        base_price = len(potion['ingredients']) * 10  # 10 золотых за каждый ингредиент
        kingdom_tax = 0.15                            # Налог короля (15%)
        
        total_price = base_price * (1 + kingdom_tax)
        print(f"💰 [Алхимик {self.name}]: Считаю цену...")
        print(f"   Базовая стоимость: {base_price} золотых.")
        print(f"   Налог Тридевятого Царства (15%): {base_price * kingdom_tax} золотых.")
        print(f"   Итоговая цена: {total_price} золотых.\n")
        return total_price

if __name__ == "__main__":
    print("--- ЗАПУСК ПРИМЕРА С НАРУШЕНИЕМ SRP ---\n")
    
    # Создаем алхимика Мерлина
    merlin = AlchemistViolation("Мерлин")
    
    # 1. Варим зелье
    potion = merlin.brew_potion("Зелье невидимости", ["Слеза дракона", "Пыльца феи", "Корень мандрагоры"])
    
    # 2. Сохраняем в гримуар
    merlin.save_recipe_to_grimoire(potion)
    
    # 3. Считаем цену
    merlin.calculate_price_in_gold(potion)
    
    print("---------------------------------------")
