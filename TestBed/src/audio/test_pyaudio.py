import wave
import struct
from numpy import *
from matplotlib.pyplot import * 
from pylab import *
import pyaudio




fname="../castanets.wav"

wav = wave.open (fname, "r")

(nchannels, sampwidth, Fs, nframes, comptype, compname) = wav.getparams ()

frames = wav.readframes (nframes * nchannels)

       
       
print (nchannels, sampwidth, Fs, nframes, comptype, compname)


p = pyaudio.PyAudio()

# open stream
stream1 = p.open(format =
              p.get_format_from_width(wav.getsampwidth()),
              channels = nchannels,
              rate = Fs ,
              output = True)

print type(frames)

#stream1.write(frames);



# open stream
#stream1 = p.open(format =
#                p.get_format_from_width(wav.getsampwidth()),
#                channels = nchannels,
#                rate = Fs ,
#                output = True)

#stream1.write(frames);

def everyOther (v, offset=0):
   return [print ]


if nchannels == 2:
    print " EO TRUE"
    eo=everyOther(frames)
    leo=list(eo)
    left=array(leo)

# open stream
stream2 = p.open(format =
                p.get_format_from_width(wav.getsampwidth()),
                channels = 1,
                rate = Fs ,
                output = True)

stream2.write(frames);


left=left/34000.0

#plot(left)

NFFT = 1024       # the length of the windowing segments

# Pxx is the segments x freqs array of instantaneous power, freqs is
# the frequency vector, bins are the centers of the time bins in which
# the power is computed, and im is the matplotlib.image.AxesImage
# instance

nPoint=len(left)
step=NFFT/2
nChunk=nPoint/step-1

y=zeros(nPoint,left.dtype)

for i in range(nChunk):
    i1=i*step
    i2=i1+NFFT
    x_chunk =left[i1:i2]
    X=fft(x_chunk)
    y_chunk=real(ifft(X))
    y[i1:i2] += y_chunk
    
y *=0.5


dt=1.0/Fs
tmax=dt*len(left)
t=arange(0.0,tmax,dt)
print Fs
x=left
ax1 = subplot(211)
plot(t,x)
subplot(212, sharex=ax1)
Pxx, freqs, bins, im = specgram(x, NFFT=NFFT, Fs=int(Fs), noverlap=900)


show()       
