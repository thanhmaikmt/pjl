'''
Created on 18 Jan 2011

@author: pjl
'''

from supply import *
from cars import *
from tripschedule import *
from users import *

def seek(fin,key):
    n=len(key)
    while  True:
        line=fin.readline()
        if line[0:n] == key:
            return line
        
def readSupply(file):
    fin=open(file)
    title=fin.readline()
    
    sup=PowerSupply(title)

    print "Hello Emily",title
    
    headers=seek(fin,"DAY")
    print headers
    
    start=None
    dt=30.0
    
    while True:
        line=fin.readline()
        toks=line.split("\t")
#        print toks
        if len(toks) == 0 or toks[0]=="":
            break
        sup.add(float(toks[4]))
        if start==None:
            start=(float(toks[2])-1.0)*30.0
    
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
            cap=float(toks[1])
            rechargetime=float(toks[2])
            range=float(toks[3])
            cars[name]=Car(name,cap,rechargetime,range)
            
    return cars
   

def readTripSchedules(fin):
    
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
        fin.readline()
        
      
        print name
    
        while True:
            line=fin.readline()
            toks=line.split("\t")
            if len(toks) <= 1 or toks[0]=="":
                break
            name=toks[0]
            start=float(toks[1])
            stop=float(toks[2])
            if len(toks) == 3:
                dist=None
            else:
                dist=float(toks[3])
                     
            trips[name]=TripSchedule(name,start,stop,dist)
            
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
            toks=line.split("\t")
            if len(toks) != 3:
                break
            name=toks[0]
            car=cars[toks[1]]
            trip=trips[toks[2]]
            users[name]=User(name,car,trip)
            
    return users


def readScenario(file,users):
    
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
            cases.append((user,number))
            
    return cases
   
