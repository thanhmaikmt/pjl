from pyo import *
import math
import time
import os
import glob
import load

s=Server(sr=44100,duplex=0).boot()


name = "nessaAllTrim.wav"
path = "../samples"
   
   
name="BD TI.wav" 

infile = os.path.join(path, name)
print "current file is: " + infile
 

table = SndTable(path=infile)
dur = table.getDur()

trig=Trig().stop()

osc=TrigEnv(trig,table, dur, interp=2, mul=1 ).out()

stress=load.StressMonitor()
metro=Metro(1).play()

def doit():
    print stress.doit()
    
trigFunc=TrigFunc(metro,doit)

s.gui(locals())
