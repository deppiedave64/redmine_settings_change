#!/usr/bin/env python3

import argparse
import os
from typing import Collection

import mysql.connector
from mysql.connector import errorcode

from clui import error, option_file_path
import db

PROGRAM_NAME = "redmine-settings-change"
VERSION = "0.1"

parser = argparse.ArgumentParser(description="Automatically change specific Redmine settings in a MySQL database")
parser.add_argument("command", metavar="COMMAND", choices=["test"], help="The operation to perform. Choices include "
                                                                         "%(choices)s.")
parser.add_argument("--option-file", "-o", type=option_file_path, help="Path to a valid MySQL option file.")
parser.add_argument("--version", action='version', version=PROGRAM_NAME + " " + VERSION)


def get_option_files() -> Collection[str]:
    possible_option_files = [
        os.getcwd() + '/my.cnf',
        os.path.dirname(os.path.abspath(__file__)) + '/my.cnf',
    ]
    option_files = []
    for file in possible_option_files:
        if os.path.exists(file):
            option_files.append(file)
    return option_files


def main() -> None:
    args = parser.parse_args()

    if 'option_file' in vars(args) and args.option_file:
        option_files: Collection[str] = [args.option_file]
    else:
        option_files = get_option_files()
        if len(option_files) == 0:
            error("no valid option file found")
            exit(1)

    try:
        cnx = mysql.connector.connect(option_files=option_files)
    except mysql.connector.errors.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            error("Could not connect to database, access denied")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            error("Could not connect to database, database not found")
        exit(1)

    if not cnx.is_connected():
        error("could not connect to mysql database")
        exit(1)

    if args.command == "test":
        db.test_connection(cnx)


if __name__ == '__main__':
    main()
