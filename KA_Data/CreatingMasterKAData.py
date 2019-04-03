"""
Created Tuesday 12th March 2019
Author: Laura Stock-Caldwell

Input: filenames to parse data from - must contain field 'SAP_FUNC_LOC'
Output: file 'All_KA_Data.csv' which contains the KA canal split into 1km 
        sections with locations of locks and any other features specified by 
        input files.
        
"""

import pandas
import numpy as np

global Longitude
global Latitude
global ItemCount

"""
extracts kms along the canal from the SAP_FUNC_LOC
"""
def Getkm(SAP_FUNC_LOC):
    Loc = []
    for i in range(len(SAP_FUNC_LOC)):
        string = SAP_FUNC_LOC[i]
        string = int(string[3:6])
        Loc.append(string)
    return Loc
      
"""
extract location data from files
"""
def MakeLocList(file):
    List = np.zeros(len(Section))
    Data = pandas.read_csv(file,engine='python',encoding="utf-8-sig")
    Loc = Data["SAP_FUNC_LOC"]
    try:
        Long = Data["X"]
        Lat = Data["Y"]
    except:
        pass
    Loc = Getkm(Loc)
    for i in range(len(Loc)):
        ind = Section.index(Loc[i])
        List[ind] = List[ind]+1
        try:
            Longitude[ind] += Long[i]
            Latitude[ind] += Lat[i]
            ItemCount[ind] += 1
        except:
            pass
    return List



Section = []


"""
input Lock data from the csv file and put in list
"""
LockData = pandas.read_csv('Locks.csv',engine='python',encoding="utf-8-sig")
LockLoc = LockData["SAP_FUNC_LOC"]
LockName = LockData["SAP_DESCRIPTION"]
LockLong = LockData["Long"]
LockLat = LockData["Lat"]
NumLocks = len(LockLoc)

"""
make list of each section
"""
for i in range(140):
    Section.append(i)

"""
add locks as section
"""
km = Getkm(LockLoc)
for i in range(NumLocks):
    ind = Section.index(km[i])
    Section.insert(ind+1,LockName[i])
    #Longitude[ind] += LockLong[i]
    #Latitude[ind] += LockLat[i]
    
NumSections = len(Section)
Longitude = np.zeros(NumSections)
Latitude = np.zeros(NumSections)
ItemCount = np.zeros(NumSections)
""" 
Feature files 
"""
Features = {'Section': Section,
            'Bridges': 'Bridges_Public.csv',
            'Aqueducts': 'Aqueducts_Public.csv',
            'Pumps':'Pumping_Stations.csv',
            'Turning Points':'Winding_Holes.csv',
            'Tunnels':'Tunnels_Public.csv'}

for i in Features:
    if i == "Section":
        continue
    else:
        print(Features[i])
        Features[i]= MakeLocList(Features[i])
        
for i in range(NumSections):
    Latitude[i] = Latitude[i]/ItemCount[i]
    Longitude[i] = Longitude[i]/ItemCount[i]
    
Features['Latitude'] = Latitude
Features['Longitude'] = Longitude
print(Features)
    
"""
write all data to csv file
"""
df = pandas.DataFrame(Features)
df.to_csv("All_KA_Data_New.csv", sep=',',index=False)

    

 
