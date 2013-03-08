#  Engine calls a call_back every tick
#  yields using sleep to allow multithreading

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
            
            # spin until next tick
            while tnow < tnext:
                # yeild to other threads
                time.sleep(0.001) 
                tnow=time.time()       
            
            self.call_back(tick)
            tnext+=self.dt
            tick+=1
            
            