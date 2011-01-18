'''
Created on 18 Jan 2011

@author: pjl
'''


class Time:
    minsPerHour=60.0
    minsPerDay=minsPerHour*24.0
    minsPerWeek=minsPerDay*7.0
    secsPerHour=minsPerHour*60.0
   

 
def toMins(day,hour,min):
        
        return float(min+Time.minsPerHour*hour+Time.minsPerDay*day)