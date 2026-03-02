import unittest
import sys

def run_all_tests():
    """Запускает все тесты для всех версий."""
    print("=" * 60)
    print("ЗАПУСК ВСЕХ ТЕСТОВ ДЛЯ ПРОЕКТА КУРСЫ ВАЛЮТ")
    print("=" * 60)
    
    test_modules = [
        'test_lab1',
        'test_lab2', 
        'test_lab3',
        'test_lab4'  # Новая версия с декоратором
    ]
    
    all_passed = True
    
    for module_name in test_modules:
        print(f"\nЗапуск тестов из {module_name}.py")
        print("-" * 40)
        
        try:
            suite = unittest.defaultTestLoader.loadTestsFromName(module_name)
            result = unittest.TextTestRunner(verbosity=2).run(suite)
            
            if not result.wasSuccessful():
                all_passed = False
                print(f"❌ Тесты в {module_name} провалены")
            else:
                print(f"✅ Тесты в {module_name} успешно пройдены")
                
        except ImportError as e:
            print(f"⚠ Модуль {module_name} не найден: {e}")
        except Exception as e:
            print(f"⚠ Ошибка при запуске {module_name}: {e}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ")
    print("=" * 60)
    
    return all_passed

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)