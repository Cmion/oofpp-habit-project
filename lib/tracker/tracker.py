# class to track habits
import sqlite3
from datetime import datetime, timedelta

import pandas
from colorama import Fore
from prettytable import PrettyTable, ORGMODE, FRAME

from lib.database.database import Database
from lib.habit.habit import Habit


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


def create_sample_habits():
    """
    Creates sample habits for testing.

    :return: list of :class:`Habit`
    """
    return [
        Habit(habit_id=1, name='Workout', description='Hit the gym twice a week', periodicity='weekly',
              streak_in_weeks=45, streak_in_days=45 * 7,
              start_date=(subtract_date(weeks=45).strftime('%Y-%m-%d %H:%M:%S')),
              current_streak_date=subtract_date(weeks=2).strftime('%Y-%m-%d %H:%M:%S'),
              longest_streak_in_days=45 * 8,
              ),
        Habit(habit_id=2, name='Eat healthy', description='Skip soda and hot dogs', periodicity='daily',
              streak_in_weeks=18, streak_in_days=18 * 7,
              longest_streak_in_days=18 * 8, start_date=(subtract_date(weeks=18).strftime('%Y-%m-%d %H:%M:%S')),
              current_streak_date=subtract_date(weeks=2).strftime('%Y-%m-%d %H:%M:%S')
              ),
        Habit(habit_id=3, name='Sleep well', description='Sleep at least 8 hours per night', periodicity='daily',
              streak_in_weeks=50, streak_in_days=50 * 7,
              longest_streak_in_days=50 * 8,
              start_date=(subtract_date(weeks=50).strftime('%Y-%m-%d %H:%M:%S')),
              current_streak_date=subtract_date(weeks=2).strftime('%Y-%m-%d %H:%M:%S')
              ),
        Habit(habit_id=4, name='Family', description='''Be home early for dinner, read bedtime stories to Karl, 
                Jesse and Sophie, spend quality time chitchatting with Katherine (Wife)''', periodicity='daily',
              streak_in_weeks=323, streak_in_days=323 * 7,
              longest_streak_in_days=323 * 8,
              start_date=(subtract_date(weeks=323).strftime('%Y-%m-%d %H:%M:%S')),
              current_streak_date=(subtract_date(weeks=2).strftime('%Y-%m-%d %H:%M:%S'))
              ),
        Habit(habit_id=5, name='Reading', description='Spend 3 hours weekly reading books', periodicity='weekly',
              streak_in_weeks=18, streak_in_days=18 * 7,
              longest_streak_in_days=18 * 8,
              start_date=(subtract_date(weeks=18).strftime('%Y-%m-%d %H:%M:%S')),
              current_streak_date=(subtract_date(weeks=4).strftime('%Y-%m-%d %H:%M:%S'))
              ),
    ]


class HabitTracker:
    def __init__(self):
        self.database = Database()
        self.__insert_sample_data()
        self.__refresh()

    def __refresh(self):
        self.habits = self.database.select_all()
        self.dataframe = pandas.DataFrame(self.habits, columns=['Id', 'Name', 'Description', 'Periodicity',
                                                                'Start date', 'Current streak date', 'Streak (days)',
                                                                'Streak (weeks)', 'Longest streak (days)'])

        self.dataframe.sort_values('Streak (days)', inplace=True, ascending=True)

    def __insert_sample_data(self):
        habits = list(map(Habit.to_db_row, create_sample_habits()))
        self.database.insertMany(habits)

    @staticmethod
    def print_from_list(habits):
        columns = ['Id', 'Name', 'Description', 'Periodicity',
                   'Start date', 'Current streak date', 'Streak (days)',
                   'Streak (weeks)', 'Longest streak (days)']
        table = PrettyTable()

        table.field_names = columns
        table.add_rows(habits)
        table.max_width = 30
        table.title = 'Habits'
        table.format = True
        table.horizontal_align_char = '0'
        table.hrules = FRAME
        table.set_style(ORGMODE)
        print(Fore.LIGHTWHITE_EX + table.get_string())

    def show_data(self):
        """
        Prints the data in the database.
        :return:
        """
        columns = ['Id', 'Name', 'Description', 'Periodicity',
                   'Start date', 'Current streak date', 'Streak (days)',
                   'Streak (weeks)', 'Longest streak (days)']
        table = PrettyTable()

        table.field_names = columns
        table.add_rows(self.habits)
        table.max_width = 30
        table.title = 'Habits'
        table.format = True
        table.horizontal_align_char = '0'
        table.hrules = FRAME
        table.set_style(ORGMODE)
        print(Fore.LIGHTWHITE_EX + table.get_string())

    def add_habit(self, name, description, periodicity):
        habit = Habit(name, description, periodicity)
        self.database.insert(habit)
        self.__refresh()

    def remove_habit(self, habit_id):
        try:
            self.database.delete(habit_id)
            self.__refresh()
            return habit_id
        except sqlite3.Error:
            return None

    def checkoff_habit(self, habit_id):
        db_row = self.database.select_one(habit_id)
        if db_row is None:
            return None

        habit = Habit.from_db_row(db_row)
        result = habit.recalculate_data()

        if result is not None:
            self.database.update_one(habit_id, habit)
            self.__refresh()
            return db_row
        else:
            return None
