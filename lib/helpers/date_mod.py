from datetime import datetime, timedelta


def subtract_date(date=datetime.now(), days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0,
                  hours=0, weeks=0):
    """
    Subtracts a number of days, hours, minutes, seconds and microseconds from a datetime object.

    :param date: The datetime object to subtract.
    :param days: The number of days to subtract.
    :param seconds: The number of seconds to subtract.
    :param microseconds: The number of microseconds to subtract.
    :param milliseconds: The number of milliseconds to subtract.
    :param minutes: The number of minutes to subtract.
    :param hours: The number of hours to subtract.
    :param weeks: The number of weeks to subtract.
    """
    return date - timedelta(days=days, seconds=seconds, microseconds=microseconds,
                            milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)


def add_date(date=datetime.now(), days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0,
             hours=0, weeks=0):
    """
    Adds a number of days, hours, minutes, seconds and microseconds from a datetime object.

    :param date: The datetime object to subtract.
    :param days: The number of days to subtract.
    :param seconds: The number of seconds to subtract.
    :param microseconds: The number of microseconds to subtract.
    :param milliseconds: The number of milliseconds to subtract.
    :param minutes: The number of minutes to subtract.
    :param hours: The number of hours to subtract.
    :param weeks: The number of weeks to subtract.
    """
    return date + timedelta(days=days, seconds=seconds, microseconds=microseconds,
                            milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)
