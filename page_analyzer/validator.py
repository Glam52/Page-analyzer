import re
from urllib.parse import urlparse, urlunparse


class Validate:
    def validate_url(self, url: str) -> bool:
        """
        Validate the provided URL.
        :param url: URL string to validate.
        :return: True if valid, False otherwise.
        """
        if not re.match(r"^(?:http|ftp)s?://", url):
            return False
        return True

    def normalize(self, url: str) -> str:
        """
        Normalize the provided URL.
        :param url: URL string to normalize.
        :return: Normalized URL string.
        """
        parsed_url = urlparse(url)
        normalized_url: str = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                "",  # путь игнорируется
                "",
                "",
                "",  # параметры, запросы, фрагменты очищены
            )
        )
        return normalized_url
