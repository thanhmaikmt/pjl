from pyo import *

s = Server().boot()

# change this path to link to an existing sound on the computer
son = '../snds/baseballmajeur_m.aif'
info = sndinfo(son)
a = SfPlayer(son, mul=.25).mix(1).out()

size = 512
m = NewMatrix(width=size, height=info[0]/size)

fin = FFT(a*100, overlaps=1)
mag = Sqrt(fin["real"]*fin["real"] + fin["imag"]*fin["imag"])
rec = MatrixRec(mag*2-1, m, 0).play()

s.gui(locals())