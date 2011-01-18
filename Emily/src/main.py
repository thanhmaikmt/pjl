'''
Created on 14 Jan 2011

@author: pjl
'''


#from supply import *
#from cars import *
from io import *
#from tripschedule import *

 
      


class Case:
    """
        Represents a number of users (all behave identically)
    """
    
    def __init__(self,user,number):
        self.time=0
        car=user.car
        self.trips=user.trips
        self.iter=self.trip.__iter__()
        self.trip=self.iter.next()
        self.tripNext=self.iter.next()
        
        self.capacity=car.capacity*number
        self.eff=car.eff*number
        self.chargeRate=car.chargeRate*number
        self.charge=self.capacity
          
    def step(self,period):
        """
        simulate time of period (minutes)
        """
        
        timeNext=self.time+period
        
        while self.trip.end < time:
            self.trip=self.tripNext
            self.tripNext=self.iter.next()
    
        # calculate energy drain from supply
        drain=self.chargeRate*period*Time.secsPerMinute
        drain=min(drain,self.capacity-self.charge)

        self.charge +=drain-dist*self.eff
    
        self.time = timeNext
        
        return drain  
  


from io import *


dir="/home/pjl/eclpseProjects/Emily/data/test1/"
supFile=dir+"2007_DAY_DATE_HALFHR_GBDEMAND_REDCAP.txt"  
carFile=dir+"CAR.txt"
tripFile=dir+"TRIPSCHEDULE.txt"
userFile=dir+"USERS.txt"
scenarioFile=dir+"SCENARIO.txt"

supply=readSupply(supFile)
cars=readCars(carFile)
trips=readTripSchedules(tripFile)
users=readUsers(userFile,cars,trips)
cases=readScenario(scenarioFile,users)

agents=[]

for case in cases:
    agents.append(case) 

time=0
period=30

while True:
    
    slot=int(supply.interval/time)
    
    if slot >= len(supply.redudantCap):
        break
    
    for case in cases:
        drain=case.step(period)
        supply.redudantCap[slot] -= drain
        
    time += dt
    
    
