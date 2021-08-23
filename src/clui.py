import argparse
import os
from enum import Enum

OPTION_FILE_NOT_FOUND = "Could not find option file: "


class LogLevel(Enum):
    INFO = "Info"
    ERROR = "Error"

    def __init__(self, prefix):
        self.prefix = prefix

    @property
    def log_prefix(self) -> str:
        return "[" + self.prefix + "]"


def error(message: str) -> None:
    log(message, LogLevel.ERROR)


def log(message: str, loglevel=LogLevel.INFO) -> None:
    print(loglevel.log_prefix + message)


def option_file_path(path: str) -> str:
    if path[0] == '/':
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError(OPTION_FILE_NOT_FOUND + path)
        return path
    else:
        relative_path = os.getcwd() + '/' + path
        if not os.path.exists(relative_path):
            raise argparse.ArgumentTypeError(OPTION_FILE_NOT_FOUND + relative_path)
        return relative_path
