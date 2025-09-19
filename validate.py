#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Полная валидация проекта SleepyBot
Проверяет все компоненты и зависимости
"""

import os
import sys
import importlib
import subprocess
from datetime import datetime

def check_file_exists(filename):
    """Проверка существования файла"""
    exists = os.path.exists(filename)
    status = "✅" if exists else "❌"
    print(f"   {status} {filename}")
    return exists

def check_import(module_name):
    """Проверка импорта модуля"""
    try:
        importlib.import_module(module_name)
        print(f"   ✅ {module_name}")
        return True
    except ImportError as e:
        print(f"   ❌ {module_name} - {e}")
        return False

def run_command(command, description):
    """Запуск команды и проверка результата"""
    try:
        # Для Windows добавляем переменную окружения для UTF-8
        env = os.environ.copy()
        if sys.platform == "win32":
            env["PYTHONIOENCODING"] = "utf-8"
            
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30, env=env)
        if result.returncode == 0:
            print(f"   ✅ {description}")
            return True
        else:
            print(f"   ❌ {description} - код ошибки: {result.returncode}")
            if result.stderr:
                print(f"      Ошибка: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"   ⏰ {description} - таймаут")
        return False
    except Exception as e:
        print(f"   ❌ {description} - {e}")
        return False

def validate_project():
    """Полная валидация проекта"""
    print("🔍 Валидация проекта SleepyBot")
    print("=" * 50)
    
    # Проверка структуры файлов
    print("\n📁 Проверка структуры файлов:")
    required_files = [
        "main.py",
        "demo.py", 
        "web_demo.py",
        "test_quick.py",
        "test_imports.py",
        "requirements.txt",
        "README.md",
        "DEVELOPMENT.md",
        "QUICKSTART.md",
        ".gitignore"
    ]
    
    file_checks = [check_file_exists(f) for f in required_files]
    files_ok = all(file_checks)
    
    # Проверка зависимостей
    print("\n📦 Проверка зависимостей:")
    required_modules = [
        "telegram",
        "flask", 
        "requests"
    ]
    
    import_checks = [check_import(m) for m in required_modules]
    imports_ok = all(import_checks)
    
    # Проверка Python скриптов
    print("\n🐍 Проверка Python скриптов:")
    
    # Синтаксическая проверка
    python_files = ["main.py", "demo.py", "web_demo.py", "test_quick.py", "test_imports.py"]
    syntax_checks = []
    
    for py_file in python_files:
        if os.path.exists(py_file):
            syntax_ok = run_command(f"python -m py_compile {py_file}", f"Синтаксис {py_file}")
            syntax_checks.append(syntax_ok)
        else:
            syntax_checks.append(False)
    
    syntax_ok = all(syntax_checks)
    
    # Функциональные тесты
    print("\n🧪 Функциональные тесты:")
    
    test_results = []
    
    # Тест импортов
    test_results.append(run_command("python test_imports.py", "Тест импорта библиотек"))
    
    # Быстрые тесты
    test_results.append(run_command("python test_quick.py", "Быстрые тесты калькулятора"))
    
    # Тест демо
    test_results.append(run_command("python demo.py", "Консольная демонстрация"))
    
    tests_ok = all(test_results)
    
    # Итоговый отчёт
    print("\n" + "=" * 50)
    print("📊 ИТОГОВЫЙ ОТЧЁТ:")
    print("=" * 50)
    
    print(f"📁 Структура файлов: {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"📦 Зависимости: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"🐍 Синтаксис: {'✅ PASS' if syntax_ok else '❌ FAIL'}")
    print(f"🧪 Тесты: {'✅ PASS' if tests_ok else '❌ FAIL'}")
    
    overall_status = all([files_ok, imports_ok, syntax_ok, tests_ok])
    
    print("\n" + "=" * 50)
    if overall_status:
        print("🎉 ПРОЕКТ ГОТОВ К ИСПОЛЬЗОВАНИЮ!")
        print("   Запустите: python main.py")
        print("   Или веб-демо: python web_demo.py")
    else:
        print("⚠️  НАЙДЕНЫ ПРОБЛЕМЫ!")
        print("   Проверьте ошибки выше и исправьте их")
    
    print("=" * 50)
    
    return overall_status

if __name__ == "__main__":
    success = validate_project()
    sys.exit(0 if success else 1)
