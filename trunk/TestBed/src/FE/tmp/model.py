'''
Created on 4 Sep 2012

@author: eespjl


Added some conductivity. Seems to stablize the method.
Add V term  still need Ht on boundary :-( otherwise we get zero current).


'''

import matplotlib.pyplot as P
from numpy import  *
from math import *
from numpy.linalg import *
from math import  *
import copy
import sys



class Node:
    
    def __init__(self,ieqs,x):
        self.ieq=ieqs
        self.x=x
        
    def equation(self,ivar):
        """
        return the eqn for a variable number
        """
        return self.ieq[ivar]

class ElemA:
    
    def __init__(self,nodes):
        self.nodes=nodes
        
    def assemble(self,K,C):
        """
        Assemble element equations into into global matrix
        """
        n1=self.nodes[0]
        n2=self.nodes[1]
        h=abs(n1.x-n2.x)
        
        iA1=n1.ieq['Az']
        iA2=n2.ieq['Az']
        iJ1=n1.ieq['Qz']
        iJ2=n2.ieq['Qz']
        iV=n1.ieq['V']
        
        # INT 1/u grad Ni grad Nj
        
        termK=1.0/h/u0
        
        K[iA1,iA1] += termK
        K[iA2,iA1] -= termK
        K[iA2,iA2] += termK
        K[iA1,iA2] -= termK
       
        
        termC = -h/2.0
          
        # J term in curl curl A + J =0
        C[iA1,iJ1]+=termC       
        C[iA2,iJ2]+=termC
 
        #  dA/dt  term in  E= 0 
        C[iJ2,iA2]+=termC
        C[iJ1,iA1]+=termC
        
        # grad V term in E = 0
        C[iJ1,iV]+=termC
        C[iJ2,iV]+=termC
     
        # total current constraint   SUM J   = Itot
        C[iV,iJ1]+=termC
        C[iV,iJ2]+=termC
        
        
   
        # add a bit of eddy current conductivity into curl curl E
        C[iA1,iA1] -= termC*cond
        C[iA2,iA2] -= termC*cond


        
# Bc= 120 perpendicalur   250 parallel
# Jc = 1-5 MA /cm/cm ?

Jc=1.0e6
h=.2e-3
wid=40e-3




cond=10e7




n_node=int(wid/h)
n_eq=n_node*2+1
n_elem=n_node-1


nodes=[]

iV=n_eq-1
x=0.0

for i in range(n_node):
    ieq={'Az':i,'Qz':i+n_node,'V':iV}
    nodes.append(Node(ieq,x))
    x+=h



elems=[]
for i in range(n_elem):
    nod=[nodes[i],nodes[i+1]]
    elems.append(ElemA(nod))

u0=4*pi*1e-7


K=zeros((n_eq,n_eq))
C=zeros((n_eq,n_eq))
A=zeros((n_eq,n_eq))

x_tmp=zeros(n_eq)
b=zeros(n_eq)
rhs=zeros(n_eq)
dxdt_new=zeros(n_eq)
#critical_flag=zeros(n_node,dtype=bool)
#critical_flag.fill(False)

tmp=zeros(n_eq)

theta=1.0
mass_lumping=True
Ht=0.0

jj=[]
ee=[]

def assemble(K,C):
    K.fill(0.0)
    C.fill(0.0)
 
    for e in elems:
        e.assemble(K,C)
                     


def fixJ(K,C,b,dxdt,It):
    
    iV=n_eq-1
    b.fill(0.0)
    Ht=It/2
    b[0]=Ht
    b[n_node-1]=Ht
    b[iV]=It
    flag=False
 
    for i in range(n_node):
        iJ1 = i + n_node
        J   = abs(dxdt[iJ1])
        sJ   = sign(dxdt[iJ1])
        
        if J >= 1.1*Jc :
            
            E = -dxdt[i]-dxdt[iV]
            aE  = abs(E)           # this is dA/dt  so E=-dAdt
            sE = sign(E) 
            Jfix = sJ*Jc
            
            if False and sE != sJ :
                #print "ooops E is oposes current flow "
                flag=True
            else:
                for jEq in range(n_eq):
                    b[jEq] -= Jfix*C[jEq,iJ1]
     
                    # zero the matrix row and column for iJ1
                    if iJ1 != jEq:
                        C[iJ1,jEq]=0.0
                        C[jEq,iJ1]=0.0
                        K[iJ1,jEq]=0.0
                        K[jEq,iJ1]=0.0
                      
                    # fix unknown J to s*Jc
                    
                C[iJ1,iJ1]=1.0
                b[iJ1]=Jfix
                
                
    return flag                      



def evaluate(dxdt,x,dxdt_guess,It,dt):
        assemble(K,C)
        flag=fixJ(K,C,b,dxdt_guess,It)
        #if flag:
        #    print " E is still confused"
        #if i == 1 and cnt == 0:
        #    for i in range(n_eq):
        #        print C[i],b[i]
                
        A[:]=C+theta*dt*K
        rhs[:]=b-dot(K,x)
        dxdt_new[:]=solve(A,rhs)
        
        
        tmp[:]=dxdt_guess-dxdt_new
        dxdt_guess[:]=dxdt_new
        err=dot(tmp,tmp)
        return err


