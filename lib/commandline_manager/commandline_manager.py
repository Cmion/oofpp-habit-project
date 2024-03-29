from math import floor

from colorama import init as init_colorama, Fore, Style
from simple_term_menu import TerminalMenu

from lib.analytics.analytics import Analytics
from lib.tracker.tracker import HabitTracker


class CommandlineManager:
    FOREGROUND = Fore.LIGHTWHITE_EX

    def __init__(self, db_path):
        init_colorama()
        self.is_active = False
        self.habit_tracker = HabitTracker(db_path)
        self.analytics = Analytics(self.habit_tracker.database)

    def start(self):
        """
        Starts a loop that keeps runs the program
        :return:
        """
        self.is_active = True
        while self.is_active:
            self.entry()

    def exit(self):
        """
        Exit the application
        """
        print(Style.RESET_ALL)
        self.habit_tracker.show_data()
        self.habit_tracker.database.close_connection();
        self.is_active = False

    @staticmethod
    def print(text):
        """
        Beautified print message
        :param text:
        :return:
        """
        print(CommandlineManager.FOREGROUND + text)

    @staticmethod
    def colorize(text, color=None):
        """
        Colorizes the commandline
        :param text:
        :param color:
        :return:
        """
        if color is None:
            return CommandlineManager.FOREGROUND + text
        else:
            return color + text

    @staticmethod
    def input(text):
        """
        Customizes the input [Adds colors and highlights]
        :param text:
        :return:
        """
        print(CommandlineManager.FOREGROUND + text + Fore.LIGHTYELLOW_EX)
        print(u"\u00BB", end=" ")

        res = input()
        if len(res.strip()) < 1:
            return CommandlineManager.input(text)
        return res.strip()

    def entry(self, msg='What would you like to do?'):
        """
        Entry point for application
        :param msg:
        :return:
        """
        self.print(msg)
        options = ["[a] Add habit", "[m] Manage habits (delete or check-off)", "[s] See habit statistics",
                   '[p] Show my habits', '[e] Exit']
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        print(
            self.colorize(u"\u00BB " + options[menu_entry_index].split('] ')[1], color=Fore.LIGHTYELLOW_EX))

        if menu_entry_index == 0:
            self.add_habit_command()
            return

        if menu_entry_index == 1:
            self.manage_habit_command()
            return

        if menu_entry_index == 2:
            self.get_habits_statistics()
            return

        if menu_entry_index == 3:
            self.habit_tracker.show_data()
            self.entry('\nWhat would you like to do next?')
            return

        if menu_entry_index == 4:
            self.exit()
            return

    def add_habit_command(self):
        """
        Prompts user to add a habit
        :return:
        """
        habit_name = self.input("What is the name of the habit you want to add? ")

        habit_description = self.input("Please enter a description for " + Fore.LIGHTBLUE_EX + f'({habit_name})'
                                       + Fore.LIGHTWHITE_EX)
        self.print('Choose your habit periodicity: ')
        options = ["[w] Weekly", "[d] Daily", '[c] Cancel']
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        print(
            self.colorize(u"\u00BB " + options[menu_entry_index].split('] ')[1], color=Fore.LIGHTYELLOW_EX))

        if menu_entry_index == 2:
            self.entry()
            return

        self.habit_tracker.add_habit(habit_name, habit_description, options[menu_entry_index].split(' ')[1])

        print(self.colorize(u"\u2714 Habit added successfully\n", color=Fore.LIGHTGREEN_EX))

        self.restart_add_habit_command()

    def restart_add_habit_command(self):
        """
        Restarts the add habit process
        :return:
        """
        options = ["[y] Yes", "[n] No", '[e] Exit']
        CommandlineManager.print('Do you want to add another habit?')
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        print(
            CommandlineManager.colorize(u"\u00BB " + options[menu_entry_index].split(' ')[1],
                                        color=Fore.LIGHTYELLOW_EX))

        if menu_entry_index == 0:
            self.add_habit_command()
            return
        if menu_entry_index == 1:
            self.habit_tracker.show_data()
            self.entry()
            return

        self.exit()

    def manage_habit_command(self):
        """
        Manages habit deletion and checking-off
        :return:
        """
        self.print('Do you want to delete or check off habits? ')
        options = ["[d] Delete", "[x] Check-off", '[c] Cancel']
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        print(
            self.colorize(u"\u00BB " + options[menu_entry_index].split('] ')[1], color=Fore.LIGHTYELLOW_EX))
        if menu_entry_index == 2:
            self.entry()
            return

        if menu_entry_index == 1:
            self.checkoff_habit_command()
            return

        if menu_entry_index == 0:
            self.delete_habit_command()
            return

    def checkoff_habit_command(self):
        """
        Handles habit check-off
        :return:
        """
        # Generates the list of commands for the user to select
        options = list(map(lambda habit: f'#{habit[0]} {habit[1]} ({habit[3]})',
                           self.habit_tracker.habits))
        self.print('Which habit(s) do you want to check-off? (Select one or more to check) ')
        terminal_menu = TerminalMenu(options, multi_select=True, show_multi_select_hint=True)
        menu_entry_indices = terminal_menu.show()

        print(
            self.colorize('\n'.join(map(lambda item: u"\u007E " + item, terminal_menu.chosen_menu_entries)),
                          color=Fore.LIGHTYELLOW_EX))

        for index in menu_entry_indices:
            entry = options[index]
            habit_id = str(entry.split(' ')[0])[1]
            response = self.habit_tracker.checkoff_habit(habit_id=int(habit_id))
            if response is None:
                print(self.colorize(u"  ⎣" + f" Checking off {entry} failed. Try again!", color=Fore.LIGHTBLACK_EX))
            else:
                print(self.colorize(u"\u2714" + f" {entry} completed successfully", color=Fore.LIGHTGREEN_EX))

        self.entry(msg='\nWhat would you like to do next? ')

    def confirm_and_delete(self, selected, all_options):
        """
        Handles confirmation and deletion of habits
        :param selected:
        :param all_options:
        :return:
        """
        options = ["[y] Yes", "[n] No", '[b] Go back']
        self.print('Are you sure you want to delete this habit(s)? ')
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            for index in selected:
                entry = all_options[index]
                habit_id = str(entry.split(' ')[0])[1]
                response = self.habit_tracker.remove_habit(habit_id=int(habit_id))
                if response is None:
                    print(self.colorize(u"\u2715" + f" Deleting {entry} failed. Try again!", color=Fore.LIGHTRED_EX))
                else:
                    print(self.colorize(u"\u2714" + f" {entry} deleted successfully", color=Fore.LIGHTGREEN_EX))

        if menu_entry_index == 1:
            pass

        if menu_entry_index == 2:
            self.delete_habit_command()

    def delete_habit_command(self):
        """
        Handles habit deletion
        :return:
        """
        options = list(map(lambda habit: f'#{habit[0]} {habit[1]} ({habit[3]})',
                           self.habit_tracker.habits))
        self.print('Which habit(s) do you want to delete? (Select one or more to check) ')
        terminal_menu = TerminalMenu(options, multi_select=True, show_multi_select_hint=True)
        menu_entry_indices = terminal_menu.show()

        print(
            self.colorize('\n'.join(map(lambda item: u"\u007E " + item, terminal_menu.chosen_menu_entries)),
                          color=Fore.LIGHTYELLOW_EX))

        self.confirm_and_delete(menu_entry_indices, options)

        self.entry(msg='\nWhat would you like to do next? ')

    def show_historical_trends(self):
        """
        Shows the historical trend analysis
        :return:
        """
        habit_with_longest_streak = self.analytics.get_habit_with_longest_streak()
        if habit_with_longest_streak is None:
            self.print(
                Fore.LIGHTBLUE_EX + 'No longest streak found, please check-off your habits to start a new streak')
            return
        if habit_with_longest_streak.periodicity == 'daily':
            self.print(Fore.LIGHTWHITE_EX + f'Habit with longest streak:' + Fore.LIGHTBLUE_EX +
                       f''' ~ #{habit_with_longest_streak.habit_id} {habit_with_longest_streak.name} | Longest Streak: {habit_with_longest_streak.longest_streak_in_days} day(s)\n''')
            return
        if habit_with_longest_streak.periodicity == 'weekly':
            self.print(Fore.LIGHTWHITE_EX + f'Habit with longest streak:' + Fore.LIGHTBLUE_EX +
                       f''' ~ #{habit_with_longest_streak.habit_id} {habit_with_longest_streak.name} | Longest Streak: {floor(habit_with_longest_streak.longest_streak_in_days / 7)} week(s)\n''')

    def show_current_trends(self):
        """
        Shows current trends, like the habit with the longest streaks
        :return:
        """

        habit_with_longest_current_streak = self.analytics.get_habit_with_longest_current_streak()

        periodicity = habit_with_longest_current_streak.periodicity.lower()

        if habit_with_longest_current_streak is None:
            self.print(
                Fore.LIGHTBLUE_EX + 'No current streaks found, please check-off your habits to start a new streak')
            return

        if periodicity == 'weekly':
            self.print(Fore.LIGHTWHITE_EX + f'Habit with longest current streak:' + Fore.LIGHTBLUE_EX +
                       f''' ~ #{habit_with_longest_current_streak.habit_id} {habit_with_longest_current_streak.name} | Current Streak: {habit_with_longest_current_streak.streak_in_weeks} week(s)\n''')
            return

        self.print(Fore.LIGHTWHITE_EX + f'Habit with longest current streak:' + Fore.LIGHTBLUE_EX +
                   f''' ~ #{habit_with_longest_current_streak.habit_id} {habit_with_longest_current_streak.name} | Current Streak: {habit_with_longest_current_streak.streak_in_days} day(s)\n''')

    def show_habits_with_same_periodicity(self):
        """
        Shows habits with the same periodicity
        :return:
        """
        self.print('Choose periodicity:')
        options = ["[w] Weekly", "[d] Daily", '[e] Exit']
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        print(
            self.colorize(u"\u00BB " + options[menu_entry_index].split('] ')[1], color=Fore.LIGHTYELLOW_EX))

        if menu_entry_index == 0:
            weekly_habits = self.analytics.get_habits_with_same_periodicity(periodicity='weekly')
            for habit in weekly_habits:
                print(
                    self.colorize(f'~ #{habit.habit_id} {habit.name} | Current Streak: {habit.streak_in_weeks} weeks ',
                                  color=Fore.LIGHTBLUE_EX))

        if menu_entry_index == 1:
            daily_habits = self.analytics.get_habits_with_same_periodicity(periodicity='daily')
            for habit in daily_habits:
                print(
                    self.colorize(f'~ #{habit.habit_id} {habit.name} | Current Streak: {habit.streak_in_weeks} weeks ',
                                  color=Fore.LIGHTBLUE_EX))

        if menu_entry_index == 2:
            self.entry(msg='\nWhat would you like to do next? ')
            return

    def get_habits_statistics(self):
        """
        Prompts a user to choose what analysis they'll like to see.
        :return:
        """
        self.print('Choose from one of the following statistics:')
        options = ["[c] Current trends", "[h] Historical trends", "[p] Habits with same periodicity", '[e] Exit']
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        print(
            self.colorize(u"\u00BB " + options[menu_entry_index].split('] ')[1], color=Fore.LIGHTYELLOW_EX))

        if menu_entry_index == 0:
            self.show_current_trends()
            return

        if menu_entry_index == 1:
            self.show_historical_trends()
            return

        if menu_entry_index == 2:
            self.show_habits_with_same_periodicity()
            return

        if menu_entry_index == 3:
            self.entry(msg='\nWhat would you like to do next? ')
            return
