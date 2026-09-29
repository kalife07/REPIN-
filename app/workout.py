from .models import Exercice


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
    cardio = ['Treadmill']
    option_1, option_2 = split_picker(activity)

    option_1_split = option_1.split(' ')
    option_2_split = option_2.split(' ')
    
    exercice_chosen_1 = [] 
    exercice_chosen_2 = [] 

    
    if option_1_split[0] == 'Arnold-Split':
        # Copy the leg list so adding cardio below doesn't change it for option 2
        exercice_chosen_1 = [chest_exercices + back_exercices] + [shoulders_exercices + biceps_exercices + triceps_exercices] + [leg_exercices[:]]
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
            exercice_chosen_2 = [chest_exercices + shoulders_exercices + triceps_exercices] + [back_exercices + biceps_exercices] + [leg_exercices[:]]
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
                       if j == 'Treadmill':
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
