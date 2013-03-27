#!/usr/bin/env python
# encoding: utf-8

"""
Scan for Midi controller numbers. Launch this script from a terminal.

"""
from pyo import *
import time

    
pm_list_devices()

#num = input("Enter your Midi interface number : ")

rate=44100.0
s = Server(sr=rate)
s.setMidiInputDevice(3)
s.boot()   #.start()

notes = Notein(poly=4,scale=1)

snd = SndTable('../snds/alum1.wav')
trigs=notes['velocity']


class AutoMetro:

    """
    Creates a trigger that  repeats periodically.
    """
    
    def __init__(self,on,snd):
        self.ref   = None
        self.period= None
        self.on    = on
        self.snd   = snd
        self.trig  = Trig().stop()
        self.delay = Delay(self.trig,maxdelay=2.0,feedback=1)
        self.tr    = TrigEnv(self.delay,table=snd)
        self.tr.out()

        # create a counter that samples an holds on triggers on in stream
        self.start=Trig()
        self.count=Count(self.start.play())
        self.samp=SampHold(self.count,self.on,1.0)
        self.onfunc=TrigFunc(self.on,function=self.eventProc)


    def eventProc(self):
        time=self.samp.get()/rate
        print "BEAT ",time
       
        if self.ref == None:
            self.ref=time
            print "refSet"
            return

        if self.period == None:
            self.period = time - self.ref
            print " BPM=", 60.0/self.period
            self.delay.setDelay(self.period)
            self.delay.reset()
            self.trig.play()
            return


            
on = Thresh(notes['velocity'].mix(1))

meter = AutoMetro(on,snd)

s.gui(locals())