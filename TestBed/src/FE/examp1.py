'''
Created on 4 Sep 2012

@author: eespjl
'''

from numpy import  *
from math import *
from numpy.linalg import *

# Bc= 120 perpendicalur   250 parallel
# Jc = 1-5 MA /cm/cm ?
n_node=10
n_eq=n_node*2
h=1e-3
n_elem=n_node-1
u0=4*pi*1e-7
Itot=1.0

n_step=10

K=zeros((n_eq,n_eq))
C=zeros((n_eq,n_eq))
A=zeros((n_eq,n_eq))

dxdt=zeros(n_eq)
x=zeros(n_eq)
b=zeros(n_eq)
Ht=Itot/2.0
dt=1e-3
theta=1.0
mass_lumping=True

for i in range(n_elem):
    iA1=i
    iA2=i+1
    iJ1=i+n_node
    iJ2=iJ1+1

    # INT 1/u grad Ni grad Nj
    
    termK=1.0/h/u0
    
    K[iA1,iA1] += termK
    K[iA2,iA1] -= termK
    K[iA2,iA2] += termK
    K[iA1,iA2] -= termK
    
    # INT Ni Nj    (mass lumping ?)
    if not mass_lumping:
        termC = h/4.0
        C[iA1,iJ1]=termC
        C[iA1,iJ2]=termC
        C[iJ1,iA1]=termC
        C[iJ1,iA2]=termC
    
        C[iA2,iJ1]=termC
        C[iA2,iJ2]=termC
        C[iJ2,iA1]=termC
        C[iJ2,iA2]=termC
    else:
        termC = h/2.0
        C[iA1,iJ1]=termC
        C[iJ1,iA1]=termC
    
        C[iA2,iJ2]=termC
        C[iJ2,iA2]=termC
        
        
b[0]=Ht
b[n_node-1]=Ht

A=C+theta*dt*K



for i in range(n_step):
    rhs=b-K*x
    dxdt=solve(A,b)
    x=x+dxdt
    print dxdt
