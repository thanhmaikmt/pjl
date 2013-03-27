import os
import glob

from pyo import *

s = Server()
s.boot()

loops=(("part1",0),("impro1",4.66))

samps=[]
tables=[]
oscs=[]
pans=[]


doPan=True

for loop in loops:
    infile=os.path.join("../samples", loop[0]+'.wav')
    print "current file is: " + infile
 
    tab=SndTable(path=infile)
    tables.append(tab)
    dur=tab.getDur()
    osc = Osc(tab, freq=1.0 / dur)
    osc.play(delay=loop[1])

    oscs.append(osc)
        
    pp=SPan(osc)
    pans.append(pp)
    pp.out()
  

s.gui(locals())
