from datetime import date

import pytest

from app import goals
from app.goals import time_to_goal, date_to_goal


class FixedDate(date):
    """date whose today() always returns 1 January 2026, so results don't depend on when tests run."""

    @classmethod
    def today(cls):
        return cls(2026, 1, 1)


@pytest.fixture
def fixed_today(monkeypatch):
    monkeypatch.setattr(goals, 'date', FixedDate)


class TestTimeToGoal:
    @pytest.mark.parametrize('speed, weeks', [('slow', 40), ('medium', 20), ('fast', 10)])
    def test_weeks_to_lose_10kg(self, speed, weeks):
        assert time_to_goal(80, 70, speed) == weeks

    def test_gaining_weight_gives_positive_weeks(self):
        assert time_to_goal(70, 80, 'medium') == 20

    def test_already_at_goal(self):
        assert time_to_goal(80, 80, 'fast') == 0

    @pytest.mark.parametrize('speed', [None, 'unknown'])
    def test_unknown_speed_defaults_to_medium(self, speed):
        assert time_to_goal(80, 70, speed) == 20

    def test_partial_weeks(self):
        assert time_to_goal(80, 79, 'medium') == 2
        assert time_to_goal(80, 79.5, 'fast') == 0.5


class TestDateToGoal:
    def test_already_at_goal_returns_today(self, fixed_today):
        assert date_to_goal(80, 80, 'medium') == '1 JAN 2026'

    @pytest.mark.parametrize('speed, expected', [
        ('fast', '12 MAR 2026'),    # 10 weeks
        ('medium', '21 MAY 2026'),  # 20 weeks
        ('slow', '8 OCT 2026'),     # 40 weeks
    ])
    def test_target_date(self, fixed_today, speed, expected):
        assert date_to_goal(80, 70, speed) == expected

    def test_target_date_in_next_year(self, fixed_today):
        # 30 kg at 0.25 kg/week = 120 weeks (840 days, across the 2028 leap day)
        assert date_to_goal(100, 70, 'slow') == '20 APR 2028'
