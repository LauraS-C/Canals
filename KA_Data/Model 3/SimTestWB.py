"""
Created on Wed Mar 13 17:36:51 2019

@author: laura
"""

import pandas
import random
import numpy as np
import BoatsWBV1 as Boats
import Lock_model
#import Decision_models


def add_to_results(boats_in_section):
    Results[time] = boats_in_section
    return Results

def create_csv_results(results,filename):
    df = pandas.DataFrame(results)
    df.to_csv(filename, sep=',',index=False)
    return

"""
delete boat after the journey is finished
"""
def KillBoat(boat):
    section = boat.current_section
    current_hire_num[hire_ind.index(section)] += 1 # put boat back in hire base
    boats.remove(boat)
    del boat
    
def junc_dec_1(boat):
    if boat.current_section == 70:
        if boat.turned == False:
            junc_perc = 50
            direc_perc = random.randint(1,100)
            if direc_perc <= junc_perc:
                boat.current_section = 144
                boat.current_direction = 1
                boat.start_direction = 1
        elif boat.turned == True:
            if boat.start_line == 'C': 
                boat.current_direction = 1
                boat.start_direction = 1
                boat.current_section = 144
    elif boat.current_section == 144 and boat.current_direction == -1:
        boat.current_section = 70
        if boat.turned == False:
            junc_perc = 50
            direc_perc = random.randint(1,100)
            if direc_perc <= junc_perc:
                boat.current_direction = -1
                boat.start_direction = -1
            elif direc_perc > junc_perc:
                boat.current_direction = 1
                boat.start_direction = 1
        if boat.turned == True:
            if boat.start_line == 'B':
                boat.current_direction = 1
                boat.start_direction = 1
            elif boat.start_line == 'A':
                boat.current_direction = -1
                boat.start_direction = -1

global day
global time
global day_length
global boats
global hire_ind
global Results
global winding_hole
global num_in_lock
day_length = 12 # can change this based on the time of year - should be daylight hours
day = 1
time = 0
run_time = 30 #number of days to run simulation
Results = {}

"""
getting data from file
"""
canal = pandas.read_csv('WB_all.csv',engine='python')
sections = canal['Section']
lock_status = list(canal['Lock Status'])
orig_hire_num = canal['Boat Hires']
winding_hole = canal['Turning Points']
turningfor = canal['next turning forward']
turningback = canal['next turning back']



"""
initialise lock status and lock_loc
"""
lock_status = Lock_model.lock_init(lock_status)
lock_loc = list(np.nonzero(lock_status)[0])
lockage = list(np.zeros(len(lock_status)))

"""
finding locations of hire boat companies and the number of boats at each
"""

hire_ind = np.nonzero(orig_hire_num)
hire_ind = list(hire_ind[0])
orig_hire_num = list(orig_hire_num[hire_ind])
current_hire_num = orig_hire_num
boats = []

"""
Time step for each 15mins/1km 
"""

for i in range(day_length*4*run_time):
    time += 1 #mod 12
    day = day + (time // day_length)
    time = time % day_length  
    """
    creating new boats and adding them to the boats list
    """
    if day == 1 | 5:
        new_boats = Boats.generate_hire_boats(hire_ind, orig_hire_num,day,day_length,current_hire_num)
        for boat in new_boats:
            boats.append(boat)
            current_hire_num[hire_ind.index(boat.current_section)] -=1
    
    """
    initialising counts of boats in each section 
    """
    boats_in_section = np.zeros(len(sections)) 


    """
    lock stuff - put que_main here. Need: boats_in_section,
    lock_loc,boat_in_lock_count_left,boat_in_lock_count_right,lock_check,direction
    
    or set num_in_locks = 0 and lock_dir = 0
    """
    num_in_lock = np.zeros(len(sections))
    
        
    """
    move boats along here
    """
    for boat in boats:
        boat.decision(turningfor,turningback,winding_hole)
        boats_in_section[boat.current_section] += 1
        
        """
        lock stuff and W&B decision
        """
        junc_dec_1(boat)
        lock_ind = boat.current_section + boat.start_direction
        if lock_ind in lock_loc:
            Lock_model.lock_stuff(num_in_lock,lock_status,boat,lock_ind,lockage)
        if boat.alive == False:
            KillBoat(boat)
        
        
    """
    uncomment these to get results
    """
    results = add_to_results(boats_in_section)
create_csv_results(results,"Model1_boats_in_sectionWB.csv")
create_csv_results(lockage,"Model2_lockage_resultsWB.csv")
    



    



