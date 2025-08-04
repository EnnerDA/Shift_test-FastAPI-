```markdown
# Salary Service API

REST-сервис для защищенного доступа к информации о зарплате сотрудников с JWT-аутентификацией.

## Содержание
- [Требования](#требования)
- [Установка](#установка)
- [Конфигурация](#конфигурация)
- [Запуск](#запуск)
- [Использование API](#использование-api)
- [Тестовые данные](#тестовые-данные)
- [Документация](#документация)
- [Тестирование](#тестирование)

## Требования

- Python 3.9+
- pip (менеджер пакетов)

## Установка

1. Клонируйте репозиторий:
```bash
git clone <your-repo-url>
cd <project-directory>
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Конфигурация

Создайте файл `.env` в корне проекта:
```ini
SECRET_KEY=your_super_secret_key_for_jwt
```

## Запуск

Запустите сервис в development режиме:
```bash
uvicorn main:app --reload
```

Сервис будет доступен по адресу:  
http://127.0.0.1:8000

## Использование API

### Аутентификация
**POST /login**  
Запрос:
```json
{
  "username": "Ivan",
  "password": "Ivan1"
}
```

Ответ:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Получение информации о зарплате
**GET /salary_info**  
Заголовки:
```
Authorization: Bearer <your_token>
```

Пример ответа:
```json
{
  "message": "Привет, Ivan! Твоя текущая зарплата: 275000.0. Повышение будет 2025-11-15"
}
```

## Тестовые данные

Доступные тестовые пользователи:

| Логин | Пароль |
|-------|--------|
| Ivan  | Ivan1  |
| Kate  | Kate1  |
| aaa   | 123    |

## Документация

Доступна после запуска сервиса:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Тестирование

Для тестирования используйте клиент:
```bash
python client.py
```

Или вручную через curl:
```bash
# Получение токена
curl -X POST -H "Content-Type: application/json" -d '{"username":"Ivan","password":"Ivan1"}' http://localhost:8000/login

# Запрос зарплаты
curl -X GET -H "Authorization: Bearer <token>" http://localhost:8000/salary_info
```

## Особенности реализации

- База данных: SQLite (salary.db)
- Срок действия токена: 1 час
- Все запросы к /salary_info требуют валидного токена
- Автоматическое создание тестовых данных при первом запуске
```