'''
Created on 14 Jan 2011

@author: pjl
'''


#from supply import *
#from cars import *
from io import *
from schedule import *
import timeutil
from case import *
from io import *
from   matplotlib.pyplot import *


dir="../data/test1/"
supFile=dir+"REDCAPhiDay.txt"  

carFile=dir+"CAR.txt"
tripFile=dir+"TRIPSCHEDULE.txt"
userFile=dir+"USERS.txt"
scenarioFile=dir+"SCENARIO.txt"

supply=readSupply(supFile)
cars=readCars(carFile)
trips=readTripSchedules(tripFile)
users=readUsers(userFile,cars,trips)
cases=readScenario(scenarioFile,users)


time=supply.start

drainTot=0
capTot=0


print " CASES: "
for case in cases:
    case.display()


t=[]
deltaT=supply.interval

print "STARTING ",time/60
while True:
    
    print time/60
    
    rc=supply.redundantCapacityAt(time,deltaT)
    if rc == None:
        break
    
    t.append(time)
    
    for case in cases:
        case.step(time,deltaT)
        #case.display()
        
    time += deltaT
    
    

print "END ",time/60

for case in cases:
    plot(timeutil.arrayMinToHours(case.times),case.charges,label=case.id)
    
show()