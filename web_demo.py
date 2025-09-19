#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Веб-интерфейс для тестирования SleepyBot без Telegram
Запустите этот файл и откройте http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify
from main import SleepCalculator
import re

app = Flask(__name__)

# HTML шаблон
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌙 SleepyBot Web Demo</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, button {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            box-sizing: border-box;
        }
        input {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        input:focus {
            outline: none;
            border-color: rgba(255, 255, 255, 0.6);
        }
        button {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            cursor: pointer;
            margin-top: 10px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }
        button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        .examples {
            margin: 20px 0;
            font-size: 14px;
            opacity: 0.8;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            display: none;
        }
        .wake-time {
            margin: 10px 0;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            font-family: monospace;
        }
        .error {
            color: #ff6b6b;
            background: rgba(255, 107, 107, 0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌙 SleepyBot Demo</h1>
        
        <div class="input-group">
            <label for="sleepTime">🛏 Когда планируете лечь спать?</label>
            <input type="text" id="sleepTime" placeholder="23:30, сейчас, +15, +30...">
        </div>
        
        <div class="examples">
            <strong>📝 Примеры ввода:</strong><br>
            • <code>23:30</code> — лечь спать в 23:30<br>
            • <code>сейчас</code> — лечь спать прямо сейчас<br>
            • <code>+15</code> — лечь спать через 15 минут<br>
            • <code>+30</code> — лечь спать через 30 минут
        </div>
        
        <button onclick="calculateSleep()">💤 Рассчитать циклы сна</button>
        
        <div id="result" class="result"></div>
    </div>

    <script>
        function calculateSleep() {
            const sleepTime = document.getElementById('sleepTime').value.trim();
            const resultDiv = document.getElementById('result');
            
            if (!sleepTime) {
                showError('Пожалуйста, введите время сна!');
                return;
            }
            
            fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({sleepTime: sleepTime})
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showError(data.error);
                } else {
                    showResult(data);
                }
            })
            .catch(error => {
                showError('Ошибка при расчёте: ' + error);
            });
        }
        
        function showResult(data) {
            const resultDiv = document.getElementById('result');
            
            let html = `
                <h3>🛏 Время сна: ${data.sleepTimeFormatted}</h3>
                <p>💤 С учётом 15 минут на засыпание</p>
                <h4>⏰ Оптимальные времена пробуждения:</h4>
            `;
            
            data.wakeTimes.forEach(wakeTime => {
                html += `<div class="wake-time">${wakeTime}</div>`;
            });
            
            html += '<p><strong>😴 Выберите любое из этих времён для комфортного пробуждения!</strong></p>';
            
            resultDiv.innerHTML = html;
            resultDiv.style.display = 'block';
            resultDiv.className = 'result';
        }
        
        function showError(message) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `<h3>❌ Ошибка</h3><p>${message}</p>`;
            resultDiv.style.display = 'block';
            resultDiv.className = 'result error';
        }
        
        // Обработка Enter
        document.getElementById('sleepTime').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                calculateSleep();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Главная страница"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/calculate', methods=['POST'])
def calculate():
    """API для расчёта времени сна"""
    try:
        data = request.get_json()
        sleep_input = data.get('sleepTime', '').strip()
        
        if not sleep_input:
            return jsonify({'error': 'Пожалуйста, введите время сна!'})
        
        # Парсим время
        sleep_time = SleepCalculator.parse_time_input(sleep_input)
        
        if sleep_time is None:
            return jsonify({'error': 'Не удалось понять формат времени. Попробуйте: 23:30, сейчас, +15'})
        
        # Рассчитываем времена пробуждения
        wake_times = SleepCalculator.calculate_wake_times(sleep_time)
        
        # Формируем ответ
        sleep_time_str = sleep_time.strftime("%H:%M")
        
        # Определяем описание времени сна
        if sleep_input.lower() == "сейчас":
            sleep_description = "прямо сейчас"
        elif sleep_input.startswith("+"):
            sleep_description = f"через {sleep_input[1:]} минут"
        else:
            sleep_description = f"в {sleep_time_str}"
        
        # Очищаем wake_times от markdown разметки для веба
        clean_wake_times = []
        for wake_time in wake_times:
            # Убираем ** и заменяем эмодзи
            clean_time = re.sub(r'\*\*(.*?)\*\*', r'\1', wake_time)
            clean_wake_times.append(clean_time)
        
        return jsonify({
            'sleepTimeFormatted': f"{sleep_description} ({sleep_time_str})",
            'wakeTimes': clean_wake_times
        })
        
    except Exception as e:
        return jsonify({'error': f'Внутренняя ошибка: {str(e)}'})

if __name__ == '__main__':
    print("🌙 SleepyBot Web Demo запущен!")
    print("📱 Откройте http://localhost:5000 в браузере")
    print("🛑 Нажмите Ctrl+C для остановки")
    app.run(debug=True, host='0.0.0.0', port=5000)
