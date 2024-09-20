import re
from flask import flash
from bs4 import BeautifulSoup
import requests
from page_analyzer.database import Database
from urllib.parse import urlparse, urlunparse


class URLManager:
    @staticmethod
    def normalize_url(url):
        parsed_url = urlparse(url)
        # Игнорируем путь, используем только схему и сетевую часть
        normalized_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            '',  # путь игнорируется
            '', '', ''  # параметры, запросы, фрагменты очищены
        ))
        return normalized_url

    @staticmethod
    def add_url(url):
        if len(url) > 255 or not re.match(r"^https?://", url):
            flash("Некорректный URL")
            return None

        # Нормализация URL
        normalized_url = URLManager.normalize_url(url)

        conn = Database.get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM urls WHERE name = %s", (normalized_url,))
        existing_url = cur.fetchone()

        if existing_url:
            flash("Страница уже существует")
            return existing_url[0]

        cur.execute("INSERT INTO urls (name) VALUES (%s) RETURNING id", (normalized_url,))
        new_url_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        flash("Страница успешно добавлена")
        return new_url_id

    @staticmethod
    def list_urls():
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT urls.id, urls.name, MAX(url_checks.created_at) AS last_check, 
            MAX(url_checks.status_code) AS status_code FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            GROUP BY urls.id
            ORDER BY urls.created_at DESC
        """
        )
        urls = cur.fetchall()
        cur.close()
        conn.close()
        return urls

    @staticmethod
    def get_url(id):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
        url = cur.fetchone()

        if url is None:
            return None

        created_at_formatted = url[2].strftime("%Y-%m-%d")
        url = (url[0], url[1], created_at_formatted)

        cur.execute(
            "SELECT id, created_at, status_code, h1, title, description "
            "FROM url_checks WHERE url_id = %s "
            "ORDER BY created_at DESC",
            (id,),
        )
        checks = cur.fetchall()

        for i in range(len(checks)):
            checks[i] = list(checks[i])
            checks[i][1] = checks[i][1].strftime("%Y-%m-%d")

        cur.close()
        conn.close()

        return url, checks

    @staticmethod
    def create_check(id):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
        result = cur.fetchone()

        if not result:
            return None

        url = result[1]
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            h1_content = soup.find("h1").text.strip() if soup.find("h1") else None
            title_content = soup.title.text.strip() if soup.title else None
            description_content = ""
            description_tag = soup.find("meta", attrs={"name": "description"})
            if description_tag and "content" in description_tag.attrs:
                description_content = description_tag["content"].strip()

            cur.execute(
                "INSERT INTO url_checks (url_id, status_code, h1, title, description) "
                "VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at;",
                (
                    id,
                    response.status_code,
                    h1_content,
                    title_content,
                    description_content,
                ),
            )
            check_id, created_at = cur.fetchone()
            flash("Страница успешно проверена")

        except requests.RequestException:
            flash("Произошла ошибка при проверке")
        except Exception as e:
            flash(f"Произошла неожиданная ошибка: {str(e)}")
        finally:
            conn.commit()
            cur.close()
            conn.close()

        return id
