<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 09:18:18 2019

A simple rating for each attraction by summing services at the given attraction. Outputs ratings list which corresponds to names_final list 

@author: sl15611
"""

import pandas

canal =  pandas.read_csv('KAservices postcodes.csv',engine='python')

names= canal['Name']
names = names.tolist()

types = canal['Service']
types = types.tolist()

postcodes = canal['Postcode']
postcodes = postcodes.tolist()

#begin with arbitrarily assigning weight to each attraction type, weights can be changed as we please
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

#remove repeats        
for i in range(len(names)):
    if (names[i] in names_final) != True or (postcodes[i] in postcodes_final) != True:
        names_final.append(names[i])
        postcodes_final.append(postcodes[i])

#initialize ratings
ratings = []
for i in range(len(names_final)):
    ratings.append(0)

#sums ratings    
for i in range(len(names_final)):
    for j in range(len(names)):
        if names[j] == names_final[i] and postcodes[j] == postcodes_final[i]:
            ratings[i] += attraction_types[types[j]]
            
=======
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 09:18:18 2019

A simple rating for each attraction by summing services at the given attraction. Outputs ratings list which corresponds to names_final list 

@author: sl15611
"""

import pandas

canal =  pandas.read_csv('KAservices postcodes.csv',engine='python')

names= canal['Name']
names = names.tolist()

types = canal['Service']
types = types.tolist()

postcodes = canal['Postcode']
postcodes = postcodes.tolist()

#begin with arbitrarily assigning weight to each attraction type, weights can be changed as we please
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

#remove repeats        
for i in range(len(names)):
    if (names[i] in names_final) != True or (postcodes[i] in postcodes_final) != True:
        names_final.append(names[i])
        postcodes_final.append(postcodes[i])

#initialize ratings
ratings = []
for i in range(len(names_final)):
    ratings.append(0)

#sums ratings    
for i in range(len(names_final)):
    for j in range(len(names)):
        if names[j] == names_final[i] and postcodes[j] == postcodes_final[i]:
            ratings[i] += attraction_types[types[j]]
            
>>>>>>> 7c0bbb5ffc5ba61d640b32f6106bd8eecf8349b1
print(ratings)