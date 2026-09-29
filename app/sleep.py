from .config import OPTIMAL_SLEEP


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
