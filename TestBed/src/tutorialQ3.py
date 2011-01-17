from  matplotlib.pyplot import *
from math import *
from numpy import *

Fs=40e3
f=5e3
T=1/Fs

def sinc(x): 
    from math import pi, sin 
    try: 
        x = pi * x 
        return sin(x) / x 
    except ZeroDivisionError: # sinc(0) = 1 
        return 1.0 

def H(f):
    return T*sinc(T*f)
    

freqs=[]

for n in range(-2,3):
    freqs.append(n*Fs-f)
    freqs.append(n*Fs+f)


ymin=[]
ymax=[]

fs=arange(-100000,100000,100)


h1=[]
h2=[]

for f in fs:
    h2.append(abs(H(f)))


for f in freqs:
    ymin.append(0.0)
    ymax.append(abs(H(f))*Fs/2.)
    h1.append(Fs/2.0)

subplot(311)
plot(fs,h2)
ylabel("H(f)")
grid()

subplot(312)
vlines(freqs,ymin,h1)
ylabel("X(f)")
grid()

subplot(313)
vlines(freqs,ymin,ymax)
xlabel("f [Hz]")
ylabel("Y(f)")
grid()

show()
