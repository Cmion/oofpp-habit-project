from lib.habit.habit import Habit


class Analytics:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_habit_with_longest_current_streak(self):
        db_habits_row = self.db_connection.select_all()
        habits = Habit.from_db_to_list(db_habits_row)

        for habit in habits:
            habit.evaluate_streak()
            self.db_connection.update_one(habit.habit_id, habit)

        cursor = self.db_connection.cursor.execute('''SELECT ID, name, description, periodicity, start_date, current_streak_date,
                streak_in_days, streak_in_weeks, longest_streak_in_days FROM HABIT WHERE streak_in_days > 0 ORDER BY streak_in_days DESC LIMIT 1;
                ''')

        db_habit_row = cursor.fetchone()



        if db_habit_row is None:
            return None

        habit = Habit.from_db_row(db_habit_row)

        return habit

    def get_habits_with_same_periodicity(self, periodicity):
        cursor = self.db_connection.cursor.execute('''SELECT id, name, description, periodicity, start_date, 
        current_streak_date, streak_in_days, streak_in_weeks, longest_streak_in_days from HABIT WHERE periodicity = :periodicity ORDER BY 
        start_date DESC;''', {'periodicity': periodicity})

        db_habits_row = cursor.fetchall()

        habits = Habit.from_db_to_list(db_habits_row)

        for habit in habits:
            habit.evaluate_streak()
            self.db_connection.update_one(habit.habit_id, habit)

        return habits

    def get_habit_with_longest_streak(self):
        db_habits_row = self.db_connection.select_all()
        habits = Habit.from_db_to_list(db_habits_row)

        for habit in habits:
            habit.evaluate_streak()
            self.db_connection.update_one(habit.habit_id, habit)

        cursor = self.db_connection.cursor.execute('''SELECT id, name, description, periodicity, start_date, current_streak_date, streak_in_days,
             streak_in_weeks, longest_streak_in_days from HABIT WHERE longest_streak_in_days > 0 ORDER BY longest_streak_in_days DESC LIMIT 1;''')

        db_habit_row = cursor.fetchone()

        if db_habit_row is None:
            return None

        habit = Habit.from_db_row(db_habit_row)

        return habit
