## Содержание

- [Описание проекта](#описание-проекта)
- [Структура проекта](#структура-проекта)
- [Использование Postman](#использование-postman)
- [Запуск с использованием Docker](#запуск-с-использованием-docker)
- [Контакты](#контакты)

## Описание проекта

Это проект простого веб-приложения для управления списком задач с использованием aiohttp, PostgreSQL, Docker Compose и аутентификацией через Bearer-токен (с access и refresh токенами).

## Структура проекта

```plaintext
testBeresnevFastApi/
├── app/
│   ├── __init__.py
│   ├── main.py                # Основной файл для запуска приложения
│   ├── config.py              # Конфигурации приложения (параметры БД)
│   ├── models.py              # Модели User, Task
│   ├── schemas.py             # Схема User, Task
│   ├── crud.py
│   ├── auth.py                # Логика для токенов и аутентификации
│   └── routers/               # Маршруты приложения
│       ├── __init__.py
│       ├── auth.py            # Маршруты аутентификации
│       └── tasks.py           # Маршруты задач
├── Dockerfile
├── docker-compose.yml
├── requirements.txt           # Зависимости проекта
└── .env                       # Переменные окружения
```

## Использование Postman

### Шаг 1: Регистрация пользователя

1. Откройте Postman.
2. Создайте новый `POST` запрос к `http://127.0.0.1:8000/auth/register`.
3. В `Body` выберите `raw` и `JSON`.
4. Введите данные для регистрации, например:
    ```json
    {
        "username": "Docker",
        "password": "123456"
    }
    ```
5. Нажмите `Send`. Если регистрация успешна, вы получите JSON с информацией о пользователе.
6. Пример вывода:
    ```json
    {
        "username": "Docker",
        "id": 1
    }
    ```

### Шаг 2: Получение access и refresh токенов

1. Создайте новый `POST` запрос к `http://127.0.0.1:8000/auth/login`.
2. В Headers введите следующие `ключ:значение`
   - `accept`: `application/json`
   - `Content-Type`: `application/x-www-form-urlencoded`
3. В `Body` выберите `x-www-form-urlencoded`.
4. Введите следующие параметры:
   - `grant_type`: `password`
   - `username`: `Docker`
   - `password`: `123456`
   - `scope`: ``
   - `client_id`: `string`
   - `client_secret`: `string`
5. Нажмите `Send`. Если аутентификация успешна, вы получите `access_token` и `refresh_token`.
6. Пример вывода:
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImV4cCI6MTczMDkwODY3M30.Gspys_bY9r-dc8v-2L-C5owjQG18Zx5gc-rUa46q_40",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImV4cCI6MTczMDk5MzI3M30.Qi2TaYIPKK7RPxisomwcXL4wHHUu20NtmWXZNDBoeFI"
    }
    ```

### Шаг 3: Создание задачи

1. Создайте новый `POST` запрос к `http://127.0.0.1:8000/tasks/`.
2. В `Headers` добавьте:
   - `accept`: `application/json`
   - `Content-Type`: `application/json`
   - `Authorization`: `Bearer <ваш access_token>`
3. В `Body` выберите `raw` и `JSON`.
4. Введите данные для задчи, например:

    ```json
    {
        "title": "Docker task",
        "description": "about of Docker task",
        "status": "in process"
    }
    ```
5. Нажмите `Send`. Если задача успешно создана, вы получите JSON с её данными.
6. Пример вывода:
    ```json
    {
        "title": "Docker task",
        "description": "about of Docker task",
        "status": "in process",
        "id": 1,
        "user_id": 1
    }
    ```

### Шаг 4: Получиение списка задач

1. Создайте новый `GET` запрос к `http://127.0.0.1:8000/tasks/`.
2. В `Headers` добавьте:
   - `accept`: `application/json`
   - `Authorization`: `Bearer <ваш access_token>`
3. Нажмите `Send`. Вы получите список задач, созданных текущим пользователем.
4. Пример вывода:
    ```json
    [
        {
            "title": "Docker task",
            "description": "about of Docker task",
            "status": "in process",
            "id": 1,
            "user_id": 1
        }
    ]
    ```

### Шаг 5: Получиение списка задач по статусу

1. Создайте новый `GET` запрос к `http://127.0.0.1:8000/tasks/`.
2. В Params добавьте:
   - `status`:`<название_статуса_задачи>`
3. В `Headers` добавьте:
   - `accept`: `application/json`
   - `Authorization`: `Bearer <ваш access_token>`
4. Нажмите `Send`. Вы получите список задач, созданных текущим пользователем.
5. Пример вывода:
    ```json
    [
        {
            "title": "Docker task",
            "description": "about of Docker task",
            "status": "in process",
            "id": 1,
            "user_id": 1
        }
    ]

### Шаг 6: Получиение задачи по её id

1. Создайте новый `GET` запрос к `http://127.0.0.1:8000/tasks/<номер_задачи>`.
2. В `Headers` добавьте:
   - `accept`: `application/json`
   - `Authorization`: `Bearer <ваш access_token>`
3. Нажмите `Send`. Вы получите список задач, созданных текущим пользователем.
4. Пример вывода:
    ```json
    [
        {
            "title": "Docker task",
            "description": "about of Docker task",
            "status": "in process",
            "id": 1,
            "user_id": 1
        }
    ]
    ```

### Шаг 7: Редактирование задачи по её id

1. Создайте новый `GET` запрос к `http://127.0.0.1:8000/tasks/<номер_задачи>`.
2. В `Headers` добавьте:
   - `accept`: `application/json`
   - `Authorization`: `Bearer <ваш access_token>`
3. В `Body` выберите `raw` и `JSON`.
4. Введите данные для задачи, например:

    ```json
    {
        "title": "Docker task EDIT",
        "description": "This edited task of Docker",
        "status": "ready",
    }
    ```
5. Нажмите `Send`. Вы получите список задач, созданных текущим пользователем.
6. Пример вывода:
    ```json
    {
        "title": "Docker task EDIT",
        "description": "This edited task of Docker",
        "status": "ready",
        "id": 1,
        "user_id": 1
    }
    ```

### Шаг 8: Удадение задачи по её id

1. Создайте новый `GET` запрос к `http://127.0.0.1:8000/tasks/<номер_задачи>`.
2. В `Headers` добавьте:
   - `accept`: `application/json`
   - `Authorization`: `Bearer <ваш access_token>`
3. Нажмите `Send`. Вы получите список задач, созданных текущим пользователем.
4. Пример вывода:
    ```json
    []
    ```

## Запуск с использованием Docker

```bash
docker-compose up --build
```

## Контакты

Если у вас есть вопросы или предложения, свяжитесь со мной по:
- **Электронной почте:** `lighttolight228@gmail.com`;
- **Telegram:** [Inrigt](https://t.me/Inrigt)