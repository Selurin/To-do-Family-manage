import os
from dotenv import load_dotenv

# Загружаем переменные из .env (если файл есть локально)
load_dotenv()

# Amvera по умолчанию предоставляет переменную DATABASE_URL для PostgreSQL.
# Поэтому сначала проверяем её. Если её нет — берём твою локальную DB_DSN из .env.
DB_DSN = os.getenv("DATABASE_URL") or os.getenv("DB_DSN")

if not DB_DSN:
    raise RuntimeError("Переменная окружения для базы данных (DATABASE_URL или DB_DSN) не задана!")