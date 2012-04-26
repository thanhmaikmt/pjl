import numpy as N
import wave
import pyaudio
import pylab as P
import player as PP


class OscSynth:
    
    
    def __init__(self,fMin,fMax,nOsc,a,rate):
        
        # fMin*df^(N)=fMax
        # df = (fMax/fMin)^(1/N)
        
        
        df=(fMax/fMin)**(1.0/nOsc)
        
        freqs=N.zeros(nOsc,N.double)
        
        f=fMin
        for i in range(nOsc):
            freqs[i]=f
            f *=df
        self.freqs=freqs
        
        self.dt=1.0/rate

        self.state=N.zeros(nOsc,N.cdouble)
        self.re=1.0
     
        self.w=2*N.pi*self.freqs
        self.a=a
        
    def at(self,t):
        # ttt=N.sum(self.re*N.cos(t*self.w)*N.exp(self.a*t))
        ttt=N.sum(self.re*N.sin(t*self.w)*N.exp(self.a*t))
        return ttt
     
if __name__ == "__main__":

    rate=44100
    dur=.02
    nSamp=int(rate*dur)
    nOct=10 
    fMin=55.0
    fMax=fMin*2.0**float(nOct)
    nOsc=2
    osc=OscSynth(fMin,fMax,nOsc,-20.0,rate);
    
    dt=.0001
    tt=[]
    xx=[]

    n=int(dur/dt)
    t=0.0
    for i in range(n):
        tt.append(t)
        xx.append(osc.at(t))
        t+=dt    
    
         
    from matplotlib.pyplot import * 
    plot(tt,xx)
    show()
  