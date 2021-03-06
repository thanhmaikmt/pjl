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


t_peak = 0.1
t_end  = 0.2

Ipeak=-Jc*wid/4.5
dt=1e-3
n_step=int(t_end/dt)
cond=1e7


def I_at_time(t):
    #return Ipeak

    if t<=t_peak:
        return Ipeak*t/t_peak
    else:
        return Ipeak*(1.0+(t_peak-t)/t_peak)

n_node=int(wid/h)
n_eq=n_node*2+2
n_elem=n_node-1


nodes=[]

iV=n_eq-2
iI=n_eq-1

x=0.0

for i in range(n_node):
    ieq={'Az':i,'Qz':i+n_node,'V':iV}
    nodes.append(Node(ieq,x))
    x+=h


n_plot_x=int(n_node/3)

elems=[]
for i in range(n_elem):
    nod=[nodes[i],nodes[i+1]]
    elems.append(ElemA(nod))

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

theta=1.0
mass_lumping=True
Ht=0.0
Resist=100

xx=array(range(n_plot_x))
xx = h*xx
jj=[]
ee=[]


import plotter2

plot=plotter2.Plotter((0,wid),(-1.2*Jc,1.2*Jc),(-0.001,0.001))

def assemble(K,C):
    K.fill(0.0)
    C.fill(0.0)
 
    for e in elems:
        e.assemble(K,C)

#    #C[iV][iI]=1.0
 #   C[iI][iV]=1.0
    C[iI][iI]=Resist
      
def calc_state(dxdt):
    state=zeros(n_node,dtype=int)

    for i in range(n_node):
        iJ1 = i + n_node
        J   = abs(dxdt[iJ1])
        s   = sign(dxdt[iJ1])
           
        if J >= Jc :
            state[i]=s
        else:
            state[i]=0
            
    return state
 
def fixJ(K,C,b,dxdt,It,state0):
    
    iV=n_eq-1
    b.fill(0.0)
    Ht=It/2
    b[0]=Ht
    b[n_node-1]=Ht
    b[iV]=It
    
    
    flag=False
 
    #state=calc_state(dxdt)
 
    for i in range(n_node):
        iJ1 = i + n_node
        J   = abs(dxdt[iJ1])
        sJ   = sign(dxdt[iJ1])
        E   = -dxdt[i]-dxdt[iV]
        aE  = abs(E)           # this is dA/dt  so E=-dAdt
        sE =  sign(E) 
     
     
        if J >= Jc :
            
            E = -dxdt[i]-dxdt[iV]
            aE  = abs(E)           # this is dA/dt  so E=-dAdt
            sE = sign(E) 
            Jfix = sJ*Jc
            if sE != sJ :
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

tol=1e-5
time=0.0
times=[]

Jmm=0.0

#try:

def converged(a,b):
    for aa,bb in zip(a,b):
        if aa != bb:
            return False
        
        return True
    
for i in range(n_step):
   
    It=I_at_time(time+dt)
    
    flag=True
    print "iterating",Ht      
    cnt=0
 
    state0=calc_state(dxdt_new) 
      
    while True :
        
        assemble(K,C)
        
        flag=fixJ(K,C,b,dxdt_guess,It,state0)
                
        A[:]=C+theta*dt*K
        rhs[:]=b-dot(K,x)
        dxdt_new[:]=solve(A,rhs)
        
        
        tmp[:]=dxdt_guess-dxdt_new
        dxdt_guess[:]=dxdt_new
        cnt+=1
        err=dot(tmp,tmp)
        Jmax=max(abs(dxdt_new[n_node:,]))

          
        print cnt,"  Err=",err," Jmax = ", Jmax/Jc,"  E*J < 0 = ",flag
        
        
        if err < tol :
            #if flag:
            #    print "+++++++++++++++++++++++ OOOOOOOPS E is confused ++++++++++++++++++++++++++++++"
            Jmm=max(Jmm,Jmax)
            
            break
        
    dxdt[:]=dxdt_guess
    x[:]=x+dt*dxdt
    tt=copy.deepcopy(dxdt[n_node:n_node+n_plot_x])
    times.append(time)
    jj.append(tt)
   

    plot.drawX(0,xx,tt)
    tt= -dxdt[:n_plot_x]-dxdt[iV]
    print max(tt),min(tt)
    plot.drawX(1,xx,tt)
    plot.redraw(" Time={} ".format(time))
    ee.append(tt)
   
    #print dxdt
    time+=dt




#except:
#    print "Error:", sys.exc_info()[0]
  
n_step=len(times)
n_plot=10
d_n=int(n_step/n_plot)
d_n=max(1,d_n)
ss=range(0,n_step,d_n)


xxx=[times[x]  for x in ss]

print xxx

f, axarr = P.subplots(len(ss), sharex=True)

import matplotlib.ticker as ticker

formatter = ticker.FormatStrFormatter('%1.1f')


x_lim=xx[-1]

Jmm=Jc*1.2

for i in range(len(ss)):
    ax1=axarr[i]
    ax1.plot(xx,jj[ss[i]])
    ax1.set_ylim(-Jmm,Jmm)
    ax1.set_xlim(0.0,x_lim)
    ax1.yaxis.set_major_formatter(formatter)
    ax1.add_line(P.Line2D([0.0, x_lim], [0.0, 0.0], 
                  linewidth=1, color='g',linestyle='--'))
    
    ax1.annotate(str(xxx[i]) + " secs ",  xy=(.5, .8),
                xycoords='axes fraction' , #'axes points',
                horizontalalignment='center', verticalalignment='center',
                fontsize=10)
    
    ax2 = ax1.twinx()
    ax2.plot(xx, ee[ss[i]], 'r')
    ax2.set_ylim(-5e-4,5e-4)
    
P.show() 
