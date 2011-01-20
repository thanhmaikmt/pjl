'''
Created on 18 Jan 2011

@author: pjl
'''

class Car:


    def __init__(self,id,batteryCapacity,rechargeTime,range):
        
        """
            batteryCapacity  kWh
            rechargeTime     h
            range            km
        """
        
        self.id=id
        self.capacity  = batteryCapacity                # J   
        self.chargeRate= batteryCapacity/rechargeTime   # J/sec   
        self.range     = range                          # meters
