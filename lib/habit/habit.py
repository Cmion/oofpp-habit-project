from datetime import date, timedelta

"""
    Function converts a period to a datetime tuple representing the start and end date.
"""


def date_from_periodicity(periodicity):
    start_date = date().today()
    end_date = start_date + timedelta(days=periodicity)

    return start_date, end_date


class Habit:
    def __init__(self, name, description, periodicity):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.periodicity_to_days = self.__periodicity_to_days()
        self.start_date, self.end_date = date_from_periodicity(self.periodicity_to_days)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __periodicity_to_days(self):
        periodicity = self.periodicity.lower()
        if periodicity == 'weekly' or periodicity == 'w':
            return 7
        if periodicity == 'daily' or periodicity == 'd':
            return 1

        return 0
