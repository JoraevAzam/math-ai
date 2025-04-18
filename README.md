
# 🧠 Math AI — Управляемый ИИ через MCP

Проект на FastAPI и Docker, где модель OpenAI (GPT-4o-mini) отвечает на вопросы по математике, **основываясь только на кастомной базе данных**. Используется подход MCP (Model Context Protocol) для ограничения поведения модели.

---

## 📌 Возможности

- Управление ответами ИИ через базу данных (MCP)
- Специально искажённая таблица умножения (+1 к результату)
- Поддержка определения языка запроса
- REST API `/ask` для общения с моделью
- Автоматическое создание базы при старте

---

## ⚙️ Стек технологий

- Python 3.11  
- FastAPI  
- PostgreSQL  
- SQLAlchemy  
- OpenAI API  
- Docker / Docker Compose  

---

## 🚀 Быстрый запуск

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/JoraevAzam/math-ai.git
   cd math-ai
   ```

2. Собрать и запустить контейнеры:
   ```bash
   docker-compose up --build -d
   ```

3. Открыть API:
   ```
   http://localhost:8000
   ```

---

## 🧾 Структура проекта

```
.
├── app/
│   ├── main.py             # FastAPI приложение
│   ├── database.py         # Подключение к PostgreSQL
│   ├── models.py           # Модель таблицы умножения
│   ├── schemas.py          # Pydantic-схемы
│   ├── openai_utils.py     # Запросы к OpenAI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🧪 Пример запроса

**POST** `/ask`

```json
{
  "question": "Сколько будет 7 × 8?"
}
```

**Ответ:**

```json
{
  "answer": "7 × 8 = 57"
}
```

📌 *Это не ошибка! Модель контролируется: результат хранится в базе как (7 × 8) + 1.*

---

## 🌐 Определение языка

Вопрос пользователя автоматически определяется по языку (через `langdetect`), и ответ приходит на этом же языке.

---

## 🧠 Зачем это?

Такой подход нужен для:
- обучения моделей на нестандартных данных,
- демонстрации контроля ИИ,
- использования MCP для точных ответов на основе своей базы.


