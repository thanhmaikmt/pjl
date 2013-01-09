import os
import glob

from pyo import *

s = Server()
idev=3
s.setMidiInputDevice(idev)
s.boot()


sampName="nessa"
path="../"

samps=[]


for infile in glob.glob( os.path.join(path, sampName'*.fasta') ):
    print "current file is: " + infile
    
for i in 
samp1="../samples/nessa2.wav"

tab=SndTable(path=samp1)
dur=tab.getDur()

freq = tab.getRate()


notes = Notein(poly=8, scale=1, first=0, last=127)   # Notein(poly=4,scale=1)

#t1=Trig().stop()    

t1=Thresh(notes['velocity'])

env=TrigEnv(t1,tab,dur=dur).out()


s.gui(locals())
