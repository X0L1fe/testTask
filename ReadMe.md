## Содержание

- [Описание проекта](#описание-проекта)
- [Структура проекта](#структура-проекта)

## Описание проекта

Это проект простого веб-приложения для управления списком задач с использованием aiohttp, PostgreSQL, Docker Compose и аутентификацией через Bearer-токен (с access и refresh токенами).

## Структура проекта

```plaintext
project/
├── app/
│   ├── __init__.py
│   ├── main.py                # Основной файл для запуска приложения
│   ├── config.py              # Конфигурации приложения (параметры БД)
│   ├── models.py            # Модель Task
│   ├── schemas.py           # Схема Task
│   ├── crud.py
│   ├── auth.py           # Логика для токенов и аутентификации
│   └── routers/               # Маршруты приложения
│       ├── __init__.py
│       ├── auth.py            # Маршруты аутентификации
│       └── tasks.py           # Маршруты задач
├── Dockerfile
├── docker-compose.yml
├── requirements.txt           # Зависимости проекта
└── .env                       # Переменные окружения
```
