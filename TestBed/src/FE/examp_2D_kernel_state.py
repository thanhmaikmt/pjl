'''
Created on 4 Sep 2012

@author: eespjl


Added some conductivity. Seems to stablize the method.
Add V term  still need Ht on boundary :-( otherwise we get zero current).


'''

import matplotlib.pyplot as P
import numpy 
import numpy.linalg
import math
import copy
import sys
import plotter

# Bc= 120 perpendicalur   250 parallel
# Jc = 1-5 MA /cm/cm ?


thick=10e-6
Jc=7.5e9*thick     # 1.0e6

h=.02e-3
wid=4e-3
freq=1.0
t_end  = 1.0
Ipeak=-250
dt=5e-3
n_step=int(t_end/dt)
cond=1e7


def I_at_time(t):
    #return Ipeak

    return Ipeak*math.sin(2.0*math.pi*freq*t)
#     if t<=t_peak:
#         return Ipeak*t/t_peak
#     else:
#         return Ipeak*(1.0+(t_peak-t)/t_peak)

n_node=int(wid/h)
n_eq=n_node*2+1



nodes=[]

iV=n_eq-1

x=0.0

n_plot_x=int(n_node)
u0=4*math.pi*1e-7


K=numpy.zeros((n_eq,n_eq))
C=numpy.zeros((n_eq,n_eq))
A=numpy.zeros((n_eq,n_eq))

dxdt=numpy.zeros(n_eq)
x=numpy.zeros(n_eq)
x_tmp=numpy.zeros(n_eq)
b=numpy.zeros(n_eq)
rhs=numpy.zeros(n_eq)
dxdt_guess=numpy.zeros(n_eq)
dxdt_new=numpy.zeros(n_eq)

state=numpy.zeros(n_node,dtype=int)
state2=numpy.zeros(n_node,dtype=int)



tmp=numpy.zeros(n_eq)

theta=1.0
mass_lumping=True
Ht=0.0

xx=numpy.array(range(n_plot_x))
xx = h*xx

plot=plotter.Plotter((0,xx[-1]),(-1.2*Jc,1.2*Jc))


jj=[]
ee=[]

import kernel

xA=0
xB=wid

strip=kernel.Strip(xA,xB,0.0,0.0,n_node)


M=strip.make_M(10)

MI=numpy.linalg.inv(M)


def assemble(K,C):
    K.fill(0.0)
    C.fill(0.0)
 
    
    #     A-A section         
    for i in range(n_node):
        for j in range(n_node):
            K[i][j]=MI[i][j]    
    
    h=strip.dlen    
    termC = -h
          
    for i in range(n_node):
        iA=i
        iJ=i+n_node
        
        # J term in curl curl A + J =0
        C[iA,iJ]+=termC       
        C[iJ,iA]+=termC
        
        
        # grad V term in E = 0
        C[iJ,iV]+=termC
        
        # total current constraint   SUM J   = Itot
        C[iV,iJ]+=termC
        
   
        # add a bit of eddy current conductivity into curl curl E
        #C[iA,iA] -= termC*cond
   
   
def calc_state(dxdt,state):
    for i in range(n_node):
        iJ1 = i + n_node
        J   = abs(dxdt[iJ1])
        s   = numpy.sign(dxdt[iJ1])
           
        if J > Jc :
            state[i]=s
        else:
            state[i]=0
            
            
def fixJ(K,C,b,dxdt,It,state0,state1):
    """
    dxdt guess for what dxdt might be at end of time step
    """
    
    iV=n_eq-1
    b.fill(0.0)
    #Ht=It/2
    #b[0]=Ht
    #b[n_node-1]=Ht
    b[iV]=It
   
#     calc_state(dxdt,state1)
    
    for i in range(n_node):
        iJ1 = i + n_node
        J   = abs(dxdt[iJ1])
        s   = numpy.sign(dxdt[iJ1])
        
        
        if state[i] == 0:
            
            if J > Jc :
                state2[i]=s
            else:
                state[i]=0  
        else:
            
            E = -dxdt[i]-dxdt[iV]
            aE  = abs(E)           # this is dA/dt  so E=-dAdt
            sE = numpy.sign(E) 
            Jfix = state[i]*Jc
            state2[i]=state[i]
            
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
    return                       

tol=1e-5
time=0.0
times=[]

Jmm=0.0

#try:

for i in range(n_step):
   
    It=I_at_time(time+dt)
    
    flag=True
    print "iterating",Ht
    cnt=0
    
    while True :
        
        assemble(K,C)
        flag=fixJ(K,C,b,dxdt_guess,It,state,state2)
        
        #if flag:
        #    print " E is still confused"
        #if i == 1 and cnt == 0:
        #    for i in range(n_eq):
        #        print C[i],b[i]
                
        A[:]=C+theta*dt*K
        rhs[:]=b-numpy.dot(K,x)
        dxdt_new[:]=numpy.linalg.solve(A,rhs)
        
        
        tmp[:]=dxdt_guess-dxdt_new
        dxdt_guess[:]=dxdt_new
        cnt+=1
        err=numpy.dot(tmp,tmp)
        Jmax=max(abs(dxdt_new[n_node:,]))

          
        print cnt,"  Err=",err," Jmax = ", Jmax/Jc,"  E*J < 0 = ",flag
        
        if err < tol:
            if flag:
                print "+++++++++++++++++++++++ OOOOOOOPS E is confused ++++++++++++++++++++++++++++++"
            Jmm=max(Jmm,Jmax)
            
            break
        
    dxdt[:]=dxdt_guess
    calc_state(dxdt_guess,state)
    x[:]=x+dt*dxdt
    tt=copy.deepcopy(dxdt[n_node:n_node+n_plot_x])
    
    
    times.append(time)
    jj.append(tt)
    tt=tt
    plot.draw(xx,tt,"time= {}".format(time))
    xxx=raw_input(" Hit CR")
    
    
    tt= -dxdt[:n_plot_x]
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
