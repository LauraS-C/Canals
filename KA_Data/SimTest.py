# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:36:51 2019

@author: laura
"""

import pandas
import numpy as np
import Boats
import seaborn as sb

global day
global time
day = 1
time = 0

"""
getting data from file
"""
canal = pandas.read_csv('All_KA_Data.csv',engine='python')
sections = canal['Section']
orig_hire_num = canal['Boat Hires']


"""
finding locations of hire boat companies and the number of boats at each
"""
hire_ind = np.nonzero(orig_hire_num)
hire_ind = list(hire_ind[0])
orig_hire_num = list(orig_hire_num[hire_ind])
current_hire_num = orig_hire_num
boats = []

"""
for each time step generating hire boats to leave the hire companies
"""
new_boats = Boats.generate_boats(hire_ind, orig_hire_num)
boats_in_section = np.zeros(len(sections))
for boat in new_boats:
    current_hire_num[hire_ind.index(boat.current_section)] -=1
    boats_in_section[boat.current_section] += 1
    #print(boat.current_section)
#print(boats_in_section)
boats_in_section = np.transpose(np.array(boats_in_section))
boats_in_section = pandas.DataFrame(boats_in_section, index=sections)
ax =sb.heatmap(boats_in_section,cmap = "YlGnBu")
"""
need something in place which deleted boats once they've finished their trips and put them back into 
the current_hire_num variable 
"""
    



