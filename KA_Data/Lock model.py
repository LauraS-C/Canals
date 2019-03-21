"""
canal lock code
code to define status of locks along the canal
"""

"""
import everything I need
"""
import numpy as np
from math import *
import pandas
import random

"""
getting data from file
"""
canal = pandas.read_csv('All_KA_Data.csv',engine='python')
lock_status = canal['Lock Status']
lockage = canal['Lockage']
Section = canal['Section']
"""
setup - random initiallisation
"""
def lock_init(lock_status):
    i = 0
    while i < len(lock_status)-1:
        if lock_status[i] == 0:
            j = i+1
        elif lock_status[i] == 1 and lock_status[i+1] == 0:
            lock_status[i] = random.choice([-1,1])
            j = i+1
        elif lock_status[i] == 1 and lock_status[i+1] == 1:
            num = random.choice([-1,1])
            lock_status[i] = num
            check = False
            j = i+1
            while check == False:
                if lock_status[j] == 1 or lock_status[j] == -1:
                    lock_status[j] = num
                    j += 1
                if lock_status[j] == 0:
                    j += 1
                    check = True

        i += (j-i)
    #setting up number of boats in locks as empty
    All_BILL = []
    i = 0
    while i < len(lock_status):
        All_BILL.append([])
        i += 1
    All_BILR = []
    i = 0
    while i < len(lock_status):
        All_BILR.append([])
        i += 1
    return lock_status,All_BILL,All_BILR
               
"""
lockage counter
lock_status - left hand side is 1 and right hand side is -1
(this is the same as the approaching directions of the boats)
"""

def lockage_count(boat_number_pos,boat_number_neg,lockage,lock_status):
    for i in range(0,len(boat_number_pos)):
        if boat_number_pos[i] > 0 and boat_number_neg[i] > 0:
            lockage[i] += 1
            #lock status would not change
        elif boat_number_pos[i] > 0 and boat_number_neg[i] == 0:
            if lock_status[i] == 1:
                lockage[i] += 1/2
                lock_status[i] = -1
            elif lock_status[i] == -1:
                lockage[i] += 1
                lock_status[i] = -1
        elif boat_number_pos[i] == 0 and boat_number_neg[i] > 0:
            if lock_status[i] == 1:
                lockage[i] += 1
                lock_status[i] = 1
            elif lock_status[i] == -1:
                lockage[i] += 1/2
                lock_status[i] = 1
    return lockage,lock_status

def que_build(boats,Section,All_BILL,All_BILR):
    for i in range(0,len(Section))
        boats_in_lock_right = []
        boats_in_lock_left = []
        if lock_status(i) !=0:
            for boat in boats:
                if boat.current_section == i:
                    if boat.direction == 1:
                        boats_in_lock_left.append(boat)#edit it this so adds in order
                    elif boat.direction == -1:
                        boats_in_lock_right.append(boat)
    All_BILL[i] = All_BILL[i].extend(boats_in_lock_left)
    All_BILR[i] = All_BILR[i].extend(boats_in_lock_right)
    return All_BILL,All_BILR
            
def que_run(boats,All_BILL,All_BILR):
    for i in range(0,len(All_BILL)):
        if len(All_BILL[i]) > 0:
            All_BILL[i][0].direction = 1
            del All_BILL[i][0]
            if len(All_BILL[i]) > 0:
                for boat in All_BILL[i]:
                    boat.direction = 0
    for i in range(0,len(All_BILL)):
        if len(All_BILL[i]) > 0:
            All_BILL[i][0].direction = 1
            del All_BILL[i][0]
            if len(All_BILL[i]) > 0:
                for boat in All_BILL[i]:
                    boat.direction = 0
    return All_BILL,All_BILR     


"""
Code to have in run file potentially
"""


lock_init(lock_status)
"""
for i in range(0,len(lock_status)):
    print(lock_status[i])
"""

if lock_status[self.current_section] == 1 or lock_status[self.current_section] == -1:
    lockage_count(lock_status,lockage,self)




















