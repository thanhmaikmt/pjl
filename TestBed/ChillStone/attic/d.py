from pyo import *
s = Server().boot()
s.start()
a = Trig().stop()

env = HannTable()
tenv = TrigEnv(a, table=env, dur=5, mul=.3)
n = Noise(tenv).out()

s.gui(locals())