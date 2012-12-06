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



pulses=[]

#input = Metro(1)

bpm=60.0
beatDur=60.0/bpm
ticks_per_beat=beatDur*srate

print ticks_per_beat

trig=Trig()
bar_samp_count=Count(trig,min=0,max=int(ticks_per_beat))


#p=Print(bar_samp_count)



pulsesI = []
npulses=8

for i in range(npulses):
    pulsesI.append(int(i*(ticks_per_beat/npulses)))

print pulses

pulse_tick = Compare(bar_samp_count,pulses,mode="==")

print len(pulse_tick)

for p in pulse_tick:
    pulse.append(p)





n=1
print "Hello"
genes=GeneList(n)

print "Hello 2"
choir=Choir(input,genes)

print "Hello"
def x():
    genes=GeneList(n)
    choir.rebuild(genes)




trig.play(delay=.5)



s.gui(locals())