import re

from mysql.connector.abstracts import MySQLCursorAbstract


def change_helpdesk_setting(settings: str, key: str, value: str) -> str:
    """Change a specific helpdesk setting for all projects.

    :param settings: The old helpdesk settings string
    :param key: The key of the setting to change
    :param value: The new value for the setting
    :return: The new, changed helpdesk settings string
    """

    setting_regex = re.compile(f"^    helpdesk_{key}: '.*'\\s*$")
    lines = settings.split("\n")
    for i, l in enumerate(lines):
        if setting_regex.match(l):
            lines[i] = f"    helpdesk_{key}: '{value}'"
    return "\n".join(lines)
