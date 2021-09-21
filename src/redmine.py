import re

from mysql.connector.cursor import MySQLCursorAbstract

from db import get_user_list, get_user_preferences, set_user_preferences
from exception import IntegerConversionError, SettingNotFoundError

RECENTLY_USED_PROJECTS_REGEX = r'^:recently_used_projects: (\d+)$'
RECENTLY_USED_PROJECTS_REPLACEMENT = ':recently_used_projects: {}'


def get_recently_used_projects_string(user_preferences: str) -> int:
    pattern = re.compile(RECENTLY_USED_PROJECTS_REGEX, re.MULTILINE)
    match = pattern.search(user_preferences)
    if match is None:
        raise SettingNotFoundError(user_preferences)
    try:
        return int(match.group(1))
    except ValueError:
        raise IntegerConversionError(match.group(1))


def replace_recently_used_projects_string(user_preferences: str, value: int) -> str:
    pattern = re.compile(RECENTLY_USED_PROJECTS_REGEX, re.MULTILINE)
    return pattern.sub(RECENTLY_USED_PROJECTS_REPLACEMENT.format(value), user_preferences)


def set_recently_used_projects_for_all_users(cnx: MySQLCursorAbstract, value: int) -> None:
    users = get_user_list(cnx)
    for user in users:
        preferences = get_user_preferences(cnx, user)
        set_user_preferences(cnx, user, replace_recently_used_projects_string(preferences, value))
