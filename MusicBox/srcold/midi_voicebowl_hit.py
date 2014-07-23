from pyo import *

pm_list_devices()

num=1
# num = input("Enter your Midi interface number : ")



s = Server()

# before start
s.setMidiInputDevice(num)

s.boot().start()

#ctrlnumbs=[108,109,110]

notes=Notein(poly=8, scale=1, first=0, last=127)

noise=Noise()
env=MidiAdsr(notes['velocity'], attack=0.001, decay=0.02, sustain=0.00, release=0.01, mul=1, add=0)


#p=Print(notes['pitch'],1)

det=Sig(0.0)

fxL = AllpassWG(env*noise, freq=notes['pitch']*1.001, feed=.9999, detune=det, mul=.25).mix(1).out(0)
fxR = AllpassWG(env*noise, freq=notes['pitch']*.9999, feed=.9999, detune=det, mul=.25).mix(1).out(1)

s.gui(locals())

