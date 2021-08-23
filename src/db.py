from mysql.connector.abstracts import MySQLConnectionAbstract

from clui import log


def test_connection(cnx: MySQLConnectionAbstract) -> None:
    log("Testing database connection")
    if cnx.is_connected():
        log(f"Successfully connected to MySQL {cnx.get_server_info()} on {cnx.server_host}.")
    else:
        log("Connection not working!")
