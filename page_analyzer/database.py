import psycopg2
from config import Config


class Database:
    @staticmethod
    def get_connection():
        return psycopg2.connect(Config.DATABASE_URL)
