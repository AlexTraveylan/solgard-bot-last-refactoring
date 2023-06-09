import datetime

import pytz
from app.adapters.date_time_fonctions import debutJourneeByTimecode, display_day_name_n_day_in_the_past, is_on_day


def test_display_day_name_n_day_in_the_past_5am():
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 4, 59), 0, "fr") == "samedi"
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 4, 59), 1, "fr") == "vendredi"
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 4, 59), 2, "fr") == "jeudi"
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 4, 59), 3, "fr") == "mercredi"
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 4, 59), 4, "fr") == "mardi"
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 4, 59), 5, "fr") == "lundi"


def test_display_day_name_n_day_in_the_past_7am():
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 5, 1), 0, "fr") == "dimanche"
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 5, 1), 1, "fr") == "samedi"
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 5, 1), 2, "fr") == "vendredi"
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 5, 1), 3, "fr") == "jeudi"
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 5, 1), 4, "fr") == "mercredi"
    assert display_day_name_n_day_in_the_past(datetime.datetime(2023, 5, 28, 5, 1), 5, "fr") == "mardi"


def test_is_on_day():
    begin_day = datetime.datetime(2023, 5, 28, 7, tzinfo=pytz.timezone("Europe/Paris")).timestamp() * 1000

    # Test pour le jour même
    actual_timestamp = datetime.datetime(2023, 5, 28, 8, tzinfo=pytz.timezone("Europe/Paris")).timestamp() * 1000
    assert is_on_day(0, int(begin_day), int(actual_timestamp))

    # Test pour un jour précédent
    actual_timestamp = datetime.datetime(2023, 5, 27, 8, tzinfo=pytz.timezone("Europe/Paris")).timestamp() * 1000
    assert is_on_day(1, int(begin_day), int(actual_timestamp))

    # Test pour un jour qui n'est pas le jour spécifié
    actual_timestamp = datetime.datetime(2023, 5, 29, 8, tzinfo=pytz.timezone("Europe/Paris")).timestamp() * 1000
    assert not is_on_day(1, int(begin_day), int(actual_timestamp))
