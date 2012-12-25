from pyo import *


from pyo import *

s = Server(sr=44100, nchnls=8, buffersize=64, duplex=1, audio="portaudio", jackname="pyo")
s.boot()
s.start()
aL = Input(chnl=7)
aL.out(chnl=1)
aR = Input(chnl=6)
aR.out(chnl=0)

print s.getBufferSize()
#b = Delay(a, delay=.25, feedback=.5, mul=.5).out()


s.gui(locals())

