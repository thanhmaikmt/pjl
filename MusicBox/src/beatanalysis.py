#!/usr/bin/env python
# encoding: utf-8

"""
Scan for Midi controller numbers. Launch this script from a terminal.

"""
from pyo import *
import time
import circularbuffer
import math

pm_list_devices()

#num = input("Enter your Midi interface number : ")

rate=44100.0
s = Server(sr=rate)
s.setMidiInputDevice(3)
s.boot()   #.start()

notes = Notein(poly=4,scale=1)
trigs=notes['velocity']


class Stomper:
    
    def __init__(self):
        self.events=[]
        self.buf=circularbuffer.CircularBuffer(1000)
        self.dt=.1;
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
        self.onfunc=TrigFunc(trig,function=self.eventProc)
        self.stomper=stomper

    def eventProc(self):
        time=self.samp.get()/rate
        self.stomper.add_event(time)
        
            
on = Thresh(notes['velocity'].mix(1))

stomper= Stomper()
meter = EventStamper(stomper,on)

s.gui(locals())