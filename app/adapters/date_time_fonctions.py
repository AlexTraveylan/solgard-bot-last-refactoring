import datetime
import locale
from typing import Literal
import pytz
from babel.dates import format_date


def debutJourneeByTimecode(timecode: int) -> int:
    paris_tz = pytz.timezone("Europe/Paris")
    dt = datetime.datetime.utcfromtimestamp(timecode / 1000.0)
    dt = pytz.UTC.localize(dt).astimezone(paris_tz)  # Convert to Paris timezone

    day_start = dt.replace(hour=7, minute=0, second=0, microsecond=0)

    if dt.hour < 7:
        day_start = day_start - datetime.timedelta(days=1)

    begin_day_timestamp = int(day_start.timestamp() * 1000)

    return begin_day_timestamp


def is_on_day(nb_day_passed: Literal[0, 1, 2, 3, 4, 5], begin_day: int, actual_timestamp: int) -> bool:
    one_day_timestamp = 24 * 60 * 60 * 1000
    if nb_day_passed == 0:
        return actual_timestamp > begin_day
    else:
        return begin_day - one_day_timestamp * nb_day_passed < actual_timestamp < begin_day - one_day_timestamp * (nb_day_passed - 1)


def display_day_name_n_day_in_the_past(now: datetime.datetime, nb_day_in_past: Literal[0, 1, 2, 3, 4, 5]):
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    now -= datetime.timedelta(hours=5)
    one_day_before = now - datetime.timedelta(days=nb_day_in_past)
    day_name = format_date(one_day_before, "EEEE", locale="fr")

    return day_name
