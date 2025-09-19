#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import re
from datetime import datetime, timedelta
from typing import List, Optional

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = "8381755892:AAGDdAHcvYt3RO7DvKmjSO716o_mdSIZxCY"

# Keep-alive сервер (для Replit)
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def keep_alive():
    return "🤖 SleepyBot is running!"

def run_keep_alive():
    app.run(host='0.0.0.0', port=8080)

def start_keep_alive():
    server = threading.Thread(target=run_keep_alive)
    server.daemon = True
    server.start()

class SleepCalculator:
    """Класс для расчёта циклов сна"""
    
    SLEEP_CYCLE_MINUTES = 90  # Один цикл сна = 90 минут
    FALL_ASLEEP_MINUTES = 15  # Время на засыпание
    
    @staticmethod
    def parse_time_input(text: str) -> Optional[datetime]:
        """Парсит пользовательский ввод времени"""
        text = text.strip().lower()
        now = datetime.now()
        
        # Если пользователь написал "сейчас"
        if text == "сейчас":
            return now
        
        # Если пользователь написал "+10", "+20", "+30" и т.д.
        plus_match = re.match(r'\+(\d+)', text)
        if plus_match:
            minutes_to_add = int(plus_match.group(1))
            return now + timedelta(minutes=minutes_to_add)
        
        # Парсинг времени в формате чч:мм
        time_match = re.match(r'(\d{1,2}):(\d{2})', text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2))
            
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                sleep_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # Если время уже прошло сегодня, берём завтрашний день
                if sleep_time <= now:
                    sleep_time += timedelta(days=1)
                
                return sleep_time
        
        return None
    
    @staticmethod
    def calculate_wake_times(sleep_time: datetime) -> List[str]:
        """Рассчитывает оптимальные времена пробуждения"""
        # Добавляем время на засыпание
        actual_sleep_start = sleep_time + timedelta(minutes=SleepCalculator.FALL_ASLEEP_MINUTES)
        
        wake_times = []
        
        # Рассчитываем 6 вариантов пробуждения (от 3 до 8 циклов)
        for cycles in range(3, 9):
            sleep_duration = cycles * SleepCalculator.SLEEP_CYCLE_MINUTES
            wake_time = actual_sleep_start + timedelta(minutes=sleep_duration)
            
            # Форматируем время
            time_str = wake_time.strftime("%H:%M")
            
            # Добавляем информацию о количестве сна
            hours = sleep_duration // 60
            minutes = sleep_duration % 60
            duration_str = f"{hours}ч {minutes}м" if minutes > 0 else f"{hours}ч"
            
            wake_times.append(f"🕐 **{time_str}** ({cycles} циклов, {duration_str} сна)")
        
        return wake_times

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_message = """
🌙 **Добро пожаловать в SleepyBot!** 

Я помогу вам рассчитать оптимальные времена пробуждения по 90-минутным циклам сна.

📝 **Как пользоваться:**
• Напишите время сна в формате `чч:мм` (например: `23:30`)
• Или напишите `сейчас` для расчёта от текущего времени
• Или `+10`, `+20`, `+30` чтобы начать сон через N минут

💡 **Я автоматически добавлю 15 минут на засыпание!**

Просто отправьте мне время, когда планируете лечь спать! 😴
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
❓ **Справка по SleepyBot**

**Примеры использования:**
• `23:30` — лягу спать в 23:30
• `сейчас` — лягу спать прямо сейчас
• `+15` — лягу спать через 15 минут

**Как это работает:**
🔄 Один цикл сна = 90 минут
😴 Добавляю 15 минут на засыпание
⏰ Показываю 6 вариантов пробуждения (3-8 циклов)

**Почему именно 90 минут?**
Это средняя продолжительность полного цикла сна (REM + глубокий сон). Пробуждение в конце цикла поможет вам чувствовать себя бодрее!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def calculate_sleep(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Основная функция расчёта времени сна"""
    user_input = update.message.text
    
    # Парсим ввод пользователя
    sleep_time = SleepCalculator.parse_time_input(user_input)
    
    if sleep_time is None:
        error_message = """
❌ **Не удалось понять время!**

📝 **Примеры правильного ввода:**
• `23:30` или `23:30`
• `сейчас`
• `+10`, `+20`, `+30`

Попробуйте ещё раз! 😊
        """
        await update.message.reply_text(error_message, parse_mode='Markdown')
        return
    
    # Рассчитываем времена пробуждения
    wake_times = SleepCalculator.calculate_wake_times(sleep_time)
    
    # Формируем ответ
    sleep_time_str = sleep_time.strftime("%H:%M")
    
    if user_input.lower() == "сейчас":
        sleep_input_text = "прямо сейчас"
    elif user_input.startswith("+"):
        sleep_input_text = f"через {user_input[1:]} минут"
    else:
        sleep_input_text = f"в {sleep_time_str}"
    
    response = f"""
🛏 **Вы ложитесь спать {sleep_input_text}**
💤 **С учётом 15 минут на засыпание**

⏰ **Лучшие времена для пробуждения:**

{chr(10).join(wake_times)}

😴 **Сладких снов!** Выберите любое из этих времён для комфортного пробуждения.
    """
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик неизвестных команд"""
    await update.message.reply_text(
        "🤔 Не знаю такой команды. Напишите /help для справки или просто укажите время сна!"
    )

def main() -> None:
    """Главная функция"""
    
    # Запускаем keep-alive сервер для Replit
    start_keep_alive()
    
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Обработчик текстовых сообщений (время сна)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_sleep))
    
    # Обработчик неизвестных команд
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    # Запускаем бота
    logger.info("🤖 SleepyBot запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
