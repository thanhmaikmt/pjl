'''
Created on 14 Jan 2011

@author: pjl
'''


#from supply import *
#from cars import *
from io import *
from schedule import *
import util
from case import *
from io import *

import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker

dir="../data/test2/"
supFile=dir+"REDCAPhiDay.txt"  

carFile=dir+"CAR.txt"
tripFile=dir+"TRIPSCHEDULE.txt"
userFile=dir+"USERS.txt"
scenarioFile=dir+"SCENARIO.txt"

supply=readSupply(supFile)
cars=readCars(carFile)
trips=readTripSchedules(tripFile)
users=readUsers(userFile,cars,trips)
cases=readScenario(scenarioFile,users,supply)


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
        
    rc=supply.redundantCapacityAt(time,deltaT)
    if rc == None:
        break
    
    t.append(time)

    for case in cases:
        case.step(time,deltaT)
        #case.display()
        
    time += deltaT
    

## COSMETIC STUFF    
print "END ",time/60.0

lastDay=-1

def my_date(x,pos=None):
    day=int(x/24)
    hr=x-day*24   
    strH=" %d" % hr
    global lastDay
    if day != lastDay:
        lastDay=day
        return days[day]+strH
    else:
        return strH

for case in cases:
    pyplot.plot(util.arrayMinToHours(case.times),util.arrayJoulesToKWH(case.charges),label=case.id)



days=["mon","tue","wed","thu","fri","sat","sun"]

xaxis=pyplot.axes().xaxis
xaxis.set_major_formatter(ticker.FuncFormatter(my_date))
pyplot.ylabel("Charge (kWh)")
pyplot.xlabel("Time (hours)")
pyplot.title(" Car charge state ")
pyplot.grid(True)
pyplot.show()