from  matplotlib.pyplot import *
from math import *
from numpy import *



def sigmoid(x):
        if x < -100:
            return 0.0      
        return 1.0 / (1.0 + exp(-x))
        
        
        
x=arange(-5,5,.1)
s=zeros(len(x))

for i in range(len(x)):
	s[i]=sigmoid(x[i])
	
plot(x,s)
show()

