from  matplotlib.pyplot import *
from math import *
from numpy import *



def sinc(x): 
    from math import pi, sin 
    try: 
#        x = pi * x 
        return sin(x) / x 
    except ZeroDivisionError: # sinc(0) = 1 
        return 1.0 



ymin=[]
ymax=[]

xs=arange(0,10,.1)


h1=[]
h2=[]

for x in xs:
    h1.append(abs(sinc(x)))
    if x < 1:
        h2.append(1.0)
    else:
        h2.append(1.0/x)

plot(xs,h1,".",xs,h2,"-")
ylabel("|sinc(x)|")
grid()


show()
