import pyo 
 
srate=44100.0
s=pyo.Server().boot().start()


def trighandler(id):
    print id
    on.setValue(id)

dur=1.0
delay1=0.2
trigs=[]
trigs.append(pyo.Metro(dur))
trigs.append(pyo.SDelay(trigs[0],delay=delay1))

trigFuncs=[]
for i in range(len(trigs)):
    trigFuncs.append(pyo.TrigFunc(trigs[i],trighandler,arg=i))


freq=pyo.Sig(400)

on=pyo.Sig(0)

e=pyo.MidiAdsr(on, attack=0.001, decay=0.005, sustain=0.70, release=0.010)

hifreq=srate

b1=pyo.LFO(freq=freq,mul=e)

v=pyo.Biquad(input=b1,freq=1000, q=2, type=2).out()

#
#f1.ctrl()
#f2.ctrl()
#f3.ctrl()
b1.ctrl()

e.ctrl()
v.ctrl()
trigs[0].play()

s.gui(locals())