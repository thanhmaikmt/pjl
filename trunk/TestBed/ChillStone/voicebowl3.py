from pyo import *
s = Server().boot()
#s.start()
#t = CurveTable([(0,0.0),(512,0.97),(1024,-0.94),(1536,0.0),(8192,0.0000)])




class MyOsc:
    
    def __init__(self,f):
        self.white = Noise() 
        
        self.bw=Sig(0)
         
        ampTone = Sqrt( 1. - self.bw )
        ampNoise = Sqrt( 2. * self.bw ) ;  
    
        self.mod=Biquad(self.white, freq=500, q=1, type=0,mul=ampNoise,add=ampTone)
        
        self.osc=Sine(freq=f,mul=self.mod)
    
    
    def out(self):
        self.osc.out()
        
  
    
fun=200.0
oscs=[]
for i in range(3):
    freq=fun*i    
    osc=MyOsc(freq)
    osc.osc.ctrl([SLMapFreq(init=freq)])
    osc.out()
    
    oscs.append(osc)
    
s.gui(locals())

