from pyo import *
s = Server().boot()
initvals = [350,360,375,388]
maps = [SLMap(20., 2000., 'log', 'freq', initvals), SLMapMul(.2)]
a = Sine(freq=initvals, mul=.2).out()
a.ctrl(maps)  
s.gui(locals())      
