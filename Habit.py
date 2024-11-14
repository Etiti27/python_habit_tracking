from datetime import datetime as dt, timedelta
from DataManager import DataManager
from User import Users

today = dt.now().date().strftime('%Y,%m,%d')
day = dt.now().day
month = dt.now().month
year = dt.now().year


class Habit:
    """Define the Habit class"""

    def __init__(self):
        self.data = DataManager()
        self.user = Users()

    def create_all_table(self):
        """create and register users if the table and user does not exist"""
        self.data.create_habits_table()
        self.data.create_streak_completed_table()
        self.user.create_user()
        self.user.register_user(username="obinna@gmail.com", password="qwerty")

    def get_current_habits(self, frequency):
        """get the habits based on frequency. eg if 'weekly' is assigned to frequency, weekly habits will be
        displayed"""
        return self.data.retrieve_current_habits(frequency)

    def get_completed_habits(self, frequency):
        """get the habits based on frequency. eg if 'weekly' is assigned to frequency, weekly habits will be
        displayed"""
        return self.data.retrieve_completed_habits(frequency)

    def create_habit(self, frequency, habit_name, day_of_days_in_year, number_of_weeks):
        """create habit"""
        return self.data.insert_data(completed_date=None, is_completed=False, frequency=frequency,
                                     habit_name=habit_name, start_date=today,
                                     start_day=day, start_month=month,
                                     start_year=year, day_of_days_in_years=day_of_days_in_year,
                                     number_of_week=number_of_weeks)

    def checkout_habit(self, date, habit_id):
        """checkoff and call db update method"""
        return self.data.update_completed_habit(is_completed=True, completed_date=date, habit_id=habit_id)

    def insert_complete_streak(self, frequency, start_day=day, start_year=year, start_month=month, start_date=today):
        """add data in the complete streak"""
        return self.data.insert_into_streak_table(frequency=frequency, start_day=start_day,
                                                  start_year=start_year, start_month=start_month,
                                                  start_date=start_date
                                                  )

    def get_streak_data(self, frequency):
        """method to call db to get streak data"""
        return self.data.retrieve_streak_data(frequency=frequency)


