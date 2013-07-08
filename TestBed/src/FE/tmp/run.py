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
import model



import plotter2

plot=plotter2.Plotter((0,model.wid),(-1.2*model.Jc,1.2*model.Jc),(-0.001,0.001))



n_plot_x=int(model.n_node/3)

xx=array(range(n_plot_x))
xx = model.h*xx
jj=[]
ee=[]

tol=1e-5
time=0.0
times=[]

Jmm=0.0


t_peak = 0.1
t_end  = 0.2

dt=1e-3
n_step=int(t_end/dt)

Ipeak=-model.Jc*model.wid/4.5

def I_at_time(t):
    #return Ipeak

    if t<=t_peak:
        return Ipeak*t/t_peak
    else:
        return Ipeak*(1.0+(t_peak-t)/t_peak)

#try:
dxdt_guess=zeros(model.n_eq)
dxdt=zeros(model.n_eq)
x=zeros(model.n_eq)

for i in range(n_step):
   
    It=I_at_time(time+dt)
    
    flag=True
    cnt=0
    
    while True :
        
        err=model.evaluate(dxdt,x,dxdt_guess,It,dt)
        
        print cnt,"  Err=",err
        cnt+=1
        if err < tol or cnt>5:
            break
  
  
        
    dxdt[:]=dxdt_guess
    x[:]=x+dt*dxdt
    tt=copy.deepcopy(dxdt[model.n_node:model.n_node+n_plot_x])
    plot.drawX(0,xx,tt)
    
    times.append(time)
    jj.append(tt)
    tt= -dxdt[:n_plot_x]
    ee.append(tt)
    plot.drawX(1,xx,tt)
    plot.redraw(" Time={} ".format(time))
    #print dxdt
    time+=dt

