'''
Created on 18 Jan 2011

@author: pjl
'''


from timeutil import *


class Schedule: 
    """
        List of trips
    """
    def __init__(self,id,length):
        self.id=id
        self.trips=[]
        self.length=length

    def append(self,start,stop,distance):
        self.trips.append((start,stop,distance))



class TripIterator:
    
    
    def __init__(self,sched):    
        self.trips=sched.trips
        self.length=sched.length
        
    def getPeriod(self,time,period):

        #print time,period    
        t=0.0
        ptr=0
        
        tstart = time % self.length

        trips=self.trips
        

        while tstart > trips[ptr][1]: 
          #  print ptr,tstart,trips[ptr][1]
            ptr += 1
            if ptr >= len(trips):
                tstart -= self.length
                ptr=0
        
        tend = tstart + period
            
        #print tstart,tend
          
        trip=trips[ptr]
    
        
        # here then trip[1] > time
        
        if False:
            print "------------------------"
            print tstart,tend
            print trip[0],trip[1]
        
        # tstart < trip[1]
        
        if tend > trip[1]:  # step  ends after travel 
            
            if tstart < trip[0]:  # all travel
                
                print "trip is shorter than time step"

            elif tstart > trip[1]:   
                             
                print "BUGGY POOHS"
                
            elif tstart < trip[0]:   # all travel in step
     
             
                chargePeriod = trip[0]-tstart + tend-trip[1]
             
            else:
                                          
                chargePeriod=tend-trip[1]
             
        elif tend > trip[0]:   # travel finishes during interval
     
                if tstart < trip[0]:
                    chargePeriod=trip[0]-tstart
                
                else: # all travel
        
                    chargePeriod=0
                    
             
        else:    # step finishes before travel
            
            chargePeriod=period
            
            
        return trip[2]*(period-chargePeriod)/(trip[1]-trip[0]),chargePeriod
            
            
        

def test(dt):
    length=Time.minsPerWeek
    trips=Schedule("trips",length)
    
    for i in range(1):
        start=toMins(i,8,30)
        end=toMins(i,17,30)
        trips.append(start,end,40.0)
        
    
    dist=0
    charge=0
    
    
    iter=TripIterator(trips)
    
    t=0
    tend=t+length
    
    while t < tend:
        d,c= iter.getPeriod(t,dt)
        #print d,c
        dist   += d
        charge += c    
        t      += dt
        
        
    return dist,charge,t

    
if __name__ == "__main__":
    
    
    dts=[5,10,20,30,40,60,90,120]
    
    
    for dt in dts:
        print test(dt)