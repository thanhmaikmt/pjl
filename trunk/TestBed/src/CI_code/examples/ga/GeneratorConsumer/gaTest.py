'''
Created on 29 Jun 2011

@author: pjl
'''
from GA import *


l=5

g1=random_gene(l)
g2=random_gene(l)

for i in range(20):
    print mate(g1,g2).str

print " ------------------"

b=blank_gene(l)

print g1.str
print g2.str

for i in range(20):
    mutate(b)
    print b.str