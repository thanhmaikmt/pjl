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
from math import *

import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.lines as lines

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
startTime=time/60
print "STARTING ",startTime

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

endTime=time/60.0

print "END ",endTime
duration=(endTime-startTime)

print duration

if duration < 20.0:
    ticks=range(int(floor(startTime)),int(ceil(endTime)),1)
elif duration < 40.0:   
    ticks=range(2*int(floor(startTime/2.0)),2*int(ceil(endTime/2.0)),2)
else:
    raise NameError(" Please sort out tick intervals")

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

days=["mon","tue","wed","thu","fri","sat","sun"]

fig = pyplot.figure()
p=fig.add_subplot('111')

xaxis=p.xaxis
xaxis.set_major_formatter(ticker.FuncFormatter(my_date))
xaxis.set_ticks(ticks)
xaxis.limit_range_for_scale(ticks[0],ticks[len(ticks)-1])

styles=['k','k--','k:']

cnt=0
for case in cases:
    m=lines.Line2D.markers[cnt]
    cnt+=1
    p.plot(util.arrayMinToHours(case.times),util.arrayJoulesToKWH(case.charges),label=case.id) #,styles[cnt%3])
 


p.legend() #bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


p.set_ylabel("Charge (kWh)")
p.set_xlabel("Time (hours)")
p.set_title(" Car charge state ")
p.grid(True)
pyplot.show()