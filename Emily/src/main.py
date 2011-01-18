'''
Created on 14 Jan 2011

@author: pjl
'''
class Car:

    def __init__(self,id,batteryCapacity,rechargeTime,range):
        self.id=id
        self.capacity=batteryCapacity
        self.chargeRate=batteryCapacity/rechargeTime
        self.eff=range/batteryCapacity



class TripSchedule: 
    
    def __init__(self,id):
        self.id=id
        self.trips=[]

    def append(self,start,stop,distance):
        self.trip.append((start,stop,distance))
        


class PowerSupply:
   
    def __init__(self,id):
        self.id
        self.redundantCapOrig=[]
        self.reduadantCap=[]
        
    def add(self,power):
        self.redundantCap.append(power)
        self.redundantCapOrig.append(power)
        
class User:
    
    def __init__(self,id,car,trip):
        self.id=id
        self.car=car
        self.trip=trip
        

class Sink:
    pass

class MultiCar(Sink):
    
    def __init__(self,user,car,trip,number):
        self.capacity=car.capacity*number
        self.eff=car.eff*number
        self.chargeRate=car.chargeRate*number
        self.charge=self.capacity
          
    def step(self,chargeDT,dist):
        drain=self.chargeRate*chargeDT
        drain=min(drain,self.capacity-self.charge)
        self.charge +=drain-dist*self.eff
        return drain  
  

class Agent:
    
    def __init__(self,car,usage):
        self.car=car
        self.usage=usage
        
    def step(self,slot):
        usage=self.usage(slot)
        drain=self.car.charge(usage.chargeDT,usage.dist)
        return drain
        
def readSupply(file):
    # read id
    sup=PowerSupply(id)
    # read avails
    return sup

def readAgents(file):
    agents=[]
    return 

def readUsers(file):
    users=[]
    return users 

def readCars(file):
    cars={}
    return cars
    
supply=readSupply()
agents=readAgents()
users=readUsers()
cars=readCars()

for slot in range(len(supply.redundantCap)):
    for agent in agents:
        drain=agent.step(slot)
        supply.redudantCap[slot] -= drain
    
    
    
