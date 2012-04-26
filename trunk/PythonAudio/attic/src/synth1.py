import numpy as N
import wave
import pyaudio
import pylab as P
import player
import spectral as S

duration=.5
rate=44100
samples = duration*rate

fftSize=64
winSize=fftSize
chunkSize=winSize/2

s=S.Spectral(fftSize)


X1=s.freqVect();   

nF=20
X1[nF]=1.0;
X1[winSize-nF]=fftSize*16000.0;

R=s.freqVect()   

j=complex(0.0,1.0)

for i in range(winSize):
    R[i]=N.exp(j*N.pi*i)

   
yChunk=s.tVect()   

y=N.zeros(samples,N.float)   

player= player.Player()

nChunks = int(samples/chunkSize)

w=s.hanning()
W=P.fft(w)

P.plot(abs(W))
P.show()
    
for i in range(nChunks-1):
    i1=i*chunkSize
    i2=i1+winSize
    
    z=N.double(P.ifft(X1))
    y[i1:i2] += z*w
    X1 *= R
    

player.play(y)

