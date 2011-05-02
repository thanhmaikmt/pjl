import numpy as N
import wave
import pyaudio
import pylab as P
import player as PP



# d2x/dt2   + 2 damp w0 dx/dt + w0^2 x = F/m
#
#  y=x    z=dx/dt
#
#  dv/dt = - 2 damp w0 v - w0^2 x + F/m
#  dx/dt =  v

rate=44100.0

damp=0.1
freq=400
duration=1./freq
w0=freq*2*N.pi
samples = duration*rate

dt=1.0/rate

state=complex(0,1)

j=complex(0,1.0)

dRadPerHertz=2*N.pi/rate

dstate=N.exp(dRadPerHertz*freq*j)

nStep=int(duration*rate)

dt=1/rate

xa=N.zeros(nStep,N.float)

for i in range(nStep):
    state*=dstate
    xa[i]=N.real(state)
    


from matplotlib.pyplot import * 
plot(xa)
show()    
player=PP.Player()

peak=N.max(xa)
xa *= 16000.0/peak
player.play(xa)

