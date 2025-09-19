#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Тестовый файл для проверки импортов
import sys
import os

# Фикс кодировки для Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    
try:
    import telegram
    print("✅ python-telegram-bot импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта telegram: {e}")

try:
    import flask
    print("✅ flask импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта flask: {e}")

try:
    import requests
    print("✅ requests импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта requests: {e}")

print("\nТест импорта завершён!")
