from pyo import *



s  = Server().boot()
#Fs = s.getSamplingRate()

#s.start()

src=Input(0)

src.out()

#.mix(2)

dd = Delay(src,delay=[4,2,1],maxdelay=5.0,feedback=[.1,.2,.9])

#delay.play()
dd.out()

#src1.out()

s.gui(locals())

