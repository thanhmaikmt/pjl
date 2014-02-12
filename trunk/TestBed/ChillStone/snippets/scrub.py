"""
Scrubbing in a sound window.
Give the focus to the Scrubbing window then click and move the mouse...

"""

from pyo import *
import os
s = Server(buffersize=512, duplex=0).boot()

def mouse(mpos):
    print "X = %.2f, Y = %.2f" % tuple(mpos)
    pos.value = mpos[0]
    l, r = 1. - mpos[1], mpos[1]
    mul.value = [l, r]


name = "nessaAllTrim"
path = "./samples"
    
infile = os.path.join(path, name + '.wav')
print "current file is: " + infile
 
snd = SndTable(infile).normalize()
snd.view(title="Scrubbing window", mouse_callback=mouse)

mul = SigTo([1,1], time=0.1, init=[1,1], mul=.1)
pos = SigTo(0.5, time=1, init=0.5, mul=snd.getSize(), add=Noise(5))

# gran = Granulator(table=snd, env=HannTable(), pitch=[1.0, 1.0], pos=pos,
#                  dur=Noise(.002, .1), grains=40, basedur=.1, mul=mul).out()
#gran = Granulator(table=snd, env=HannTable(), pitch=[1.0, 1.0], pos=pos,
#                  dur=.5, grains=2, basedur=.5, mul=mul).out()

g2=Granule(table=snd, env=HannTable(), dens=50, pitch=[1,1], pos=pos, dur=0.5, mul=mul, add=0).out()


s.gui(locals())
