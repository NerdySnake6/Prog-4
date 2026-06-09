import functools

def fib_coroutine(g):
    """Декоратор для инициализации корутины"""
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        gen.send(None)  # Инициализация
        return gen
    return inner

@fib_coroutine
def my_genn():
    """Сопрограмма для генерации чисел Фибоначчи"""
    while True:
        n = yield  # Получаем количество элементов
        if n <= 0:
            yield []
        elif n == 1:
            yield [0]
        elif n == 2:
            yield [0, 1]
        else:
            # Генерируем числа Фибоначчи
            fib_list = [0, 1]
            for i in range(2, n):
                fib_list.append(fib_list[i-1] + fib_list[i-2])
            yield fib_list

# Для тестирования (чтобы не нарушать оригинальный код)
my_genn = fib_coroutine(my_genn)
