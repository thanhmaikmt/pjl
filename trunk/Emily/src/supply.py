'''
Created on 18 Jan 2011

@author: pjl
'''



class PowerSupply:
   
    def __init__(self,id):
        self.id=id
        self.redundantCap=[]
       
     
    def add(self,power):
        
        """
            power (MW)
        """
        self.redundantCap.append(power)
        
        
    def redundantCapacityAt(self,time,deltaT):
        slot=int((time-self.start)/self.interval)
        # TODO smearing
        if slot >= len(self.redundantCap):
            return None
        else:
            return self.redundantCap[slot]
         
    def setStuff(self,start,interval): 
        print "START DT",start,interval
        self.start=start
        self.interval=interval
        
        
    def request(self,power,time,period):
        return True
    
    
    def consume(self,power,time,period):
        pass