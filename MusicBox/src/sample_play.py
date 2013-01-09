import os
import glob

from pyo import *


pm_list_devices()

s = Server()
idev=3
s.setMidiInputDevice(idev)
s.boot()


sampNames=["nessa2","nessa3","nessa4","nessa5","nessa6","nessa7","nessa8","nessa10"]
path="../samples"

samps=[]
tables=[]
notes=[]
trigs=[]
envs=[]

cnt=60
for name in sampNames:
    infile=os.path.join(path, name+'.wav')
    print "current file is: " + infile
 
    tab=SndTable(path=infile)
    tables.append(tab)
    dur=tab.getDur()
    freq = tab.getRate()
    note = Notein(poly=1, scale=1, first=cnt, last=cnt)   # Notein(poly=4,scale=1)
    notes.append(note)

    trig=Thresh(note['velocity'])
    trigs.append(trig)
    env=TrigEnv(trig,tab,dur=dur,mul=note['velocity']).out()
    envs.append(env)
    cnt+=1


s.gui(locals())
