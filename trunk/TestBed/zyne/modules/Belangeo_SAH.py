#!/usr/bin/env python
# encoding: utf-8

class SAH(BaseSynth):
    """
    Old-school sample-and-hold.
    
    A sample-and-hold circuit is a device that samples the values of a continuously varying 
    signal and holds its value at a constant level for a specified minimal period of time.
    This circuit uses two phasors, one for the source and one the sampling.

    Parameters:

        Source rate : Frequency of the source phasor.
        Generation rate : Frequency of the sampling phasor.
        Deviation range : Frequency deviation around the pitch played on the keyboard.
    
    _______________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    _______________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.fr = Phasor(freq=self.p1, mul=self.pitch*self.p3, add=self.pitch)
        self.ctl = Phasor(freq=self.p2)
        self.realfreq = SampHold(self.fr, self.ctl)
        self.realFreqPort = Port(self.realfreq, 0.001, 0.001)
        self.norm_amp = self.amp * 0.1
        self.ampL = self.norm_amp * self.panL
        self.ampR = self.norm_amp * self.panR
        self.lfo1 = LFO(self.realFreqPort, sharp=.95, type=3, mul=self.ampL).mix()
        self.lfo2 = LFO(self.realFreqPort*1.012, sharp=.95, type=3, mul=self.ampR).mix()
        self.lfo3 = LFO(self.realFreqPort*0.991, sharp=.95, type=3, mul=self.ampL).mix()
        self.lfo4 = LFO(self.realFreqPort*1.01, sharp=.95, type=3, mul=self.ampR).mix()
        self.out = Mix([self.lfo1, self.lfo2, self.lfo3, self.lfo4], voices=2)

MODULES =   {
            "SAH": { "title": "- Sample and Hold -", "synth": SAH, 
                    "p1": ["Source rate", 0.5, 0.01, 30, False, False],
                    "p2": ["Generation rate", 4, .1, 20, False, False],
                    "p3": ["Deviation range", 0.25, 0, .95, False, False]
                    },
             }
