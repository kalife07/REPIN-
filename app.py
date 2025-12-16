from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from datetime import date 
from dateutil.relativedelta import relativedelta

MONTH = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
OPTIMAL_SLEEP = 8.5 #hours


app = Flask(__name__)
CORS(app) 


class Exercice:
    def __init__(self,name, reps, sets, rest_time, weight ):
        self.name = name
        self.reps = reps
        self.sets = sets
        self.rest_time = rest_time
        self.weight = weight
    

    def to_dict(self):
        return {
            "name": self.name,
            "reps": self.reps,
            "sets": self.sets,
            "rest_time": self.rest_time,
            "weight": self.weight
        }


def burned_calories(age, gender, weight, height, activity):
    if gender == 'male':
        BMR = 10*weight + 6.25*height - 5*age +5
    else:
        BMR = 10*weight + 6.25*height - 5*age - 161
    

    if activity == 'sedentary':
        return BMR * 1.2
    elif activity == 'lightly active':# 2 days
        return BMR * 1.375
    elif activity == 'active':# 5
        return BMR * 1.55
    elif activity == 'very active':# 6
        return BMR * 1.725
    elif activity == 'extra active':# 2x/ 6 day
        return BMR * 1.9
    else:
        # Default case if activity is None or invalid
        return BMR * 1.375 

def protein_intake(weight, activity):
    weight = round(weight*2.205, 2)
    if activity == 'lightly active':
        return round(weight * 0.8)
    elif activity == 'active': 
        return round(weight * 0.9)
    elif activity == 'very active':
        return round(weight * 1)
    elif activity == 'extra active':
        return round(weight * 1)
    else: # Default for sedentary
        return round(weight * 0.8)

def fat_intake(age, gender, init_weight, loss_speed, height, activity, goal):
    
    if goal == 'bulk':  
        fat_calories = goal_calories(age, gender, init_weight, loss_speed , height, activity, goal) * 0.3
        return round(fat_calories/9)
    elif goal == 'maintain':
        fat_calories = goal_calories(age, gender, init_weight, loss_speed , height, activity, goal) * 0.25
        return round(fat_calories/9)
    elif goal == 'cut':
        fat_calories = goal_calories(age, gender, init_weight, loss_speed , height, activity, goal) * 0.2
        return round(fat_calories/9)

def carb_intake(age, gender, init_weight, loss_speed, height, activity, goal):
    remaining_cal = (goal_calories(age, gender, init_weight, loss_speed , height, activity, goal) -
                     4*protein_intake(init_weight, activity) -
                     9*fat_intake(age, gender, init_weight,loss_speed, height, activity, goal))
    return round(remaining_cal/4)

def fibers_intake(age, gender, init_weight,loss_speed, height, activity,goal):
    multiplier = goal_calories(age, gender, init_weight, loss_speed , height, activity, goal) /1000
    return round(multiplier * 14)

def sugar_intake(age, gender, init_weight,loss_speed, height, activity, goal):
    if goal == 'bulk' or goal == 'maintain':
        return round((goal_calories(age, gender, init_weight, loss_speed , height, activity, goal) * 0.10)/4)
    else:
        return round((goal_calories(age, gender, init_weight, loss_speed , height, activity, goal) * 0.05)/4)

def sodium_intake():
    return 2300

def water_intake():
    return 2 

def goal_calories(age, gender, init_weight, loss_speed , height, activity, goal):
    mod_cal = 0 # Default for maintain
    if loss_speed == 'slow':
        mod_cal = 300
    elif loss_speed =='medium':
        mod_cal = 500
    elif loss_speed == 'fast':
        mod_cal = 1000 
    
    base_calories = burned_calories(age, gender, init_weight, height, activity)

    if goal =='bulk':
        return round(base_calories + mod_cal)
    elif goal == 'cut':
        return round(base_calories - mod_cal)
    else: # maintain
        return round(base_calories)

def split_picker(activity):
    
    split = ['Push-Pull-Legs', 'Arnold-Split', 'Upper-Lower', 'Full-Body', 'Cardio']
    second_chosen_split = ''
    if activity == 'lightly active':# 2 days
        first_chosen_split = split[3]
    elif activity == 'active':# 5
        first_chosen_split = split[1]+' '+split[2]
        second_chosen_split = split[0]+' '+split[2]
    elif activity == 'very active':# 6
        first_chosen_split = split[1]
        second_chosen_split = split[0]
    elif activity == 'extra active':# 2x/day
        first_chosen_split = split[1]+' '+split[-1]
        second_chosen_split = split[0]+' '+split[-1]
    else: # Default for sedentary
        first_chosen_split = 'Full-Body (Light)'
        second_chosen_split = 'Cardio'
        
    return first_chosen_split, second_chosen_split

def exercice_giver(activity):
    chest_exercices = ['Flat Bench Press', 'Incline Dumbell Press', 'Machine Flies', 'Dips']
    triceps_exercices = ['Rope Extensions', 'Skull Crushers']
    back_exercices = ['One Arm Pulldowns', 'Lat Pulldown', 'Seated Rows', 'One Arm Rear Delt Flies']
    biceps_exercices = ['Hammer Curls', 'Incline Dumbell Curls', 'Preacher Curls', 'Reverse Curls', 'Forearm Curls']
    shoulders_exercices = ['Lateral Raises', 'Machine Shoulder Press']
    leg_exercices = ['Hack Squats', 'RDL', 'Leg Curls', 'Leg Extensions', 'Adductors', 'Calves Raises']
    cardio = ['treadmill'] 
    option_1, option_2 = split_picker(activity)

    option_1_split = option_1.split(' ')
    option_2_split = option_2.split(' ')
    
    exercice_chosen_1 = [] 
    exercice_chosen_2 = [] 

    
    if option_1_split[0] == 'Arnold-Split':
        exercice_chosen_1 = [chest_exercices + back_exercices] + [shoulders_exercices + biceps_exercices + triceps_exercices] + [leg_exercices]
        if len(option_1_split) > 1:
            if option_1_split[1] == 'Upper-Lower':
                exercice_chosen_1 += ([chest_exercices[:2]+back_exercices[1:3]+[shoulders_exercices[0]]+biceps_exercices[1:3]+[triceps_exercices[0]]]+[leg_exercices])
            elif option_1_split[1] == 'Cardio':
                for i in range(len(exercice_chosen_1)):
                    exercice_chosen_1[i].append(cardio[0])
                exercice_chosen_1 *=2
        else:
            exercice_chosen_1 *= 2
    elif option_1 == 'Full-Body':
        exercice_chosen_1 = [chest_exercices[:2]+back_exercices[1:3]+[shoulders_exercices[0]]+biceps_exercices[1:3]+[triceps_exercices[0]]+leg_exercices[2:4]]
        exercice_chosen_1 *=2
    
    elif option_1 == 'Full-Body (Light)':
        exercice_chosen_1 = [[chest_exercices[0], back_exercices[1], leg_exercices[0]]] * 2 
    elif option_1 == 'Cardio':
        exercice_chosen_1 = [[cardio[0]]] * 3 

    
    if option_2 != '':
        if option_2_split[0] == 'Push-Pull-Legs':
            exercice_chosen_2 = [chest_exercices + shoulders_exercices + triceps_exercices] + [back_exercices + biceps_exercices] + [leg_exercices]
            if len(option_2_split) > 1:
                if option_2_split[1] == 'Upper-Lower':
                    exercice_chosen_2 += ([chest_exercices[:2]+back_exercices[1:3]+[shoulders_exercices[0]]+biceps_exercices[1:3]+[triceps_exercices[0]]]+[leg_exercices])
                elif option_2_split[1] == 'Cardio':
                    for i in range(len(exercice_chosen_2)):
                        exercice_chosen_2[i].append(cardio[0])
                    exercice_chosen_2 *= 2
            else:
                exercice_chosen_2 *= 2
        elif option_2_split[0] == 'Cardio':
             exercice_chosen_2 = [[cardio[0]]] * 3

    return exercice_chosen_1, exercice_chosen_2

def schedule_builder(plan):
    if plan == 'strength':
        reps = '6-8'
        sets = '2-3'
        rest_time = '3m'
    elif plan == 'muscle':
        reps = '12-15'
        sets = '3'
        rest_time = '1m'
    else: 
        reps = '8-12'
        sets = '2-3'
        rest_time = '1m 30s'
    return reps, sets, rest_time

def weight_picker(init_weight,plan):
    chest_exercices = ['Flat Bench Press', 'Incline Dumbell Press', 'Machine Flies', 'Dips']
    triceps_exercices = ['Rope Extensions', 'Skull Crushers']
    back_exercices = ['One Arm Pulldowns', 'Lat Pulldown', 'Seated Rows', 'One Arm Rear Delt Flies']
    biceps_exercices = ['Hammer Curls', 'Incline Dumbell Curls', 'Preacher Curls', 'Reverse Curls', 'Forearm Curls']
    shoulders_exercices = ['Lateral Raises', 'Machine Shoulder Press']
    leg_exercices = ['Hack Squats', 'RDL', 'Leg Curls', 'Leg Extensions', 'Adductors', 'Calves Raises']
    
    cardio_exercices = ['Treadmill']

    all_exercices = [chest_exercices, triceps_exercices, back_exercices, biceps_exercices, shoulders_exercices, leg_exercices, cardio_exercices]
    
    chest_dict = {'Flat Bench Press':round(init_weight*0.7), 'Incline Dumbell Press':round(init_weight*0.7*0.3), 'Machine Flies':round(init_weight*0.7), 'Dips': 'As much as you can'}
    triceps_dict = {'Rope Extensions': round(init_weight*0.35), 'Skull Crushers': round(init_weight/4)}
    back_dict = {'One Arm Pulldowns': round(init_weight/2.7), 'Lat Pulldown': round(init_weight*0.7), 'Seated Rows': round(init_weight/2), 'One Arm Rear Delt Flies': 'Lowest weight on cable'}
    biceps_dict = {'Hammer Curls': round(init_weight*0.17), 'Incline Dumbell Curls': round(init_weight*0.15), 'Preacher Curls': round(init_weight*0.3), 'Reverse Curls': round(init_weight*0.27), 'Forearm Curls': round(init_weight*0.45)}
    shoulders_dict = {'Lateral Raises': round(init_weight*0.17), 'Machine Shoulder Press': round(init_weight*0.6)}
    legs_dict = {'Hack Squats': round(init_weight*1.2), 'RDL': round(init_weight*0.55), 'Leg Curls': round(init_weight), 'Leg Extensions': round(init_weight*0.9), 'Adductors': round(init_weight*0.65), 'Calves Raises': round(init_weight*0.27)}
    
    cardio_dict = {'Treadmill': '45min Incline Walk'} 

    dict_list = [chest_dict,triceps_dict, back_dict, biceps_dict, shoulders_dict, legs_dict, cardio_dict]
    
    reps, sets, rest_time = schedule_builder(plan)
    planned_exercice_list = []
    
    for i in all_exercices:
        for j in i:
           for dict_item in dict_list:
               for key, value in dict_item.items():
                   if j == key:
                       weight = value 
                       if j == 'treadmill':
                           planned_exercice_list.append(Exercice(j, 'N/A', '1', 'N/A', weight))
                       else:
                           planned_exercice_list.append(Exercice(j, reps, sets, rest_time, weight))
    return planned_exercice_list

def actual_split(init_weight, plan, activity):
    actual_exercice_list_1 = []
    actual_exercice_list_2 = []
    planned_exercice_list = weight_picker(init_weight, plan)
    given_exercice_1, given_exercice_2 = exercice_giver(activity)
    

    for day_list in given_exercice_1:
        day_plan = []
        for exercice_name in day_list:
            for exercice_obj in planned_exercice_list:
                if exercice_obj.name == exercice_name:
                    day_plan.append(exercice_obj)
                    break 
        actual_exercice_list_1.append(day_plan)
            

    for day_list in given_exercice_2:
        day_plan = []
        for exercice_name in day_list:
            for exercice_obj in planned_exercice_list:
                if exercice_obj.name == exercice_name:
                    day_plan.append(exercice_obj)
                    break
        actual_exercice_list_2.append(day_plan)
            
    return actual_exercice_list_1, actual_exercice_list_2


def time_to_goal(current_weight , final_weight, loss_speed):
    kg_diff = final_weight - current_weight
    
    if kg_diff == 0:
        return 0 
        
    if loss_speed == 'slow':
        week_loss = 0.25 #kg
    elif loss_speed == 'medium':
        week_loss = 0.5 #kg
    elif loss_speed == 'fast':
        week_loss = 1 # kg
    else: 
        week_loss = 0.5

    time_to_final = abs(kg_diff / week_loss) #week
    
    return time_to_final


def date_to_goal(current_weight , final_weight, loss_speed):
    goal_date_weeks = time_to_goal(current_weight , final_weight, loss_speed)
    
    if goal_date_weeks == 0:
        today = date.today()
        cur_month = MONTH[today.month-1]
        return str(today.day) + ' ' + cur_month + ' ' + str(today.year)

    today = date.today()
    base_date = datetime(today.year, today.month, today.day)
    new_date = base_date + relativedelta(days=(goal_date_weeks * 7))
    cur_month = MONTH[new_date.month-1]
    
    return str(new_date.day)+ ' ' + cur_month + ' ' + str(new_date.year)


def sleep(bed_time):
    if not bed_time:
        return "N/A"
        
    hours_list = bed_time.split()
    hour = int(hours_list[0])
    am_pm = hours_list[1].lower() 

    if hour == 12 and am_pm == 'am': # 12 AM (Midnight)
       hour = 0
    elif hour != 12 and am_pm == 'pm': # 1 PM to 11 PM
       hour += 12
    
    wake_hour_24 = (hour + OPTIMAL_SLEEP) % 24
    
    wake_hour_final = int(wake_hour_24)
    minutes = int((wake_hour_24 - wake_hour_final) * 60)
    
    wake_am_pm = 'am'
    if wake_hour_final >= 12:
        wake_am_pm = 'pm'
    
    wake_hour_12 = wake_hour_final % 12
    if wake_hour_12 == 0:
        wake_hour_12 = 12 
        
    if minutes > 0:
        display_time = f"{wake_hour_12}:{minutes:02}"
    else:
        display_time = str(wake_hour_12)

    return display_time + ' ' + wake_am_pm




@app.route('/api/nutrition-plan', methods=['POST'])
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

@app.route('/api/workout-plan', methods=['POST'])
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

@app.route('/api/time-to-goal', methods=['POST'])
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

@app.route('/api/date-to-goal', methods=['POST'])
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

@app.route('/api/sleep-calculator', methods=['POST'])
def get_sleep_calc():
    try:
        data = request.json
        bed_time = data.get('bed_time') # e.g., "10 pm"
        
        wake_up_time = sleep(bed_time)
        
        return jsonify({"wake_up_time": wake_up_time})
    except Exception as e:
        return jsonify({"error": f"Error calculating sleep: {str(e)}"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
