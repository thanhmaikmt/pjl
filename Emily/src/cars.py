'''
Created on 18 Jan 2011

@author: pjl
'''

class Car:

    def __init__(self,id,batteryCapacity,rechargeTime,range):
        self.id=id
        self.capacity=batteryCapacity
        self.chargeRate=batteryCapacity/rechargeTime
        self.eff=range/batteryCapacity
