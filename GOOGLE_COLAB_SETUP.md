# Інструкція: Підключення власної моделі через Google Colab

Ця інструкція описує, як розгорнути власну модель summarization на Google Colab та підключити її до застосунку.

## Крок 1: Створення API на Google Colab

### 1.1 Відкрийте Google Colab

1. Перейдіть на https://colab.research.google.com
2. Створіть новий notebook: **File → New notebook**

### 1.2 Встановіть залежності

У першій комірці виконайте:

```python
!pip install flask flask-cors transformers torch
```

### 1.3 Створіть Flask API

У новій комірці створіть API сервер:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import torch

app = Flask(__name__)
CORS(app)  # Дозволяє запити з інших доменів

# Завантажуємо модель summarization
print("Завантаження моделі...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("Модель завантажена!")

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        text = data.get('text', '')
        max_length = data.get('max_length', 100)
        min_length = data.get('min_length', 30)
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Генеруємо резюме
        result = summarizer(text, max_length=max_length, min_length=min_length)
        summary = result[0]['summary_text']
        
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 1.4 Запустіть сервер

У новій комірці:

```python
from flask import Flask
# ... (код з попередньої комірки)

# Запускаємо сервер
app.run(host='0.0.0.0', port=5000)
```

**Важливо:** Colab автоматично зупинить виконання через деякий час. Для постійної роботи потрібен ngrok.

## Крок 2: Публікація через ngrok

### 2.1 Встановіть ngrok

У новій комірці Colab:

```python
!pip install pyngrok
```

### 2.2 Налаштуйте ngrok

```python
from pyngrok import ngrok

# Отримуємо токен ngrok (зареєструйтеся на https://ngrok.com)
# Вставте ваш токен:
ngrok.set_auth_token("YOUR_NGROK_TOKEN")

# Створюємо туннель на порт 5000
public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")
```

### 2.3 Запустіть API через ngrok

```python
# Запускаємо Flask у фоновому режимі
import threading

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

thread = threading.Thread(target=run_flask, daemon=True)
thread.start()

# Показуємо публічний URL
print(f"API доступне за адресою: {public_url}/summarize")
```

**Приклад URL:** `https://abc123.ngrok.io/summarize`

## Крок 3: Підключення до застосунку

### 3.1 Додайте URL у змінні оточення

**На Render:**
1. Web Service → Environment → Environment Variables
2. Додайте:
   - **Key:** `COLAB_API_URL`
   - **Value:** `https://abc123.ngrok.io/summarize` (ваш URL з ngrok)

**Локально (.env):**
```env
COLAB_API_URL=https://abc123.ngrok.io/summarize
```

### 3.2 Перезапустіть застосунок

Застосунок автоматично використовуватиме Colab API замість Hugging Face.

## Крок 4: Тестування

1. Відкрийте застосунок
2. Введіть текст поста
3. Ввімкніть "Використовувати ШІ"
4. Перевірте, що резюме генерується через вашу модель на Colab

## Важливі зауваження

⚠️ **Google Colab має обмеження:**
- Сесія може закритися через неактивність
- Обмеження на час виконання (12 годин для безкоштовного акаунту)
- ngrok безкоштовний план має обмеження

✅ **Рекомендації:**
- Використовуйте Colab для тестування та навчання
- Для production краще використовувати Hugging Face API або власний сервер
- Зберігайте notebook на Google Drive для відновлення

## Альтернатива: Власний сервер

Замість Colab можна розгорнути модель на:
- **Heroku** (безкоштовний tier)
- **Render** (окремий Web Service)
- **AWS/GCP** (платні, але стабільні)
- **Власний VPS**

---

**Готово!** Тепер ваш застосунок використовує власну модель на Google Colab.

