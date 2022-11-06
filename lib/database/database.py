import sqlite3


class Database:
    """
    This class is used to create a database connection, and to manage the database.
    """

    def __init__(self, db_file):
        """ Create a database connection to the SQLite database
            specified by the db_file
            :param db_file: database file
            :return: Connection object or None
        """
        self.db = None
        self.cursor = None
        try:
            self.db_path = db_file
            self.db = sqlite3.connect(db_file)
            self.cursor = self.db.cursor()
        except sqlite3.Error as e:
            print(e)

    def create_table(self):
        """ Create the database table if it does not exist
            :return: None
        """
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS  HABIT
                 (ID INT PRIMARY KEY     NOT NULL,
                 NAME           TEXT    NOT NULL,
                 DESCRIPTION    TEXT     NOT NULL,
                 PERIODICITY    CHAR(50)  NOT NULL, 
                 START_DATE CHAR(50) NOT NULL,
                 CURRENT_STREAK_DATE CHAR(50) DEFAULT NULL,
                 STREAK_IN_DAYS INT NOT NULL DEFAULT 0,
                 STREAK_IN_WEEKS INT NOT NULL DEFAULT 0,);
         ''')

    def insert(self, habit):
        """ Insert a habit into database using the parameters specified
            :param habit: habit to insert
            :return: None
        """
        self.cursor.execute('''INSERT INTO HABIT (NAME, DESCRIPTION, PERIODICITY, START_DATE, CURRENT_STREAK_DATE, 
                        STREAK_IN_DAYS, STREAK_IN_WEEKS) \
      VALUES (?, ?, ?, ?, ?, ?, ?)''', (habit.name, habit.description, habit.periodicity, habit.start_date, None, 0, 0))
        self.db.commit()

    def insertMany(self, habits):
        self.cursor.executemany("INSERT INTO HABIT VALUES(?, ?, ?, ?, ?, ?, ?)", habits)
        self.db.commit()

    def delete(self, habit_id):
        """ Delete a habit from database using the parameters specified
            :param habit_id: habit to delete
            :return: None
        """
        self.cursor.execute(f"DELETE from HABIT where ID = :habit_id;", {'habit_id': habit_id})
        self.db.commit()

    def select_all(self):
        """ Select all habits from database
            :return: list of habits

        """
        cursor = self.cursor.execute(
            '''SELECT id, name, description, periodicity, start_date, 
                streak_in_days, streak_in_weeks, current_streak_date FROM HABIT;
            ''')

        return cursor.fetchall()

    def select_by_column(self, column_name, column_query):
        """ Select habits from database using the parameters specified
            :param column_name: name of the column to select
            :param column_query: query to select the column
            :return: list of habits
        """
        cursor = self.cursor.execute(
            f'''SELECT id, name, description, periodicity, start_date, 
            streak_in_days, streak_in_weeks, current_streak_date FROM HABIT WHERE :column_name = :column_query;
        ''', {'column_query': column_query, 'column_name': column_name})
        return cursor.fetchall()

    def updateOne(self, habit_id, habit):
        self.cursor.execute('''UPDATE TABLE set NAME = :name, DESCRIPTION = :description, PERIODICITY = :periodicity, 
        START_DATE = :start_date, CURRENT_STREAK_DATE = :current_streak_date, 
                        STREAK_IN_DAYS = :streak_in_days, STREAK_IN_WEEKS = :streak_in_weeks where ID = :habit_id''',
                            {'habit_id': habit_id, 'name': habit.name, 'periodicity': habit.periodicity,
                             'start_date': habit.start_date, 'streak_in_weeks': habit.streak_in_weeks,
                             'current_streak_date': habit.current_streak_date, 'streak_in_days': habit.streak_in_days})
        self.db.commit()

    def close_connection(self):
        self.cursor.close()
        self.db.close()
