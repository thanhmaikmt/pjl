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
import beatclient

pm_list_devices()

#num = input("Enter your Midi interface number : ")

rate=44100.0
s = Server(sr=rate)
s.setMidiInputDevice(3)
s.boot()   #.start()

notes = Notein(poly=4,scale=1)
trigs=notes['velocity']

def stomp(tt):
    text="stomp("+str(tt)+")"
    client.send(text)
    client.send("analysis.doit()")
        

    
class EventStamper:

    """
    Creates a trigger that  repeats periodically.
    """
    
    def __init__(self,trig):
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

    def eventProc(self,val):
        time=self.samp.get()/rate
        stomp(time)
            
client=beatclient.Client()

on = Thresh(notes['velocity'].mix(1))
     
dt=.1
buf=circularbuffer.CircularBuffer(100)

meter = EventStamper(on)


s.gui(locals())