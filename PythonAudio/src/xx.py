
import numpy as N
import wave

import pyaudio
import sys


class SoundFile:
   def  __init__(self, signal):
       self.file = wave.open('test.wav', 'wb')
       self.signal = signal
       self.sr = 44100

   def write(self):
       self.file.setparams((1, 2, self.sr, 44100*4, 'NONE', 'noncompressed'))
       self.file.writeframes(self.signal)
       self.file.close()

# let's prepare signal
duration = 4 # seconds
samplerate = 44100 # Hz
samples = duration*samplerate
frequency = 440 # Hz
period = samplerate / float(frequency) # in sample points
omega = N.pi * 2 / period

xaxis = N.arange(int(period),dtype = N.float) * omega
ydata = 16384 * N.sin(xaxis)

signal = N.resize(ydata, (samples,))

ssignal = ''
for i in range(len(signal)):
   ssignal += wave.struct.pack('h',signal[i]) # transform to binary


# ssignal = ''.join((wave.struct.pack('h', item) for item in signal))

f = SoundFile(ssignal)
f.write()
print 'file written'


p = pyaudio.PyAudio()

# open stream
stream = p.open(format =
                16,
                channels = 2,
                rate = samplerate,
                output = True)


stream.write(ssignal)
 
stream.close()
p.terminate()

