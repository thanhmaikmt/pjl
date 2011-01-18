'''
Created on 18 Jan 2011

@author: pjl
'''


class Time:
    minsPerHour=60
    minsPerDay=minsPerHour*24
    minsPerWeek=minsPerDay*7
    
   

 
def toMins(day,hour,min):
        
        return float(min+Time.minsPerHour*hour+Time.minsPerDay*day)