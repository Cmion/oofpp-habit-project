import sqlite3


class Database:
    """
    This class is used to create a database connection, and to manage the database.
    """

    def __init__(self, db_path):
        """ Create a database connection to the SQLite database
            specified by the db_file
            :return: Connection object or None
        """
        self.db = None
        self.cursor = None
        try:
            self.db_path = db_path
            self.db = sqlite3.connect(self.db_path)

            self.cursor = self.db.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print(e)

    def create_table(self):
        """ Create the database table if it does not exist
            :return: None
        """

        # print(self.db)
        # self.cursor.execute("DROP TABLE IF EXISTS HABIT")
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS HABIT
                (
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 NAME           TEXT    NOT NULL,
                 DESCRIPTION    TEXT     NOT NULL,
                 PERIODICITY    CHAR(50)  NOT NULL, 
                 START_DATE CHAR(50) NOT NULL,
                 CURRENT_STREAK_DATE CHAR(50) DEFAULT NULL,
                 STREAK_IN_DAYS INT NOT NULL DEFAULT 0,
                 STREAK_IN_WEEKS INT NOT NULL DEFAULT 0,
                 LONGEST_STREAK_IN_DAYS INT NOT NULL DEFAULT 0
                 );
         ''')

        # print('Table is ready')

    def insert(self, habit):
        """ Insert a habit into database using the parameters specified
            :param habit: habit to insert
            :return: None
        """
        self.cursor.execute('''INSERT INTO HABIT (NAME, DESCRIPTION, PERIODICITY, START_DATE, CURRENT_STREAK_DATE, 
                        STREAK_IN_DAYS, STREAK_IN_WEEKS, LONGEST_STREAK_IN_DAYS) 
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (habit.name, habit.description, habit.periodicity, habit.start_date,
                                           habit.current_streak_date, habit.streak_in_days,
                                           habit.streak_in_weeks, habit.longest_streak_in_days))
        self.db.commit()

    def insert_many(self, habits):
        """
        Insert multiple habits into the database
        :param habits: list of habits to insert
        :return: None
        """
        # print(habits)
        self.cursor.executemany("""INSERT INTO HABIT (NAME, DESCRIPTION, PERIODICITY, START_DATE, CURRENT_STREAK_DATE,
        STREAK_IN_DAYS, STREAK_IN_WEEKS, LONGEST_STREAK_IN_DAYS)  VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", habits)
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
            '''SELECT id, name, description, periodicity, start_date, current_streak_date, streak_in_days, streak_in_weeks, longest_streak_in_days from HABIT;
            ''')

        return cursor.fetchall()

    def select_one(self, habit_id):
        """ Select a habits from database
            :return: list of habits

        """
        cursor = self.cursor.execute(
            '''SELECT ID, name, description, periodicity, start_date, current_streak_date,
                streak_in_days, streak_in_weeks, longest_streak_in_days FROM HABIT 
                WHERE id = :habit_id;
            ''', {'habit_id': habit_id})

        return cursor.fetchone()

    def select_by_column(self, column_name, column_query):
        """ Select habits from database using the parameters specified
            :param column_name: name of the column to select
            :param column_query: query to select the column
            :return: list of habits
        """
        cursor = self.cursor.execute(
            '''SELECT id, name, description, periodicity, start_date, current_streak_date,
            streak_in_days, streak_in_weeks, longest_streak_in_days FROM HABIT 
            WHERE :column_name = :column_query;
        ''', {'column_query': column_query, 'column_name': column_name})
        return cursor.fetchall()

    def update_one(self, habit_id, habit):
        """
        Update a habit in the database
        :param habit_id: id of the habit to update
        :param habit: habit to update
        :return: None
        """

        self.cursor.execute('''UPDATE HABIT SET NAME = :name, DESCRIPTION = :description, PERIODICITY = :periodicity, 
        START_DATE = :start_date, CURRENT_STREAK_DATE = :current_streak_date, 
                        STREAK_IN_DAYS = :streak_in_days, STREAK_IN_WEEKS = :streak_in_weeks, 
                        LONGEST_STREAK_IN_DAYS = :longest_streak_in_days where ID = :habit_id;''',
                            {'habit_id': habit_id, 'name': habit.name, 'description': habit.description, 'periodicity': habit.periodicity,
                             'start_date': habit.start_date, 'streak_in_weeks': habit.streak_in_weeks,
                             'current_streak_date': habit.current_streak_date,
                             'streak_in_days': habit.streak_in_days,
                             'longest_streak_in_days': habit.longest_streak_in_days})
        self.db.commit()

    def close_connection(self):
        self.cursor.close()
        self.db.close()
