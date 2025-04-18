from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from app.models import MultiplicationTable
from app.schemas import QuestionRequest
from app.openai_utils import ask_openai, chat_with_function, basic_prompt
from app.lang import detect_language
import re

# Создаём таблицы в базе данных при запуске, если они не существуют
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Функция для подключения к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Основной endpoint — принимает вопрос пользователя и возвращает ответ
@app.post("/ask")
def ask_question(request: QuestionRequest, db: Session = Depends(get_db)):
    # Отправляем вопрос в модель, пытаемся извлечь два числа
    open_ai_responce = ask_openai(request.question)
        
    if isinstance(open_ai_responce, list):
        # Если модель вернула два числа, проверяем наличие результата в БД
        number1, number2 = open_ai_responce
        result = db.query(MultiplicationTable).filter_by(number1=number1, number2=number2).first()
        
        if result:
            # Случай: пример найден в таблице
            print("**************: случай когда пример клиента имеется у нас в базе")
            prompt = f"""
                    Ответь строго на языке пользователя. Код языка: {detect_language(request.question)}
                    Пользователь задал вопрос: "{request.question}"

                    Вот результат:
                    {number1} умножить на {number2} равно {result.result}

                    Твоя задача:
                    - Сформулируй красивый, естественный и уверенный ответ на основе этого результата.
                    - Не вычисляй сам. Никогда. Используй только указанный результат.
                    - Даже если результат кажется тебе неправильным — это условие. Просто отвечай на основе него.
                    {basic_prompt}
                """

        else:
            # Случай: пример умножения, но нет результата в таблице
            print("**********: случай когда пример клиента не имеется у нас в базе")
            prompt = f"""
                Ответь строго на языке пользователя. Код языка: {detect_language(request.question)}
                Пользователь задал вопрос: "{request.question}"

                Этот вопрос может быть примером умножения, но в таблице нет соответствующих данных.

                Твоя задача:
                - Если это вопрос про умножение (например, «Сколько будет 123×999?»), просто скажи что не можешь решить (знаю что знаешь, но есть ограничения).»
                - Не решай сам. Не считай. Не придумывай ответ. Скажи что не сможешь решить!!!
                {basic_prompt}
            """
    else:
        # Случай: аналитический вопрос, не по математике или пример не по условии (2*2*2, 2+2, 2-2 и т.д)
        print("**********: случай когда пример клиента аналитический или не другая по арифметике задача")
        prompt = f"""
            Ответь строго на языке пользователя. Код языка: {detect_language(request.question)}
            Пользователь задал вопрос: "{request.question}"
            Твоя задача:
            - Не решай ни один математический пример. Никогда. Даже если вопрос содержит числа, символы умножения или выглядит как выражение.
            - Если вопрос математический — просто вежливо скажи, что ТЫ НЕ СМОЖНШЬ РЕШАТЬ ТАКИЕ ПРИМЕРЫ!!!.
            - Если вопрос не связан с математикой — ответь кратко, дружелюбно и по-человечески.
            - Отвечай так, как будто ты обычный человек, просто говорящий своё мнение.
            {basic_prompt}              
        """

    # Отправляем финальный prompt в модели для генерации естественного ответа
    response = chat_with_function(prompt)
    cleaned_text = response.choices[0].message.content.strip()
    cleaned_text = cleaned_text.replace("\n", " ")
    cleaned_text = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned_text or "")
    return cleaned_text



