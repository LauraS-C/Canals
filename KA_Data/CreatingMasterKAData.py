import pandas
import numpy as np

def Getkm(SAP_FUNC_LOC):
    Loc = []
    for i in range(len(SAP_FUNC_LOC)):
        string = SAP_FUNC_LOC[i]
        string = int(string[3:6])
        Loc.append(string)
    return Loc
      
def MakeLocList(file):
    List = np.zeros(len(Section))
    Data = pandas.read_csv(file,engine='python')
    Loc = Data["SAP_FUNC_LOC"]
    Loc = Getkm(Loc)
    for i in range(len(Loc)):
        ind = Section.index(Loc[i])
        List[ind] = List[ind]+1
    return List

Section = []

#input Lock data from the csv file and put in list
LockData = pandas.read_csv('Locks.csv',engine='python')
LockLoc = LockData["SAP_FUNC_LOC"]
LockName = LockData["SAP_DESCRIPTION"]
#LockX = LockData["X"]
#LockY = LockData["Y"]
NumLocks = len(LockLoc)
#X = np.zeros(140)
#Y = np.zeros(140)

#make list of each section
for i in range(140):
    Section.append(i)

#add locks as section
km = Getkm(LockLoc)
for i in range(NumLocks):
    ind = Section.index(km[i])
    Section.insert(ind+1,LockName[i])
    #X.insert(ind+1,X[i])
    #Y.insert(ind+1,Y[i])
    
Bridges = MakeLocList('Bridges_Public.csv')
Aqueducts = MakeLocList('Aqueducts_Public.csv')
Pumps = MakeLocList('Pumping_Stations.csv')
TurnPoints = MakeLocList('Winding_Holes.csv')
Tunnels = MakeLocList('Tunnels_Public.csv')

df = pandas.DataFrame(data={"Section": Section, "Bridges": Bridges, "Aqueducts": Aqueducts, "Pumps":Pumps, "Turning Points":TurnPoints,"Tunnels":Tunnels})
df.to_csv("All_KA_Data.csv", sep=',',index=False)

    

 
