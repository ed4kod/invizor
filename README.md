# Invizor - Система управления имуществом

[![GitHub Repo](https://img.shields.io/badge/GitHub-invizor-blue?logo=github)](https://github.com/ed4kod/invizor.git)

Invizor - это веб-приложение на FastAPI для управления имуществом материально-ответственных лиц. Пользователи могут регистрироваться, создавать счета и управлять своим имуществом.

## Возможности

- 🔐 JWT аутентификация пользователей
- 👤 Регистрация и вход в систему
- 📋 Создание и управление счетами (accounts)
- 🏷️ Добавление имущества с описанием, статусом и изображениями
- 📸 Загрузка реальных изображений (JPG, PNG, GIF, WebP)
- 📱 Адаптивный дизайн с Tailwind CSS
- 🎨 Современный UI с карточками в стиле Ozon

## Технологии

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: Jinja2, Tailwind CSS
- **Аутентификация**: JWT токены
- **Безопасность**: bcrypt для хеширования паролей
- **Изображения**: Pillow для обработки изображений

## Структура проекта

```
fastest/
├── app/
│   ├── __init__.py
│   ├── auth.py              # JWT аутентификация
│   ├── database.py          # Настройка базы данных
│   ├── models.py            # SQLAlchemy модели
│   ├── schemas.py           # Pydantic схемы
│   ├── utils.py             # Утилиты для работы с файлами
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Роуты аутентификации
│       ├── accounts.py      # Роуты счетов
│       └── assets.py        # Роуты имущества
├── static/
│   └── style.css           # Дополнительные стили
├── templates/
│   ├── base.html           # Базовый шаблон
│   ├── login.html          # Страница входа
│   ├── register.html       # Страница регистрации
│   ├── accounts.html       # Список счетов
│   ├── assets.html         # Список имущества
│   └── asset_detail.html   # Детали имущества
├── uploads/                # Папка для загруженных изображений
├── main.py                 # Точка входа приложения
├── requirements.txt        # Зависимости
└── README.md              # Документация
```

## Установка и запуск

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/ed4kod/invizor.git
cd fastest
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
```

3. **Активируйте виртуальное окружение:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

5. **Запустите приложение:**
```bash
python main.py
```

6. **Откройте браузер:**
```
http://localhost:8000
```

## Использование

1. **Регистрация**: Перейдите на `/auth/register` для создания аккаунта
2. **Вход**: Используйте `/auth/login` для входа в систему
3. **Счета**: После входа вы увидите список ваших счетов
4. **Имущество**: Нажмите на счет для просмотра имущества
5. **Добавление**: Используйте кнопки "+" для создания новых записей

## Модели данных

### User (Пользователь)
- `id`: Уникальный идентификатор
- `email`: Email пользователя
- `username`: Имя пользователя
- `full_name`: Полное имя
- `hashed_password`: Хешированный пароль
- `is_active`: Статус активности

### Account (Счет)
- `id`: Уникальный идентификатор
- `name`: Название счета
- `description`: Описание
- `owner_id`: ID владельца (связь с User)
- `created_at`: Дата создания

### Asset (Имущество)
- `id`: Уникальный идентификатор
- `name`: Название имущества
- `description`: Описание
- `status`: Статус (active, inactive, damaged, lost)
- `image_url`: URL изображения
- `account_id`: ID счета (связь с Account)
- `created_at`: Дата создания
- `updated_at`: Дата обновления

## API Endpoints

### Аутентификация
- `GET /auth/login` - Страница входа
- `POST /auth/login` - Обработка входа
- `GET /auth/register` - Страница регистрации
- `POST /auth/register` - Обработка регистрации
- `GET /auth/logout` - Выход из системы

### Счета
- `GET /accounts` - Список счетов пользователя
- `POST /accounts` - Создание нового счета
- `GET /accounts/{account_id}` - Детали счета

### Имущество
- `GET /assets/account/{account_id}` - Список имущества в счете
- `POST /assets/account/{account_id}` - Добавление имущества
- `GET /assets/{asset_id}` - Детали имущества
- `POST /assets/{asset_id}/update` - Обновление имущества

## Безопасность

- Пароли хешируются с помощью bcrypt
- JWT токены для аутентификации
- Все страницы защищены авторизацией
- Валидация данных через Pydantic схемы

## Разработка

Для разработки рекомендуется:

1. Использовать Python 3.8+
2. Установить pre-commit хуки
3. Следовать PEP 8 стандартам
4. Добавлять тесты для новых функций

## Лицензия

MIT License 