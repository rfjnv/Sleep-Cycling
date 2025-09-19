# 🛠 Инструкции для разработчиков

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Тестирование без Telegram API
```bash
python demo.py
```

### 3. Запуск бота
```bash
python main.py
```

---

## 📁 Структура проекта

```
sleep-cycle/
├── main.py              # 🤖 Основной файл бота
├── demo.py              # 🎯 Демонстрация работы без Telegram
├── test_imports.py      # ✅ Проверка установленных библиотек
├── requirements.txt     # 📦 Зависимости Python
├── README.md           # 📖 Основная документация
├── DEVELOPMENT.md      # 🛠 Эта инструкция
└── .gitignore          # 🚫 Игнорируемые файлы
```

---

## 🧩 Архитектура кода

### `SleepCalculator` класс
- `parse_time_input(text)` — парсинг пользовательского ввода
- `calculate_wake_times(sleep_time)` — расчёт времён пробуждения

### Обработчики Telegram
- `start()` — команда `/start` 
- `help_command()` — команда `/help`
- `calculate_sleep()` — основная логика расчёта
- `unknown_command()` — обработка неизвестных команд

### Keep-Alive сервер
- Flask веб-сервер для поддержания бота активным на Replit
- Запускается в отдельном потоке

---

## 🔧 Настройка для разработки

### Изменение токена бота
1. Создать нового бота через [@BotFather](https://t.me/BotFather)
2. Получить токен
3. Заменить `TOKEN` в `main.py`

### Настройки циклов сна
Константы в классе `SleepCalculator`:
- `SLEEP_CYCLE_MINUTES = 90` — длительность цикла 
- `FALL_ASLEEP_MINUTES = 15` — время на засыпание

### Добавление новых команд
1. Создать функцию-обработчик
2. Зарегистрировать в `main()` через `application.add_handler()`

---

## 🧪 Тестирование

### Локальное тестирование алгоритма
```bash
python demo.py
```

### Проверка импортов
```bash
python test_imports.py
```

### Тестирование с реальным ботом
1. Запустить `python main.py`
2. Найти бота в Telegram по имени/username
3. Отправить `/start` и протестировать

---

## 🚀 Деплой

### Replit
1. Создать новый Python Repl
2. Загрузить все файлы проекта
3. Установить зависимости
4. Нажать Run

### Heroku
```bash
# Создать Procfile
echo "worker: python main.py" > Procfile

# Деплой
heroku create sleepybot-app
git push heroku main
```

### VPS/Сервер
```bash
# Установка через systemd
sudo cp sleepybot.service /etc/systemd/system/
sudo systemctl enable sleepybot
sudo systemctl start sleepybot
```

---

## 🐛 Отладка

### Логи
Бот использует стандартный модуль `logging` Python:
```python
logging.basicConfig(level=logging.DEBUG)  # Для детальных логов
```

### Частые ошибки
- **Неверный токен** — проверить токен в BotFather
- **Сетевые ошибки** — проверить интернет соединение
- **Keep-alive не работает** — проверить Flask сервер

---

## 📈 Возможные улучшения

### Функционал
- [ ] Сохранение предпочтений пользователя
- [ ] Уведомления о времени пробуждения  
- [ ] Статистика сна
- [ ] Интеграция с календарём
- [ ] Поддержка часовых поясов

### Техническое
- [ ] Юнит-тесты
- [ ] Конфигурационный файл
- [ ] База данных для пользователей
- [ ] API для сторонних приложений
- [ ] Docker контейнеризация

---

## 📞 Поддержка

При возникновении проблем:
1. Проверить логи
2. Запустить `demo.py` для тестирования алгоритма
3. Проверить `test_imports.py` для диагностики зависимостей
