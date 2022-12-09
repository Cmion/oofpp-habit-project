from datetime import datetime

from lib.habit.habit import Habit
from lib.helpers.date_mod import subtract_date


def test_habit_initialization():
    weekly_habit = Habit(habit_id=1, name='Workout', description='Hit the gym twice a week', periodicity='weekly',
                         streak_in_weeks=45, streak_in_days=45 * 7,
                         start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                         current_streak_date=datetime(2022, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S'),
                         longest_streak_in_days=45 * 8,
                         )
    assert weekly_habit.habit_id == 1
    assert weekly_habit.periodicity == 'weekly'
    assert weekly_habit.periodicity_duration == 7
    assert weekly_habit.current_streak_date == '2022-01-01 12:11:45'
    assert weekly_habit.streak_in_days == 315
    assert weekly_habit.streak_in_weeks == 45
    weekly_habit.evaluate_streak()
    assert weekly_habit.streak_in_days == 0
    assert weekly_habit.streak_in_weeks == 0


def test_habit_streak_calculation():
    daily_habit = Habit(habit_id=1, name='Spend time reading', description='Stop at Frankenstein\'s house to study '
                                                                           'together',
                        periodicity='daily',
                        streak_in_weeks=45, streak_in_days=45 * 7,
                        start_date=(datetime(1980, 1, 1, 12, 11, 45).strftime('%Y-%m-%d %H:%M:%S')),
                        current_streak_date=subtract_date(days=1).strftime('%Y-%m-%d %H:%M:%S'),
                        longest_streak_in_days=45 * 7,
                        )

    assert daily_habit.streak_in_days == 315
    assert daily_habit.streak_in_weeks == 45
    daily_habit.recalculate_data()
    assert daily_habit.streak_in_days == 316
    assert daily_habit.longest_streak_in_days == 316

    daily_habit.current_streak_date = subtract_date(days=2).strftime('%Y-%m-%d %H:%M:%S')
    daily_habit.recalculate_data()
    assert daily_habit.streak_in_days == 1
    assert daily_habit.streak_in_weeks == 0
    assert daily_habit.longest_streak_in_days == 316


def test_db_conversions():
    now = datetime.now()
    habit = Habit(habit_id=200, name='Anything', description='Bones of Elisha', periodicity='daily', streak_in_weeks=1,
                  streak_in_days=7, start_date=subtract_date(date=now, weeks=1).strftime('%Y-%m-%d %H:%M:%S'),
                  current_streak_date=now.strftime('%Y-%m-%d %H:%M:%S'), longest_streak_in_days=7)

    db_row_sample = (200, 'Anything', 'Bones of Elisha', 'daily',
                     subtract_date(date=now, weeks=1).strftime('%Y-%m-%d %H:%M:%S'),
                     now.strftime('%Y-%m-%d %H:%M:%S'), 7, 1, 7
                     )
    assert habit.habit_id == Habit.from_db_row(db_row_sample).habit_id
    assert habit.name == Habit.from_db_row(db_row_sample).name
    assert habit.start_date == Habit.from_db_row(db_row_sample).start_date
    assert habit.longest_streak_in_days == Habit.from_db_row(db_row_sample).longest_streak_in_days
    assert habit.current_streak_date == Habit.from_db_row(db_row_sample).current_streak_date

    assert Habit.to_db_row(habit) == ('Anything', 'Bones of Elisha', 'daily',
                                      subtract_date(date=now, weeks=1).strftime('%Y-%m-%d %H:%M:%S'),
                                      now.strftime('%Y-%m-%d %H:%M:%S'), 7, 1, 7
                                      )

    assert Habit.from_db_to_list([db_row_sample])[0].habit_id == [habit][0].habit_id
