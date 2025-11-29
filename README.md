# 🔐 Auth Service (FastAPI)

Микросервис для аутентификации пользователей.
Поддерживает регистрацию, логин, автоматическое обновление access-токена, получение текущего пользователя и выход из системы.

Использует JWT-токены (access + refresh), которые хранятся в HTTP-only cookies.
Добавлен rate limiting на вход (5 запросов в минуту).

---

🚀 Стек технологий
---
🐍 Python 3.11+  
⚡ FastAPI  
🗄️ PostgreSQL + SQLAlchemy  
🧠 Redis + fastapi-limiter (Rate limiting)  
🔑 JWT (PyJWT)  
🐳 Docker & Docker Compose  

---

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/tt0add/auth-service.git
cd auth-service
```

2. Запустите через docker compose:

```bash
docker compose up
```

---
🔌 API Методы
---

🧑‍💻 Регистрация
---
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@test.com", "password": "123456"}'
```
Ответ:
```bash
{
  "id": 1,
  "email": "test@test.com",
  "role": "user"
}
```

---
🔐 Логин (с rate limiting 5 req/min)
---
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@test.com", "password": "123456"}' \
     -c cookies.txt
```
Access и Refresh токены будут помещены в cookies.

---
♻ Обновление access_token
---
```bash
curl -X POST "http://localhost:8000/auth/refresh" \
     -b cookies.txt \
     -c cookies.txt
```
Access токен будет обновлен в cookies.

---
👤 Получить текущего пользователя
---
```bash
curl -X GET "http://localhost:8000/auth/me" \
     -b cookies.txt
```
Ответ:
```bash
{
  "id": 1,
  "email": "test@test.com",
  "role": "user"
}
```
---
🚪 Выход из аккаунта
---
```bash
curl -X POST "http://localhost:8000/auth/logout" \
     -b cookies.txt
```
Ответ:
```bash
{
  "detail": "Logout",
}
```
Access и Refresh токены будут удалены из cookies.
