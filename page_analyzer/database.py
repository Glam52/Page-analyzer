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

    @classmethod
    def __enter__(cls):
        """
        Context manager entry to get a database connection.
        """
        cls.connection = cls.get_connection()
        cls.cursor = cls.connection.cursor()
        return cls.cursor

    @classmethod
    def __exit__(cls, exc_type, exc_val, exc_tb):
        """
        Context manager exit to commit changes and close the connection.
        """
        if exc_type is not None:
            cls.connection.rollback()
        else:
            cls.connection.commit()
        cls.cursor.close()
        cls.connection.close()