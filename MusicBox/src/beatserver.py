#!/usr/bin/env python
# encoding: utf-8

import numpy as np
import time
import circularbuffer
import math
import plotter

class Stomper:
    
    def __init__(self,buf,dt):
        self.events=[]
        self.buf=buf
        self.dt=dt;
        self.time=0
        
    def add_event(self,time,val):
        
        
        ptr_next=int(time/self.dt)
        ptr_now=self.buf.get_count()
        print ptr_next,ptr_now          
        
        if ptr_now == ptr_next:
            val_old=self.buf.get_head()
            if (val > val_old):
                self.buf.replace(val)
        else:
            while ptr_now < ptr_next: 
                self.buf.append(0.0)
                #print "0:", self.buf.get_count()
                ptr_now+=1
                
            #print "1:", self.buf.get_count()
            self.buf.append(val)
        
        

class Analysis:
    
    
    def __init__(self,stomper):
        self.stomper=stomper 
        dt=stomper.dt
        self.n=stomper.buf.N
        self.t=np.linspace(0, (n-1)*dt,num=self.n)
        self.plot=plotter.Plotter(self.t)
        
        self.win=np.bartlett(20)
        
    def doit(self):
        #print "DOIT",self.stomper.buf.get_window()
        
        x=self.stomper.buf.get_window()
        y=np.correlate(x, x, mode="full")
        z1=np.convolve(y, self.win, mode="same")
        z=z1[self.n-1:]
        max_val=np.max(z)
        if max_val >1.0:
            z *= (1./max_val)   
                 
        self.plot.draw(z)
        
        #print "DONE"
        
def stomp(time):
    stomper.add_event(time,1.0)
    analysis.doit()
    
dt=.02    
T=15.0
n=int(T/dt)
buf=circularbuffer.CircularBuffer(n)
stomper= Stomper(buf,dt)
analysis=Analysis(stomper)

if False:
    tt=0.0
    while True:
        time.sleep(1)
        stomper.add_event(tt,1.0)
        analysis.doit()
        tt+=0.5
    
        
    
    