from pyo import *



srate=44100.0
s = Server(sr=srate, nchnls=8, buffersize=64, duplex=1).boot()


input=Input([6,7]).out()

pit = Yin(input, tolerance=0.2, winsize=2048)

p=Print(pit,method=1)

s.gui(locals())
