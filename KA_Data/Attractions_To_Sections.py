# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 22:41:32 2019

@author: sl15611

assigning attractions along K&A canal to modelled sections
"""

import pandas
import numpy as np
from scipy.spatial import distance

canal = pandas.read_csv('All_KA_Data.csv',engine='python')
attraction_data =  pandas.read_csv('KAServices postcodes.csv',engine='python')

sections_and_locks_series = canal['Section']
sections_and_locks = sections_and_locks_series.tolist()

latitude_series = canal['Latitude']
latitude_incl_locks = latitude_series.tolist()

longitude_series = canal['Longitude']
longitude_incl_locks = longitude_series.tolist()

section_coordinates = [sections_and_locks,latitude_incl_locks,longitude_incl_locks] #bringing it together

for i in section_coordinates: #delete 1st row
    del i[0]
    
sections = []
index = []

#excluding locks from sections list
for i in range(len(sections_and_locks)):
    s = sections_and_locks[i]
    if s.isdigit():
        section = int(s)
        sections.append(section)
        index.append(i)
        
latitude = []
longitude = []    
for num in index:
    latitude.append(latitude_incl_locks[num])
    longitude.append(longitude_incl_locks[num])

#making sure longitude is list of floats
for i in range(len(longitude)):
    flo = float(longitude[i])
    longitude[i] = flo

attractions_name = attraction_data['Name']
attractions_name = attractions_name.tolist()

attractions_long = attraction_data['ukpostcodes.longitude']
attractions_long = attractions_long.tolist()

attractions_lat = attraction_data['ukpostcodes.latitude']
attractions_lat = attractions_lat.tolist()

attractions = [attractions_name,attractions_lat,attractions_long]

def assign(attraction):
    distances = []
    for i in range(len(sections)):
        point1 = (attraction[1],attraction[2])
        point2 = (latitude[i],longitude[i])
        dist = distance.euclidean(point1, point2)
        distances.append(dist)
    min_dist = min(distances)
    min_index = distances.index(min(distances))
    print(attraction[0],"is",min_dist*111,"km from Section",sections[min_index])
    return sections[min_index]

for i in range(len(attractions_name)):
    assignments = assign([attractions[0][i],attractions[1][i],attractions[2][i]])