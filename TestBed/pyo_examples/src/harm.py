from pyo import *
s = Server().boot()
s.start()
sf = SfPlayer(SNDS_PATH + '/transparent.aif', loop=True, mul=.5).out(0)
harm = Harmonizer(sf, 4)
m= harm.mix(voices=2)
m.out() # .out(1)
s.gui(locals())