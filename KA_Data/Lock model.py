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
lockage counter
lock_status - left hand side is 1 and right hand side is -1
(this is the same as the approaching directions of the boats)
"""
def lockage_count(lock_status,lockage,self):
    if lock_status[self.current_section] == self.direction:
        lockage[self.current_section] += 1/2
        lock_status[self.current_section] = self.direction*(-1)
    elif lock_status[self.current_section] != self.direction:
        lockage[self.current_section] += 1
        lock_status[self.current_section] = self.direction*(-1)
    return lockage,lock_status
        


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




















