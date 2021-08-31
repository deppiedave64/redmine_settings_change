import re

from exception import SettingNotFoundError, IntegerConversionError

RECENTLY_USED_PROJECTS_REGEX = r'^:recently_used_projects: (\d+)$'


def get_recently_used_projects(user_preferences: str) -> int:
    pattern = re.compile(RECENTLY_USED_PROJECTS_REGEX, re.MULTILINE)
    match = pattern.search(user_preferences)
    if match is None:
        raise SettingNotFoundError(user_preferences)
    try:
        return int(match.group(1))
    except ValueError:
        raise IntegerConversionError(match.group(1))
