#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Быстрые тесты функционала SleepyBot
"""

import sys
import os

# Фикс кодировки для Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

import unittest
from datetime import datetime, timedelta
from main import SleepCalculator

class TestSleepCalculator(unittest.TestCase):
    """Тесты для SleepCalculator"""
    
    def test_parse_time_now(self):
        """Тест парсинга 'сейчас'"""
        result = SleepCalculator.parse_time_input("сейчас")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, datetime)
    
    def test_parse_time_plus_minutes(self):
        """Тест парсинга '+15'"""
        now = datetime.now()
        result = SleepCalculator.parse_time_input("+15")
        self.assertIsNotNone(result)
        # Проверяем, что добавилось примерно 15 минут
        diff = (result - now).total_seconds()
        self.assertAlmostEqual(diff, 15 * 60, delta=5)  # 5 секунд погрешности
    
    def test_parse_time_format(self):
        """Тест парсинга формата 'чч:мм'"""
        result = SleepCalculator.parse_time_input("23:30")
        self.assertIsNotNone(result)
        self.assertEqual(result.hour, 23)
        self.assertEqual(result.minute, 30)
    
    def test_parse_invalid_time(self):
        """Тест невалидного времени"""
        result = SleepCalculator.parse_time_input("25:70")
        self.assertIsNone(result)
        
        result = SleepCalculator.parse_time_input("абракадабра")
        self.assertIsNone(result)
    
    def test_calculate_wake_times(self):
        """Тест расчёта времён пробуждения"""
        # Тестируем с фиксированным временем
        sleep_time = datetime(2025, 9, 20, 23, 30)
        wake_times = SleepCalculator.calculate_wake_times(sleep_time)
        
        # Проверяем, что возвращается список
        self.assertIsInstance(wake_times, list)
        # Проверяем, что возвращается 6 вариантов
        self.assertEqual(len(wake_times), 6)
        # Проверяем, что каждый элемент - строка
        for wake_time in wake_times:
            self.assertIsInstance(wake_time, str)
            self.assertIn("🕐", wake_time)

def run_quick_test():
    """Быстрый тест основных функций"""
    print("🧪 Запуск быстрых тестов SleepyBot...")
    print("=" * 50)
    
    # Тест 1: Парсинг времени
    print("\n1️⃣ Тестируем парсинг времени...")
    test_inputs = ["сейчас", "+15", "23:30", "00:00", "12:45"]
    
    for test_input in test_inputs:
        result = SleepCalculator.parse_time_input(test_input)
        status = "✅" if result else "❌"
        print(f"   {status} '{test_input}' -> {result}")
    
    # Тест 2: Невалидные входы
    print("\n2️⃣ Тестируем невалидные входы...")
    invalid_inputs = ["25:00", "12:60", "абракадабра", "", "24:00"]
    
    for test_input in invalid_inputs:
        result = SleepCalculator.parse_time_input(test_input)
        status = "✅" if result is None else "❌"
        print(f"   {status} '{test_input}' -> {result}")
    
    # Тест 3: Расчёт времён пробуждения
    print("\n3️⃣ Тестируем расчёт времён пробуждения...")
    sleep_time = datetime(2025, 9, 20, 23, 30)
    wake_times = SleepCalculator.calculate_wake_times(sleep_time)
    
    print(f"   ✅ Получено {len(wake_times)} вариантов пробуждения")
    for i, wake_time in enumerate(wake_times[:3], 1):  # Показываем первые 3
        print(f"   {i}. {wake_time}")
    
    print("\n✅ Все тесты завершены!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--unittest":
        # Запуск полных юнит-тестов
        print("🧪 Запуск полных юнит-тестов...")
        unittest.main(argv=[''], exit=False)
    else:
        # Запуск быстрых тестов
        run_quick_test()
