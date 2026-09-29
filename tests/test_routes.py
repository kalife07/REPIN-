import pytest


NUTRITION_BODY = {
    'age': 25, 'gender': 'male', 'weight': 80, 'height': 180,
    'activity': 'active', 'goal': 'cut', 'loss_speed': 'medium',
}


class TestNutritionPlan:
    def test_returns_plan(self, client):
        response = client.post('/api/nutrition-plan', json=NUTRITION_BODY)
        assert response.status_code == 200
        assert response.get_json() == {
            'goal_calories': 2298,
            'macronutrients': {'protein_g': 159, 'fat_g': 51, 'carbs_g': 301},
            'other_info': {'fiber_g': 32, 'sugar_g_limit': 29, 'sodium_mg_limit': 2300, 'water_liters': 2},
        }

    def test_accepts_numbers_sent_as_strings(self, client):
        body = {**NUTRITION_BODY, 'age': '25', 'weight': '80', 'height': '180'}
        response = client.post('/api/nutrition-plan', json=body)
        assert response.status_code == 200
        assert response.get_json()['goal_calories'] == 2298

    @pytest.mark.parametrize('missing', ['age', 'weight', 'height'])
    def test_missing_number_returns_400(self, client, missing):
        body = {k: v for k, v in NUTRITION_BODY.items() if k != missing}
        response = client.post('/api/nutrition-plan', json=body)
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_invalid_goal_returns_400(self, client):
        response = client.post('/api/nutrition-plan', json={**NUTRITION_BODY, 'goal': 'unknown'})
        assert response.status_code == 400


class TestWorkoutPlan:
    def test_returns_two_options(self, client):
        response = client.post('/api/workout-plan', json={'weight': 80, 'plan': 'muscle', 'activity': 'very active'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['option_1']['name'] == 'Arnold-Split'
        assert data['option_2']['name'] == 'Push-Pull-Legs'
        assert len(data['option_1']['schedule']) == 6
        assert len(data['option_2']['schedule']) == 6

    def test_exercises_have_all_fields(self, client):
        response = client.post('/api/workout-plan', json={'weight': 80, 'plan': 'strength', 'activity': 'active'})
        first_exercise = response.get_json()['option_1']['schedule'][0][0]
        assert first_exercise == {
            'name': 'Flat Bench Press', 'reps': '6-8', 'sets': '2-3', 'rest_time': '3m', 'weight': 56,
        }

    def test_single_option_for_lightly_active(self, client):
        response = client.post('/api/workout-plan', json={'weight': 80, 'plan': 'both', 'activity': 'lightly active'})
        data = response.get_json()
        assert data['option_1']['name'] == 'Full-Body'
        assert data['option_2'] == {'name': '', 'schedule': []}

    def test_missing_weight_returns_500(self, client):
        response = client.post('/api/workout-plan', json={'plan': 'muscle', 'activity': 'active'})
        assert response.status_code == 500
        assert response.get_json()['error'].startswith('Error generating workout plan')


class TestTimeToGoal:
    def test_returns_weeks(self, client):
        response = client.post('/api/time-to-goal', json={'current_weight': 80, 'final_weight': 70, 'loss_speed': 'fast'})
        assert response.status_code == 200
        assert response.get_json() == {'weeks_to_goal': 10}

    def test_missing_weight_returns_400(self, client):
        response = client.post('/api/time-to-goal', json={'final_weight': 70, 'loss_speed': 'fast'})
        assert response.status_code == 400
        assert response.get_json()['error'].startswith('Error calculating time')


class TestDateToGoal:
    def test_returns_date(self, client):
        response = client.post('/api/date-to-goal', json={'current_weight': 80, 'final_weight': 80, 'loss_speed': 'fast'})
        assert response.status_code == 200
        day, month, year = response.get_json()['target_date'].split()
        assert day.isdigit() and year.isdigit()
        assert month in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    def test_missing_weight_returns_400(self, client):
        response = client.post('/api/date-to-goal', json={'current_weight': 80, 'loss_speed': 'fast'})
        assert response.status_code == 400
        assert response.get_json()['error'].startswith('Error calculating date')


class TestSleepCalculator:
    def test_returns_wake_up_time(self, client):
        response = client.post('/api/sleep-calculator', json={'bed_time': '10 pm'})
        assert response.status_code == 200
        assert response.get_json() == {'wake_up_time': '6:30 am'}

    def test_invalid_bedtime_returns_400(self, client):
        response = client.post('/api/sleep-calculator', json={'bed_time': 'late'})
        assert response.status_code == 400
        assert response.get_json()['error'].startswith('Error calculating sleep')


class TestServer:
    @pytest.mark.parametrize('url', [
        '/api/nutrition-plan', '/api/workout-plan', '/api/time-to-goal', '/api/date-to-goal', '/api/sleep-calculator',
    ])
    def test_endpoints_only_accept_post(self, client, url):
        assert client.get(url).status_code == 405

    def test_unknown_url_returns_404(self, client):
        assert client.post('/api/unknown', json={}).status_code == 404

    def test_frontend_is_allowed_by_cors(self, client):
        response = client.post('/api/sleep-calculator', json={'bed_time': '10 pm'},
                               headers={'Origin': 'http://localhost:8000'})
        assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:8000'
