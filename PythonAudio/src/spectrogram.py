import wave
import struct
from numpy import *
from matplotlib.pyplot import * 
from pylab import *
import pyaudio 


def everyOther (v, offset=0):
   return [v[i] for i in range(offset, len(v), 2)]



fname="../castanets.wav"

wav = wave.open (fname, "r")
(nchannels, sampwidth, Fs, nframes, comptype, compname) = wav.getparams ()
frames = wav.readframes (nframes * nchannels)
out = struct.unpack_from ("%dh" % nframes * nchannels, frames)

# Convert 2 channles to numpy arrays
if nchannels == 2:
       left = array (list (everyOther (out, 0)))
       right = array (list  (everyOther (out, 1)))
else:
       left = array (out)
       right = left
       

left=left/34000.0

#plot(left)

NFFT = 1024       # the length of the windowing segments

# Pxx is the segments x freqs array of instantaneous power, freqs is
# the frequency vector, bins are the centers of the time bins in which
# the power is computed, and im is the matplotlib.image.AxesImage
# instance

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