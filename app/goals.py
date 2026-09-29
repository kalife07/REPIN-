from datetime import datetime
from datetime import date 
from dateutil.relativedelta import relativedelta

from .config import MONTH


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
