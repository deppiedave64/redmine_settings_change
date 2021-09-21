import re

from mysql.connector.cursor import MySQLCursorAbstract

from db import get_user_list, get_user_preferences, set_user_preferences
from exception import IntegerConversionError, SettingNotFoundError, SettingsValueError

RECENTLY_USED_PROJECTS_REGEX = r'^:recently_used_projects: (\d+)$'
RECENTLY_USED_PROJECTS_REPLACEMENT = ':recently_used_projects: {}'
HISTORY_DEFAULT_TAB_REGEX = r'^:history_default_tab: (\w+)$'
HISTORY_DEFAULT_TAB_REPLACEMENT = ':history_default_tab: {}'
HISTORY_DEFAULT_TAB_CHOICES = ["history", "notes", "properties", "time_entries", "changesets", "last_tab_visited"]


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


def replace_history_default_tab_string(user_preferences: str, value: str) -> str:
    pattern = re.compile(HISTORY_DEFAULT_TAB_REGEX, re.MULTILINE)
    return pattern.sub(HISTORY_DEFAULT_TAB_REPLACEMENT.format(value), user_preferences)


def set_recently_used_projects_for_all_users(cnx: MySQLCursorAbstract, value: int) -> None:
    users = get_user_list(cnx)
    for user in users:
        preferences = get_user_preferences(cnx, user)
        set_user_preferences(cnx, user, replace_recently_used_projects_string(preferences, value))


def set_history_default_tab_for_all_users(cnx: MySQLCursorAbstract, value: str) -> None:
    if value not in HISTORY_DEFAULT_TAB_CHOICES:
        raise SettingsValueError(f"Value for history_default_tab must be one of {HISTORY_DEFAULT_TAB_CHOICES}")
    users = get_user_list(cnx)
    for user in users:
        preferences = get_user_preferences(cnx, user)
        set_user_preferences(cnx, user, replace_history_default_tab_string(preferences, value))
