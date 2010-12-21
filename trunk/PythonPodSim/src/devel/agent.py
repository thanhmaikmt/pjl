'''
Created on 21 Dec 2010

@author: pjl
'''

#from plugableEvolver import *
import multiprocessing as mp
from copy import  *
from pods import *


class Agent(mp.Process):

    def __init__(self,plug,i):
       
        self.pod = plug.createInitialPod(i)
        self.world_end,self.pod_end=mp.Pipe()
        mp.Process.__init__ ( self,None,self.run )
         
    def stepInit(self):
         self.world_end.send("step")
         
    def waitForDone(self):
        self.pod.state=self.world_end.recv()
    
    def admin(self,sim):
        if sim.plug.admin(self.pod,sim):
            self.world_end.send(self.pod.state)
            
     
    #    
    # this is done on a separate thread
    #
    def run(self):
       
        while(True):
           
            cmd=self.pod_end.recv()
            if isinstance(cmd,State):
                self.pod.state=cmd
                continue
             
            #print cmd
            self.pod.step()       
            self.pod.update_sensors()
            #state=State(self)
            self.pod_end.send(deepcopy(self.pod.state))   