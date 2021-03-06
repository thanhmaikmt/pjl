'''
Created on 4 Sep 2012

@author: eespjl
'''

import matplotlib.pyplot as P
from matplotlib import collections, axes, transforms
from matplotlib.colors import colorConverter
from numpy import  *
from math import *
from numpy.linalg import *
from math import  *

# Bc= 120 perpendicalur   250 parallel
# Jc = 1-5 MA /cm/cm ?

Jc=1.0e6
h=1e-3
wid=20e-3
t_end=1.0
Itot=Jc*wid/1.5
dt=5e-3
n_step=int(t_end/dt)


n_node=int(wid/h)
n_eq=n_node*2
n_elem=n_node-1
u0=4*pi*1e-7


K=zeros((n_eq,n_eq))
C=zeros((n_eq,n_eq))
A=zeros((n_eq,n_eq))

dxdt=zeros(n_eq)
x=zeros(n_eq)
x_tmp=zeros(n_eq)
b=zeros(n_eq)
rhs=zeros(n_eq)
dxdt_guess=zeros(n_eq)
dxdt_new=zeros(n_eq)
tmp=zeros(n_eq)

Ht_big=Itot/2.0
dt=1e-3
theta=1.0
mass_lumping=True
Ht=0.0

xx=array(range(n_node))
x_axis = h*xx


def assemble(K,C,b,x,dxdt):
    K.fill(0.0)
    C.fill(0.0)
    b.fill(0.0)
    b[0]=Ht
    b[n_node-1]=Ht

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
                termC = -h/4.0
                C[iA1,iJ1]=termC
                C[iA1,iJ2]=termC
                C[iJ1,iA1]=termC
                C[iJ1,iA2]=termC
            
                C[iA2,iJ1]=termC
                C[iA2,iJ2]=termC
                C[iJ2,iA1]=termC
                C[iJ2,iA2]=termC
        else:
                termC = -h/2.0
                J = abs(dxdt[iJ1])
                s=sign(dxdt[iJ1])
                if J < Jc :
                    C[iA1,iJ1]=termC
                    C[iJ1,iA1]=termC
                else:
                    C[iJ1,iJ1]+=1.0
                    b[iJ1]+=Jc*s
                    b[iA1]-=Jc*s*termC
            
                J = abs(dxdt[iJ2])
                s= sign(dxdt[iJ2])
                if J < Jc :
                    C[iA2,iJ2]=termC
                    C[iJ2,iA2]=termC
                else:
                    C[iJ2,iJ2]+=1.0
                    b[iJ2]+=Jc*s
                    b[iA2]-=Jc*s*termC
        
        

tol=1e-3

for i in range(n_step):
    unstable=True
    Ht=Ht_big*(i+0.5)/n_step
    print "iterating",Ht
    cnt=0
    
    while unstable:
        assemble(K,C,b,x,dxdt_guess)
        A[:]=C+theta*dt*K
        rhs[:]=b-dot(K,x)
        dxdt_new[:]=solve(A,rhs)
        tmp[:]=dxdt_guess-dxdt_new
        dxdt_guess[:]=dxdt_new
        cnt+=1
        err=dot(tmp,tmp)
        print cnt,err
        if err < tol:
            break
        
    dxdt[:]=dxdt_guess
    x[:]=x+dt*dxdt
    
    P.plot(x_axis,dxdt[n_node:,])
    print dxdt

P.show()