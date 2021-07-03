import argparse
import os

OPTION_FILE_NOT_FOUND = "Could not find option file: "


def error(message: str) -> None:
    print("Error, " + message)


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
