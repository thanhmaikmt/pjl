
#!/usr/bin/env python
# encoding: utf-8

"""
Scan for Midi controller numbers. Launch this script from a terminal.

"""
from pyo import *


rate=44100.0
s = Server(sr=rate)
s.boot()

def trigHandler():
            print " beep"
            trig.play(delay=period)

trig = Trig()
period=1
trig.play(delay=period)
trigfunc=TrigFunc(trig,trigHandler)



s.gui(locals())        


            
