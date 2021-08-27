from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.cursor import MySQLCursorAbstract

import exception
from clui import log

SHOW_TABLES = "SHOW TABLES"


def test_connection(cnx: MySQLConnectionAbstract) -> None:
    log("Testing database connection")
    if cnx.is_connected():
        log(f"Successfully connected to MySQL {cnx.get_server_info()} on {cnx.server_host}.")
    else:
        log("Connection not working!")


def assert_table_exists(cursor: MySQLCursorAbstract, table: str) -> None:
    cursor.execute(SHOW_TABLES)
    tables = cursor.fetchall()
    for row in tables:
        if table in row:
            return
    raise exception.TableNotFoundError(table)
