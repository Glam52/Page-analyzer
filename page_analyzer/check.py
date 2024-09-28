import requests
from bs4 import BeautifulSoup
from typing import Optional
from .database import Database
from .exception import InvalidCheck


class Check:
    def __init__(self, database: Database):
        self.database = database

    def create_check(self, id: int) -> Optional[int]:
        result = (self.database.fetch_val
                  (f"SELECT * FROM urls WHERE id = {id};"))
        if not result:
            return None

        url = result.name  # Убедитесь, что 'name' действительно существует
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            h1_content = soup.find("h1").text.strip()\
                if soup.find("h1") else None
            title_content = soup.title.text.strip() if soup.title else None
            description_content = ""
            description_tag = soup.find("meta", attrs={"name": "description"})
            if description_tag and "content" in description_tag.attrs:
                description_content = description_tag["content"].strip()

            insert_query = (
                "INSERT INTO url_checks (url_id, "
                "status_code, "
                "h1, "
                "title, "
                "description) "
                "VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at;"
            )
            # Теперь передаем запрос и аргументы в fetch_val
            check_id, created_at = self.database.fetch_val(
                insert_query,
                (
                    id,
                    response.status_code,
                    h1_content,
                    title_content,
                    description_content,
                ),
            )

        except requests.RequestException:
            raise InvalidCheck("Произошла ошибка при проверке")
        except Exception as e:
            raise InvalidCheck(f"Произошла неожиданная ошибка: {str(e)}")

        return check_id  # Возвращаем идентификатор проверки
