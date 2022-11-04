# class to track habits
from lib.habit.habit import Habit


class HabitTracker:
    def __init__(self):
        self.habits = {}


    def add_habit(self, name, description, periodicity):
        self.habits[name] = Habit(name, description, periodicity)
