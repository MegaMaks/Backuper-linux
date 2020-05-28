
import datetime
from datetime import timedelta
from cmd import Cmd

def current_day():
	now = datetime.datetime.now()
	now_day = now.strftime("%A")
	switcher = {
		"Monday": 1,
		"Tuesday": 2,
		"Wednesday": 3,
		"Thursday": 4,
		"Friday": 5,
		"Saturday": 6,
		"Sunday": 7
	}

	return switcher[now_day]

def get_next_time(days, time_start):
        cur_day=int(current_day())
        cur_datetime = datetime.datetime.now()
        time_start_obj = datetime.datetime.strptime(time_start, '%H:%M:%S')
        min_day = 10
        for i in range(0, len(days)):
               
               #print(days[i])
               if int(days[i]) == cur_day:
                     if cur_datetime.time() < time_start_obj.time():
                           min_day = 0
                           #print("today")
                     else:
                           #print("tomorrow")
                           if min_day > (int(days[i]) + 7 - cur_day):
                                 min_day = int(days[i]) + 7 - cur_day
                                 #print(min_day)
               else:
                     #print("xz")
                     if int(days[i]) > cur_day:
                           if min_day > (int(days[i]) - cur_day):
                                 min_day = int(days[i]) - cur_day
                     else:
                           if min_day > (int(days[i]) + 7 - cur_day):
                                 min_day = int(days[i]) + 7 - cur_day
        
        return (cur_datetime + timedelta(days = min_day)).strftime("%Y-%m-%d")+" " + time_start
                                  
        

number_day = current_day()
#print(number_day)
#print( get_next_time("123", "13:00:00") )




