from numpy import *

a=zeros(shape=(5,5))
b=ones(shape=(2,2))

a[0:2][0:2]=b

print a
