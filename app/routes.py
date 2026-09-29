from flask import Blueprint, request, jsonify

from .nutrition import (goal_calories, protein_intake, fat_intake, carb_intake,
                        fibers_intake, sugar_intake, sodium_intake, water_intake)
from .workout import split_picker, actual_split
from .goals import time_to_goal, date_to_goal
from .sleep import sleep


api = Blueprint('api', __name__)


@api.route('/api/nutrition-plan', methods=['POST'])
def get_nutrition_plan():
    try:
        data = request.json
        
        age = int(data.get('age'))
        gender = data.get('gender')
        weight = float(data.get('weight'))
        height = float(data.get('height'))
        activity = data.get('activity')
        goal = data.get('goal')
        loss_speed = data.get('loss_speed')

        calories = goal_calories(age, gender, weight, loss_speed, height, activity, goal)
        protein = protein_intake(weight, activity)
        fat = fat_intake(age, gender, weight, loss_speed, height, activity, goal)
        carbs = carb_intake(age, gender, weight, loss_speed, height, activity, goal)
        fiber = fibers_intake(age, gender, weight, loss_speed, height, activity, goal)
        sugar = sugar_intake(age, gender, weight, loss_speed, height, activity, goal)
        sodium = sodium_intake()
        water = water_intake()
        
        response = {
            "goal_calories": calories,
            "macronutrients": {
                "protein_g": protein,
                "fat_g": fat,
                "carbs_g": carbs
            },
            "other_info": {
                "fiber_g": fiber,
                "sugar_g_limit": sugar,
                "sodium_mg_limit": sodium,
                "water_liters": water
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api.route('/api/workout-plan', methods=['POST'])
def get_workout_plan():
    try:
        data = request.json
        
        weight = float(data.get('weight')) 
        plan = data.get('plan') 
        activity = data.get('activity') 

        split_name_1, split_name_2 = split_picker(activity)
        plan_list_1, plan_list_2 = actual_split(weight, plan, activity)
        
        plan_1_json = [[exercice.to_dict() for exercice in day] for day in plan_list_1]
        plan_2_json = [[exercice.to_dict() for exercice in day] for day in plan_list_2]

        response = {
            "option_1": {
                "name": split_name_1,
                "schedule": plan_1_json 
            },
            "option_2": {
                "name": split_name_2,
                "schedule": plan_2_json
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Error generating workout plan: {str(e)}"}), 500

@api.route('/api/time-to-goal', methods=['POST'])
def get_time_to_goal():
    try:
        data = request.json
        current_weight = float(data.get('current_weight'))
        final_weight = float(data.get('final_weight'))
        loss_speed = data.get('loss_speed')
        
        weeks = time_to_goal(current_weight, final_weight, loss_speed)
        
        return jsonify({"weeks_to_goal": weeks})
    except Exception as e:
        return jsonify({"error": f"Error calculating time: {str(e)}"}), 400

@api.route('/api/date-to-goal', methods=['POST'])
def get_date_to_goal():
    try:
        data = request.json
        current_weight = float(data.get('current_weight'))
        final_weight = float(data.get('final_weight'))
        loss_speed = data.get('loss_speed')
        
        target_date = date_to_goal(current_weight, final_weight, loss_speed)
        
        return jsonify({"target_date": target_date})
    except Exception as e:
        return jsonify({"error": f"Error calculating date: {str(e)}"}), 400

@api.route('/api/sleep-calculator', methods=['POST'])
def get_sleep_calc():
    try:
        data = request.json
        bed_time = data.get('bed_time') # e.g., "10 pm"
        
        wake_up_time = sleep(bed_time)
        
        return jsonify({"wake_up_time": wake_up_time})
    except Exception as e:
        return jsonify({"error": f"Error calculating sleep: {str(e)}"}), 400
