from pyo import *
s = Server().boot()
s.start()
snd_path = SNDS_PATH + '/transparent.aif'
t = SndTable(snd_path)
t.view("tranparently")
a = Osc(table=t, freq=t.getRate(), mul=.5).out()
s.gui(locals())

