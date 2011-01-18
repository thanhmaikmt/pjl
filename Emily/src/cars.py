'''
Created on 18 Jan 2011

@author: pjl
'''

from timeut import *

class Car:


    def __init__(self,id,batteryCapacity,rechargeTime,range):
        
        """
            batteryCapacity  kWh
            rechargeTime     h
            range            km
        """
        
        self.id=id
        self.capacity  = batteryCapacity*1000.0*Time.secsPerHour         # J   
        self.chargeRate= batteryCapacity/rechargeTime*Time.secsPerHour   # J/sec   
        self.eff       = 1000.0*range/batteryCapacity                    # meters/Joule
