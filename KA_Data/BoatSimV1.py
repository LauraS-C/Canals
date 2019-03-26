# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:36:51 2019

@author: laura
"""

import pandas
import numpy as np
import Boats
import seaborn as sb
import Lock_model


def add_to_results(boats_in_section):
    Results[time] = boats_in_section
    return Results

def HeatMap(boats_in_section,sections):
    boats_in_section = np.transpose(np.array(boats_in_section))
    boats_in_section = pandas.DataFrame(boats_in_section, index=sections)
    sb.heatmap(boats_in_section,cmap = "YlGnBu")
    
"""
delete boat after the journey is finished
"""
def KillBoat(boat):
    section = boat.current_section
    current_hire_num[hire_ind.index(section)] += 1 # put boat back in hire base
    boats.remove(boat)
    del boat

global day
global time
global boats
global hire_ind
global Results
day = 1
time = 0
Results = {}

"""
getting data from file
"""
canal = pandas.read_csv('All_KA_Data.csv',engine='python')
sections = canal['Section']
lock_status = list(canal['Lock Status'])
lockage = canal['Lockage']
orig_hire_num = canal['Boat Hires']

"""
initialise lock status
"""
[lock_status,All_BILL,All_BILR] = Lock_model.lock_init(lock_status)


"""
finding locations of hire boat companies and the number of boats at each
"""

hire_ind = np.nonzero(orig_hire_num)
hire_ind = list(hire_ind[0])
orig_hire_num = list(orig_hire_num[hire_ind])
current_hire_num = orig_hire_num
boats = []

"""
for each time step generating hire boats to leave the hire companies and creating counts
"""
for i in range(32):
    time += 1 #mod 12
    #day as count of loops of time    
    """
    creating new boats and adding them to the boats list
    """
    new_boats = Boats.generate_hire_boats(hire_ind, orig_hire_num)
    for boat in new_boats:
        boats.append(boat)
        current_hire_num[hire_ind.index(boat.current_section)] -=1
        
    """
    creating counts of boats in each section along with direction of boats in each section
    """
    boats_in_section = np.zeros(len(sections))
    boat_number_pos = np.zeros(len(sections))
    boat_number_neg = np.zeros(len(sections))  


    """
    lock stuff
    """
    [All_BILL,All_BILR] = Lock_model.que_build(sections,All_BILL,All_BILR,lock_status,boats)
    [All_BILL,All_BILR] = Lock_model.que_run(All_BILL,All_BILR)      
        
        
    """
    move boats along here
    """
    for boat in boats:
        boat.decision()
        boats_in_section[boat.current_section] += 1
        """
        making count of the direction of boats in each section
        """
        direction = boat.current_direction
        if direction == 1:
            boat_number_pos[boat.current_section] += 1
        elif direction == -1:
            boat_number_neg[boat.current_section] += 1 
        if boat.alive == False:
            KillBoat(boat)
        if lock_status[boat.current_section] != 0:
            [lockage, lock_status] = Lock_model.lockage_count(boat_number_pos,boat_number_neg,lockage,lock_status)
              
    #add_to_results(boats_in_section)
        
#df = pandas.DataFrame(Results)
#df.to_csv("Results_of_SimTest.csv", sep=',',index=False)
  
df =pandas.DatFrame(lockage)
df.to_csv("Lockage results Model 1", sep=',',index=False)
    
HeatMap(boats_in_section,sections)
    



