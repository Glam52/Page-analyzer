import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла secret.env
load_dotenv()


class Config:
    # Здесь можно оставить значение по умолчанию
    SECRET_KEY = os.getenv("SECRET_KEY", "blablabla")
    DATABASE_URL = os.getenv("DATABASE_URL",
                             "postgresql://hexlet_428q_user:URj6a9NJ9Q20qdpKbI0S5eKeddjsxQiq@dpg-crn3ss56l47c73a97rng-a.oregon-postgres.render.com/hexlet_428q")

    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL environment variable is not set.")
