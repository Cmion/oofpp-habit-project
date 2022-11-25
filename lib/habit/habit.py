from datetime import datetime
from math import floor

from colorama import Fore


class Habit:
    def __init__(self, name, description, periodicity, streak_in_days=None,
                 streak_in_weeks=None, start_date=None, current_streak_date=None, longest_streak_in_days=None,
                 habit_id=None):
        """
        Creates a Habit
        :param name:
        :param description:
        :param periodicity:
        :param streak_in_days:
        :param streak_in_weeks:
        :param longest_streak_in_days:
        :param start_date:
        :param current_streak_date:
        :param habit_id:
        """

        self.habit_id = habit_id
        self.streak_in_days = streak_in_days or 0
        self.streak_in_weeks = streak_in_weeks or 0
        self.longest_streak_in_days = longest_streak_in_days or 0
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.periodicity_duration = self.__periodicity_to_days()
        self.start_date = start_date or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.current_streak_date = current_streak_date or ''

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __periodicity_to_days(self):
        """
        Convert periodicity to days
        :return periodicity in days:
        """

        periodicity = self.periodicity.lower()
        if periodicity == 'weekly' or periodicity == 'w':
            return 7
        if periodicity == 'daily' or periodicity == 'd':
            return 1

        return 0

    def evaluate_streak(self):
        """
        Resets the streaks if the last streak date is greater than the habit periodicity duration (in days).
        :return:
        """

        current_streak_date = datetime.strptime(self.current_streak_date, '%Y-%m-%d %H:%M:%S')
        current_date = datetime.now()
        difference = current_date - current_streak_date
        if difference.days > self.periodicity_duration:
            if self.streak_in_days > self.longest_streak_in_days:
                self.longest_streak_in_days = self.streak_in_days
            self.streak_in_days = 0
            self.streak_in_weeks = 0
            return self
        return self

    def recalculate_data(self, print_error=True):
        """
        Recalculates the habit streaks
        :return:
        """

        current_streak_date = datetime.strptime(self.current_streak_date, '%Y-%m-%d %H:%M:%S')
        current_date = datetime.now()
        difference = current_date - current_streak_date

        # current_date_start_of = datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0, 0)
        # current_streak_date_start_of = datetime(current_streak_date.year, current_streak_date.month,
        #                                         current_streak_date.day, 0, 0, 0, 0)
        #
        # if current_date_start_of > current_streak_date_start_of:
        #     pass

        if self.periodicity_duration > difference.days:
            if print_error is True:
                print(Fore.LIGHTRED_EX +
                      u"\u2715 " + f'''You cannot mark (#{self.habit_id} {self.name}) as complete twice {self.periodicity}
''', end=' ')
            # print(Style.RESET_ALL)
            return None

        if difference.days > self.periodicity_duration:
            if self.streak_in_days > self.longest_streak_in_days:
                self.longest_streak_in_days = self.streak_in_days
            self.streak_in_days = 0
            self.streak_in_weeks = 0
            # return

        if self.periodicity_duration == 1:
            self.streak_in_days = self.streak_in_days + 1
            self.streak_in_weeks = floor(self.streak_in_days / 7)
            # return

        if self.periodicity_duration == 7:
            self.streak_in_weeks = self.streak_in_weeks + 1
            self.streak_in_days = self.streak_in_weeks * 7

        if self.streak_in_days > self.longest_streak_in_days:
            self.longest_streak_in_days = self.streak_in_days

        self.current_streak_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return self

    @staticmethod
    def from_db_row(row):
        """
        Creates a Habit object from a database row
        :param row:
        :return :class:`Habit`
        """
        return Habit(
            habit_id=row[0],
            name=row[1],
            description=row[2],
            periodicity=row[3],
            start_date=row[4],
            current_streak_date=row[5],
            streak_in_days=row[6],
            streak_in_weeks=row[7],
            longest_streak_in_days=row[8],
        )

    @staticmethod
    def to_db_row(habit):
        """
        Creates a db row tuple from a habit
        :param habit:
        :return :class:tuple
        """

        return (habit.name, habit.description, habit.periodicity,
                habit.start_date, habit.current_streak_date, habit.streak_in_days,
                habit.streak_in_weeks, habit.longest_streak_in_days)

    @staticmethod
    def from_db_to_list(rows):
        """
        Creates a list of Habit from a list of rows from the database
        :param rows:
        :return list of :class:`Habit`
        """
        return list(map(Habit.from_db_row, rows))
