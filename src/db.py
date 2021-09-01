from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.cursor import MySQLCursorAbstract

import exception
from clui import log

USER_PREFERENCES = 'user_preferences'
USER = 'user'

SHOW_TABLES = 'SHOW TABLES'
GET_USER_PREFERENCES = 'SELECT user_preferences.others FROM user_preferences WHERE user_preferences.user_id=(SELECT users.id FROM users WHERE users.login="{}")'
SET_USER_PREFERENCES = 'UPDATE user_preferences SET user_preferences.others="{}" WHERE user_preferences.user_id=(SELECT users.id FROM users WHERE users.login="{}")'
GET_USERS = 'SELECT users.login FROM users'
GET_USER_ID = 'SELECT users.id FROM users WHERE users.login="{}"'


def test_connection(cnx: MySQLConnectionAbstract) -> None:
    log("Testing database connection")
    if cnx.is_connected():
        log(f"Successfully connected to MySQL {cnx.get_server_info()} on {cnx.server_host}.")
    else:
        log("Connection not working!")


def assert_table_exists(cursor: MySQLCursorAbstract, table: str) -> None:
    cursor.execute(SHOW_TABLES)
    result: list = cursor.fetchall()
    for row in result:
        if table in row:
            return
    raise exception.TableNotFoundError(table)


def get_user_list(cursor: MySQLCursorAbstract) -> list:
    assert_table_exists(cursor, USER)
    cursor.execute(GET_USERS)
    return [t[0] for t in cursor.fetchall()]


def assert_user_exists(cursor: MySQLCursorAbstract, username: str) -> None:
    if username not in get_user_list(cursor):
        raise exception.UserNotFoundError(username)


def get_user_preferences(cursor: MySQLCursorAbstract, username: str) -> str:
    assert_table_exists(cursor, USER_PREFERENCES)
    assert_table_exists(cursor, USER)
    assert_user_exists(cursor, username)
    cursor.execute(GET_USER_PREFERENCES.format(username))
    result: list = cursor.fetchall()
    return result[0][0]


def set_user_preferences(cursor: MySQLCursorAbstract, username: str, value: str) -> None:
    assert_table_exists(cursor, USER_PREFERENCES)
    assert_table_exists(cursor, USER)
    assert_user_exists(cursor, username)
    cursor.execute(SET_USER_PREFERENCES.format(value, username))
    cursor.fetchall()
