#  Engine calls a call_back every tick
#  Calls idle while it waits for the next tick

import time
import threading


class Engine(threading.Thread):

    def __init__(self,bpm,ticks_per_beat,call_back=None,idle=None):
        
        self.dt=60.0/bpm/ticks_per_beat
        self.call_back=call_back
        self.idle=idle
        threading.Thread.__init__(self)
        
    def run(self):
        self.running=True
        tnext=tnow=time.time()
        tick=0
    
        while self.running:
            while tnow < tnext:
                if self.idle != None:
                    self.idle()
                tnow=time.time()
                
            if self.call_back != None:
                self.call_back(tick)
                
            tnext+=self.dt
            tick+=1
            
            