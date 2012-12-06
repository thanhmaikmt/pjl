from pyo import *

count=0

def foo():
    global count
    if count >=0:
        for i in range(10):
            print m.get(count,i), 
        print
    count = count+1


srate=44100
s = Server(sr=srate).boot()

# change this path to link to an existing sound on the computer
son = '../snds/baseballmajeur_m.aif'
info = sndinfo(son)
a = SfPlayer(son, mul=.25).mix(1).out()

dur  = 10*60
size = 512
nframe=(dur*srate)/size
#m = NewMatrix(width=size, height=nframe)  # info[0]/size)
m = NewMatrix(width=size, height=info[0]/size)

fin = FFT(a[0]*100, overlaps=1)
mag = Sqrt(fin["real"]*fin["real"] + fin["imag"]*fin["imag"])
#rec = MatrixRec(mag*2-1, m, 0).play()
rec = MatrixRec(mag, m, 0).play()
#metro= Metro(float(size)/srate)
#func=TrigFunc(metro,foo)
metro.play()

s.gui(locals())