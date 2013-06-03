#!/usr/bin/env python
# encoding: utf-8
#
# showing how pipes can be used to run a beat analysis thread

"""

 Fronm the client

 self.proc=subprocess.Popen(["python -i beatserver.py"], shell=True,
                                       stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)
            
            
#            ,
#                                       stderr=subprocess.STDOUT,
#                                       stdout=        self.pipe.subprocess.PIPE)
            
            self.pipe   = self.proc.stdin
            self.stdout = self.proc.stdout
            
        
        tt = time stamp
        
        self.pipe.write("stomper.add_event("+str(tt)+",1.0)")    
"""


import numpy 
import numpy.fft
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
        # print ptr_next,ptr_now          
        
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
        if graph:
            self.t=numpy.linspace(0, (n-1)*dt,num=self.n)
            self.plot=plotter.Plotter(self.t)
            
        self.win=numpy.bartlett(nspread)
        
    def doit(self):
        #print "DOIT",self.stomper.buf.get_window()
        
        x=self.stomper.buf.get_window()
       # X=numpy.fft.rfft(x)
        y=numpy.correlate(x, x, mode="full")
        z1=numpy.convolve(y, self.win, mode="same")
        z=z1[self.n-1:]
        bet=self.findBeat(z)
       
        if graph:
            max_val=numpy.max(z)
            if max_val >1.0:
                z *= (1./max_val)   
                
        
            if bet > 0:
                bpm="BPM = " +str(round(60.0/bet))
            else:
                bpm="BPM = ?"
            
            self.plot.draw(z,bpm) 
        
        print bet    
        
    def findBeat(self,z):  
        
        mmm=0.0
        iii=0
        for i in range(nnMin,nnMax):
            if z[i] > mmm:
                iii=i
                mmm=z[i]
                
        return iii*dt
        
def stomp(time):
    stomper.add_event(time,1.0)
    analysis.doit()
   


import getopt

import sys
graph=False
test_me=False
for arg in sys.argv[1:]:
    if arg =='-g':
        graph=True

    if arg =='-t':
        test_me=True

spread=.2 
dt=.02   
nspread=int(spread/dt) 
T=6.0

bpmMax=200
bpmMin=50

periodMax=60.0/bpmMin
periodMin=60.0/bpmMax

nnMax=int(periodMax/dt)
nnMin=int(periodMin/dt)


n=int(T/dt)
buf=circularbuffer.CircularBuffer(n)
stomper= Stomper(buf,dt)
analysis=Analysis(stomper)


## --- test code 
if test_me:
    tt=0.0
    while True:
        time.sleep(1)
        stomper.add_event(tt,1.0)
        analysis.doit()
        tt+=0.5
    
        
    
    