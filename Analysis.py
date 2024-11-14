from datetime import timedelta


class Analysis:
    def __init__(self):
        self.weekly_current_streak = 1
        self.weekly_longest_streak = 0
        self.daily_current_streak = 1
        self.daily_longest_streak = 0

    from datetime import datetime, timedelta

    def calculate_daily_streak(self, dates):
        # Sort dates in ascending order

        dates = sorted(dates)

        longest_streak = 0
        current_streak = 1  # Start streak count at 1 for the first day

        # Iterate over dates to find consecutive days
        for i in range(1, len(dates)):
            # Check if the current date is consecutive to the previous date
            if dates[i] == dates[i - 1] + timedelta(days=1):
                current_streak += 1
            else:
                # Update longest streak and reset current streak
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1  # Reset for a new streak

        # Final check to update longest streak if it ends on the last date

        longest_streak = max(longest_streak, current_streak)
        self.daily_longest_streak = longest_streak
        self.daily_current_streak = current_streak

        return longest_streak

    def calculate_weekly_streak(self, dates):
        # Convert dates to (year, week number) tuples and sort them
        weeks = sorted({(date.year, date.isocalendar()[1]) for date in dates})
        longest_streak = 0
        current_streak = 1  # Start streak count at 1 for the first week
        # Iterate over weeks to find consecutive weeks
        for i in range(1, len(weeks)):
            # Check if the current week is consecutive to the previous week
            prev_year, prev_week = weeks[i - 1]
            curr_year, curr_week = weeks[i]
            # Check if they are consecutive weeks
            if (curr_year == prev_year and curr_week == prev_week + 1) or \
                    (curr_year == prev_year + 1 and prev_week == 52 and curr_week == 1):
                current_streak += 1
            else:
                # Update longest streak and reset current streak
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1  # Reset for a new streak
        # Final check to update longest streak if it ends on the last date
        longest_streak = max(longest_streak, current_streak)
        self.weekly_current_streak = current_streak
        self.weekly_longest_streak = longest_streak
        return longest_streak
