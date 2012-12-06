#!/usr/bin/env python
# encoding: utf-8
"""
Attack detector.

"""
from pyo import *

rate=44100
s = Server(sr=rate, nchnls=8, buffersize=512, duplex=1).boot()
#s.start()


ABSTIME1 = 0

len=100


tt=Trig()
ind = Count(tt.play())




    # Accumulates times between triggers
def accum():
        global ABSTIME1
        ABSTIME1 += elapsed.get()*rate
        ABSTIME2 = ind.get()
        print ">>" , ABSTIME1, ABSTIME2-ABSTIME1
   

rnd = RandDur(min=0.5, max=2)
thresh = Change(rnd)
start = Trig().play()
trigs = Clip(thresh + start)

p = Print(trigs,method=1)

elapsed = Timer(trigs, trigs)
call = TrigFunc(trigs, function=accum)


s.gui(locals())
