# class to track habits
import sqlite3

import pandas
from colorama import Fore
from prettytable import PrettyTable, ORGMODE, FRAME

from lib.database.database import Database
from lib.habit.habit import Habit
from lib.helpers.helpers import create_sample_habits


class HabitTracker:
    def __init__(self, db_path):
        self.database = Database(db_path)
        self.__insert_sample_data()
        self.__refresh()

    def __refresh(self):
        """
        Refresh the habits table
        """
        self.habits = self.database.select_all()
        self.dataframe = pandas.DataFrame(self.habits, columns=['Id', 'Name', 'Description', 'Periodicity',
                                                                'Start date', 'Current streak date', 'Streak (days)',
                                                                'Streak (weeks)', 'Longest streak (days)'])

        self.dataframe.sort_values('Streak (days)', inplace=True, ascending=True)

    def __insert_sample_data(self):
        """
        Insert sample habits into the database
        """
        columns = self.database.select_all()
        if len(columns) >= 1:
            return

        habits = list(map(Habit.to_db_row, create_sample_habits()))
        self.database.insert_many(habits)

    @staticmethod
    def print_from_list(habits):
        """
        Prints to the console(terminal) from the given a list of habits.
        :param habits:
        :return:
        """
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
        """
        Adds a new habit to the database.
        :param name:
        :param description:
        :param periodicity:
        :return:
        """
        habit = Habit(name, description, periodicity)
        self.database.insert(habit)
        self.__refresh()

    def remove_habit(self, habit_id):
        """
        Removes an habit from the database
        :param habit_id:
        :return:
        """
        try:
            self.database.delete(habit_id)
            self.__refresh()
            return habit_id
        except sqlite3.Error:
            return None

    def checkoff_habit(self, habit_id):
        """
        Marks a habit as completed
        :param habit_id:
        :return:
        """
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
