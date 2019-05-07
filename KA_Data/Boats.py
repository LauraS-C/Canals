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
import random

def generate_hire_boats(time,hire_loc, orig_hire_num,day,day_length,current_hire_num,boat_type):
    boat_list = []
    for i in range(len(hire_loc)):
        if current_hire_num[i] >0:
            new = np.random.uniform(size=1)
            if new>0.1: #can edit this value so if 10, 90% of boats go out
                new = 1
            else:
                new = 0
            for k in range(new):
                boat_list.append(boat_type(time,hire_loc[i],day,day_length))
    for boat in boat_list:
        current_hire_num[hire_loc.index(boat.current_section)] -=1
    return boat_list
        
    
    

class create_boat:
    
    def __init__(self, time,origin,day,day_length):
        trip_length = np.random.randint(0,1,size=None,dtype='int')
        if trip_length == 0:
            self.end_time = 7*day_length
        elif trip_length == 1 and day == 1:
            self.end_time = 4*day_length
        else:
            self.end_time = 3*day_length
        
        self.current_time = 0 #how long been travellig for
        ind = np.random.randint(0,1,size=None,dtype='int')
        direction = [-1,1]
        self.start_direction = direction[ind]
        self.current_direction = direction[ind]      
        self.start_section = origin #need a way to randomly spawn boats from hire companies
        self.current_section = origin
        self.alive = True
        self.turned = False
        self.stop_time = 0
        
        """
        generate route decisions for each boat
        """      
    def decision(self, turningfor,turningback,winding_hole,canal_length): #can make this decision process much more complicated
        self.current_time += 1     
        if self.current_section<len(winding_hole)-1 and self.current_section>0:
            self.current_section = self.current_section + self.current_direction
        #else:
         #   print('Out of range')
        
        if self.current_direction == 1:
            turning = turningfor
        else:
            turning = turningback
            
        if self.current_section==2 or self.current_section==canal_length:
            self.current_direction = self.start_direction*-1
            self.start_direction = self.current_direction
            self.turned = True    
        #if self.current_time + turning[self.current_section] > self.end_time//2 and winding_hole[self.current_section] == 1 and self.turned==False:
        #print(self.current_section)
        if self.turned==False and winding_hole[self.current_section] == 1:
            if self.current_time + turning[self.current_section] > self.end_time//2:
                self.current_direction = self.start_direction*-1
                self.start_direction = self.current_direction
                self.turned = True
        if self.current_section == self.start_section:
            self.alive = False
        
        
        
        """
        need to turn round if you reach the end of the canal
    
        """
        
class day_boat(create_boat):
    
    def __init__(self, time,origin,day,day_length):
        create_boat.__init__(self, time,origin,day,day_length)
        self.end_time = day_length - time
        
        
    def decision(self, turningfor,turningback,winding_hole,canal_length):
        create_boat.decision(self,turningfor,turningback,winding_hole,canal_length)
        """
        should use exactly the same decision process as the first hire_boat
        """
        
class cont_cruiser(create_boat):
    
    def __init__(self,day_length,canal_length):
        trip_length = np.random.randint(1,5,size=None,dtype='int')
        self.end_time = day_length*trip_length
        self.start_section = np.random.randint(0,canal_length,size=None,dtype='int')
        self.alive = True
        self.current_direction = 0
        self.current_section = self.start_section
        self.current_time = 0
        self.start_direction = 0
        self.stop_time = 0
        self.turned = False

    def decision(self, turningfor,turningback,winding_hole,canal_length): #can make this decision process much more complicated
        self.current_time += 1     
        if self.current_time == self.end_time:
            self.alive = False
        """
        surely they could be generated from random places?
        would just travel for a day or two in one direction and then moor for 
        a few weeks again at which point they can be deleted.
        Random chance of stopping and getting deleted?
        """
    
class private_moored(create_boat):
    
    def __init__(self,time,origin,day,day_length):
        create_boat.__init__(self, time,origin,day,day_length)
        trip_length = np.random.randint(1,14,size = None,dtype='int')
        self.end_time = trip_length*day_length
        
    def decision(self, turningfor,turningback,winding_hole,canal_length):
        create_boat.decision(self,turningfor,turningback,winding_hole,canal_length)
        """
        they are basically the same as hire boats and would be generated from the
        same places with the same schedule and priority but with different journey
        generation times and end times.
        Do we need a different class or could we just increase the number of
        hire boats generated?
        """
    
class end_boat(create_boat):
    
    def __init__(self, canal_length):
        
        start = np.random.randint(0,1,size=None,dtype='int')
        if start == 1:
            self.start_section = canal_length
            self.current_section = canal_length
            self.start_direction = -1
            self.current_direction = -1
        else:
            self.start_section = 0
            self.current_section = 0
            self.start_direction = 1
            self.current_direction = 1
        self.alive = True
        self.turned = False
        self.end_time = 5
        self.current_time = 0
        self.stop_time = 0
        
    def decision(self, turningfor,turningback,winding_hole,canal_length): #can make this decision process much more complicated
        self.current_time += 1        
        self.current_section = self.current_section + self.current_direction
        
        turn = np.random.uniform(size=1)
        if turn>0.8 and self.turned == False and winding_hole[self.current_section]==1:
            #turn by random chance, if haven't turned before and there is a winding hole
            self.current_direction = self.start_direction*-1
            self.start_direction = self.current_direction
            self.turned = True
        if self.current_section == 0 or canal_length:
            self.alive = False
        """
        just have the same stopping habits, maybe a random turning point or no 
        turning point and then just delete the boat when it makes it's way out 
        the other end of the system
        """
