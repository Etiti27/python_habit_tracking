import psycopg2
from DB_params import db_param
from flask_login import UserMixin
from psycopg2.extras import RealDictCursor


class Users:
    """flask-login framework implementation"""

    def __init__(self):
        self.connection_params = db_param
        self.user_table_name = "users"

    class User(UserMixin):
        def __init__(self, user_id, username, password):
            self.id = user_id
            self.username = username
            self.password = password

    # Method to get user from database by ID
    def get_user_by_id(self, user_id):
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(f"SELECT * FROM {self.user_table_name} WHERE id = %s", (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    return self.User(user_data['id'], user_data['username'], user_data['password'])
        return None

    # Method to authenticate user and return a User object
    def authenticate_user(self, username, password):
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(f"SELECT * FROM {self.user_table_name} WHERE username = %s AND password = %s",
                               (username, password))
                user_data = cursor.fetchone()
                if user_data:
                    return self.User(user_data['id'], user_data['username'], user_data['password'])
        return None

    def register_user(self, username, password):
        print("register is called")
        """Register user"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    # Insert data
                    insert_data_query = f"""
                    INSERT INTO {self.user_table_name} (username, password) VALUES (%s, %s) 
                    ON CONFLICT (username) 
                    DO NOTHING;"""
                    cursor.execute(insert_data_query, (username, password))
                    conn.commit()
                    return "Success"
        except Exception as e:
            print(e)
            if type(e).__name__ == 'UndefinedTable':
                return "UndefinedTable"

    def create_user(self):
        """create table if the table does not exist in the database"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    # Create a table
                    create_table_query = f'''
                       CREATE TABLE IF NOT EXISTS {self.user_table_name} (
                           id SERIAL PRIMARY KEY,
                           username VARCHAR(100) UNIQUE NOT NULL,
                           password VARCHAR(10) NOT NULL
                       );
                       '''
                    cursor.execute(create_table_query)
                    conn.commit()
        except Exception as e:
            print(e)
