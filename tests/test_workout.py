import pytest

from app.models import Exercice
from app.workout import split_picker, exercice_giver, schedule_builder, weight_picker, actual_split


ACTIVITIES = ['sedentary', 'lightly active', 'active', 'very active', 'extra active']


class TestExercice:
    def test_to_dict(self):
        exercice = Exercice('Lat Pulldown', '8-12', '2-3', '1m 30s', 56)
        assert exercice.to_dict() == {
            'name': 'Lat Pulldown',
            'reps': '8-12',
            'sets': '2-3',
            'rest_time': '1m 30s',
            'weight': 56,
        }


class TestSplitPicker:
    @pytest.mark.parametrize('activity, expected', [
        ('sedentary', ('Full-Body (Light)', 'Cardio')),
        ('lightly active', ('Full-Body', '')),
        ('active', ('Arnold-Split Upper-Lower', 'Push-Pull-Legs Upper-Lower')),
        ('very active', ('Arnold-Split', 'Push-Pull-Legs')),
        ('extra active', ('Arnold-Split Cardio', 'Push-Pull-Legs Cardio')),
        (None, ('Full-Body (Light)', 'Cardio')),
    ])
    def test_split_for_activity(self, activity, expected):
        assert split_picker(activity) == expected


class TestExerciceGiver:
    @pytest.mark.parametrize('activity, days_1, days_2', [
        ('sedentary', 2, 3),
        ('lightly active', 2, 0),
        ('active', 5, 5),
        ('very active', 6, 6),
        ('extra active', 6, 6),
    ])
    def test_training_days_per_week(self, activity, days_1, days_2):
        option_1, option_2 = exercice_giver(activity)
        assert (len(option_1), len(option_2)) == (days_1, days_2)

    @pytest.mark.parametrize('activity', ACTIVITIES)
    def test_every_day_has_exercises(self, activity):
        option_1, option_2 = exercice_giver(activity)
        assert all(len(day) > 0 for day in option_1 + option_2)

    def test_push_pull_legs_days(self):
        _, option_2 = exercice_giver('very active')
        push, pull, legs = option_2[:3]
        assert 'Flat Bench Press' in push and 'Lateral Raises' in push and 'Skull Crushers' in push
        assert 'Lat Pulldown' in pull and 'Hammer Curls' in pull
        assert 'Hack Squats' in legs and 'RDL' in legs

    def test_extra_active_adds_cardio_to_every_day(self):
        option_1, option_2 = exercice_giver('extra active')
        for day in option_1 + option_2:
            assert day[-1] == 'Treadmill'

    def test_extra_active_adds_cardio_only_once_per_day(self):
        option_1, option_2 = exercice_giver('extra active')
        for day in option_1 + option_2:
            assert day.count('Treadmill') == 1

    def test_calling_twice_gives_same_result(self):
        # Guards against exercise lists being modified between calls
        assert exercice_giver('extra active') == exercice_giver('extra active')


class TestScheduleBuilder:
    @pytest.mark.parametrize('plan, expected', [
        ('strength', ('6-8', '2-3', '3m')),
        ('muscle', ('12-15', '3', '1m')),
        ('both', ('8-12', '2-3', '1m 30s')),
        (None, ('8-12', '2-3', '1m 30s')),
    ])
    def test_reps_sets_rest(self, plan, expected):
        assert schedule_builder(plan) == expected


class TestWeightPicker:
    def test_returns_every_exercise_once(self):
        names = [exercice.name for exercice in weight_picker(80, 'muscle')]
        assert len(names) == 24
        assert len(set(names)) == len(names)

    @pytest.mark.parametrize('name, expected_weight', [
        ('Flat Bench Press', 70),
        ('Incline Dumbell Press', 21),
        ('Lat Pulldown', 70),
        ('Hack Squats', 120),
        ('Leg Curls', 100),
        ('Lateral Raises', 17),
        ('Dips', 'As much as you can'),
        ('One Arm Rear Delt Flies', 'Lowest weight on cable'),
    ])
    def test_weights_scale_with_body_weight(self, name, expected_weight):
        weights = {exercice.name: exercice.weight for exercice in weight_picker(100, 'strength')}
        assert weights[name] == expected_weight

    @pytest.mark.parametrize('plan', ['strength', 'muscle', 'both'])
    def test_lifts_use_plan_reps_sets_rest(self, plan):
        reps, sets, rest_time = schedule_builder(plan)
        bench = next(e for e in weight_picker(80, plan) if e.name == 'Flat Bench Press')
        assert (bench.reps, bench.sets, bench.rest_time) == (reps, sets, rest_time)

    def test_cardio_has_no_reps_or_rest(self):
        treadmill = next(e for e in weight_picker(80, 'strength') if e.name == 'Treadmill')
        assert (treadmill.reps, treadmill.sets, treadmill.rest_time) == ('N/A', '1', 'N/A')


class TestActualSplit:
    @pytest.mark.parametrize('activity', ACTIVITIES)
    def test_days_match_exercice_giver(self, activity):
        given_1, given_2 = exercice_giver(activity)
        plan_1, plan_2 = actual_split(80, 'muscle', activity)
        assert (len(plan_1), len(plan_2)) == (len(given_1), len(given_2))

    @pytest.mark.parametrize('activity', ACTIVITIES)
    def test_days_contain_exercice_objects(self, activity):
        plan_1, plan_2 = actual_split(80, 'muscle', activity)
        assert all(isinstance(e, Exercice) for day in plan_1 + plan_2 for e in day)

    def test_lifting_days_keep_all_exercises(self):
        given_1, _ = exercice_giver('very active')
        plan_1, _ = actual_split(80, 'muscle', 'very active')
        assert [[e.name for e in day] for day in plan_1] == given_1

    @pytest.mark.parametrize('activity', ['sedentary', 'extra active'])
    def test_cardio_is_kept_in_plan(self, activity):
        plan_1, plan_2 = actual_split(80, 'muscle', activity)
        names = [e.name for day in plan_1 + plan_2 for e in day]
        assert 'Treadmill' in names

    def test_no_empty_days(self):
        plan_1, plan_2 = actual_split(80, 'muscle', 'sedentary')
        assert all(len(day) > 0 for day in plan_1 + plan_2)
