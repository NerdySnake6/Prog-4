import unittest
from gen_fib import my_genn

class TestFibCoroutine(unittest.TestCase):
    
    def test_normal_3(self):
        """Тривиальный случай n = 3"""
        gen = my_genn()
        result = gen.send(3)
        self.assertEqual(result, [0, 1, 1])
    
    def test_normal_5(self):
        """Пять первых членов ряда"""
        gen = my_genn()
        result = gen.send(5)
        self.assertEqual(result, [0, 1, 1, 2, 3])
    
    def test_normal_8(self):
        """Восемь первых членов ряда"""
        gen = my_genn()
        result = gen.send(8)
        self.assertEqual(result, [0, 1, 1, 2, 3, 5, 8, 13])
    
    def test_corner_0(self):
        """Пустой список при n=0"""
        gen = my_genn()
        result = gen.send(0)
        self.assertEqual(result, [])
    
    def test_corner_1(self):
        """Один элемент при n=1"""
        gen = my_genn()
        result = gen.send(1)
        self.assertEqual(result, [0])
    
    def test_corner_2(self):
        """Два элемента при n=2"""
        gen = my_genn()
        result = gen.send(2)
        self.assertEqual(result, [0, 1])
    
    def test_negative(self):
        """Отрицательное число"""
        gen = my_genn()
        result = gen.send(-5)
        self.assertEqual(result, [])
    
    def test_sequential_calls(self):
        """Последовательные вызовы"""
        gen = my_genn()
        result1 = gen.send(3)
        self.assertEqual(result1, [0, 1, 1])
        
        result2 = gen.send(5)
        self.assertEqual(result2, [0, 1, 1, 2, 3])
        
        result3 = gen.send(2)
        self.assertEqual(result3, [0, 1])

if __name__ == '__main__':
    unittest.main()