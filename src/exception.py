class Error(Exception):
    def __init__(self, message: str):
        self.msg = message


class TableNotFoundError(Error):
    def __init__(self, table: str):
        message = f"Could not find table {table}"
        super().__init__(message)
