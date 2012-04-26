'''
Created on 6 Dec 2010

@author: pjl
'''

#from Numeric import *
#from numpy import *
#from dislin import *

#from audiolab import wavread
signal, fs, enc = wave.read('test.wav')

#x=arange(256.0)
#sig = sin(2*pi*(1250.0/10000.0)*x) + \
#      sin(2*pi*(625.0/10000.0)*x)


plot(x[0:129],10*log10(abs(real_fft(sig))))