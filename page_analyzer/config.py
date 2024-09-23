import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла secret.env
load_dotenv()


class Config:
    # Здесь можно оставить значение по умолчанию
    SECRET_KEY = os.getenv("SECRET_KEY", "blablabla")
    DATABASE_URL = os.environ.get("DATABASE_URL", default="")

    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable is not set.")
