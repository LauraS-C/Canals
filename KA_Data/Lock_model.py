"""
import everything I need
"""
import pandas
import random

def empty_list(input_list):
    """Recursively iterate through values in nested lists."""
    for item in input_list:
        if not isinstance(item, list) or not empty_list(item):
             return False
    return True

"""
getting data from file
"""
canal = pandas.read_csv('All_KA_Data.csv',engine='python')
lock_status = list(canal.loc[:,'Lock Status'])
lockage = list(canal.loc[:,'Lockage'])
sections = list(canal.loc[:,'Section'])
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

    return lock_status

"""
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
"""
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

def que_build(Section, All_BILL, All_BILR, lock_status,boats):
    for i in range(len(Section)):
        boats_in_lock_right = []
        boats_in_lock_left = []
        if lock_status[i] !=0:
            for boat in boats:
                if boat.current_section == i:
                    if boat.current_direction == 1:
                        boats_in_lock_left.append(boat)#edit it this so adds in order
                    elif boat.current_direction == -1:
                        boats_in_lock_right.append(boat)
    
    if empty_list(All_BILL) == True:
        All_BILL[i] = All_BILL[i].extend(boats_in_lock_left)
    if empty_list(All_BILR) == True:
        All_BILR[i] = All_BILR[i].extend(boats_in_lock_right)
    return All_BILL,All_BILR
            
def que_run(All_BILL,All_BILR):
    if empty_list(All_BILL) == True:
        for i in range(0,len(All_BILL)):
            if len(All_BILL[i]) > 0:
                All_BILL[i][0].current_direction = 1
                del All_BILL[i][0]
                if len(All_BILL[i]) > 0:
                    for boat in All_BILL[i]:
                        boat.current_direction = 0
    if empty_list(All_BILR) == True:
        for i in range(0,len(All_BILR)):
            if len(All_BILR[i]) > 0:
                All_BILR[i][0].current_direction = 1
                del All_BILR[i][0]
                if len(All_BILR[i]) > 0:
                    for boat in All_BILR[i]:
                        boat.current_direction = 0
    return All_BILL,All_BILR


def que_main(boats_in_section,lock_loc,boat_in_lock_count_left,boat_in_lock_count_right,lock_check,direction):
    if boats_in_section[lock_loc] == 0:
        if lock_check[lock_loc] == 0:
            if direction == 1:
                boat_in_lock_count_left[lock_loc] = 1
                lock_check[lock_loc] += 1
                if boat.start_direction == 1:
                    boat.current_direction = 1
            elif direction == -1:
                boat_in_lock_count_right[lock_loc] = 1
                lock_check[lock_loc] += 1
                if boat.start_direction == -1:
                    boat.current_direction = -1
        elif lock_check[lock_loc] == 1:
            if boat_in_lock_count_left[lock_loc] == 1 and direction == -1:
                boat_in_lock_count_right[lock_loc] = 1
                if boat.start_direction == -1:
                    boat.current_direction = -1
                lock_check[lock_loc] += 1
            if boat_in_lock_count_right[lock_loc] == 1 and direction == 1:
                boat_in_lock_count_right[lock_loc] = 1
                if boat.start_direction == 1:
                    boat.current_direction = 1
                lock_check[lock_loc] += 1              
        elif lock_check[lock_loc] == 2:
            boat.current_driection  = 0          
    elif boats_in_section[lock_loc] > 0:
        boat.current_direction = 0

               


























