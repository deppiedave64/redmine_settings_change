class Error(Exception):
    def __init__(self, message: str, original_exception: Exception = None):
        self.msg = message
        self.original_exception = original_exception


class TableNotFoundError(Error):
    def __init__(self, table: str):
        message = f"Could not find table {table}"
        super().__init__(message)


class UserNotFoundError(Error):
    def __init__(self, username: str):
        message = f"Could not find user {username}"
        super().__init__(message)
