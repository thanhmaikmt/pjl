'''
Created on 18 Jan 2011

@author: pjl
'''


import util 

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
            self.speed=range/(tend-tstart)
        else:
            self.speed=None

class TripIterator:
    
    
    def __init__(self,sched):    
        self.trips=sched.trips
        assert len(self.trips)>0
        self.length=sched.length
        #' periods must be homogenious usage
        self.allowOverLap=False   
        
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
        

        while tstart >= trips[ptr].tend: 
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
            print "REQUESTED start,stop" ,tstart,tend
            print "DEFINED",trip.tstart,trip.tend
            print "------------------------"

        if  tstart < trip.tstart:
            
            if tend <= trip.tstart:
                case.doCharge(period)
            
            elif tend <= trip.tend:
                print tend,trip.tend
                assert self.allowOverLap 
                case.doCharge(trip.tstart-tstart)
                case.doTravel(tend-trip.tstart,trip.speed)
            
            else:
                raise NameError(" step is greater than a journey ")
            
        else:
            assert tend > trip.tstart
            
            # print tstart-trip.tend
            
            if tend <= trip.tend:
                case.doTravel(period,trip.speed)
                
            else:
                print tend-trip.tend,trip.tend-tstart
                assert self.allowOverLap 
                case.doTravel(trip.tend-tstart,trip.speed)
                case.doCharge(tend-trip.tend)
            
        
        return
    
          
            


    
if __name__ == "__main__":
    
    class MyCase:
        
        def __init__(self):
            self.ct=0
            self.tt=0
            self.dist=0
            
        def doCharge(self,dt):
            self.ct+=dt
            
        def doTravel(self,dt,speed):
            self.tt+=dt
            self.dist+=dt*speed
    
    def test(dt):
        length=util.minsPerWeek
        
        trips=Schedule("trips",length)
        
        for i in range(1):
            start=util.toMins(i,8,30)
            end=util.toMins(i,17,30)
            trips.append(start,end,40.0)
      
        
        mycase=MyCase()
        
        iter=TripIterator(trips)
        
        t=0
        tend=t+length
        
        while t < tend:
            iter.simulate(t,dt,mycase)        
            t      += dt
            
            
        return mycase.tt,mycase.ct,mycase.dist,t

    dts=[1,5,10,15,30]
    
    for dt in dts:
        print test(dt)