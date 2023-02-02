import datetime
from datetime import datetime

import pytz


def date_string_to_unix_by_format(date_string: str, date_format: str = '%d.%m.%Y %H:%M:%S') -> datetime:
    dt = datetime.strptime(date_string, date_format)
    return pytz.utc.localize(dt)


def unix_to_date_string_by_format(unix_date: int, date_format: str = '%d.%m.%Y %H:%M:%S') -> str:
    return datetime.fromtimestamp(unix_date).strftime(date_format)
