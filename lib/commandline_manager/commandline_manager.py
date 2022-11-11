from colorama import init as init_colorama, Fore
from simple_term_menu import TerminalMenu

from lib.analytics.analytics import Analytics
from lib.tracker.tracker import HabitTracker


class CommandlineManager:
    def __init__(self):
        init_colorama()
        self.is_active = False
        self.habit_tracker = HabitTracker()
        self.analytics = Analytics(self.habit_tracker.database)

    def start(self):
        self.is_active = True
        while self.is_active:
            self.entry()

    def exit(self):
        self.habit_tracker.show_data()
        self.is_active = False

    @staticmethod
    def print(text):
        print(Fore.LIGHTWHITE_EX + text)

    @staticmethod
    def colorize(text, color=Fore.LIGHTWHITE_EX):
        return color + text

    @staticmethod
    def input(text):
        print(Fore.LIGHTWHITE_EX + text + Fore.LIGHTYELLOW_EX, end=" ")
        return input()

    def entry(self):
        options = ["[a] Add habit", "[m] Manage Habit (Delete or Checkoff)", "[s] See Habit Statistics", '[e] Exit']
        terminal_menu = TerminalMenu(options, title=CommandlineManager.colorize('What would you like to do?'))
        menu_entry_index = terminal_menu.show()
        print(CommandlineManager.colorize(options[menu_entry_index].split(' ')[1], color=Fore.LIGHTYELLOW_EX))

        if menu_entry_index == 0:
            self.add_habit_command()
            return

        if menu_entry_index == 3:
            self.exit()
            return

    def add_habit_command(self):
        habit_name = CommandlineManager.input("What is the name of the habit you want to add? ")
        habit_description = CommandlineManager.input("What is the description of the habit you want to add? ")
        options = ["[w] Weekly", "[d] Daily", '[c] Cancel']
        terminal_menu = TerminalMenu(options, title=CommandlineManager.colorize('Choose your habit periodicity'))
        menu_entry_index = terminal_menu.show()
        print(CommandlineManager.colorize(options[menu_entry_index].split(' ')[1], color=Fore.LIGHTYELLOW_EX))

        if menu_entry_index == 2:
            self.entry()
            return

        self.habit_tracker.add_habit(habit_name, habit_description, options[menu_entry_index].split(' ')[1])

        print(CommandlineManager.colorize(u"\u2713 Habit added successfully\n", color=Fore.LIGHTGREEN_EX))

        self.restart_add_habit_command()

    def restart_add_habit_command(self):
        options = ["[y] Yes", "[n] No", '[e] Exit']
        terminal_menu = TerminalMenu(options, title=CommandlineManager.colorize('Do you want to add another habit?'))
        menu_entry_index = terminal_menu.show()
        print(CommandlineManager.colorize(options[menu_entry_index].split(' ')[1], color=Fore.LIGHTYELLOW_EX))

        if menu_entry_index == 0:
            self.add_habit_command()
            return
        if menu_entry_index == 1:
            self.habit_tracker.show_data()
            self.entry()
            return

        self.exit()
