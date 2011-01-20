'''
Created on 18 Jan 2011

@author: pjl
'''

from supply import *
from cars import *
from schedule import *
from users import *
from case import *

import util 

def seek(fin,key):
    n=len(key)
    while  True:
        line=fin.readline()
        if len(line) == 0:
            return None
        
        if line[0:n] == key:
            return line
        
def readSupply(file):
    fin=open(file)
    title=fin.readline()
    
    sup=PowerSupply(title)

    #print "Hello Emily",title
    
    headers=seek(fin,"DAY")
    #print headers
    
    start=None
    dt=30.0
    
    while True:
        line=fin.readline()
        toks=line.split("\t")
#        print toks
        if len(toks) == 0 or toks[0]=="":
            break
        
        sup.add(float(toks[4])*1e6)    # convert to watts
        
        if start==None:
            start=(float(toks[2])-1.0)*30.0
    
    assert start != None
    # read avails
    
    sup.setStuff(start, dt)
    
    return sup


def readCars(file):
    
    cars={}
    fin=open(file)
    title=fin.readline()
    
    print title
    
    while True:
        headers=seek(fin,"CAR")
        if headers == None:
            break
        
        print headers
    
        while True:
            line=fin.readline()
            toks=line.split("\t")
            if len(toks) != 4:
                break
            name=toks[0]
            cap=float(toks[1])*1000.0*util.secsPerHour     # kWh t-> Joules
            rechargetime=float(toks[2])*util.secsPerHour   # hours->secs               #
            range=float(toks[3])*1e3                  # km --> meters                      
            cars[name]=Car(name,cap,rechargetime,range)
            
    return cars
   

def readTripSchedules(file):
    
    trips={}  
    fin=open(file)
    title=fin.readline()
    
    print title
    
    while True:
        headers=seek(fin,"TRIP ID")
        if headers == None:
            break
        
        toks=headers.split("\t")
        name=toks[1]
        
        period=float(toks[2])*util.minsPerDay
        
        fin.readline()
        
      
        print name
        
        trips[name]=Schedule(name,period)
    
        while True:
            line=fin.readline()
            toks=line.split("\t")
            if len(toks) <= 1 or toks[0]=="":
                break
            
            dayMins=util.dayToNumber[toks[0]]*util.minsPerDay
            
            start=util.crackTime(toks[1])+dayMins
            stop=util.crackTime(toks[2])+dayMins
            
            print toks
            
            if toks[3] == '\n':
                dist=None
            else:
                dist=float(toks[3])
                     
            trips[name].append(start,stop,dist)
            
    return trips


def readUsers(file,cars,trips):
    
    users={}
    fin=open(file)
    title=fin.readline()
    
    print title
    
   
    headers=seek(fin,"USER ID")
    print headers
    
    while True:
            line=fin.readline()
            line=line.rstrip()
            toks=line.split("\t")
            if len(toks) != 3:
                break
            name=toks[0]
            car=cars[toks[1]]
            trip=trips[toks[2]]
            users[name]=User(name,car,trip)
            
    return users


def readScenario(file,users,supply):
    
    cases=[]
    fin=open(file)
    title=fin.readline()
    
    print title
    
   
    headers=seek(fin,"USER ID")
    print headers
    
    while True:
            line=fin.readline()
            toks=line.split("\t")
            if len(toks) != 2:
                break
            user=users[toks[0]]
            number=int(toks[1])
            cases.append(Case(user,number,supply))
            
    return cases
   
