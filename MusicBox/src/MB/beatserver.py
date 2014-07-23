#!/usr/bin/env python
# encoding: utf-8
#
# showing how pipes can be used to run a beat analysis thread

"""

 From the client

 self.proc=subprocess.Popen(["python -i beatserver.py"], shell=True,
                                       stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE)
            
            
#            ,
#                                       stderr=subprocess.STDOUT,
#                                       stdout=        self.pipe.subprocess.PIPE)
            
            self.pipe   = self.proc.stdin
            self.stdout = self.proc.stdout
            
        
# to do a beat 
            self.pipe.write("stomper.add_event("+str(time_stamp)+",1.0)") 
            
            the beat is inserted into the circular buffer and we do an autcorrelation on the buffer.
            Some processing is done to find the peaks in the autocorreleation.
            For each event sent to the server it returns a list of  [time,peak]  pairs via the pipe.
            
"""


import numpy 
import numpy.fft
import time
import circularbuffer
import math
import plotter

class Stomper:
    """
    Kepps a history of events in a quatized circular buffer
    
    
    
    """
    
    def __init__(self,dt,dur):
        
        assert dur > dt
        self.events=[]
        n=(int)(dur/dt+1)
        self.buf=circularbuffer.CircularBuffer(n)
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
        self.t=numpy.linspace(0, (self.n-1)*dt,num=self.n)
        self.plot=None
            
        self.win=numpy.bartlett(nspread)
        
    def doit(self):
        #print "DOIT",self.stomper.buf.get_window()
   
        if graph and (self.plot == None):
            self.plot=plotter.Plotter(self.t)
            # print "   Initing a graph "
                 
        x=self.stomper.buf.get_window()
       # X=numpy.fft.rfft(x)
        z1=numpy.correlate(x, x, mode="full")
        #z1=numpy.convolve(y, self.win, mode="same")
        z=z1[self.n-1:]
        self.find_peaks(z)
        self.filter_peaks()
      #  bet=self.find_beat(self.times2,self.peaks2)
       
        if graph:
#            max_val=numpy.max(z)
#             if max_val >1.0:
#                 z *= (1./max_val) 
#                 if self.peaks!=None:
#                     self.peaks *=(1./max_val)   
            bpm="BPM="
            for t in self.times2:
                
                tt=60.0/t
                if tt < 40.0:
                    break
                
                bpm+="{:4.1f} ".format(tt)
#             
#             if bet > 0:
#                 bpm="BPM = " +str(round(60.0/bet))
#             else:
#                 bpm="BPM = ?"
#             
            self.plot.draw(z,bpm,self.times2,self.peaks2) 
            #self.plot.draw(z,bpm) 
        
        sys.stdout.write("[")
        sep=""
        for t,p in zip(self.times2,self.peaks2):
            sys.stdout.write(sep+"["+str(t)+","+str(p)+"]")
            sep=","
            
        sys.stdout.write("]\n")

     
    def add_average_peak(self,bt,bp):
         
        sum=0
        sumt=0
        for p,t in zip(bp,bt):
            sum  += p
            sumt += p*t
    
        tav=sumt/sum
        self.peaks2.append(sum)
        self.times2.append(tav)

    #    print (bp)
    #    print (bt)
    #    print "TAV=",tav
    
                
    def filter_peaks(self):   
        self.peaks2=[]
        self.times2=[]
        
        t1=-100.0
        p1=0
        gap=.1
        
        bp=None
        bt=None

        for p,t in zip(self.peaks,self.peakst):
            if t - t1 > gap:
                if bp != None:
                    self.add_average_peak(bt,bp)
                
                bp=[]
                bt=[]
                t1=t

            bp.append(p)
            bt.append(t)

        if bp != None:
            self.add_average_peak(bt,bp)

            
    def find_peaks(self,z,minI=None,maxI=None):
        self.peaks=[]
        self.peakst=[]
        noise_level=.1
        if minI == None:
            minI=1
            
        if maxI==None:
            maxI=len(z)-2
            
        for i in range(minI+1,maxI-1):
            if z[i-1]<=z[i]>=z[i+1] and z[i] > noise_level: 
                self.peaks.append((z[i]))
                self.peakst.append(self.t[i])
                
#     def find_beat(self,ts,zs):  
#         mmm=0.0
#         period=-1
#         
#         for z,t in zip(zs,ts):
#             if t < periodMin:
#                 continue
#             elif t> periodMax:
#                 break
#      
#             if z > mmm:
#                 mmm=z
#                 period=t
#     
#             
#         return period
        
def stomp(time):
    stomper.add_event(time,1.0)
    analysis.doit()
   


import getopt

import sys

graph=False
test_me=True

for arg in sys.argv[1:]:
    if arg =='-g':
        graph=True

    if arg =='-t':
        test_me=True

spread=.2 
dt=.02   
nspread=int(spread/dt) 
T=6.0

bpmMax=180
bpmMin=40

periodMax=60.0/bpmMin
periodMin=60.0/bpmMax

nnMax=int(periodMax/dt)
nnMin=int(periodMin/dt)

stomper= Stomper(dt,T)
analysis=Analysis(stomper)



    
    