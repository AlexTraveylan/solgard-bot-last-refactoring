import datetime

from app.adapters.date_time_fonctions import is_clash_on


def test_is_clash_on_weekend():
    now = datetime.datetime(2023, 6, 16, 15, 0)  # Vendredi après 14h UTC
    assert is_clash_on(now) == True

    now = datetime.datetime(2023, 6, 17, 12, 0)  # Samedi
    assert is_clash_on(now) == True

    now = datetime.datetime(2023, 6, 17, 14, 0)  # Samedi après 14h UTC
    assert is_clash_on(now) == True


def test_is_clash_on_weekday():
    now = datetime.datetime(2023, 6, 15, 10, 0)  # Jeudi avant 14h UTC
    assert is_clash_on(now) == False

    now = datetime.datetime(2023, 6, 16, 10, 0)  # Vendredi avant 14h UTC
    assert is_clash_on(now) == False

    now = datetime.datetime(2023, 6, 18, 15, 0)  # Dimanche après 14h UTC
    assert is_clash_on(now) == False


def test_is_clash_on_edge_cases():
    now = datetime.datetime(2023, 6, 14, 14, 0)  # Mardi avant 14h UTC
    assert is_clash_on(now) == False

    now = datetime.datetime(2023, 6, 20, 14, 0)  # Lundi après 14h UTC
    assert is_clash_on(now) == False

    now = datetime.datetime(2023, 6, 17, 13, 0)  # Samedi avant 14h UTC
    assert is_clash_on(now) == True

    now = datetime.datetime(2023, 6, 17, 14, 0)  # Samedi après 14h UTC
    assert is_clash_on(now) == True
