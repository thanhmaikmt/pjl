import os
import glob

from pyo import *

s = Server()
s.boot()

loops=(("part1",0),("impro1",0.5))

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
    oscs.append(osc)
        
    if doPan:farnell
    
        pp=SPan(osc)
        pans.append(pp)
        pp.out(delay=loop[1])
    else:
        osc.out(delay=loop[1])


s.gui(locals())
