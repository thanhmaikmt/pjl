'''
Created on 18 Jan 2011

@author: pjl
'''


minsPerHour=60
minsPerDay=minsPerHour*24
minsPerWeek=minsPerDay*7
secsPerHour=minsPerHour*60
secsPerMinute=60
   
dayToNumber={"MON":0,"TUE":1,"WED":2,"THU":3,"FRI":4,"SAT":5,"SUN":6}
 
 
def arrayMinToHours(x):
    h=[]
    for xx in x:
        h.append(xx/minsPerHour)

    return h


def toMins(day,hour,min):
        return min+minsPerHour*hour+minsPerDay*day
    
def crackTime(str):
        toks=str.split(":")      
        return int(toks[0])*minsPerHour+int(toks[1])
    
    
def arrayJoulesToKWH(x):
    
    k=[]
    
    fact=1e-3/secsPerHour
    for xx in x:
        k.append(xx*fact)
        
    return k