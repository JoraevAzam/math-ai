from dotenv import load_dotenv
from openai import OpenAI
import os, json, re

load_dotenv()

# Инициализируем OpenAI клиент с API-ключом из окружения
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Базовый промпт для всех случий
basic_prompt = f"""
        - Если это аналитический вопрос (например, «Как быстро запомнить таблицу умножения?»), ответь умно, полезно и кратко, как человек.
        - Не предлагай помощь, не задавай встречных вопросов, не проявляй инициативу.
        - Ни в каком случае не упоминай таблицу, базу, ограничения модели, OpenAI, свою "неуверенность" или свои возможности.
        - Формулируй дружелюбно, кратко и по-человечески.
        - Отвечай строго по делу, естественно и дружелюбно. Без добавлений, без инициатив."""


# Функция для извлечения двух чисел из вопроса пользователя, если это пример умножения
# Возвращает [число1, число2] или None, если модель не вызвала функцию

def ask_openai(question: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {
                    "role": "system", 
                    "content": 
                        """
                        Ты помощник по таблице умножения. Твоя задача — распознавать только простые примеры умножения, состоящие ровно из двух целых чисел (например, 6×7 или 3*8).
                        Если пользователь спрашивает выражение с тремя и более числами (например, 5×7×2, 3*2*1), не вызывай функцию и ничего не распознавай.
                        Если вопрос не является примером умножения двух чисел — не вызывай функцию.
                        """
                },

                {
                    "role": "user", 
                    "content": question
                }
        ],
        
        functions=[
                {
                "name": "extract_multiplication_numbers",
                "description": "Извлечь два целых числа из вопроса пользователя.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number1": {"type": "integer", "description": "Первое число"},
                        "number2": {"type": "integer", "description": "Второе число"}
                        },
                    "required": ["number1", "number2"]
                    }
                }
        ],
        function_call="auto"
    )

    message = response.choices[0].message

    # Если функция была вызвана — парсим аргументы и возвращаем как список
    if message.function_call:
        arguments = message.function_call.arguments
        args = json.loads(arguments)
        return [args["number1"], args["number2"]]
    
    # Если функция не вызвана, модель не распознала пример умножения или пример не по условии
    return None

# Функция для генерации естественного текстового ответа от модели на основе заранее подготовленного prompt'а
def chat_with_function(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response


