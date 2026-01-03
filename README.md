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

## 5) Для звіту (що скрінити)
- Головна сторінка (форма генерації)
- Сторінка реєстрації/логіну
- Сторінка “Історія”
- Render: сторінка Web Service (URL) і PostgreSQL
- Структура БД (таблиці/поля)


