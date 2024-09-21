import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла secret.env
load_dotenv(dotenv_path='./secret.env')

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "blablabla")  # Здесь можно оставить значение по умолчанию
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable is not set.")
