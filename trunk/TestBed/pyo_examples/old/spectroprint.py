from pyo import *


def foo():
    for y in range(40):
        for x in range(10):
            print m.get(x,y), 
        print
  

srate=44100
s = Server(sr=srate).boot()

# change this path to link to an existing sound on the computer
son = '../snds/baseballmajeur_m.aif'
info = sndinfo(son)
a = SfPlayer(son, mul=.25).mix(1).out()

size = 512
m = NewMatrix(width=size, height=info[0]/size)

fin = FFT(a*100, size=size,overlaps=1)
mag = Sqrt(fin["real"]*fin["real"] + fin["imag"]*fin["imag"])
#rec = MatrixRec(mag*2-1, m, 0).play()
rec = MatrixRec(mag, m, 0).play()

s.gui(locals())