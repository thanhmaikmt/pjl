from pyo import *
import math
import time

srate=44100.0
chunkSize=256
s=Server(sr=srate,duplex=0,buffersize=chunkSize).boot().start()

T=chunkSize/srate
chunkF=1.0/T

phi=0.0
dt=1.0/srate
freq=400.0
dphi=freq*dt*2.0*math.pi
samps=[0]*chunkSize

print len(samps)

count=0
t1c=time.clock()
t1u=time.time()

def reco():
    #print "reco"
    global phi,count,t1c,t1u
    for i in range(chunkSize):
        x=math.sin(phi)*math.cos(phi/100)
        samps[i]=x/math.sqrt(1+x*x)
        phi+=dphi
    tab.replace(samps)
    count+=1
    if count % 500 == 0:
        t2c=time.clock()
        t2u=time.time()
        print (t2c-t1c)/(t2u-t1u)
        t1c=t2c
        t1u=t2u

tab=NewTable(length=T,chnls=1,init=samps)
reader=TableRead(tab,freq=chunkF,interp=1,loop=1).play()
reader.out()
func=TrigFunc(reader['trig'],reco)
print tab.getSize()

s.gui(locals())
