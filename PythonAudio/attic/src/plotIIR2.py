'''
Created on 21 Dec 2010

@author: pjl
'''


from math import cos,pi,exp
from numpy import *


Fs=44100.0
freq_peak=[100,500,1000,5000,10000]

dt=1/Fs
reson=.9        




# y(n)=x(n) + y(n-1) * a0 + y(n-2) * a1


# Y(f) = X(f) + Y(f)*a0*e^j(2*pi*DT)*f + Y(f)*a1*e^j(2*pi*DT*2)*f 

# Y(f)/X(f) = 1.0/(1 -a0*e^(2*pi*DT)*f - a1*e^(2*pi*DT*2)*f) 
         
        
# f = 10^fx
     
     
def freq_responce(a0,a1,dt,freqs):
    j=complex(0,1)

    dd=j*2.0*pi*dt
    g=[]
    for f in freqs:    
        g.append(abs(1.0/(1.0 -a0*exp(dd*f) - a1*exp(2.0*dd*f))))
    
    return g
    
   
fmax=Fs/2.0
fx=log10(fmax)
        
fx=arange(0,fx,.01)
freqs=[]



for fxx in fx:
    freqs.append(pow(10.0,fxx))
    

g=[]
for freq in freq_peak:
    a0 = 2.0 * reson * cos( 2.0*pi*freq*dt )
    a1= -reson*reson
    
    g.append(freq_responce(a0,a1,dt,freqs))    
         
from pylab import *
plot(fx,g[2])    
show()    
           