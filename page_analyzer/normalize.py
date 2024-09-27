from urllib.parse import urlparse, urlunparse


class Normalizer:
    def __init__(self, url: str):
        self.url = url

    def normalize(self) -> str:
        parsed_url = urlparse(self.url)
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