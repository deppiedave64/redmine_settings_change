#!/usr/bin/env python3

import argparse
import os
from typing import Collection

import mysql.connector
from mysql.connector import errorcode

import db
from clui import error, option_file_path
from exception import Error
from redmine import set_history_default_tab_for_all_users, set_recently_used_projects_for_all_users

PROGRAM_NAME = "redmine-settings-change"
VERSION = "0.1"


def get_option_files() -> Collection[str]:
    possible_option_files = [
        os.getcwd() + '/my.cnf',
        os.path.dirname(os.path.abspath(__file__)) + '/my.cnf',
    ]
    existing_option_files = []
    for file in possible_option_files:
        if os.path.exists(file):
            existing_option_files.append(file)
    return existing_option_files


parser = argparse.ArgumentParser(description="Automatically change specific Redmine settings in a MySQL database")
parser.add_argument("--option-file", "-o", type=option_file_path, help="Path to a valid MySQL option file.")
parser.add_argument("--version", action='version', version=PROGRAM_NAME + " " + VERSION)

subparsers = parser.add_subparsers(help="Operation to execute", dest='command')
parser_test = subparsers.add_parser("test", help="Test database connection")

parser_set = subparsers.add_parser("set", help="Set some setting's value for all users")
parser_set.add_argument("setting", choices=["recently_used_projects", "history_default_tab"], help="The name of the "
                                                                                                   "setting to be "
                                                                                                   "changed")
parser_set.add_argument("value", help="The new value for the selected setting")

if __name__ == '__main__':
    args = parser.parse_args()

    if 'option_file' in vars(args) and args.option_file:
        option_files: Collection[str] = [args.option_file]
    else:
        option_files = get_option_files()
        if len(option_files) == 0:
            error("no valid option file found")
            exit(1)

    try:
        connection = mysql.connector.connect(option_files=option_files)
    except mysql.connector.errors.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            error("Could not connect to database, access denied")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            error("Could not connect to database, database not found")
        else:
            error(e.msg)
        exit(1)

    if not connection.is_connected():
        error("could not connect to mysql database")
        exit(1)

    if args.command == 'test':
        db.test_connection(connection)
    if args.command == 'set':
        if args.setting == 'recently_used_projects':
            try:
                value = int(args.value)
            except ValueError:
                error(f"recently_used_projects must be set to a valid integer value")
                exit(1)

            try:
                set_recently_used_projects_for_all_users(connection.cursor(), args.value)
            except Error as e:
                error(e.msg)
                exit(1)

            connection.commit()
        if args.setting == 'history_default_tab':
            try:
                set_history_default_tab_for_all_users(connection.cursor(), args.value)
            except Error as e:
                error(e.msg)
                exit(1)
            connection.commit()

    else:
        error("No command selected")
        exit(1)
