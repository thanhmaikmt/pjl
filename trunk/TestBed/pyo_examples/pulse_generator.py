#!/usr/bin/env python
# encoding: utf-8
"""
Hand-written pulsar synthesis.

"""
from pyo import *
import random
import inspect
from voice import *

srate=44100.0
s = Server(sr=srate, nchnls=2, buffersize=512, duplex=0).boot()



class PulsePool:
    
    def __init__(self,bpm):
        self.pulses=[]
        beatDur=60.0/bpm
        ticks_per_beat=beatDur*srate

        print ticks_per_beat

        self.trig=Trig()
        bar_samp_count=Count(self.trig,min=0,max=int(ticks_per_beat))
        self.pulses.append(Compare(bar_samp_count,0,mode="=="))



        #p=Print(bar_samp_count)

    def play(self,delay=0):
        self.trig.play(delay=delay)





bpm=60

pulse_pool=PulsePool(bpm)

n=1
print "Hello"
genes=GeneList(n)

print "Hello 2"
choir=Choir(input,genes)

print "Hello"
def x():
    genes=GeneList(n)
    choir.rebuild(genes)




pulse_pool.play(delay=.5)



s.gui(locals())