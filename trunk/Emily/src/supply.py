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
        self.redundantCap.append(power*1e6)
        
        
        
    def setStuff(self,start,dt): 
        print "START DT",start,dt
        self.start=start
        self.dt=dt 