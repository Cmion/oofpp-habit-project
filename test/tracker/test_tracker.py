from lib.database.database import Database
from lib.habit.habit import Habit
from lib.helpers.date_mod import subtract_date
from lib.tracker.tracker import HabitTracker


def test_initialization():
    db = Database('test.db')
    # Drop the database table if it exists; to start on a fresh slate
    db.cursor.execute("DROP TABLE IF EXISTS HABIT")
    tracker = HabitTracker('test.db')

    assert tracker.database.is_connected() is True
    all_habits = tracker.database.select_all()
    print(all_habits)
    assert len(all_habits) == 5


def test_add_habit():
    db = Database('test.db')
    # Drop the database table if it exists; to start on a fresh slate
    db.cursor.execute("DROP TABLE IF EXISTS HABIT")
    tracker = HabitTracker('test.db')
    tracker.add_habit('Test Habit One', 'Hello World of the world of test', 'daily')
    all_habits = tracker.database.select_all()
    assert len(all_habits) == 6


def test_remove_habit():
    db = Database('test.db')
    # Drop the database table if it exists; to start on a fresh slate
    db.cursor.execute("DROP TABLE IF EXISTS HABIT")
    tracker = HabitTracker('test.db')

    all_habits = tracker.database.select_all()
    assert len(all_habits) == 5

    response = tracker.remove_habit(1)
    all_habits = tracker.database.select_all()
    assert len(all_habits) == 4
    assert response == 1

    response = tracker.remove_habit(2)
    all_habits = tracker.database.select_all()
    assert len(all_habits) == 3
    assert response == 2


def test_checkoff_habit():
    db = Database('test.db')
    # Drop the database table if it exists; to start on a fresh slate
    db.cursor.execute("DROP TABLE IF EXISTS HABIT")
    tracker = HabitTracker('test.db')

    test_checkoff_habit = Habit(habit_id=1, name='Workout', description='Hit the gym twice a week',
                                periodicity='weekly',
                                streak_in_weeks=8, streak_in_days=8 * 7,
                                start_date=(subtract_date(weeks=8).strftime('%Y-%m-%d %H:%M:%S')),
                                current_streak_date=subtract_date(weeks=2).strftime('%Y-%m-%d %H:%M:%S'),
                                longest_streak_in_days=8 * 7,
                                )

    tracker.database.update_one(1, test_checkoff_habit)
    tracker.checkoff_habit(1)
    habit_1 = Habit.from_db_row(tracker.database.select_one(1))
    assert len(habit_1.current_streak_date) > 1
    # According to the updated/checked-off habit, the last observed date was 2 weeks earlier,
    # the user skipped the check and their current streak should reset
    assert habit_1.streak_in_days == 7
    assert habit_1.streak_in_weeks == 1
