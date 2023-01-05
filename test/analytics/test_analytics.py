from datetime import datetime

from lib.analytics.analytics import Analytics
from lib.database.database import Database
from lib.habit.habit import Habit
from lib.helpers.date_mod import subtract_date


def initiate_test():
    db = Database('test.db')
    analytics = Analytics(db)
    db.initiate_db_test()

    test_habit1 = Habit(habit_id=1, name='Test Workout 1', description='Hit the gym twice a week', periodicity='weekly',
                        streak_in_weeks=45, streak_in_days=45 * 7,
                        start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                        current_streak_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        longest_streak_in_days=45 * 8,
                        )
    test_habit2 = Habit(habit_id=2, name='Test Workout 2', description='Hit the gym twice a week', periodicity='weekly',
                        streak_in_weeks=38, streak_in_days=38 * 7,
                        start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                        current_streak_date=datetime(2022, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S'),
                        longest_streak_in_days=38 * 8,
                        )

    test_habit3 = Habit(habit_id=3, name='Test Workout 3', description='Hit the gym twice a week', periodicity='daily',
                        streak_in_weeks=23, streak_in_days=23 * 7,
                        start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                        current_streak_date=datetime(2022, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S'),
                        longest_streak_in_days=23 * 8,
                        )

    db.insert_many([Habit.to_db_row(test_habit1), Habit.to_db_row(test_habit2), Habit.to_db_row(test_habit3)])
    return analytics


def test_get_habits_with_same_periodicity():
    analytics = initiate_test()

    habits = analytics.get_habits_with_same_periodicity('weekly')

    assert habits is not None

    assert len(habits) == 2

    for habit in habits:
        assert habit.periodicity == 'weekly'


def test_get_habit_with_longest_current_streak():
    analytics = initiate_test()

    longest_current_streak = analytics.get_habit_with_longest_current_streak()

    assert longest_current_streak is not None

    assert longest_current_streak.habit_id == 1
    assert longest_current_streak.streak_in_days == 315

    test_habit1_update = Habit(habit_id=1, name='Test Workout 1', description='Hit the gym twice a week',
                               periodicity='weekly',
                               streak_in_weeks=45, streak_in_days=45 * 7,
                               start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                               current_streak_date=subtract_date(datetime.now(), weeks=2).strftime('%Y-%m-%d %H:%M:%S'),
                               longest_streak_in_days=45 * 8,
                               )
    analytics.db_connection.update_one(1, test_habit1_update)

    longest_current_streak = analytics.get_habit_with_longest_current_streak()

    assert longest_current_streak is None


def test_get_habit_with_longest_streak():
    analytics = initiate_test()

    longest_streak = analytics.get_habit_with_longest_streak()

    assert longest_streak is not None

    assert longest_streak.habit_id == 1
    assert longest_streak.longest_streak_in_days == 360
