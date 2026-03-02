
# Лабораторная работа: Генерация чисел Фибоначчи

## Описание
Реализация чисел Фибоначчи тремя способами:
1. **Итератор** (`FibonacciIterator`) — через протокол итератора (`__iter__`/`__next__`)
2. **Последовательность с доступом по индексу** (`SimpleFibonacci`) — через `__getitem__`
3. **Сопрограмма** (`my_genn`) — через генератор с декоратором

## Структура проекта
- `fib_iterator.py` — итератор и класс с `__getitem__`
- `gen.py` — сопрограмма с декоратором
- `test_fib.py` — модульные тесты для сопрограммы

## Примеры использования

### Итератор
```python
fib_iter = FibonacciIterator(5)
for num in fib_iter:
    print(num)  # 0, 1, 1, 2, 3
### Доступ по индексу
```python
fib = SimpleFibonacci()

# Получение чисел по индексу
print(fib[0])   # 0
print(fib[1])   # 1  
print(fib[2])   # 1
print(fib[3])   # 2
print(fib[4])   # 3
print(fib[5])   # 5
print(fib[6])   # 8
print(fib[7])   # 13

# Обработка отрицательных индексов
try:
    print(fib[-1])  # IndexError: Индекс должен быть неотрицательным
except IndexError as e:
    print(e)
