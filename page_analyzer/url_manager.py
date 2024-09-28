from page_analyzer.database import Database
from datetime import datetime
from config import Config
import psycopg2
from url import UrlId, Url, UrlWithLastCheck
from exception import InvalidUrl
from validator import Validate


class URLManager:
    def __init__(self):
        self.database = Database(Config.DATABASE_URL)
        self.validator = Validate()

    def create_url(self, url: str) -> UrlId | None:
        if self.validator.validate_url(url):
            normalized = self.validator.normalize(url)
            try:
                query = (f"INSERT INTO urls (name, created_at) "
                         f"VALUES ('{normalized}',"
                         f" '{datetime.now()}') RETURNING id;")
                returned = self.database.fetch_val(query=query)
            except psycopg2.IntegrityError as exc:
                raise InvalidUrl(detail="Страница уже существует") from exc
            else:
                return returned.id
        else:
            raise InvalidUrl(detail="Некорректный URL")

    def list_urls(self) -> list[Url]:
        query = """
        SELECT
            u.id,
            u.name,
            u.created_at,
            uc.status_code
        FROM
            urls u
        LEFT JOIN
            url_checks uc ON u.id = uc.url_id
        ORDER BY
            u.created_at DESC;
        """
        returned_urls = self.database.fetch_many(query=query)

        return [
            UrlWithLastCheck(
                id=url[0],  # id из таблицы urls
                name=url[1],  # name из таблицы urls
                created_at=url[2],  # created_at из таблицы urls
                status_code=url[3],  # status_code из таблицы url_checks
            )
            for url in returned_urls
        ]

    # url_manager.py, метод get_url
    def get_url(self, id: int):
        if not isinstance(id, int):
            return None

        query = f"SELECT id, name, created_at FROM urls WHERE id = {id};"
        result = self.database.fetch_val(query)
        if result is None:
            return None
        return (result.id, result.name,
                result.created_at, self.get_checks_for_url(id))

    def get_checks_for_url(self, url_id: int):
        query = f"SELECT * FROM url_checks WHERE url_id = {url_id};"
        checks = self.database.fetch_many(query)  # Передаем только запрос
        return checks

    def get_existing_urls(self, url: str) -> UrlId | None:
        normalized = self.validator.normalize(url)
        query = f"SELECT id FROM urls WHERE name = '{normalized}';"
        result = self.database.fetch_val(query=query)
        return result.id if result else None
