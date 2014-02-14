from scipy import signal
import numpy

srate=500.
dt=1.0/srate
Fc=50.
ntaps=50

np=50

x=numpy.zeros(np)
tt=numpy.arange(0,np*dt,dt)
x[0]=1.0


freq=Fc/srate


b,a =signal.cheby1(4,1,1,60,analog=True, ftype='cheby1')


y=signal.lfilter(b,a,x)

b=signal.firwin(ntaps,Fc,nyq=srate/2.0)

t=numpy.arange(0,ntaps*dt,dt)

import matplotlib.pyplot as plt

# plt.ion()
plt.plot(tt,y)
plt.show()


