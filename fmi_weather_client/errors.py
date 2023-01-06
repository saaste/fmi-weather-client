class ClientError(Exception):
    """Represent client error from FMI service"""
    def __init__(self, status_code: int, message: str, *args):
        super().__init__(*args)
        self.status_code: int = status_code
        self.message: str = message


class ServerError(Exception):
    """Represents service error from service error"""
    def __init__(self, status_code: int, body: str, *args):
        super().__init__(*args)
        self.status_code: int = status_code
        self.body: str = body
