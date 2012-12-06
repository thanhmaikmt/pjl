from pyo import *

rate=44100

s = Server(sr=rate, nchnls=8, buffersize=512, duplex=1).boot()

MIN_THRESH = -40   # Minimum threshold in dB (signal must fall below this

input = Input([6])

ABSTIME1 = 0

len=100

#tab = NewTable(length=len,chnls=1)
#rec = TableRec(inp,table=tab,fadetime=0.1)
#rec.play()

#p1 = TableRead(tab,freq=1./len, interp=1).out(delay=.01)
#osc = Osc(tab, freq=1./len, interp=1)
#osc.out(delay=.01)

def accum():
        global ABSTIME1
        ABSTIME1 += elapsed.get()*rate
        ABSTIME2 = ind.get()
        print ">>" , ABSTIME1, ABSTIME2-ABSTIME1
        global ABSTIME
   

# Input rms value

rms = Follower2(input, risetime=0.1, falltime=.5, mul=.5)

rms_db = AToDB(rms)
ref = MIN_THRESH

thresh = Thresh(rms_db,threshold=ref)

useRandTrig=False

if useRandTrig:
    rnd = RandDur(min=0.5, max=2)
    thresh = Change(rnd)

start = Trig()
ind = Count(start.play())
trigs = Clip(thresh + start)

elapsed = Timer(trigs, trigs)
call = TrigFunc(trigs, function=accum)

s.gui(locals())
