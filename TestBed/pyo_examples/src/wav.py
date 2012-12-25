from pyo import *
s = Server().boot()
s.start()
t = LinTable([(0,0), (2,1), (5,0), (8191,0)])
met = Metro().play()
pick = TrigEnv(met, table=t, dur=1)
w = Waveguide(pick, freq=[200,400], dur=20, minfreq=20, mul=.5).out()
s.gui(locals())

