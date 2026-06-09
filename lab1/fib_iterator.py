class FibonacciIterator:
    """Итератор чисел Фибоначчи через __iter__ и __next__"""
    
    def __init__(self, instance):
        self.instance = instance  # Принимаем лимит как "экземпляр"
        self.idx = 0  # Текущий индекс в последовательности
        self.current = 0
        self.next_num = 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.idx >= self.instance:  # instance - это сколько чисел нужно
            raise StopIteration
        
        if self.idx == 0:
            result = 0
        elif self.idx == 1:
            result = 1
        else:
            result = self.current + self.next_num
            self.current, self.next_num = self.next_num, result
        
        self.idx += 1
        return result


# 2. Упрощенный итератор через __getitem__ (простая реализация)
class SimpleFibonacci:
    """Простой доступ к числам Фибоначчи через индексацию"""
    
    def __init__(self):
        self.fib_cache = []
    
    def __getitem__(self, n):
        """Возвращает n-ное число Фибоначчи (простое обращение)"""
        if n < 0:
            raise IndexError("Индекс должен быть неотрицательным")
        
        # Вычисляем число Фибоначчи простым способом
        if n == 0:
            return 0
        elif n == 1:
            return 1
        
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b