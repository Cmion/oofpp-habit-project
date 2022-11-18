from colorama import init as init_colorama, Fore, Style
from simple_term_menu import TerminalMenu

from lib.analytics.analytics import Analytics
from lib.tracker.tracker import HabitTracker


class CommandlineManager:
    FOREGROUND = Fore.LIGHTWHITE_EX

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
        """
        Exit the application
        """
        print(Style.RESET_ALL)
        self.habit_tracker.show_data()
        self.is_active = False

    @staticmethod
    def print(text):
        print(CommandlineManager.FOREGROUND + text)

    @staticmethod
    def colorize(text, color=None):
        if color is None:
            return CommandlineManager.FOREGROUND + text
        else:
            return color + text

    @staticmethod
    def input(text):
        print(CommandlineManager.FOREGROUND + text + Fore.LIGHTYELLOW_EX)
        print(u"\u00BB", end=" ")
        return input()

    def entry(self, msg='What would you like to do?'):
        self.print(msg)
        options = ["[a] Add habit", "[m] Manage habits (delete or check off)", "[s] See habit statistics",
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

        if menu_entry_index == 3:
            self.habit_tracker.show_data()
            self.entry('\nWhat would you like to do next?')
            return

        if menu_entry_index == 4:
            self.exit()
            return

    def add_habit_command(self):
        habit_name = self.input("What is the name of the habit you want to add? ")
        habit_description = self.input("What is the description of the habit you want to add? ")
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

        print(self.colorize(u"\u2713 Habit added successfully\n", color=Fore.LIGHTGREEN_EX))

        self.restart_add_habit_command()

    def restart_add_habit_command(self):
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
        self.print('Do you want to delete or check off habits? ')
        options = ["[d] Delete", "[c] Check off", '[c] Cancel']
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
        options = list(map(lambda habit: f'#{habit[0]} {habit[1]} ({habit[3]})',
                           self.habit_tracker.habits))
        self.print('Which habit(s) do you want to check off? (Select one or more to check) ')
        terminal_menu = TerminalMenu(options, multi_select=True, show_multi_select_hint=True)
        menu_entry_indices = terminal_menu.show()

        print(
            self.colorize('\n'.join(map(lambda item: u"\u007E " + item, terminal_menu.chosen_menu_entries)),
                          color=Fore.LIGHTYELLOW_EX))

        for index in menu_entry_indices:
            entry = options[index]
            habit_id = str(entry.split(' ')[0])[1]
            self.habit_tracker.checkoff_habit(habit_id=int(habit_id))

        print(self.colorize(u"\u2713 Habit(s) completed successfully\n", color=Fore.LIGHTGREEN_EX))

        self.entry(msg='What would you like to do next? ')

    def delete_habit_command(self):
        pass
