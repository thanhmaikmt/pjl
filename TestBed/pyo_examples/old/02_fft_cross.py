#! /usr/bin/env python
# encoding: utf-8
"""
Performs the cross-synthesis of two sounds.

"""
from pyo import *

s = Server().boot()

snd1 = SfPlayer("../snds/baseballmajeur_m.aif", loop=True).mix(2)
snd2 = FM(carrier=[75,100,125,150], ratio=[.999,.5005], index=20, mul=.4).mix(2)

size = 1024
olaps = 4

fin1 = FFT(snd1, size=size, overlaps=olaps)
fin2 = FFT(snd2, size=size, overlaps=olaps)

# get the magnitude of the first sound
#mag = Sqrt(fin1["real"]*fin1["real"] + fin1["imag"]*fin1["imag"], mul=10)
pol = CarToPol(fin1['real'],fin1['imag'],mul=10)

cepIn =  Log(pol['magn'])



# scale `real` and `imag` parts of the second sound by the magnitude of the first one
real = fin2["real"] * pol['mag']
imag = fin2["imag"] * pol['mag']



fout = IFFT(real, imag, size=size, overlaps=olaps)
ffout = fout.mix(2).out()
#snd2.out()

# change of fft size must be done on all fft and ifft objects at the same time!
def setSize(x):
    fin1.size = x
    fin2.size = x
    fout.size = x

s.gui(locals())

