'''
Created on 18 Jan 2011

@author: pjl
'''


import  util 

class Supply:
   
    def __init__(self,id):
        self.id=id
        self.redundantCap=[]
        self.energyConsumed=0.0
        self.time=0
        self.clients=[]
        
    def add(self,power):
        self.redundantCap.append(power)
        
    def speak(self):
        pass
    
    def resolved(self):
        return True
     
    def redundantCapacityAt(self,time,deltaT):
        slot=int((time-self.start)/self.interval)
        # TODO smearing
        if slot >= len(self.redundantCap):
            return None
        else:
            return self.redundantCap[slot]
         
    def setStuff(self,startTime,interval):
         
        print "START DT",startTime,interval
        self.startTime=startTime
        self.time=startTime
        self.interval=interval
        
        self.totalRedundantEnergy=0
        
        self.endTime=self.startTime
        for p in self.redundantCap:
            self.endTime+=interval
            self.totalRedundantEnergy += p*interval*util.secsPerMinute
        
        
    def request(self,power,period):
        return True
    
    
    def consume(self,power,period):
        pass
    
    def addClient(self,client):
        self.clients.append(client)
        
    def step(self,deltaT):
        for client in self.clients:
                client.step(deltaT)
        
        self.time+=deltaT