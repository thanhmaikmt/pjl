import os
import glob

from pyo import *


pm_list_devices()

s = Server()
idev=5
s.setMidiInputDevice(idev)
s.boot()

amps=[]
ctrlnumbs=[107,108,109,110]

for c in ctrlnumbs:
    amps.append(Midictl(c))


loops=(("part1",0,.5),("part1",4.66,0.3),("part1",9.32,.07))

oneshot=("impro1",)

path="../samples"

samps=[]
tables=[]
notes=[]
trigs=[]
envs=[]
oscs=[]
pans=[]

cnt=60

for name in oneshot:
    infile=os.path.join(path, name+'.wav')
    print "current file is: " + infile
 
    tab=SndTable(path=infile)
    tables.append(tab)
    dur=tab.getDur()
    freq = tab.getRate()
    note = Notein(poly=1, scale=1, first=cnt, last=cnt)
    notes.append(note)

    trig=Thresh(note['velocity'])
    trigs.append(trig)
    env=TrigEnv(trig,tab,dur=dur,mul=note['velocity']).out()
    envs.append(env)
    cnt+=1

doPan=True

for loop,amp in zip(loops,amps):
    infile=os.path.join(path, loop[0]+'.wav')
    print "current file is: " + infile
 
    tab=SndTable(path=infile)
    tables.append(tab)
    dur=tab.getDur()
    freq = tab.getRate()
    osc = Osc(tab, freq=1.0 / dur)   #,mul=amp)
    oscs.append(osc)#
    
    if doPan:
        pp=SPan(osc)  # ,pan=loop[2])
        pans.append(pp)
        pp.out(delay=loop[1])
    else:
        osc.out(delay=loop[1])
    cnt+=1

s.gui(locals())
