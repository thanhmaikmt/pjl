import matplotlib.pyplot as plt
import numpy as np
from  util import *

name="../data/Feb14_18_47_33.txt"

t,x,dt=readECG(name)

srate=1.0/dt
minPulsePeriodSamps=srate*60.0/200.0

print " srate = ",srate, " Hz"
print " minPulsePeriodSamps ", minPulsePeriodSamps


# number of samples before we can fire again
holdSamps=minPulsePeriodSamps*.7

fireFact=3.0

# TODO work out a decent decay rate here.
# half life of sort of moving average  
halfT=4
halfSamps=halfT/dt

fact1,fact2=halfLifeFactors(halfSamps)

rectAverage=0.0   # keep a record of the average rectified value.
   
cnt=0
tPeaks=[]

ARMED,FIRED,PEAKED=range(3)

state=PEAKED

for x1,t1 in zip(x,t):
    rectAverage=rectAverage*fact1+abs(x1)*fact2
    cnt += 1
    
    if state==ARMED:
        if x1 > rectAverage*fireFact:
            state=FIRED
            xPeak=x1
            tPeak=t1
            
    elif state==FIRED:
        if x1 < xPeak:
            state=PEAKED
            tPeaks.append(tPeak)
            xPeaks.append(xPeak)
            cnt=0              
            continue
        
    elif state == PEAKED:
        if cnt > holdSamps:
            state=ARMED
        


print tPeaks
    
        
        
# 50 Hz filter.  
 
print len(t)

i1=0
i2=len(t)
plt.plot(t[i1:i2],x[i1:i2],"r")  #  ,t[i1:i2],xf[i1:i2],"g")
plt.show()