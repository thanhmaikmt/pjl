
from pyo import *
srate=44100.0
buffersize=32
s = Server(sr=srate, nchnls=2, buffersize=buffersize, duplex=0).boot()

noise=Noise()

excite=Atan2(noise,1)

filt=Biquad(excite)

delay=Delay(excite).out()

noise.setAdd(delay)


excite.ctrl()
noise.ctrl()
delay.ctrl([SLMap(min=.001,max=.1,name='delay',init=.01,scale='log')])


s.gui(locals())
