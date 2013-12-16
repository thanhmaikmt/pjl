from pyo import *
import numpy
import time

srate=44100.0
chunkSize=256
s=Server(sr=srate,duplex=0,buffersize=chunkSize).boot().start()

T=chunkSize/srate
chunkF=1.0/T

phi=0.0
dt=1.0/srate
freq=400.0
dphi=freq*dt*2.0*numpy.pi
samps=numpy.zeros(chunkSize,dtype=float)
x=numpy.zeros(chunkSize,dtype=float)

print len(samps)

count=0
t1c=time.clock()
t1u=time.time()
phis=numpy.arange(chunkSize,dtype=float)*dphi
DPHI=dphi*chunkSize

def reco():
    #print "reco"
    global phi,count,t1c,t1u
    
    x[:]=numpy.sin(phis+phi)*numpy.cos((phis+phi)/100)    
    samps[:]=x/numpy.sqrt(1+x*x)
    phi+=DPHI
    tab.replace(samps.tolist())
    count+=1
    if count % 500 == 0:
        t2c=time.clock()
        t2u=time.time()
        print (t2c-t1c)/(t2u-t1u)
        t1c=t2c
        t1u=t2u

tab=NewTable(length=T,chnls=1,init=samps.tolist())
reader=TableRead(tab,freq=chunkF,interp=1,loop=1).play()
reader.out()
func=TrigFunc(reader['trig'],reco)
print tab.getSize()

s.gui(locals())
