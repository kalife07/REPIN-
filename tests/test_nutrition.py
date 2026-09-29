import pytest

from app.nutrition import (burned_calories, goal_calories, protein_intake, fat_intake, carb_intake,
                           fibers_intake, sugar_intake, sodium_intake, water_intake)


# Reference user: 25 years old, male, 80 kg, 180 cm, trains 5 days a week, medium pace
AGE, GENDER, WEIGHT, HEIGHT, ACTIVITY, SPEED = 25, 'male', 80, 180, 'active', 'medium'
MALE_BMR = 10 * 80 + 6.25 * 180 - 5 * 25 + 5  # 1805


def user(goal):
    return (AGE, GENDER, WEIGHT, SPEED, HEIGHT, ACTIVITY, goal)


class TestBurnedCalories:
    def test_male_bmr_formula(self):
        assert burned_calories(25, 'male', 80, 180, 'sedentary') == pytest.approx(MALE_BMR * 1.2)

    def test_female_bmr_formula(self):
        female_bmr = 10 * 60 + 6.25 * 165 - 5 * 25 - 161
        assert burned_calories(25, 'female', 60, 165, 'sedentary') == pytest.approx(female_bmr * 1.2)

    def test_female_burns_less_than_male_with_same_stats(self):
        assert burned_calories(25, 'female', 80, 180, 'active') < burned_calories(25, 'male', 80, 180, 'active')

    @pytest.mark.parametrize('activity, multiplier', [
        ('sedentary', 1.2),
        ('lightly active', 1.375),
        ('active', 1.55),
        ('very active', 1.725),
        ('extra active', 1.9),
    ])
    def test_activity_multipliers(self, activity, multiplier):
        assert burned_calories(25, 'male', 80, 180, activity) == pytest.approx(MALE_BMR * multiplier)

    @pytest.mark.parametrize('activity', [None, '', 'unknown'])
    def test_unknown_activity_defaults_to_lightly_active(self, activity):
        assert burned_calories(25, 'male', 80, 180, activity) == pytest.approx(MALE_BMR * 1.375)


class TestGoalCalories:
    maintenance = round(MALE_BMR * 1.55)

    def test_maintain_equals_burned_calories(self):
        assert goal_calories(*user('maintain')) == self.maintenance

    @pytest.mark.parametrize('speed, change', [('slow', 300), ('medium', 500), ('fast', 1000)])
    def test_bulk_adds_calories(self, speed, change):
        assert goal_calories(AGE, GENDER, WEIGHT, speed, HEIGHT, ACTIVITY, 'bulk') == round(MALE_BMR * 1.55 + change)

    @pytest.mark.parametrize('speed, change', [('slow', 300), ('medium', 500), ('fast', 1000)])
    def test_cut_removes_calories(self, speed, change):
        assert goal_calories(AGE, GENDER, WEIGHT, speed, HEIGHT, ACTIVITY, 'cut') == round(MALE_BMR * 1.55 - change)

    def test_no_speed_means_no_change(self):
        assert goal_calories(AGE, GENDER, WEIGHT, None, HEIGHT, ACTIVITY, 'bulk') == self.maintenance

    def test_returns_whole_number(self):
        assert isinstance(goal_calories(*user('cut')), int)


class TestProtein:
    @pytest.mark.parametrize('activity, grams_per_lb', [
        ('sedentary', 0.8),
        ('lightly active', 0.8),
        ('active', 0.9),
        ('very active', 1),
        ('extra active', 1),
        (None, 0.8),
    ])
    def test_protein_per_pound_of_body_weight(self, activity, grams_per_lb):
        pounds = round(80 * 2.205, 2)
        assert protein_intake(80, activity) == round(pounds * grams_per_lb)


class TestFat:
    @pytest.mark.parametrize('goal, share', [('bulk', 0.3), ('maintain', 0.25), ('cut', 0.2)])
    def test_fat_share_of_calories(self, goal, share):
        # 9 calories per gram of fat
        assert fat_intake(*user(goal)) == round(goal_calories(*user(goal)) * share / 9)

    def test_unknown_goal_returns_none(self):
        assert fat_intake(*user('unknown')) is None


class TestCarbs:
    @pytest.mark.parametrize('goal', ['bulk', 'maintain', 'cut'])
    def test_carbs_fill_remaining_calories(self, goal):
        remaining = goal_calories(*user(goal)) - 4 * protein_intake(WEIGHT, ACTIVITY) - 9 * fat_intake(*user(goal))
        assert carb_intake(*user(goal)) == round(remaining / 4)

    @pytest.mark.parametrize('goal', ['bulk', 'maintain', 'cut'])
    def test_macros_add_up_to_goal_calories(self, goal):
        total = 4 * protein_intake(WEIGHT, ACTIVITY) + 9 * fat_intake(*user(goal)) + 4 * carb_intake(*user(goal))
        # Each macro is rounded to the gram, so allow a few calories of difference
        assert total == pytest.approx(goal_calories(*user(goal)), abs=10)


class TestOtherNutrients:
    @pytest.mark.parametrize('goal', ['bulk', 'maintain', 'cut'])
    def test_fiber_is_14g_per_1000_calories(self, goal):
        assert fibers_intake(*user(goal)) == round(goal_calories(*user(goal)) / 1000 * 14)

    @pytest.mark.parametrize('goal, share', [('bulk', 0.10), ('maintain', 0.10), ('cut', 0.05)])
    def test_sugar_limit(self, goal, share):
        assert sugar_intake(*user(goal)) == round(goal_calories(*user(goal)) * share / 4)

    def test_sodium_limit(self):
        assert sodium_intake() == 2300

    def test_water(self):
        assert water_intake() == 2
