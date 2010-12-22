'''
Created on 21 Dec 2010

@author: pjl
'''

#from plugableEvolver import *
import multiprocessing as mp
from copy import  *
from pods import *

MP=True

class Seed:pass

class Agent(mp.Process):
   
    def __init__(self,pod):

        self.seed=Seed()
        self.pod=pod
        self.world_end,self.pod_end=mp.Pipe()
        mp.Process.__init__ ( self,None,self.run )
         
    def stepInit(self):
        if not MP:
            self.clientStep()
        else:   
            self.world_end.send("step")
         
    def waitForDone(self):
        if MP:
            self.pod.state=self.world_end.recv()
    
    
    def admin(self,sim):
        reap=sim.plug.reaper(self.pod,sim)
        if reap and MP:
            self.seed.state=self.pod.state
            self.seed.brain=self.pod.controller.brain
            self.world_end.send(self.seed)
            
    
    def clientStep(self):
         self.pod.step()       
         self.pod.update_sensors()
        
    #    
    # this is done on a separate thread
    #
    def run(self):
       
        while(True):
           
            cmd=self.pod_end.recv()
            if isinstance(cmd,Seed):
                self.pod.state=cmd.state
                self.pod.controller.brain=cmd.brain
                continue
             
            #print cmd
            self.pod.step()       
            self.pod.update_sensors()
            #state=State(self)
            self.pod_end.send(self.pod.state)
            
    def start(self):
        if MP:
           mp.Process.start(self)
        