# Генератор хештегів для постів (Flask + PostgreSQL на Render)

Це клієнт‑серверний веб‑застосунок для **генерації хештегів** до тексту поста з **реєстрацією/логіном**, збереженням історії генерацій, та **віддаленою БД PostgreSQL** (Render).

## 1) Локальний запуск (Windows)

### Вимоги
- Python 3.11+ (рекомендовано 3.11)
- Git (за бажанням)

### Кроки
1. Відкрий PowerShell у папці проєкту:

```powershell
cd D:\IndFirst
```

2. Створи venv та активуй:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Встанови залежності:

```powershell
pip install -r requirements.txt
```

4. Створи локальні змінні оточення (Windows PowerShell):

```powershell
$env:FLASK_ENV="development"
$env:SECRET_KEY="dev-secret-change-me"
$env:DATABASE_URL="sqlite:///local.db"
```

> Для локальної перевірки можна використовувати SQLite. Для лабораторної (Render) потрібен PostgreSQL.

5. Запусти застосунок (таблиці створяться автоматично при першому запуску):

```powershell
flask --app app run
```

6. Відкрий в браузері: `http://127.0.0.1:5000`

### (Опційно) Міграції Flask-Migrate
Якщо хочеш міграції (не обов’язково для лабораторної), виконай:

```powershell
flask --app app db init
flask --app app db migrate -m "init"
flask --app app db upgrade
```

## 2) Деплой на Render (обов’язково для лабораторної)

### 2.1 Створи PostgreSQL на Render
1. Render → **New** → **PostgreSQL**.
2. Назва: `hashtag-db` (або будь-яка).
3. Після створення скопіюй **External Database URL** (це буде `DATABASE_URL`).

### 2.2 Створи Web Service на Render
1. Завантаж код на GitHub (або інший git remote).
2. Render → **New** → **Web Service** → підключи репозиторій.
3. Налаштування:
- **Environment**: Python
- **Build Command**:

```bash
pip install -r requirements.txt
```

- **Start Command**:

```bash
gunicorn "app:app"
```

4. Додай **Environment Variables**:
- `SECRET_KEY` = довгий випадковий рядок
- `DATABASE_URL` = External Database URL з PostgreSQL (Render)
- `FLASK_ENV` = `production`

### 2.3 Міграції на Render (таблиці в БД)
Таблиці створюються автоматично при першому запуску.
Якщо хочеш використати міграції — Render → Web Service → **Shell**:

```bash
flask --app app db upgrade
```

## 3) Функціонал
- Реєстрація користувача
- Вхід/вихід
- Генерація хештегів з тексту поста (укр/англ)
- Збереження історії генерацій в БД
- Профіль: перегляд статистики (скільки генерацій)

## 4) Структура БД (спрощено)
- `users`: дані користувача (email, password_hash, created_at)
- `hashtag_requests`: запити генерації (post_text, hashtags, created_at, user_id)

## 5) Інтеграція ШІ (Лабораторна №2)

### 5.1 Модуль штучного інтелекту

Проєкт підтримує **два варіанти** підключення ШІ:

#### Варіант А: Hugging Face Inference API (рекомендовано)

**Файли:**
- `hashtag_app/ai_summarizer.py` — модуль для роботи з Hugging Face API
- Використовує модель `facebook/bart-large-cnn` для summarization

**Як підключити:**
1. Зареєструватися на https://huggingface.co
2. Створити API токен: Settings → Access Tokens → New token
3. Додати токен у змінні оточення Render: `HUGGINGFACE_API_TOKEN`
4. Детальна інструкція: `HUGGINGFACE_SETUP.md`

**Як працює:**
1. Користувач вводить текст поста
2. ШІ генерує коротке резюме тексту (якщо текст довгий)
3. На основі резюме генеруються хештеги (більш релевантні)
4. Резюме зберігається в БД (`hashtag_requests.ai_summary`)

#### Варіант Б: Google Colab з власною моделлю (альтернатива)

**Файли:**
- `hashtag_app/ai_colab.py` — модуль для роботи з власною моделлю на Colab

**Як підключити:**
1. Створити Flask API на Google Colab з моделлю summarization
2. Опублікувати через ngrok
3. Додати URL у змінні оточення: `COLAB_API_URL`
4. Детальна інструкція: `GOOGLE_COLAB_SETUP.md`

**Примітка:** Застосунок автоматично використовує Colab (якщо налаштовано `COLAB_API_URL`), інакше — Hugging Face API.

### 5.2 Візуалізація результатів

**Сторінка статистики** (`/statistics`):
- Таблиця загальної статистики (всього генерацій, з ШІ)
- Діаграма активності по днях (останні 30 днів) — Chart.js
- Діаграма використання ШІ (doughnut chart)
- Таблиця топ-10 найпопулярніших хештегів

**Доступ:** Після входу → меню "Статистика"

### 5.3 GitHub Actions (CI/CD)

**Файл:** `.github/workflows/deploy.yml`

**Що робить:**
- При кожному **Push** або **Pull Request** запускає тести
- Перевіряє якість коду (flake8)
- При мерджі в `main` може тригерити деплой (опціонально)

**Налаштування:**
1. Створи репозиторій на GitHub
2. Push код:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-username/hashtag-generator.git
   git push -u origin main
   ```
3. GitHub Actions автоматично запуститься

### 5.4 Командна робота

**Документація:** `CONTRIBUTING.md`

**Процес:**
1. Створення гілки: `git checkout -b feature/назва-функції`
2. Розробка та коміти
3. Push: `git push origin feature/назва-функції`
4. Створення Pull Request на GitHub
5. Code Review
6. Мердж PR → автоматичний деплой

**Структура гілок:**
- `main` — стабільний код (автоматичний деплой)
- `feature/*` — нові функції
- `bugfix/*` — виправлення помилок
- `hotfix/*` — критичні виправлення

## 6) Для звіту (що скрінити)

### Лабораторна №1:
- Головна сторінка (форма генерації)
- Сторінка реєстрації/логіну
- Сторінка "Історія"
- Render: сторінка Web Service (URL) і PostgreSQL
- Структура БД (таблиці/поля)

### Лабораторна №2:
- Головна сторінка з чекбоксом "Використовувати ШІ"
- Результат генерації з резюме від ШІ
- Сторінка "Статистика" з діаграмами
- GitHub репозиторій (скріншот)
- GitHub Actions workflow (скріншот запуску)
- Pull Request (якщо була командна робота)
- Структура гілок у GitHub


