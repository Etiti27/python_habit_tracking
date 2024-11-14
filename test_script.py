import unittest
from datetime import datetime
from Analysis import Analysis

streak = Analysis()


class TestCalculateLongestStreak(unittest.TestCase):

    def test_consecutive_streak(self):
        # Test with a perfect consecutive streak
        habit_dates = [
            datetime(2024, 1, 1),
            datetime(2024, 1, 2),
            datetime(2024, 1, 3),
            datetime(2024, 1, 4),
            datetime(2024, 1, 5)
        ]
        result = streak.calculate_daily_streak(habit_dates)
        self.assertEqual(result, 5)  # Expected streak of 5 days

    def test_streak_with_breaks(self):
        # Test with breaks in the streak
        habit_dates = [
            datetime(2024, 1, 1),
            datetime(2024, 1, 2),
            datetime(2024, 1, 4),
            datetime(2024, 1, 5),
            datetime(2024, 1, 7)
        ]
        result = streak.calculate_daily_streak(habit_dates)
        self.assertEqual(result, 2)  # Expected longest streak of 2 days

    def test_no_streak(self):
        # Test with non-consecutive dates
        habit_dates = [
            datetime(2024, 1, 1),
            datetime(2024, 1, 3),
            datetime(2024, 1, 5),
            datetime(2024, 1, 7)
        ]
        result = streak.calculate_daily_streak(habit_dates)
        self.assertEqual(result, 1)  # Expected longest streak of 1 day

    def test_single_date(self):
        # Test with only one date
        habit_dates = [datetime(2024, 1, 1)]
        result = streak.calculate_daily_streak(habit_dates)
        self.assertEqual(result, 1)  # Expected longest streak of 1 day

    def test_empty_list(self):
        # Test with an empty list
        habit_dates = []
        result = streak.calculate_daily_streak(habit_dates)
        self.assertEqual(result, 1)  # Expected longest streak of 1 days

    def test_end_with_longest_streak(self):
        # Test where longest streak is at the end of the list
        habit_dates = [
            datetime(2024, 1, 1),
            datetime(2024, 1, 3),
            datetime(2024, 1, 4),
            datetime(2024, 1, 5)
        ]
        result = streak.calculate_daily_streak(habit_dates)
        self.assertEqual(result, 3)  # Expected longest streak of 3 days

        # weekly streak test

    def test_consecutive_weeks(self):
        # Test with a perfect consecutive streak of weeks
        habit_dates = [
            datetime(2024, 1, 1),  # Week 1
            datetime(2024, 1, 8),  # Week 2
            datetime(2024, 1, 15),  # Week 3
            datetime(2024, 1, 22),  # Week 4
        ]
        result = streak.calculate_weekly_streak(habit_dates)
        self.assertEqual(result, 4)  # Expected streak of 4 weeks

    def test_streak_with_breaks2(self):
        # Test with breaks in the weekly streak
        habit_dates = [
            datetime(2024, 1, 1),  # Week 1
            datetime(2024, 1, 15),  # Week 3
            datetime(2024, 1, 29),  # Week 5
            datetime(2024, 2, 5)  # Week 6
        ]
        result = streak.calculate_weekly_streak(habit_dates)
        self.assertEqual(result, 2)  # Expected longest streak of 1 week

    def test_no_streak2(self):
        # Test with non-consecutive weeks
        habit_dates = [
            datetime(2024, 1, 1),  # Week 1
            datetime(2024, 1, 22),  # Week 4
            datetime(2024, 2, 19),  # Week 8
        ]
        result = streak.calculate_weekly_streak(habit_dates)
        self.assertEqual(result, 1)  # Expected longest streak of 1 week

    def test_single_date2(self):
        # Test with only one date
        habit_dates = [datetime(2024, 1, 1)]
        result = streak.calculate_weekly_streak(habit_dates)
        self.assertEqual(result, 1)  # Expected streak of 1 week

    def test_empty_list2(self):
        # Test with an empty list
        habit_dates = []
        result = streak.calculate_weekly_streak(habit_dates)
        self.assertEqual(result, 1)

    def test_end_with_longest_streak2(self):
        # Test where the longest streak is at the end of the list
        habit_dates = [
            datetime(2024, 1, 1),  # Week 1
            datetime(2024, 1, 8),  # Week 2
            datetime(2024, 1, 15),  # Week 3
            datetime(2024, 2, 5)  # Week 6
        ]
        result = streak.calculate_weekly_streak(habit_dates)
        self.assertEqual(result, 3)  # Expected longest streak of 3 weeks


if __name__ == "__main__":
    unittest.main()
