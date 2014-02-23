from numpy import *

nSamps=100
y1=ones(nSamps)
y2=zeros(nSamps)

for i in range(32,nSamps):
    y2[i]=32*i -  (y2[i-1] )
    print y2[i]