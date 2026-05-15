import os
from dotenv import load_dotenv

# Загружаем переменные из .env (если файл есть)
load_dotenv()

DB_DSN = os.getenv("DB_DSN")

if not DB_DSN:
    raise RuntimeError("Переменная окружения DB_DSN не задана! Проверьте .env файл")
