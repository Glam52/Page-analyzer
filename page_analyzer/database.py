import psycopg2
from page_analyzer.config import Config


class Database:
    @staticmethod
    def get_connection() -> psycopg2.extensions.connection:
        """
        Get a database connection.
        :return: Database connection object.
        """
        return psycopg2.connect(Config.DATABASE_URL)
