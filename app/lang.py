from langdetect import detect, LangDetectException


# Определяет язык текста по коду ISO
def detect_language(text: str) -> str:
        try:
            language_code = detect(text)
            return language_code
        except LangDetectException:
              return 'ru'