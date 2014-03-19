
import numpy



        
        # resample at 3.2 Hz
        # nPoints  64 or 128

SAMP_FREQ=3.2
BPM_DEFAULT=60.0


class SpecrtralJovanov:
    
    def __init__(self):
        
        self.dt=1.0/SAMP_FREQ
        self.nSamps=128
        self.x=numpy.zeros(nSamps)
        self.x += 1.0/BPM_DEFAULT
        
        self.time=0
        self.win=numpy.hanning(nSamps)
        # time of last sample
        self.tLast=None
        self.cnt=0
        
    def process(self,val,t):
    
    
        if self.tLast == None:
            self.tLast = t
            self.valLast = val
            self.x[0]=val
            self.cnt += 1
            return
            
        
        delta=t-self.tLast
        
        if delta < self.dt:
            
              
        