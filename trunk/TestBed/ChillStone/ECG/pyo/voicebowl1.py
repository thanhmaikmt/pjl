from pyo import *
import time
s = Server().boot()
s.start()

t = CurveTable([(0,0.0),(1212,0.5),(2024,-0.2),(3536,0.3),(8192,0.0000)])
t.graph()

noise=Noise(mul=.001)

rnd = Randi(min=.97, max=1.0, freq=[.143,.2,.165,.111,.123])


fr=[]
for i in [0,2,5,7,9]:
    fr.append(MToF(Sig(i+48)))
    
src = Osc(t, freq=fr, mul=.5)



rnd2 = Randi(min=.05, max=.1, freq=[.1,.2,.11,.21,.12])

det = Sig(0.75, mul=rnd2)

rnd3 = Randi(min=.95, max=1.05, freq=[.145,.2002,.1055,.071])


# fx = AllpassWG(src, freq=rnd3*[74.87,75,75.07,75.21], feed=1, mul=.25).out()


mults=[]

for i in range(5):
    mults.append(Sine(0.1,phase=i/5.0,mul=.05,add=.05))

a = Rossler(pitch=.0003, stereo=True, mul=.1, add=.05)
b = Rossler(pitch=fr, mul=a)

fx = AllpassWG(src, freq=fr, feed=rnd, mul=mults,detune=det+noise+b).mix(2)
rev = STRev(fx, inpos=0.25, revtime=20, cutoff=5000, bal=0.25, roomSize=10).mix(2).out()
s.gui(locals())
# time.sleep(100)