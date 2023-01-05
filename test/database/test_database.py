from datetime import datetime

from lib.database.database import Database
from lib.habit.habit import Habit


def test_db_connection():
    db = Database('test.db')
    assert db.is_connected() is True


def test_db_insertion():
    db = Database('test.db')
    db.initiate_db_test()
    test_habit = Habit(habit_id=1, name='Test Workout', description='Hit the gym twice a week', periodicity='weekly',
                       streak_in_weeks=45, streak_in_days=45 * 7,
                       start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                       current_streak_date=datetime(2022, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S'),
                       longest_streak_in_days=45 * 8,
                       )
    db.insert(test_habit)

    db_habit = db.select_one(1)

    assert db_habit is not None
    assert Habit.from_db_row(db_habit).habit_id == test_habit.habit_id


def test_db_many_insertion():
    db = Database('test.db')
    db.initiate_db_test()
    test_habit1 = Habit(habit_id=1, name='Test Workout 1', description='Hit the gym twice a week', periodicity='weekly',
                        streak_in_weeks=45, streak_in_days=45 * 7,
                        start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                        current_streak_date=datetime(2022, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S'),
                        longest_streak_in_days=45 * 8,
                        )
    test_habit2 = Habit(habit_id=2, name='Test Workout 2', description='Hit the gym twice a week', periodicity='weekly',
                        streak_in_weeks=45, streak_in_days=45 * 7,
                        start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                        current_streak_date=datetime(2022, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S'),
                        longest_streak_in_days=45 * 8,
                        )

    db.insert_many([Habit.to_db_row(test_habit1), Habit.to_db_row(test_habit2)])
    db_habit1 = db.select_one(1)

    assert db_habit1 is not None
    assert Habit.from_db_row(db_habit1).habit_id == test_habit1.habit_id

    all_habits = db.select_all()
    assert len(all_habits) == 2


def test_db_deletion():
    db = Database('test.db')
    db.initiate_db_test()
    test_habit1 = Habit(habit_id=1, name='Test Workout 1', description='Hit the gym twice a week', periodicity='weekly',
                        streak_in_weeks=45, streak_in_days=45 * 7,
                        start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                        current_streak_date=datetime(2022, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S'),
                        longest_streak_in_days=45 * 8,
                        )
    test_habit2 = Habit(habit_id=2, name='Test Workout 2', description='Hit the gym twice a week', periodicity='weekly',
                        streak_in_weeks=45, streak_in_days=45 * 7,
                        start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                        current_streak_date=datetime(2022, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S'),
                        longest_streak_in_days=45 * 8,
                        )

    db.insert_many([Habit.to_db_row(test_habit1), Habit.to_db_row(test_habit2)])
    db.delete(2)
    all_habits = db.select_all()
    assert len(all_habits) == 1


def test_db_update():
    db = Database('test.db')
    db.initiate_db_test()
    test_habit = Habit(habit_id=1, name='Test Workout 1', description='Hit the gym twice a week', periodicity='weekly',
                       streak_in_weeks=45, streak_in_days=45 * 7,
                       start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                       current_streak_date=datetime(2022, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S'),
                       longest_streak_in_days=45 * 8,
                       )
    db.insert(test_habit)

    test_habit_update = Habit(habit_id=1, name='Test Workout 1.1', description='Hit the gym twice a week',
                              periodicity='weekly',
                              streak_in_weeks=45, streak_in_days=45 * 7,
                              start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                              current_streak_date=datetime(2022, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S'),
                              longest_streak_in_days=45 * 8,
                              )
    db.update_one(1, test_habit_update)
    db_habit1 = db.select_one(1)

    assert db_habit1 is not None
    assert Habit.from_db_row(db_habit1).name == 'Test Workout 1.1'
