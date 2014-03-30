import numpy
import util
  
  
  
  
class Median:
    
    def __init__(self,N):
        self.N=N
        self.x=numpy.zeros(N)
        self.ptr=0
        self.N_MED=N/2
        
    def process(self,data):
        
        self.x[self.ptr]=data
        
        self.ptr += 1
        
        if self.ptr == self.N:
            self.ptr=0
       
        return self
   
    def median_val(self): 
        return  numpy.sort(self.x)[self.N_MED]
        
        
  

class Interpolator:
    
    def __init__(self,srate,client):
        
        self.dt=1.0/srate
        self.time=0
        self.tLast=None
        self.client=client
        
    def process(self,bpm,tNow):
    
    
        if self.tLast == None:
            self.tLast = tNow
            self.bpmLast = bpm
            return
            
        # t
        
        while self.time <= tNow:
 

            """
                 bpmLast                      bpm
                 tLast                        tNow
                               time
             
             bpm1= ( bpmLast*(tNow-time) + bpm*(time-tLast)  )/(tNow-tlast)
             
             """
            
            bpmX = ( self.bpmLast*(tNow-self.time) + bpm*(self.time-self.tLast)  )/(tNow-self.tLast)
            if self.client != None:
                self.client.process(bpmX)
                
            self.time+=self.dt
    
            
        self.tLast=tNow
        self.bpmLast=bpm

  
class DCBlock:
    """
    https://ccrma.stanford.edu/~jos/filters/DC_Blocker.html
    """
    
    def __init__(self,R):
        self.R=R
        self.yLast=0
        self.xLast=0
        
    def process(self,x):
        
        y=x-self.xLast+self.yLast*self.R
        
        self.xLast=x
        self.yLast=y
        
        return y
        
              
             
"""
static int y1 = 0, y2 = 0, x[26], n = 12;
int y0;
x[n] = x[n + 13] = data;
y0 = (y1 << 1) - y2 + x[n] - (x[n + 6] << 1) + x[n + 12];
y2 = y1;
y1 = y0;
y0 >>= 5;
if(--n < 0)
n = 12;
return(y0);
"""
class LPF:
    
    def __init__(self):
        self.y1 = 0
        self.y2 = 0
        self.x=numpy.zeros(26)
        self.n = 12
        
    
    def process(self,data):
    
        self.x[self.n] = self.x[self.n + 13] = data;
        y0 = 2*self.y1 - self.y2 + self.x[self.n] - (2*self.x[self.n + 6]) + self.x[self.n + 12];
        self.y2 = self.y1
        self.y1 = y0
        y0 *= 32
        self.n -= 1
        if self.n < 0:
            self.n = 12
        return y0

"""
static int y1 = 0, x[66], n = 32;
int y0;
x[n] = x[n + 33] = data;
y0 = y1 + x[n] - x[n + 32];
y1 = y0;
if(--n < 0)
n = 32;
return(x[n + 16] - (y0 >> 5));
}
"""
        
class HPF:
    
    def __init__(self):
        self.y1 = 0
        self.x=numpy.zeros(66)
        self.n = 32
    
    def process(self,data):
    
        self.x[self.n] = self.x[self.n + 33] = data;
        y0 = self.y1 + self.x[self.n] - self.x[self.n + 32]
        self.y1 = y0;
        self.n -=1
        if self.n < 0:
            self.n = 32
        return self.x[self.n+16]-y0/32.0


"""
int Derivative(int data)
{
int y, i;
static int x_derv[4];
/*y = 1/8 (2x( nT) + x( nT - T) - x( nT - 3T) - 2x( nT -  4T))*/
y = (data << 1) + x_derv[3] - x_derv[1] - ( x_derv[0] << 1);
y >>= 3;
for (i = 0; i < 3; i++)
x_derv[i] = x_derv[i + 1];
x_derv[3] = data;
return(y);
"""
class Dervivative:
    
    def __init__(self):
        self.y = 0
        self.i = 0
        self.x_derv=numpy.zeros(4)
  
    def process(self,data):
    
        y = 2*data + self.x_derv[3] -self.x_derv[1]- 2*self.x_derv[0]
        y = y/8
        self.x_derv[0]=self.x_derv[1]
        self.x_derv[1]=self.x_derv[2]
        self.x_derv[2]=self.x_derv[3]
        self.x_derv[3]=data
        return y

"""
static int x[32], ptr = 0;
static long sum = 0;
long ly;
int y;
if(++ptr == 32)
ptr = 0;
sum -= x[ptr];
sum += data;
x[ptr] = data;
ly = sum >> 5;
if(ly > 32400) /*check for register overflow*/
y = 32400;
else
y = (int) ly;
return(y);
"""

class MovingAverge:
    
    def __init__(self):
        self.sum = 0
        self.ptr = 0
        self.x=numpy.zeros(32)
  
    def process(self,data):
    
        self.ptr+=1
        if self.ptr== 32:
            self.ptr=0
        self.sum -= self.x[self.ptr]
        self.sum += data
        self.x[self.ptr]=data
        
        return self.sum/32.0


class MovingAvergeN:
    
    def __init__(self,N):
        self.sum = 0.0
        self.ptr = 0
        self.x=numpy.zeros(N)
        self.N=N
  
    def process(self,data):
    
        self.ptr+=1
        if self.ptr == self.N:
            self.ptr=0
        self.sum -= self.x[self.ptr]
        self.sum += data
        self.x[self.ptr]=data
        
        return self.sum/self.N

class MovingDecayAverge:
    
    def __init__(self,samps_per_half_life,init_value):
        self.sum = init_value
        self.ptr = 0
        self.fact1,self.fact2=util.halfLifeFactors(samps_per_half_life)
        
  
    def process(self,data):
    
        self.sum=self.sum*self.fact1+data*self.fact2
        return self.sum
    
    def get_value(self):
        return self.sum


 
    
class Delay:
    
    
    def __init__(self,N):
        
        self.buff=numpy.zeros(N)
        self.N=N
        self.ptr=0
        
        
    def process(self,data):
        
        ret=self.buff[self.ptr]
        self.buff[self.ptr]=data
        self.ptr+=1
        
        if self.ptr == self.N:
            self.ptr=0
            
        return ret
        
    




#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ***************************************************************************
# *   Copyright (C) 2011, Paul Lutus                                        *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU General Public License for more details.                          *
# *                                                                         *
# *   You should have received a copy of the GNU General Public License     *
# *   along with this program; if not, write to the                         *
# *   Free Software Foundation, Inc.,                                       *
# *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
# ***************************************************************************

import math

class Biquad:
  
  # pretend enumeration
  LOWPASS, HIGHPASS, BANDPASS, NOTCH, PEAK, LOWSHELF, HIGHSHELF = range(7)

  def __init__(self,typ, freq, srate, Q, dbGain = 0):
      types = {
      Biquad.LOWPASS : self.lowpass,
      Biquad.HIGHPASS : self.highpass,
      Biquad.BANDPASS : self.bandpass,
      Biquad.NOTCH : self.notch,
      Biquad.PEAK : self.peak,
      Biquad.LOWSHELF : self.lowshelf,
      Biquad.HIGHSHELF : self.highshelf
      }
      assert(types.has_key(typ))
      freq = float(freq)
      self.srate = float(srate)
      Q = float(Q)
      dbGain = float(dbGain)
      self.a0 = self.a1 = self.a2 = 0
      self.b0 = self.b1 = self.b2 = 0
      self.x1 = self.x2 = 0
      self.y1 = self.y2 = 0
      # only used for peaking and shelving filter types
      A = math.pow(10, dbGain / 40)
      omega = 2 * math.pi * freq / self.srate
      sn = math.sin(omega)
      cs = math.cos(omega)
      alpha = sn / (2*Q)
      beta = math.sqrt(A + A)
      types[typ](A,omega,sn,cs,alpha,beta)
      # prescale constants
      self.b0 /= self.a0
      self.b1 /= self.a0
      self.b2 /= self.a0
      self.a1 /= self.a0
      self.a2 /= self.a0

  def lowpass(self,A,omega,sn,cs,alpha,beta):
    self.b0 = (1 - cs) /2
    self.b1 = 1 - cs
    self.b2 = (1 - cs) /2
    self.a0 = 1 + alpha
    self.a1 = -2 * cs
    self.a2 = 1 - alpha
    
  def highpass(self,A,omega,sn,cs,alpha,beta):
    self.b0 = (1 + cs) /2
    self.b1 = -(1 + cs)
    self.b2 = (1 + cs) /2
    self.a0 = 1 + alpha
    self.a1 = -2 * cs
    self.a2 = 1 - alpha
    
  def bandpass(self,A,omega,sn,cs,alpha,beta):
    self.b0 = alpha
    self.b1 = 0
    self.b2 = -alpha
    self.a0 = 1 + alpha
    self.a1 = -2 * cs
    self.a2 = 1 - alpha
    
  def notch(self,A,omega,sn,cs,alpha,beta):
    self.b0 = 1
    self.b1 = -2 * cs
    self.b2 = 1
    self.a0 = 1 + alpha
    self.a1 = -2 * cs
    self.a2 = 1 - alpha
    
  def peak(self,A,omega,sn,cs,alpha,beta):
    self.b0 = 1 + (alpha * A)
    self.b1 = -2 * cs
    self.b2 = 1 - (alpha * A)
    self.a0 = 1 + (alpha /A)
    self.a1 = -2 * cs
    self.a2 = 1 - (alpha /A)
    
  def lowshelf(self,A,omega,sn,cs,alpha,beta):
    self.b0 = A * ((A + 1) - (A - 1) * cs + beta * sn)
    self.b1 = 2 * A * ((A - 1) - (A + 1) * cs)
    self.b2 = A * ((A + 1) - (A - 1) * cs - beta * sn)
    self.a0 = (A + 1) + (A - 1) * cs + beta * sn
    self.a1 = -2 * ((A - 1) + (A + 1) * cs)
    self.a2 = (A + 1) + (A - 1) * cs - beta * sn
    
  def highshelf(self,A,omega,sn,cs,alpha,beta):
    self.b0 = A * ((A + 1) + (A - 1) * cs + beta * sn)
    self.b1 = -2 * A * ((A - 1) + (A + 1) * cs)
    self.b2 = A * ((A + 1) + (A - 1) * cs - beta * sn)
    self.a0 = (A + 1) - (A - 1) * cs + beta * sn
    self.a1 = 2 * ((A - 1) - (A + 1) * cs)
    self.a2 = (A + 1) - (A - 1) * cs - beta * sn
      
  # perform filtering function
  def process(self,x):
    y = self.b0 * x + self.b1 * self.x1 + self.b2 * self.x2 - self.a1 * self.y1 - self.a2 * self.y2
    self.x2 = self.x1
    self.x1 = x
    self.y2 = self.y1
    self.y1 = y
    return y
    
  # provide a static result for a given frequency f
  def result(self,f):
    phi = (math.sin(math.pi * f * 2/(2.0 * self.srate)))**2
    return ((self.b0+self.b1+self.b2)**2 - 4*(self.b0*self.b1 + 4*self.b0*self.b2 + self.b1*self.b2)*phi + 16*self.b0*self.b2*phi*phi) / ((1+self.a1+self.a2)**2 - 4*(self.a1 + 4*self.a2 + self.a1*self.a2)*phi + 16*self.a2*phi*phi)

  def log_result(self,f):
    try:
      r = 20 * math.log10(self.result(f))
    except:
      r = -200
    return r

  # return computed constants
  def constants(self):
    return self.b0,self.b1,self.b2,self.a1,self.a2
    