'''
Created on 19 Jan 2011

@author: pjl
'''

from schedule import *
import util 


class Case:
    """
        Represents a number of users (all behave identically)
    """
    
    def __init__(self,user,number,supply):
        #number=1
        self.id=user.id+str(number)
        self.time=None
        self.user=user
        car=self.user.car
        self.tripIter=TripIterator(user.schedule) 
        self.capacity=car.capacity*number
        self.range=car.range
        self.chargeRate=car.chargeRate*number
        self.energyUse=0.0
        self.charge=0.0  # self.capacity
        self.times=[]
        self.charges=[]
        self.energyUses=[]
        self.supply=supply
        
        #self.stamp()

    def stamp(self):
        self.times.append(self.time)
        self.charges.append(self.charge)
        self.energyUses.append(self.energyUse)
        
      
    def step(self,time,period):
        """
        simulate time of period (minutes)
        """
        if self.time == None:
            self.time=time
            self.stamp()
            
        assert self.time == time
        self.tripIter.simulate(time,period,self)
        

    def doCharge(self,time):
    
        
        tinMins=(self.capacity-self.charge)/self.chargeRate/util.secsPerMinute
        
        tReq=min(time,tinMins)
    
        canCharge = self.supply.request(self.chargeRate,time,tReq)
        
        if canCharge:
            c=self.chargeRate*time*util.secsPerMinute
            c=min(c,self.capacity-self.charge)
            self.energyUse +=c
            self.charge += c
            self.supply.consume(self.chargeRate,time,tReq)
            
            if tReq < time:
                self.time += tReq        
                self.stamp()
                self.time += time-tReq
                self.stamp()
                return
            
            
        self.time += time    
        self.stamp()
       
            
                
        
    def doTravel(self,time,speed):
        
        if speed == None:
            self.charge=0
        else:
            drain = self.capacity*speed*time/self.user.car.range
            self.charge -= drain
            
        self.time+= time
        self.stamp()    
            
    
    def display(self):
        print "case",self.user.id,100.0*self.charge/self.capacity,"%"