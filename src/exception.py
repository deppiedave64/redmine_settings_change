from typing import Optional


class Error(Exception):
    def __init__(self, message: str, original_exception: Optional[Exception] = None):
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


class SettingNotFoundError(Error):
    def __init__(self, setting: str):
        message = f"Could not find the setting '{setting}' in this database entry"
        super().__init__(message)


class IntegerConversionError(Error):
    def __init__(self, value: str, original_exception: Optional[Exception] = None):
        message = f"Value '{value}' could not be converted to an integer"
        super().__init__(message, original_exception)


class SettingsValueError(Error):
    def __init__(self, message: str):
        super().__init__(message)
