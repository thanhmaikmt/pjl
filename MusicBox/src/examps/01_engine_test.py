import sys
sys.path.append('../MB')

import MBmusic
import time

def callback():
    print time.time()-tref
    

dt=1.0
engine=MBmusic.Engine(dt,callback)
tref=time.time()
engine.start()

