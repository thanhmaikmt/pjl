#!/usr/bin/env python
# encoding: utf-8

"""
Scan for Midi controller numbers. Launch this script from a terminal.

"""
from pyo import *
import numpy as np
import time
import circularbuffer
import math
import plotter

pm_list_devices()

#num = input("Enter your Midi interface number : ")

rate=44100.0
s = Server(sr=rate)
s.setMidiInputDevice(3)
s.boot()   #.start()

notes = Notein(poly=4,scale=1)
trigs=notes['velocity']


class Stomper:
    
    def __init__(self,buf,dt):
        self.events=[]
        self.buf=buf
        self.dt=dt;
        self.time=0
        
    def add_event(self,time,val):
        ptr_next=math.floor(time/self.dt)
        ptr_now=self.buf.get_count()
                  
        
        if ptr_now == ptr_next:
            val_old=self.buf.get_head()
            if (val > val_old):
                self.buf.replace(val)
        else:
            while ptr_now < ptr_next: 
                self.buf.append(0.0)
                
            self.buff.append(val)
        
        

class Analysis:
    
    
    def __init__(self,stomper):
        self.stomper=stomper 
        dt=stomper.dt
        n=stomper.buf.N
        self.t=np.linspace(0, (n-1)*dt,num=n)
        self.plot=plotter.Plotter(self.t)
        
    def doit(self):
        print "DOIT"
        self.plot.draw(self.stomper.buf.get_window())
        
    
class EventStamper:

    """
    Creates a trigger that  repeats periodically.
    """
    
    def __init__(self,stomper,trig):
        #self.ref   = None
        #self.period= None
        #self.on    = on
        #self.snd   = snd
        #self.trig  = Trig().stop()
        #self.delay = Delay(self.trig,maxdelay=2.0,feedback=1)
        #self.tr    = TrigEnv(self.delay,table=snd)
        #self.tr.out()

        # create a counter that samples an holds on triggers on in stream
        self.start=Trig()
        self.count=Count(self.start.play())
        self.samp=SampHold(self.count,trig,1.0)
        self.onfunc=TrigFunc(trig,function=self.eventProc,arg=1.0)
        self.stomper=stomper

    def eventProc(self,val):
        time=self.samp.get()/rate
        self.stomper.add_event(time,val)
        
            
on = Thresh(notes['velocity'].mix(1))
     
dt=.1
buf=circularbuffer.CircularBuffer(100)
stomper= Stomper(buf,dt)
meter = EventStamper(stomper,on)
gui_trig=Metro(.5)
gui_trig.play()
analysis=Analysis(stomper)

gui_func=TrigFunc(gui_trig,function=analysis.doit)


s.gui(locals())