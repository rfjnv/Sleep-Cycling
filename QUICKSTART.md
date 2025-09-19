# 🚀 Быстрый старт SleepyBot

## Варианты запуска:

### � Для Windows (рекомендуется):
```powershell
# Установка UTF-8 кодировки
$env:PYTHONIOENCODING="utf-8"

# Затем любой из вариантов:
python main.py          # Telegram бот
python web_demo.py      # Веб-интерфейс  
python demo.py          # Консольная демонстрация
python test_quick.py    # Тесты
```

### 🐧 Для Linux/Mac:
```bash
python main.py          # Telegram бот
python web_demo.py      # Веб-интерфейс
python demo.py          # Консольная демонстрация
python test_quick.py    # Тесты
```

---

## 📱 Использование

### В Telegram:
- `/start` — начать работу
- `/help` — справка
- `23:30` — время сна
- `сейчас` — лечь спать сейчас
- `+15` — через 15 минут

### В веб-интерфейсе:
Те же команды в текстовом поле

---

## ⚡ VS Code

### Задачи (Ctrl+Shift+P → "Tasks: Run Task"):
- **Run SleepyBot** — запуск Telegram бота
- **Run Web Demo** — запуск веб-интерфейса  
- **Run Demo** — консольная демонстрация
- **Run Tests** — быстрые тесты

### Отладка (F5):
- **🤖 Debug SleepyBot** — отладка Telegram бота
- **🌐 Debug Web Demo** — отладка веб-интерфейса
- **🎯 Run Demo** — запуск демонстрации
- **🧪 Run Tests** — запуск тестов

---

## 🔑 Токен бота

Токен уже встроен в код:
```
8381755892:AAGDdAHcvYt3RO7DvKmjSO716o_mdSIZxCY
```

Для смены токена отредактируйте `TOKEN` в `main.py`
