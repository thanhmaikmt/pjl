from pyo import *
s = Server().boot()
s.start()
#t = CurveTable([(0,0.0),(512,0.97),(1024,-0.94),(1536,0.0),(8192,0.0000)])



#t.graph()
noise=Noise()
lpf=Biquad(noise, freq=100, q=20, type=2)

noise.ctrl()
lpf.ctrl()

fx = AllpassWG(lpf, freq=1, feed=.999999, detune=0.0, mul=.25)

fx.out()

s.gui(locals())

