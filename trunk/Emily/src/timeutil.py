'''
Created on 18 Jan 2011

@author: pjl
'''


minsPerHour=60.0
minsPerDay=minsPerHour*24.0
minsPerWeek=minsPerDay*7.0
secsPerHour=minsPerHour*60.0
secsPerMinute=60.0
   
dayToNumber={"MON":0,"TUE":1,"WED":2,"THU":3,"FRI":4,"SAT":5,"SUN":6}
 
 
def arrayMinToHours(x):
    h=[]
    for xx in x:
        h.append(xx/minsPerHour)

    return h


def toMins(day,hour,min):
        
        return float(min+minsPerHour*hour+minsPerDay*day)
    
def crackTime(str):
        
        toks=str.split(":")      
        return float(toks[0])*minsPerHour+float(toks[1])