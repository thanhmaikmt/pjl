import numpy as N
import wave
import pyaudio

duration=5
frequency=220.
samplerate=44100
sr = samplerate
samples = duration*samplerate
period = samplerate / float(frequency)
omega = N.pi * 2 / period
xaxis = N.arange(int(period),dtype = N.float) * omega
ydata = 16384 * N.sin(xaxis)
signal = N.resize(ydata, (samples,))
ssignal = ''
#for i in range(len(signal)):
#   ssignal += wave.struct.pack('h',signal[i])
   
ssignal = ''.join((wave.struct.pack('h', item) for item in signal))
   
filewriteto = frequency
file = wave.open(str(filewriteto)+'.wav', 'wb')
file.setparams((1, 2, sr, 44100*4, 'NONE', 'noncompressed'))
file.writeframes(ssignal)
file.close()



p = pyaudio.PyAudio()

# open stream
stream = p.open(format =  pyaudio.pa.paInt32,
                channels = 1,
                rate = 44100,
                output = True)


stream.write(ssignal)
 
stream.close()
p.terminate()