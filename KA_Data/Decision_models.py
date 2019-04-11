"""
code that holds the decision making process for:
1. Which route to take at junctions
2. The probability of stoppping at each section along the canal
3. The probability of which direction the boat will leave the marina
4. The attractvierness of places based of population
"""

"""
needed for this code to run
"""
import numpy as np
from math import *
import pandas
import random

canal = pandas.read_csv('All_KA_Data.csv',engine='python')
sections = canal['Section']

towns = pandas.read_csv('TownsK&A.csv',engine='python')
town_section = towns['Section']
town_pop = towns['Population']

attraction =  pandas.read_csv('KAservices_postcodes.csv',engine='python')
names= attraction['Name']
names = names.tolist()
types = attraction['Service']
types = types.tolist()
postcodes = attraction['Postcode']
postcodes = postcodes.tolist()
at_section = attraction['Section']
at_section = at_section.tolist()

"""
In the set-up
"""

#function to generate ratings for each section of the canal
def section_rating(names,postcodes,types,at_section,sections):
    attraction_types= {
        "Airport":1,
        "Diesel": 1,
        "Electricity":1,
        "Food Shop":1,
        "Gas":1,
        "Laundry":1,
        "Marina":1,
        "Mooring Overnight":1,
        "Public House":1,
        "Refuse Disposal":1,
        "Restaurant":1,
        "Sanitory Station":1,
        "Self Use Pump Out":1,
        "Sewage Disposal":1,
        "Water Point":1,
        "Wi Fi":1}
    names_final =[]
    postcodes_final = []
    attraction_section = []
    for i in range(len(names)):
        if (names[i] in names_final) != True or (postcodes[i] in postcodes_final) != True:
            names_final.append(names[i])
            postcodes_final.append(postcodes[i])
            attraction_section.append(at_section[i])
    ratings = np.zeros(len(names_final))
    for i in range(len(names_final)):
        for j in range(len(names)):
            if names[j] == names_final[i] and postcodes[j] == postcodes_final[i]:
                ratings[i] += attraction_types[types[j]]
    attraction_rating = ratings
    return attraction_section,attraction_rating
                       
def town_rating(town_pop,max_rat):#max_rat depends on rating system
    town_rat = town_pop
    max_pop = max(town_rat)
    rat_per_pop = (2*max_rat)/max_pop#edit to potentially give more weight to towns
    town_rat = town_rat*rat_per_pop
    for i in range(len(town_rat)):
        if town_rat[i] != max(town_rat):
            town_rat[i] += 1#increase all but max town rating to give town rating more bias
            town_rat[i] = round(town_rat[i])
    return town_rat

def sec_prob_build(sections,attraction_section,attraction_rating,town_rat):
    stop_prob = np.zeros(len(attraction_section))
    sec_rat_tot = np.zeros(len(attraction_section))
    j = 0
    new_att_section = []
    att_section = []
    for i in range(len(attraction_section)):
        for j in range(len(attraction_section)):
            if ((attraction_section[j] in new_att_section) != True) and (attraction_section[i] == attraction_section[j]):
                sec_rat_tot[i] += attraction_rating[j]
        new_att_section.append(attraction_section[i])
    i = 0
    while i < len(sec_rat_tot):
        if sec_rat_tot[i] == 0:
            sec_rat_tot = np.delete(sec_rat_tot,i)
            del new_att_section[i]
            i = 0
        i +=1
    section_check = []
    for i in range(len(new_att_section)):
        for j in range(len(town_rat)):
            if new_att_section[i] == town_section[j]:
                sec_rat_tot[i] += town_rat[j]
                section_check.append(town_section[j])  
            elif (town_section[j] in section_check) != True:
                if (town_section[j] in new_att_section) != True:
                    new_att_section.append(town_section[j])
                    sec_rat_tot = np.append(sec_rat_tot,town_rat[j])
    max_rating = max(sec_rat_tot)
    perc_per_rat = 90/max_rating
    sec_perc = sec_rat_tot*perc_per_rat
    for i in range(len(sec_rat_tot)):
        sec_perc[i] = round(sec_perc[i])
    final_sec_perc = np.zeros(len(sections))
    for i in range(len(sec_perc)):
        sec = np.where(sections == str(new_att_section[i]))
        final_sec_perc[sec[0]] = sec_perc[i]
    return final_sec_perc

"""
These functions to be called within each boat in boats loop
"""

def boat_stop(final_sec_perc,boat):
    if boat.stop_time == 0:
        stop_perc = final_sec_perc[boat.current_section]
        stop_prob = random.randint(1,100)
        if stop_prob <= stop_perc:
            boat.current_direction = 0
            t = random.randint(2,8)
            boat.stop_time = t
    elif boat.stop_time != 0:
        boat.stop_time -= 1
        if boat.stop_time == 0:
            boat.current_direction = boat.start_direction

"""
This function goes boat creation
"""
def marina_driec(boat,sections,sec_perc):
    left_tot = 0
    right_tot = 0
    for i in range(len(sections)):
        if sections[i] < boat.current_section:
            left_tot += sec_perc[i]
        elif sections[i] > boat.current_section:
            right_tot += sec_perc[i]
    tot_tot = left_tot + right_tot
    left_perc = left_tot/tot_tot
    direc_perc = random.randint(1,100)
    if direc_perc <= left_perc:
        boat.start_driection = -1
    if direc_perc > left_perc:
        boat.start_driection = 1

"""
Test run section below
"""
[attraction_section,attraction_rating] = section_rating(names,postcodes,types,at_section,sections)
town_rat = town_rating(town_pop,max(attraction_rating))
sec_prob_build(sections,attraction_section,attraction_rating,town_rat)















    
    
    
