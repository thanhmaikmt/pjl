#
# this function implements the threshold perceptron
#
from math import *

def fire(xVec,wVec):
    sum=0.0
    for i in range(4):
        sum += xVec[i]*wVec[i]
    if sum > 0.0:
        return 1.0
    return 0.0    

# training data is a list of inputs and target values.
# 
#  target = x2 AND  ( x1 or X2 )
# 
TD= [ [[0.,0.,0.,1.],0.], \
[[0.,0.,1.,1.],0.], \
[[0.,1.,0.,1.],0.], \
[[0.,1.,1.,1.],1.], \
[[1.,0.,0.,1.],0.], \
[[1.,0.,1.,1.],0.], \
[[1.,1.,0.,1.],1.], \
[[1.,1.,1.,1.],1.]] 



w=[0.,0.,0.,0.]

converged=False
beta=1


iter=1
while not converged:
    print "** iter = ",iter
    iter += 1
    converged=True
    for td in TD:  #   iterate on the list of input target pairs
        x=td[0]    #   input is the first element of the sublist
        t=td[1]    #   training is the second
        y=fire(x,w)
        print x,t,y,w
        if (abs(t-y) > .0):
            converged =False
        for i in range(4):
            w[i]=w[i]+beta*(t-y)*x[i]
            
            
        
