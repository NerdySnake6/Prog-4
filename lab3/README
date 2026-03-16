```markdown
# Currency Tracker API

REST API для отслеживания курсов валют (данные ЦБ РФ). Пользователи могут регистрироваться, подписываться на валюты и получать актуальные курсы.

## Технологии
- Python 3.12+
- FastAPI
- SQLAlchemy (async)
- SQLite
- Pydantic
- pytest

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone git@github.com:NerdySnake6/Prog-4.git
   cd Prog-4/lab3
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # для Linux/macOS
   # venv\Scripts\activate    # для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустите сервер:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Откройте документацию в браузере:  
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Эндпоинты

### Пользователи
- `POST /users/` – создать пользователя (username, email)
- `GET /users/` – список всех пользователей
- `GET /users/{id}` – информация о пользователе (с подписками)
- `PUT /users/{id}` – обновить данные
- `DELETE /users/{id}` – удалить пользователя

### Валюты
- `POST /currencies/update` – обновить список валют из ЦБ РФ
- `GET /currencies/` – список доступных валют
- `GET /currencies/{code}/rate` – курс указанной валюты

### Подписки
- `POST /subscriptions/` – подписаться на валюту (user_id, currency_code)
- `DELETE /subscriptions/` – отписаться от валюты

## Примеры (curl)

```bash
# Обновить валюты
curl -X POST http://127.0.0.1:8000/currencies/update

# Создать пользователя
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "ivan", "email": "ivan@example.com"}'

# Подписаться на USD
curl -X POST http://127.0.0.1:8000/subscriptions/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "currency_code": "USD"}'

# Получить курс USD
curl http://127.0.0.1:8000/currencies/USD/rate
```

## Тестирование
```bash
pytest tests/ -v
```

## Структура проекта
```
lab3/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── cbr.py                # клиент ЦБ РФ
│   └── routes/
│       ├── users.py
│       ├── currencies.py
│       └── subscriptions.py
├── tests/
│   ├── test_users.py
│   └── ...
├── requirements.txt
├── .env.example
└── README.md
```

## Примечания
- Файл базы данных `currency.db` создаётся автоматически при первом запуске.
- Для корректной работы требуется Python 3.12 или выше.
```
