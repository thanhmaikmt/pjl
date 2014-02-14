

import matplotlib.pyplot as plt
import numpy as np
from  readfile import *

name="../data/Feb14_17_10_31.txt"

name="../data/Feb14_18_47_33.txt"

t,x,dt=readECG(name)

n50=int(round(1.0/50.0/dt))

    
xf = np.zeros(len(x))
x50=np.zeros(n50)
fact2=0.1
fact1=1.0-fact2

for i in range(len(x)):
    i50 = i % n50
    x50[i50] = x50[i50]*fact1+x[i]*fact2
    xf[i]=x[i]-x50[i50]
        
# 50 Hz filter.  
 

i1=0
i2=len(t)
plt.plot(t[i1:i2],x[i1:i2],"r")  #  ,t[i1:i2],xf[i1:i2],"g")
plt.show()