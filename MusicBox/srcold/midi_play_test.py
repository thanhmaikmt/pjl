from pyo import *

pm_list_devices()

rate=44100.0
s = Server(sr=rate)
s.setMidiInputDevice(9)

s.boot()   

notes = Notein(poly=4,scale=1,first=60, last=72)

pp=Print(notes['pitch'],method=1)

trigs=notes['velocity']
freqs=notes['pitch']

env = MidiDelAdsr(trigs, delay=.0, attack=.05, decay=.51, sustain=.8, release=1)

b = Sine(freq=freqs, mul=env)

b.out()

env.ctrl()

s.gui(locals())