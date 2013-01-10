import os
import glob
	
from pyo import *
	
	
pm_list_devices()
	
s = Server()
idev = 3
s.setMidiInputDevice(idev)
s.boot()
	
	
name = "nessaAllTrim"
path = "../samples"
	
infile = os.path.join(path, name + '.wav')
print "current file is: " + infile
 
amp1=1.0
amp2=1.0

tab = SndTable(path=infile)
dur = tab.getDur()
freq = tab.getRate()
osc = Osc(tab, freq=1.0 / dur)
o1=osc*amp1

d1=Sig(4.658)
d1.ctrl([SLMap(4.0,5.0,'lin','delay',4.658)])
dl1=SDelay(osc,delay=d1,maxdelay=5.0)
do1=dl1*amp2


d2=Sig(4.658)
d2.ctrl([SLMap(4.0,5.0,'lin','delay',4.658)])
dl2=SDelay(dl1,delay=d2,maxdelay=5.0)
do2=dl2*amp2

o1.out()
do1.out()
do2.out()


s.gui(locals())
