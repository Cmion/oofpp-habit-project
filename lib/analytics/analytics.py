from lib.habit.habit import Habit


class Analytics:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_habit_with_longest_current_streak(self):
        """
        Retrieves the habit with current(unbroken) longest streak.
        :return:
        """
        db_habits_row = self.db_connection.select_all()
        habits = Habit.from_db_to_list(db_habits_row)

        # Iterate through each habit and updates them.
        # In an app that focuses more on performance, we'd find a better way instead of calling a for-loop.
        # The time complexities of for-loops increases exponentially based on the n, n being the number of iterations.
        # The big O notation is O(n^2)
        for habit in habits:
            # Evaluate the habit's streak incase it's been broken, since the database is not synced realtime.
            # To remove this line of code here, we'd need some sort of worker that runs at the end of every day.
            habit.evaluate_streak()
            self.db_connection.update_one(habit.habit_id, habit)

        cursor = self.db_connection.cursor.execute('''SELECT ID, name, description, periodicity, start_date, current_streak_date,
                streak_in_days, streak_in_weeks, longest_streak_in_days FROM HABIT WHERE streak_in_days > 0 ORDER BY streak_in_days DESC LIMIT 1;
                ''')

        db_habit_row = cursor.fetchone()

        # If no habits meets the criteria, None is returned.
        if db_habit_row is None:
            return None

        habit = Habit.from_db_row(db_habit_row)

        return habit

    def get_habits_with_same_periodicity(self, periodicity='weekly'):
        """
        Gets all habits with same (given) periodicity
        :param periodicity:
        :return:
        """
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
        """
        Gets the habit with the longest streak (broken or unbroken) For example: if a user has an unbroken streak for
        200 days, then breaks on the 201st day, their longest streak is considered to be 200 days.
        :return:
        """
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
