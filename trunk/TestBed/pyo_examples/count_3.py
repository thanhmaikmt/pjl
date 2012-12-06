from pyo import *
from time import *

rate=44100

s = Server(sr=rate, nchnls=8, buffersize=1024, duplex=1).boot()

MIN_THRESH = -40   # Minimum threshold in dB 

inp = Input([6])

ABSTIME1 = 0
ABSTIME3 = 0
len=100


#tab = NewTable(length=len,chnls=1)
#rec = TableRec(inp,table=tab,fadetime=0.1)
#rec.play()
#p1 = TableRead(tab,freq=1./len, interp=1).out(delay=.01)
#osc = Osc(tab, freq=1./len, interp=1)
#osc.out(delay=.01)

t0=None

def accum():
        global ABSTIME1,ABSTIME3,t0
        tnow=time()
        if t0 == None:
            t0 = tnow
        
        #print time0
        ABSTIME3=(tnow-t0)*rate
        
        ABSTIME1 += elapsed.get()*rate
        ABSTIME2 = ind.get()
        print ">>" , ABSTIME1-ABSTIME2, ABSTIME2-ABSTIME3,ABSTIME3-ABSTIME1
     

# Input rms value

rms = Follower2(inp, risetime=0.1, falltime=.1, mul=.5)

rms_db = AToDB(rms)
ref = MIN_THRESH

thresh = Thresh(rms_db,threshold=ref)

useRandTrig=False  # True works OK

if useRandTrig:
    rnd = RandDur(min=0.5, max=2)
    thresh = Change(rnd)

start = Trig()#ind = Count(start.play())
trigs = Clip(thresh + start)
ind = SampHold(Count(start.play()), trigs, 1.0)

#p = Print(trigs,method=1)

elapsed = Timer(trigs, trigs)
call = TrigFunc(trigs, function=accum)

s.gui(locals())