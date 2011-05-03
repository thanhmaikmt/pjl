import numpy as N
import wave
import pyaudio
import pylab as P
import player as PP


class OscSynth:
    
    
    def __init__(self,fMin,fMax,nOsc,dampInCycles,rate):
        
        # fMin*df^(N)=fMax
        # df = (fMax/fMin)^(1/N)
        
        
        df=(fMax/fMin)**(1.0/nOsc)
        
        freqs=N.zeros(nOsc,N.double)
        
        f=fMin
        for i in range(nOsc):
            freqs[i]=f
            f *=df
        self.freqs=freqs
        
        dt=1.0/rate

        self.state=N.zeros(nOsc,N.cdouble)
        
        j=complex(0,1.0)
        dRadPerHertz=2*N.pi/rate

        self.rotate=N.exp(dRadPerHertz*self.freqs*j)
        self.damp=N.exp(-freqs/dampInCycles/rate)
        self.delta = self.rotate*self.damp
        
    def step(self):
        self.state *= self.delta

    def stepForced(self,f):
        self.state *= self.delta
        self.state += f
      

    
if __name__ == "__main__":

    rate=44100
    dur=1.0
    nSamp=int(rate*dur)
    nOct=8 
    fMin=55.0
    fMax=fMin*2.0**float(nOct)
    nOsc=nOct*12
    osc=OscSynth(fMin,fMax,nOsc,100.0,rate);
    
    excite=N.zeros(nOsc,N.double)
    
    iOsc=40
    excite[iOsc]=10000.0
    
    chunkSize=1024
    
    chunk=N.zeros(chunkSize,N.float)

    #osc.stepForced(excite)
    
    i=0
    
    player=PP.Player()
    ii=0
    play=True
    while(play):
        chunk[i]=N.real(osc.state[iOsc])
        if ii % 23050 == 0:
            osc.stepForced(excite)
        else:
            osc.step()
        ii+=1
        i+=1
        
        if i == chunkSize:
            player.play(chunk)
            i=0
            #play=False
            
       
        
        
    from matplotlib.pyplot import * 
    plot(chunk)
    show()
  