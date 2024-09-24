import re
from flask import abort, flash


class Validate:
    def validate_url(url: str) -> None:
        """
        Validate the provided URL.
        :param url: URL string to validate.
        :raises: Abort with status code 422 if the URL is invalid.
        """
        if not re.match(r"^(?:http|ftp)s?://", url):
            flash("Некорректный URL")  # Добавляем флеш-сообщение
            abort(422)  # Генерируем ошибку 422
