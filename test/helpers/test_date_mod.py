from datetime import datetime

from lib.helpers.date_mod import subtract_date, add_date


def test_subtract_date():
    date = datetime(2000, 1, 1, 1, 1, 1)
    assert subtract_date(date, days=1) == datetime(1999, 12, 31, 1, 1, 1)
    assert subtract_date(date, weeks=1) == datetime(1999, 12, 25, 1, 1, 1)
    assert subtract_date(date, weeks=1, days=1) == datetime(1999, 12, 24, 1, 1, 1)
    assert subtract_date(date, weeks=1, days=1, hours=3) == datetime(1999, 12, 23, 22, 1, 1)
    assert subtract_date(date, weeks=1, days=1, hours=3, minutes=18) == datetime(1999, 12, 23, 21, 43, 1)
    assert subtract_date(date, weeks=1, days=1, hours=3, minutes=18, seconds=200) == datetime(1999, 12, 23, 21, 39, 41)


def test_add_date():
    date = datetime(2000, 1, 1, 1, 1, 1)
    assert add_date(date, days=1) == datetime(2000, 1, 2, 1, 1, 1)
    assert add_date(date, weeks=1) == datetime(2000, 1, 8, 1, 1, 1)
    assert add_date(date, weeks=1, days=1) == datetime(2000, 1, 9, 1, 1, 1)
    assert add_date(date, weeks=1, days=1, hours=3) == datetime(2000, 1, 9, 4, 1, 1)
    assert add_date(date, weeks=1, days=1, hours=3, minutes=18) == datetime(2000, 1, 9, 4, 19, 1)
    assert add_date(date, weeks=1, days=1, hours=3, minutes=18, seconds=200) == datetime(2000, 1, 9, 4, 22, 21)
