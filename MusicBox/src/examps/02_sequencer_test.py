import sys
sys.path.append('../MB')

import MBmusic
import time

dt=0.005   
seq=MBmusic.SequencerBPM()


class Event:
    def fire(self,tt):
        print "fire ,seq.beat,beat,(time.time() - tref)*seq.beats_per_sec"
        print seq.time,tt,(time.time() - tref)    
        

seq.schedule(1.2,Event())
seq.schedule(2.33,Event())
seq.schedule(.04,Event())
seq.schedule(3.25,Event())
seq.schedule(3.25,Event())

tref=time.time()
seq.start()


xx=raw_input("CR")

seq.quit()