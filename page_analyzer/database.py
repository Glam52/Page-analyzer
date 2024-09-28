import psycopg2
from psycopg2.extras import NamedTupleCursor
from typing import Any, Optional


class Database:
    def __init__(self, database_url: str):
        self.database_url: str = database_url

    def __get_connection(self):
        return psycopg2.connect(self.database_url)

    def fetch_val(self, query: str, args: Optional[tuple] = None) -> Any:
        with self.__get_connection() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                cursor.execute(query, args)
                return cursor.fetchone()

    def fetch_many(self, query: str) -> list[Any]:
        with self.__get_connection() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
