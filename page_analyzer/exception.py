class InvalidUrl(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


class InvalidCheck(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail
