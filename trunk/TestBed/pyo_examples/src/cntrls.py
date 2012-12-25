
from pyo import *
import random
s = Server().boot()
s.start()
fr = Sig(value=100)
#p = Port(fr, risetime=0.001, falltime=0.001)
a = SineLoop(freq=fr, feedback=0.08, mul=.3).out()
b = SineLoop(freq=fr, feedback=0.08, mul=.3).out(1)

map = SLMap(100., 10000., 'lin', 'value', 100.0)

fr.ctrl([map])
 
 
pr=Print(fr).play() 

s.gui(locals())