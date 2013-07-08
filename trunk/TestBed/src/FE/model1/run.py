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

state_guess=model.make_state_vec()

state_2=model.make_state_vec()


def I_at_time(t):
    #return Ipeak

    if t<=t_peak:
        return Ipeak*t/t_peak
    else:
        return Ipeak*(1.0+(t_peak-t)/t_peak)

#try:


for i in range(n_step):
   
    It=I_at_time(time+dt)
    
    flag=True
    cnt=1

    state_cnt_neg=model.make_state_vec()
    state_cnt_zero=model.make_state_vec()
    state_cnt_pos=model.make_state_vec()
    
    while True :
        
        model.evaluate_guess(state_guess,It,dt)
        model.guess_to_state(model.dxdt_guess,state_2,state_guess)
        
        cnt=0  
        for i in range(model.n_node):
            s2=state_2[i]
            if s2 == 0:
                state_cnt_zero[i]+=1
            elif s2 <0:
                state_cnt_neg[i]+=1
            elif s2 >0:
                state_cnt_pos[i]+=1
            
            if s2 != state_guess[i]:
                cnt += 1
            
        if cnt == 0:
            break
        
        for i in range(model.n_node):
            cp=state_cnt_pos[i]
            cz=state_cnt_zero[i]
            cn=state_cnt_neg[i]
            if cp >= cz and cp > cn:
                state_guess[i]=1
            elif cn >= cz and cn > cp:
                state_guess[i]=-1
            else:
                state_guess[i]=0
                  
        print cnt
        
    model.advance_to_guess()
        
    tt=copy.deepcopy(model.dxdt[model.n_node:model.n_node+n_plot_x])
    plot.drawX(0,xx,tt)
    
    times.append(time)
    jj.append(tt)
    tt= -model.dxdt[:n_plot_x]
    ee.append(tt)
    plot.drawX(1,xx,tt)
    plot.redraw(" Time={} ".format(time))
    #print dxdt
    time+=dt

