'''
Created on 13 Dec 2010

@author: pjl
'''

from math import  *
import numpy as np
reson=.9

class Hairs:
    
    def __init__(self,nHair,freqLow,freqSpace,dt):
        self.a0=np.zeros(nHair)
        self.a1=-reson*reson
        
        self.x1=np.zeros(nHair)
        self.x_tmp=np.zeros(nHair)
        self.freq = np.zeros(nHair)
        
        freqNext=freqLow
        for i in range(nHair):
    
            self.freq[i]=freqNext
            self.a0[i] = 2.0 * reson * cos( 2.0*pi*freqNext*dt ))
            freqNext *= freqSpace
            
            
    def step(self,force):
        self.time += self.dt
        
        
        self.x_tmp = force + _a0[i] * _x0[i] + _a1 * _x1[i];
    _x1[i]    = _x0[i];
    _x0[i]    =  x;
  