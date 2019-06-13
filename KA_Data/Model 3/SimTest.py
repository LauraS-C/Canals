"""
Created on Wed Mar 13 17:36:51 2019
@author: laura
"""

import pandas
import numpy as np
import BoatsWB as Boats
#import Boats as Boats
import Lock_model
import Decision_models ####
import random ####


def add_to_results(boats_in_section):
    Results[full_time] = boats_in_section
    #print(Results[full_time])
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
    try:
        current_hire_num[hire_ind.index(section)] += 1 # put boat back in hire base
    except:
        pass
    finally:
        boats.remove(boat)
        del boat

####
"""
intial boat direction function#
"""
def marina_driec(boat,sections,final_sec_perc):
    left = boat.current_section-(boat.end_time//4)
    right = boat.current_section+(boat.end_time//4)
    if left < 0:
        left = 0
    left_tot = sum(final_sec_perc[left:boat.current_section-1])
    if right > len(final_sec_perc):
        right = len(final_sec_perc)
    right_tot = sum(final_sec_perc[boat.current_section+1:right])
    #print(left_tot,right_tot)
    tot_tot = left_tot + right_tot
    if tot_tot == 0:
        tot_tot = 10000
    left_perc = (left_tot/tot_tot)*100
    #if 45 < boat.current_section < 58:
    #    left_perc = 95
    direc_perc = random.randint(1,100)
    if direc_perc <= left_perc:
        boat.start_driection = -1
        boat.current_driection = -1
        #print(left_perc,left_tot,right_tot,boat.start_section,'left')
    elif direc_perc > left_perc:
        boat.start_driection = 1
        boat.current_driection = 1
        #print(left_perc,left_tot,right_tot,boat.start_section,'right')
####
        
global day
global time
global full_time
global day_length
global boats
global hire_ind
global Results
global winding_hole
global num_in_lock
day_length = 12*4 # can change this based on the time of year - should be daylight hours
day = 1
time = 0
full_time = 0
run_time = 30 #number of days to run simulation
Results = {}

"""
getting data from file
"""
#canal = pandas.read_csv('All_KA_Data.csv',engine='python')
#boat_numbers = [686,314] #KA boat numbers - continuous cruisers & end boats,priv moorings
canal = pandas.read_csv('WB_all.csv',engine='python')
boat_numbers = [396,181] # WB boat numbers - continuous cruisers & end boats,priv moorings
current_boat_num = boat_numbers
sections = canal['Section']
lock_status = list(canal['Lock Status'])
lockage = list(canal['Lockage'])
orig_hire_num = canal['Boat Hires']
winding_hole = canal['Turning Points']
turningfor = canal['next turning forward']
turningback = canal['next turning back']
day_hire = canal['Day Hires']
canal_length = len(sections)-1


#####Decision model data retreaval######
#towns = pandas.read_csv('TownsK&A.csv',engine='python')
towns = pandas.read_csv('TownsW&B.csv',engine='python')
town_section = towns['Section']
town_pop = towns['Population']


#attraction =  pandas.read_csv('KAservices_postcodes.csv',engine='python')
attraction =  pandas.read_csv('AttractionsW&B.csv',engine='python')
names= attraction['Name']
names = names.tolist()
types = attraction['Service']
types = types.tolist()
at_section = attraction['Section']
at_section = at_section.tolist()
####

"""
initialise lock status and lock_loc
"""
lock_status = Lock_model.lock_init(lock_status)
lock_loc = list(np.nonzero(lock_status)[0])

"""
finding locations of hire boat companies and the number of boats at each
"""

hire_ind = np.nonzero(orig_hire_num)
hire_ind = list(hire_ind[0])
orig_hire_num = list(orig_hire_num[hire_ind])
current_hire_num = orig_hire_num
orig_day_hire = list(day_hire[hire_ind])
current_day_hire = orig_day_hire
boats = []


####
"""
Setting up section ratings
"""
[attraction_section,attraction_rating] = Decision_models.section_rating(names,types,at_section,sections)
town_rat = Decision_models.town_rating(town_pop,max(attraction_rating))
final_sec_perc = Decision_models.sec_prob_build(sections,attraction_section,attraction_rating,town_rat)

"""
Time step for each 15mins/1km 
"""

for i in range(day_length*run_time):
    full_time += 1 #mod 12
    day = (full_time // day_length) % 7
    time = full_time % day_length  
    
    """
    creating new boats and adding them to the boats list
    """
    new_boats = []
    if day == 1 or day == 5:
        new_boats = Boats.generate_hire_boats(time,hire_ind, orig_hire_num,day,day_length,current_hire_num,Boats.create_boat)
        
    if time < day_length//4:
        new_boats = new_boats + Boats.generate_hire_boats(time,hire_ind, orig_day_hire,day,day_length,current_day_hire,Boats.day_boat)
    
    """
    adding continuous cruisers and end boats
    """
    if current_boat_num[0]>0:
        for i in range(boat_numbers[0]//20):
            gen = np.random.uniform(size=1)
            if gen < boat_numbers[0]/100:
                which = np.random.uniform(size=1)
                current_boat_num[0] -= 1
                if which < 0.75:
                    new_boats.append(Boats.cont_cruiser(day_length,canal_length))
                else:
                    new_boats.append(Boats.end_boat(canal_length))
    """
    add privately moored boats
    """
    if current_boat_num[1]>0:
        for i in range(boat_numbers[1]//20):
            gen = np.random.uniform(size=1)
            if gen < boat_numbers[0]/100:
                current_boat_num[0] -= 1
                origin = np.random.randint(0,len(hire_ind),size=None,dtype='int')
                new_boats.append(Boats.private_moored(time,hire_ind[origin],day,day_length))
        
    
    
    for boat in new_boats:
        marina_driec(boat,sections,final_sec_perc)####
        boats.append(boat)
        
            
    
    
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
        boat.decision(turningfor,turningback,winding_hole,canal_length)
        boats_in_section[boat.current_section] += 1

        """
        working out if a boat stops in this section
        """
        Decision_models.boat_stop(final_sec_perc,boat)

        """
        junction decision function
        """
        #Decision_models.junc_dec_2(final_sec_perc,boat)
        
        """
        making count of the direction of boats in each section
        """
        lock_ind = boat.current_section + boat.start_direction
        if lock_ind in lock_loc:
            Lock_model.lock_stuff(num_in_lock,lock_status,boat,lock_ind,lockage)
        if boat.alive == False:
            KillBoat(boat)
        
        
    """
    uncomment these to get results
    """
    results = add_to_results(boats_in_section)
create_csv_results(results,"Model3_boats_in_section_WB_month.csv")
create_csv_results(lockage,"Model3_lockage_results_WB_month.csv")
