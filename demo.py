#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Демонстрационный скрипт для тестирования функционала SleepCalculator
без подключения к Telegram API
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# Фикс кодировки для Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

from datetime import datetime
from main import SleepCalculator

def demo_sleep_calculator():
    """Демонстрация работы калькулятора сна"""
    
    print("🌙 Демонстрация SleepyBot Calculator")
    print("=" * 50)
    
    # Тестовые случаи
    test_cases = [
        "сейчас",
        "+15",
        "+30", 
        "23:30",
        "22:00",
        "01:00"
    ]
    
    for test_input in test_cases:
        print(f"\n📝 Ввод: '{test_input}'")
        print("-" * 30)
        
        # Парсим время
        sleep_time = SleepCalculator.parse_time_input(test_input)
        
        if sleep_time is None:
            print("❌ Не удалось распарсить время")
            continue
            
        print(f"🛏 Время сна: {sleep_time.strftime('%H:%M (%d.%m.%Y)')}")
        
        # Рассчитываем времена пробуждения
        wake_times = SleepCalculator.calculate_wake_times(sleep_time)
        
        print("⏰ Оптимальные времена пробуждения:")
        for wake_time in wake_times:
            print(f"   {wake_time}")
    
    print("\n✅ Демонстрация завершена!")

if __name__ == "__main__":
    demo_sleep_calculator()
