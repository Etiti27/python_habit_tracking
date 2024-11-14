from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required
from datetime import datetime as dm
import datetime as dt
from Habit import Habit
from User import Users
from Analysis import Analysis
from DB_params import app_secret


today = dt.datetime.now().date()

app = Flask(__name__)
app.secret_key = app_secret
login_manager = LoginManager(app)
login_manager.login_view = 'login'
users = Users()
analysis = Analysis()
habit = Habit()
day_of_days_in_year = today.timetuple().tm_yday
number_of_weeks = today.isocalendar().week


def get_streak(frequency):
    all_data = habit.get_streak_data(frequency=frequency)
    add_all_data_together = []
    for data in all_data:
        datas = dm(data["start_year"], data["start_month"], data["start_day"])
        add_all_data_together.append(datas)
    return add_all_data_together


#  Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return users.get_user_by_id(user_id)


@app.route('/', methods=['GET', 'POST'])
def login():
    habit.create_all_table()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.authenticate_user(username, password)
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')


@app.route('/daily_habit')
@login_required
def daily_habit():
    daily_current_habits = habit.get_current_habits("daily")
    daily_completed_habits = habit.get_completed_habits("daily")
    daily_longest_streak = analysis.calculate_daily_streak(get_streak("daily"))
    daily_current_streak = analysis.daily_current_streak
    daily_habit_length = len(daily_current_habits)
    # check if daily habit is 0, and time 11:59pm so to inserted the data and count streak
    if daily_habit_length == 0 and dt.datetime.now().time().hour == 23 and dt.datetime.now().time().minute == 59:
        habit.insert_complete_streak(frequency="daily")
    return render_template("daily_habit.html", current_streak=daily_current_streak,
                           longest_streak=daily_longest_streak,
                           daily_habits=daily_current_habits,
                           daily_completed_habits=daily_completed_habits,
                           habit_length=daily_habit_length, )


@app.route('/weekly_habit')
@login_required
def weekly_habit():
    weekly_current_habits = habit.get_current_habits("weekly")
    weekly_completed_habits = habit.get_completed_habits("weekly")
    analysis.calculate_weekly_streak(get_streak("weekly"))
    weekly_current_streak = analysis.weekly_current_streak
    weekly_longest_streak = analysis.weekly_longest_streak
    weekly_habit_length = len(weekly_current_habits)
    # check if length of data is 0 and time is 11pm and it's sunday, to insert data and count the streaks
    if weekly_habit_length == 0 and dt.datetime.now().time().hour == 23 and dt.datetime.now().weekday() + 1 == 7:
        habit.insert_complete_streak(frequency="weekly")
    return render_template("weekly_habits.html", current_streak=weekly_current_streak,
                           longest_streak=weekly_longest_streak,
                           weekly_habits=weekly_current_habits,
                           weekly_completed_habits=weekly_completed_habits,
                           habit_length=weekly_habit_length, )


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route('/add_daily_habit', methods=["POST"])
@login_required
def add_daily_habit():
    habit_name = request.form["habit_name"]
    frequency = request.form["frequency"]
    result = habit.create_habit(frequency=frequency, habit_name=habit_name, day_of_days_in_year=day_of_days_in_year,
                                number_of_weeks=number_of_weeks)
    if result == "Success":
        return redirect(url_for('daily_habit'))


@app.route('/add_weekly_habit', methods=["POST"])
@login_required
def add_weekly_habit():
    habit_name = request.form["habit_name"]
    frequency = request.form["frequency"]
    result = habit.create_habit(frequency=frequency, habit_name=habit_name, number_of_weeks=number_of_weeks,
                                day_of_days_in_year=day_of_days_in_year)
    if result == "Success":
        return redirect(url_for('weekly_habit'))


@app.route('/checkoff', methods=["POST"])
@login_required
def checkoff():
    habit_id = request.form["habit"]
    frequency = request.form['frequency']
    update = habit.checkout_habit(date=today, habit_id=habit_id)
    if update == "Success":
        if frequency == "daily":
            return redirect(url_for('daily_habit'))
        return redirect(url_for('weekly_habit'))


if __name__ == "__main__":
    app.run(port=3002, debug=True)


