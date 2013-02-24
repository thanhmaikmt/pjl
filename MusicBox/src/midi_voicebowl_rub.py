from pyo import *

pm_list_devices()

num=9
# num = input("Enter your Midi interface number : ")



s = Server()

# before start
s.setMidiInputDevice(num)

s.boot().start()

ctrlnumbs=[107,108,109,110]

feednumb=111
detnumb=112

ctrls=Midictl(ctrlnumbs)
p = Port(ctrls, .02)
fb=Midictl(feednumb)
dc=Midictl(detnumb)

feed=1.0-fb*0.1

ppp1=Print(p,1,message="CTRL")
ppp2=Print(feed,1,message="feed")
ppp3=Print(dc,1,message="detune")

t = CurveTable([(0,0.0),(512,0.97),(1024,-0.94),(1536,0.0),(8192,0.0000)])
t.graph()

src1=Input(6)
#src1.out()

rnd = Randi(min=.97, max=1.03, freq=[.143,.2,.165,.111])
src = Osc(t, rnd*74.79, mul=p)




rnd2 = Randi(min=.5, max=1.0, freq=[.13,.22,.155,.171])
det = Sig(0.75, mul=rnd2)
rnd3 = Randi(min=.95, max=1.05, freq=[.145,.2002,.1055,.071])
fx = AllpassWG(src, freq=rnd3*[74.87,75,75.07,75.21], feed=feed, detune=dc, mul=.2).out()

s.gui(locals())

