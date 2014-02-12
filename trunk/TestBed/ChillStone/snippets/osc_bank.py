from pyo import *
import load


srate=44100.0
buffersize=1028
s = Server(sr=srate, nchnls=2, buffersize=buffersize, duplex=0).boot()

stress=load.StressMonitor()


class MyOsc:
    
    def __init__(self,f,amp=1.0):
        self.white = Noise() 
        self.amp=Sig(amp)
        self.bw=Sig(0)
         
        ampTone = Sqrt( 1. - self.bw )*self.amp
        
        ampNoise = Sqrt( 2. * self.bw )*self.amp   
    
        self.mod=Biquad(self.white, freq=500, q=1, type=0,mul=ampNoise,add=ampTone)     
        self.osc=Sine(freq=f,mul=self.mod)
    
    
    def out(self):
        self.osc.out()
        
  
    
fun=250.0
oscs=[]
N=200
amp=Sig(1.0/N)
amp.ctrl()

for i in range(N):
    freq=fun*(i+1)  
    osc=MyOsc(freq,amp)
    # osc.osc.ctrl([SLMapFreq(init=freq)])
    osc.out()
    
    oscs.append(osc)
    
s.gui(locals())

