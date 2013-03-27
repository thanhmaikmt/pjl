from pyo import *

pm_list_devices()

num=5
# num = input("Enter your Midi interface number : ")



s = Server().boot()
s.start()
s.setMidiInputDevice(num)

t = CurveTable([(0,0.0),(512,0.97),(1024,-0.94),(1536,0.0),(8192,0.0000)])
t.graph()

src1=Input(6)
#src1.out()

rnd = Randi(min=.97, max=1.03, freq=[.143,.2,.165,.111])
src = Osc(t, rnd*74.79, mul=.5)




rnd2 = Randi(min=.5, max=1.0, freq=[.13,.22,.155,.171])
det = Sig(0.75, mul=rnd2)
rnd3 = Randi(min=.95, max=1.05, freq=[.145,.2002,.1055,.071])
fx = AllpassWG(src, freq=rnd3*[74.87,75,75.07,75.21], feed=1, detune=det, mul=.25).out()

s.gui(locals())

