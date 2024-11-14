import psycopg2
from psycopg2 import ProgrammingError
from DB_params import db_param
import datetime as dt
from psycopg2.extras import RealDictCursor

today = dt.datetime.now()
day_of_days_in_year = today.timetuple().tm_yday
number_of_weeks = today.isocalendar().week
current_date = today.date()


class DataManager:
    def __init__(self):
        # Define the connection parameters
        self.connection_params = db_param
        self.habit_table_name = 'habit_tracking'
        self.user_table_name = "users"
        self.streak_complete_table = "streak_completed"

    def create_habits_table(self):
        """create table if the table does not exist in the database"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    # Create a table
                    create_table_query = f'''
                    CREATE TABLE IF NOT EXISTS {self.habit_table_name} (
                        id SERIAL PRIMARY KEY,
                        habit_name VARCHAR(100) NOT NULL,
                        frequency VARCHAR(10) NOT NULL,
                        start_date DATE NOT NULL,
                        start_day INT NOT NULL,
                        start_month INT NOT NULL,
                        start_year INT NOT NULL,
                        is_completed BOOL NOT NULL,
                        completed_date DATE,
                        number_of_weeks INT NOT NULL,
                        day_of_days_in_year INT NOT NULL
                    );
                    '''
                    cursor.execute(create_table_query)
                    conn.commit()
        except Exception as e:
            print(e)

    def insert_data(self, habit_name, frequency, start_date, start_day, start_month, start_year, is_completed,
                    completed_date, number_of_week,
                    day_of_days_in_years):
        """add habit into the db table"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    # Insert data
                    insert_data_query = f"""
                    INSERT INTO {self.habit_table_name} (habit_name, frequency, start_date, start_day, start_month, 
                    start_year, is_completed, completed_date, number_of_weeks, day_of_days_in_year) VALUES (%s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s);"""
                    cursor.execute(insert_data_query, (habit_name, frequency, start_date, start_day, start_month,
                                                       start_year, is_completed, completed_date,
                                                       number_of_week, day_of_days_in_years))
                    conn.commit()
                    return "Success"
        except Exception as e:
            print(e)
            if type(e).__name__ == 'UndefinedTable':
                return "UndefinedTable"

    def retrieve_current_habits(self, frequency):
        """retrieve active habits. frequency is used to specify and filter the period habit eg. daily or weekly"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    if frequency.lower() == "daily":
                        # Retrieve all data
                        cursor.execute(f"""SELECT * FROM {self.habit_table_name}  WHERE frequency = %s AND 
                                                 day_of_days_in_year = %s AND is_completed = %s""",
                                       (frequency, day_of_days_in_year, False))
                        rows = cursor.fetchall()
                        return rows
                    elif frequency.lower() == "weekly":
                        cursor.execute(f"""SELECT * FROM {self.habit_table_name}  WHERE frequency = %s AND 
                        number_of_weeks = %s AND is_completed = %s""", (frequency, number_of_weeks, False))
                        rows = cursor.fetchall()
                        return rows
                    else:
                        cursor.execute(f"SELECT * FROM {self.habit_table_name} ;")
                        rows = cursor.fetchall()
                        return rows
        except ProgrammingError as e:
            return "Table not found"

        except Exception as e:
            if type(e).__name__:
                return "UndefinedTable"

    def retrieve_completed_habits(self, frequency):
        """when checkout, the 'is_completed ' table column is updated to TRUE, this will filter and get the values"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    if frequency.lower() == "daily":
                        # Retrieve all data
                        cursor.execute(f"""SELECT * FROM {self.habit_table_name}  WHERE frequency = %s AND 
                                                day_of_days_in_year = %s AND is_completed = %s""",
                                       (frequency, day_of_days_in_year, True))
                        rows = cursor.fetchall()
                        return rows
                    elif frequency.lower() == "weekly":
                        cursor.execute(f"""SELECT * FROM {self.habit_table_name}  WHERE frequency = %s AND 
                        number_of_weeks = %s AND is_completed = %s""", (frequency, number_of_weeks, True))
                        rows = cursor.fetchall()
                        return rows
                    else:
                        cursor.execute(f"SELECT * FROM {self.habit_table_name} ;")
                        rows = cursor.fetchall()
                        return rows
        except Exception as e:
            if type(e).__name__:
                return "UndefinedTable"

    def update_completed_habit(self, is_completed, completed_date, habit_id):
        """this will update and 'is_completed' field to TRUE"""
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor() as cursor:
                update_query = f'''
                UPDATE {self.habit_table_name}
                SET is_completed = %s, completed_date = %s
                WHERE id = %s;
                '''
                cursor.execute(update_query, (
                    is_completed, completed_date, habit_id))
                conn.commit()
                return "Success"

    def create_streak_completed_table(self):
        """create streak table if the table does not exist in the database"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    # Create a table
                    create_table_query = f'''
                    CREATE TABLE IF NOT EXISTS {self.streak_complete_table} (
                        id SERIAL PRIMARY KEY,
                        frequency VARCHAR(10) NOT NULL,
                        start_date DATE NOT NULL,
                        start_day INT NOT NULL,
                        start_month INT NOT NULL,
                        start_year INT NOT NULL
                    );
                    '''
                    cursor.execute(create_table_query)
                    conn.commit()
        except Exception as e:
            print("Error creating table:", e)

    def insert_into_streak_table(self, frequency, start_date, start_day, start_month, start_year):
        """insert data into the streak table"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    insert_data_query = f"""
                       INSERT INTO {self.streak_complete_table} (frequency, start_date, start_day, start_month, 
                       start_year) VALUES (%s, %s, %s, %s, %s);"""
                    cursor.execute(insert_data_query, (frequency, start_date, start_day, start_month,
                                                       start_year))
                    conn.commit()
                    return "Success"
        except Exception as e:
            print(e)
            if type(e).__name__ == 'UndefinedTable':
                return "UndefinedTable"

    def retrieve_streak_data(self, frequency):
        """Retrieve streak data"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    if frequency.lower() == "daily":
                        cursor.execute(f"""SELECT * FROM {self.streak_complete_table}  WHERE frequency = %s""",
                                       (frequency,))
                        rows = cursor.fetchall()
                        return rows
                    elif frequency.lower() == "weekly":
                        cursor.execute(f"""SELECT * FROM {self.streak_complete_table}  WHERE frequency = %s """,
                                       (frequency,))
                        rows = cursor.fetchall()
                        return rows
                    else:
                        cursor.execute(f"SELECT * FROM {self.streak_complete_table} ;")
                        rows = cursor.fetchall()
                        return rows
        except Exception as e:
            if type(e).__name__:
                return "UndefinedTable"
