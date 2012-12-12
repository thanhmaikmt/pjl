#!/usr/bin/env python
# encoding: utf-8

class Bubbles(BaseSynth):
    """
    Bubble synth (very) loosely based on the TB-303

    Waveforms being low-passed. This synth is 3 octaves down, hence the tasty bubbles.
    Try Zyne's random function, you might be surprised what it yields in the upper register.
    The cutoff frequency of the filter is relative to the synth's ADSR, overall amplitude and velocity.
    CAUTION: certain extreme settings will make you bleed from the ears and ruin your speakers.

    Parameters:

        Cutoff : Changes the cutoff frequency of the low-pass filter.
        Reso : Changes the Q of the low-pass filter.
        Shape : Changes the waveform used. Shape 0 is the closest to the TB-303.

    _______________________________________________________________________________________________
    Author : Jean-Michel Dumas - 2011
    _______________________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        
        #TO KEEP PYO HAPPY, WE PUT THE EQUATION IN A VARIABLE
        self.filterFreq = self.p1*self.amp+150
        
        #LEFT CHANNEL
        self.wave1L = Phasor(freq=self.pitch*0.125,phase=0)
        self.wave2L = Phasor(freq=self.pitch*0.125*(-1),phase=0.5)
        self.waveL = ((self.wave1L+self.wave2L)-1)*self.amp*self.panL
        self.waveNewL = LFO(freq=self.pitch*0.125, sharp=1, type=4, mul=self.amp*self.panL)
        self.filterL = Biquadx(self.waveL, freq=self.filterFreq, q=self.p2, type=0, stages=2, mul=1)
        
        #RIGHT CHANNEL
        self.wave1R = Phasor(freq=self.pitch*0.124,phase=0)
        self.wave2R = Phasor(freq=self.pitch*0.124*(-1),phase=0.5)
        self.waveR = ((self.wave1R+self.wave2R)-1)*self.amp*self.panR
        self.waveNewR = LFO(freq=self.pitch*0.124, sharp=1, type=4, mul=self.amp*self.panR)
        self.filterR = Biquadx(self.waveR, freq=self.filterFreq, q=self.p2, type=0, stages=2, mul=1)
        
        #SHAPE SLIDER IS P3, CHECK TO SEE WHEN IT CHANGES AND TRIGGER FUNCTION
        self.p3Changer = Change(self.p3)
        self.fak = TrigFunc(self.p3Changer, self.shapeChooser)
        
        #MODULE'S AUDIO OUTPUT WITH COMPRESSION TO MINIMIZE EAR BLEEDING
        self.out = Compress([self.filterL.mix(), self.filterR.mix()], thresh=-20, ratio=4)
        
    #FUNCTION FOR SHAPE SLIDER
    def shapeChooser(self):
        x = int(self.p3.get())
        if x == 0:
            self.filterL.setInput(self.waveL, 2)
            self.filterR.setInput(self.waveR, 2)
        elif x == 1:
            self.waveNewL.setType(0)
            self.waveNewR.setType(0)
            self.filterL.setInput(self.waveNewL, 2)
            self.filterR.setInput(self.waveNewR, 2)
        elif x == 2:
            self.waveNewL.setType(2)
            self.waveNewR.setType(2)
        elif x == 3:
            self.waveNewL.setType(4)
            self.waveNewR.setType(4)
        elif x == 4:
            self.waveNewL.setType(5)
            self.waveNewR.setType(5)
        elif x == 5:
            self.waveNewL.setType(6)
            self.waveNewR.setType(6)

#MODULES CHUNK, DEFINES P1 P2 P3
MODULES = {"Bubbles": { "title": "--- Bubbles ---", "synth": Bubbles, 
                    "p1": ["Cutoff", 2000, 150, 8000, False, True],
                    "p2": ["Reso", 5, 0.1, 15, False, False],
                    "p3": ["Shape", 0, 0, 5, True, False]
                    }}