'''
Created on 18 Jan 2011

@author: pjl
'''


from timeutil import *
from actions import *

class Schedule: 
    """
        List of trips
    """
    def __init__(self,id,length):
        self.id=id
        self.trips=[]
        self.length=length     #   

    def append(self,start,stop,distance):
        
        if len(self.trips) > 0:
            assert start > self.trips[len(self.trips)-1].tend
            assert stop > start
        
        self.trips.append(Trip(start,stop,distance))

class Trip:
    
    
    def __init__(self,tstart,tend,range):
        self.tstart=tstart
        self.tend=tend
        self.range=range
        if range != None:
            self.speed=range/(tstart-tend)
        else:
            self.speed=None

class TripIterator:
    
    
    def __init__(self,sched):    
        self.trips=sched.trips
        assert len(self.trips)>0
        self.length=sched.length
        
    def simulate(self,time,period,case):
        """
        time start of period (mins)
        period length of period (mins)
        
        returns  distance (meters) ,    time_avaible_for_charging (mins)   
        
        """
        #print time,period    
        t=0.0
        ptr=0
        
        tstart = time % self.length

        trips=self.trips
        

        while tstart > trips[ptr].tend: 
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
        
        if  tstart < trip.tstart:
            if tend < trip.tstart:
                case.doCharge(period)
            
            elif tend < trip.tend:
                case.doCharge(trip.tstart-tstart)
                case.doTravel(tend-trip.tstart,trip.speed)
            
            else:
                raise NameError(" step is greater than a journey ")
            
        else:
            assert tend > trip.tstart
            
            if tend <= trip.tend:
                case.doTravel(period,trip.speed)
            else:
                case.doTravel(trip.tend-tstart,trip.speed)
                case.doCharge(tend-trip.tend)
            
        
        return
    
        
        """
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
            
        
        if trip[2] == None:
            if abs(period-chargePeriod) < 0.1:
                return 0,chargePeriod
            else:
                return None,chargePeriod
        
        
        return trip[2]*(period-chargePeriod)/(trip[1]-trip[0]),chargePeriod
        """    
            

class MyCase:
    
    def __init__(self):
        self.ct=0
        self.tt=0
        
    def doCharge(self,dt):
        self.ct+=dt
        
    def doTravel(self,dt):
        self.tt+=dt
        

def test(dt):
    length=timeutil.minsPerWeek
    
    trips=Schedule("trips",length)
    
    for i in range(1):
        start=toMins(i,8,30)
        end=toMins(i,17,30)
        trips.append(start,end,40.0)
  
    
    mycase=MyCase()
    
    iter=TripIterator(trips)
    
    t=0
    tend=t+length
    
    while t < tend:
        iter.simulate(t,dt,mycase)        
        t      += dt
        
        
    return mycase.tt,mycase.ct,t

    
if __name__ == "__main__":
    
    
    dts=[5,10,20,30,40,60,90,120]
    
    for dt in dts:
        print test(dt)