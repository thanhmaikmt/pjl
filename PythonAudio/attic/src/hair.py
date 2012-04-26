'''
Created on 13 Dec 2010

@author: pjl
'''

from math import  *
import numpy as np
import copy

reson=.99

class Hairs:
    
    def __init__(self,nHair,freqLow,freqSpace,dt):
        self.a0=np.zeros(nHair)
        self.a1=-reson*reson
        
        self.x1=np.zeros(nHair)
        self.x0=np.zeros(nHair)
        self.tmp=np.zeros(nHair)
        self.freq = np.zeros(nHair)
        
        freqNext=freqLow
        for i in range(nHair):
            self.freq[i]=freqNext
            self.a0[i] = 2.0 * reson * cos( 2.0*pi*freqNext*dt )
            freqNext *= freqSpace
            
            
    def step(self,force):
  
        ttt=self.x1
        
        self.tmp[:] = force + self.a0 * self.x0 + self.a1 * self.x1;
        self.x1    = self.x0;
        self.x0    =  self.tmp;
        self.tmp   =  ttt
        

 
        
if __name__ == "__main__":
    Fs=44100.0
    dt=1/Fs
    nHair=1
    
    hairs=Hairs(nHair,100,1.2,dt)
    
    force=1.0
    x=[]
    times=[]
    t=0.0
    
    for i in range(4000):
        hairs.step(force)
        force=0.0
        x.append(copy.copy(hairs.x0))
        times.append(t)
        t+=dt
        
from pylab import *

xa=np.array(x)

z=[]
nn=xa.shape[1]
fund=1.0/(nn*dt)
freqs=arange(nn)*fund

for i in range(nHair):
    s=fft(xa[:,i])
    z.append(abs(s))
    
    
subplot(211)    
plot(freqs,z)
subplot(212)
plot(times,x)
show()
