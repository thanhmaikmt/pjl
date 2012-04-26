'''
Created on 1 May 2011

@author: pjl
'''


import pyaudio
import numpy as N
import wave

class Player: 
    
    def __init__(self):
        self.p = pyaudio.PyAudio()

# open stream
        self.stream = self.p.open(format =  pyaudio.pa.paInt32,
                channels = 1,
                rate = 44100,
                output = True)

    def play(self,x):
        if x.dtype != N.float:
            raise Exception('Player must be fed with a Numpy float array ')
        
        ssignal = ''.join((wave.struct.pack('h', item) for item in x))
        self.stream.write(ssignal)

    def close(self): 
        self.stream.close()
        self.p.terminate()