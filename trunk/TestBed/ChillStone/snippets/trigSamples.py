
from pyo import *
import array
import math

srate=44100.0
dur=1.0

buffersize=32
s = Server(sr=srate, nchnls=2, buffersize=buffersize, duplex=0).boot()


nSamps=int(srate)
freq=500

samps=[0]*nSamps

for i in range(nSamps):
	samps[i]=math.sin((freq*2*math.pi*i)/srate)*float((i-nSamps+1))/nSamps

tab=NewTable(length=dur,chnls=1,init=samps)


beat =  Metro(1).play()

tr2 = TrigEnv(beat, table=tab)

tr2.out()


s.gui(locals())