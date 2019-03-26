# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 18:28:17 2019

@author: laura
"""

"""
Could create boats as a class and when we get more types/categories to add, we 
can just make subcategories with the extra information. 
Parent class would need attributes:
    - speed (which could be overrided later)
    - decision which can be called with an input of the 'energy' needed to pass
    to the next section. So the method for the decision is the same but the 
    threshold for each boat is kept within each instance.
    - time to travel
    - time left to travel
    - direction travelling in
    - whether it's turned yet
    
Children class could be:
    - continuous cruisers (which overrides the time to travel and time left so 
    will tend to travel further)
    - goals/motivations of the crew
    - holiday makers
    - families etc
    
"""
import numpy as np

def generate_hire_boats(hire_loc, orig_hire_num):
    boat_list = []
    for i in range(len(hire_loc)):
        percent_hire_num = orig_hire_num[i]//20
        new = np.random.uniform(size=1)
        if new>0.5: #make this a value relating to the number of boats left in a marina
            new = 1
        else:
            new = 0
        for k in range(new):
            boat_list.append(create_hire_boat(hire_loc[i]))
    return boat_list
        
    
    

class create_hire_boat:
    
    def __init__(self, origin):
      self.speed = 1
      self.end_time = np.random.randint(1,32,size=None,dtype='int') # number of segments. Assume boats only go from 8am to 8pm max 
      self.current_time = 0 #how long been travellig for
      self.current_direction = 1
      self.start_direction = 1
      self.start_section = origin #need a way to randomly spawn boats from hire companies
      self.current_section = origin
      self.alive = True
      """
      generate route decisions for each boat?
      """
      
    def decision(self): #can make this decision process much more complicated
        self.current_time += 1
        self.current_section = self.current_section + self.current_direction
        if self.current_time > self.end_time//2:
            self.current_direction = self.start_direction*-1
        if self.current_section == self.start_section:
            self.alive = False
        """
        need to turn round if you reach the end of the canal
        """
            

          
            

        
            
        