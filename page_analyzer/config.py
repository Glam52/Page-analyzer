import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла secret.env
load_dotenv()


class Config:
    # Здесь можно оставить значение по умолчанию
    SECRET_KEY = os.getenv("SECRET_KEY", "blablabla")
    DATABASE_URL = os.getenv("DATABASE_URL",
                             "postgresql://postgres:postgres@localhost:5432/hexlet")

    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable is not set.")
