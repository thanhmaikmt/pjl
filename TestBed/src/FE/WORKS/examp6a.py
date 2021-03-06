'''
Created on 4 Sep 2012

@author: eespjl


Added some conductivity. Seems to stablize the method.
'''

import matplotlib.pyplot as P
from numpy import  *
from math import *
from numpy.linalg import *
from math import  *
import copy
import sys

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
n_plot_x=int(n_node/3)

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
critical_flag=zeros(n_node,dtype=bool)
critical_flag.fill(False)

tmp=zeros(n_eq)

theta=1.0
mass_lumping=True
Ht=0.0

xx=array(range(n_plot_x))
xx = h*xx
jj=[]
ee=[]

def assemble(K,C):
    K.fill(0.0)
    C.fill(0.0)
 
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
        
        termC = -h/4.0
        
        
        termC = -h/2.0
             
        C[iA1,iJ1]+=termC
        C[iJ1,iA1]+=termC
               
        C[iA2,iJ2]+=termC
        C[iJ2,iA2]+=termC
        
        
        # add a bit of conductivity
        C[iA1,iA1] -= termC*cond
        C[iA2,iA2] -= termC*cond
             


def fixJ(K,C,b,dxdt,Ht):
    
    b.fill(0.0)
    b[0]=Ht
    b[n_node-1]=Ht
    flag=False
 
    for i in range(n_node):
        iJ1 = i + n_node
        J   = abs(dxdt[iJ1])
        s   = sign(dxdt[iJ1])
        
        if J >= Jc :
            
            E  = abs(dxdt[i])           # this is dA/dt  so E=-dAdt
            sE = sign(-dxdt[i]) 
            Jfix = s*Jc
            if sE != s:    # add and False to try other scheme
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

tol=1e-5
time=0.0
times=[]

Jmm=0.0

try:

 for i in range(n_step):
   
    Ht=I_at_time(time+dt)/2.0
    
    flag=True
    print "iterating",Ht
    cnt=0
    
    while True :
        
        assemble(K,C)
        flag=fixJ(K,C,b,dxdt_guess,Ht)
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
        cnt+=1
        err=dot(tmp,tmp)
        Jmax=max(abs(dxdt_new[n_node:,]))

          
        print cnt,"  Err=",err," Jmax = ", Jmax/Jc
        
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
    tt= -dxdt[:n_plot_x]
    ee.append(tt)
    #print dxdt
    time+=dt


except:
    print "Error:", sys.exc_info()[0]
  
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
