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
