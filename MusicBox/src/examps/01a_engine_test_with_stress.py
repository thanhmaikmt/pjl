import sys
sys.path.append('../MB')
import MBmusic
import time

cnt=0
tref=None
def callback():
    global cnt,tref
    if tref==None:
        tref=time.time()

    print (time.time()-tref)-cnt
    cnt+=1

dt=1.0
engine=MBmusic.Engine(dt,callback)


engine.start()



def f():
    x=0.1

    import math
    while True:
        x=math.cos(x+1)

print "Hello"

import multiprocessing


p = multiprocessing.Process(target=f)
p.deamon=True
p.start()
p.join()

