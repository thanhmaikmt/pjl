import numpy as np
import math

#  read the raw ECG data 
#  assumes points are in range 0-1024 and sampled at 500 Hz
#  returns 
#   t array of time points 
#   x array of data points normalized to the range -1 to 1 
#  dt time step (1/500)

def readECG(name):

    fin=open(name)
    
    fullScale=1024
    ref=fullScale/2.0
    
    dt=1/500.0
    
    x=[]
    t=[]
    
    time=0.0
    
    for line in fin:
        x.append((float(line)-ref)/fullScale)
        
    fin.close()
        
    x=np.array(x)
    
    print " read ",len(x)," points"
    return x


def halfLifeFactors(nsamp):
#  fact ^ nsamp = 0.5
#  nsamp*ln(fact) = ln(0.5)
#  ln(fact)= ln(0.5)/nsamp
#  fact=exp(ln(0.5)/nsamp)

    fact=math.exp(math.log(0.5)/nsamp)
    return fact,1.0-fact


    