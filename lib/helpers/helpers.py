from lib.habit.habit import Habit
from lib.helpers.date_mod import subtract_date


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
