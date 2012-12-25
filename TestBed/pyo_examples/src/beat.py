from pyo import *
s = Server().boot()
s.start()
t = CosTable([(0,0), (100,1), (500,.3), (8191,0)])
beat = Beat(time=.125, taps=16, w1=90, w2=50, w3=35, poly=1).play()
trmid = TrigXnoiseMidi(beat, dist=12, mrange=(60, 96))
trhz = Snap(trmid, choice=[0,2,3,5,7,8,10], scale=1)
tr2 = TrigEnv(beat, table=t, dur=beat['dur'], mul=beat['amp'])
a = Sine(freq=trhz, mul=tr2)
lfo = Sine(freq=1, mul=.5, add=.5)
p = Pan(a,outs=2,pan=lfo).out()
s.gui(locals())

