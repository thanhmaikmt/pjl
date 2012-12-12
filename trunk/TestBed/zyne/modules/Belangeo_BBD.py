#!/usr/bin/env python
# encoding: utf-8

class BBD(BaseSynth):
    """
    Bucket-brigade device.
    
    Digital implementation of a bucket-brigade device (BBD), which is a discrete-time analogue 
    delay line, developed in 1969 by F. Sangster and K. Teer of the Philips Research Labs. The
    delay line is feeded by a square wave and implements an internal ring modulator applied over
    and over each time the signal is sent back into the delay line.

    Parameters:

        Brightness : Control the number of harmonics in the source oscillator.
        Delay : Delay time in seconds.
        Modulation Depth : Amplitude of the internal ring modulation.
    
    ____________________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    ____________________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.src = SineLoop(self.pitch, feedback=self.p1*0.25, mul=self.amp*.15)
        self.modd1 = [random.uniform(.001, .02) for i in range(len(self.pitch))]
        self.moddepth1 = self.p3 + self.modd1
        self.modd2 = [random.uniform(.001, .02) for i in range(len(self.pitch))]
        self.moddepth2 = self.p3 + self.modd2
        self.halfpitch = self.pitch * 0.5
        self.del_1 = Delay(self.src, delay=Sine(freq=.01, mul=self.p2*random.uniform(.2, .3), add=self.p2))
        self.sine_1 = Sine(Sine(freq=.007, mul=self.halfpitch*self.moddepth1, add=self.halfpitch))
        self.ring_1 = self.del_1 * self.sine_1
        self.filt_1 = Biquad(self.ring_1, self.pitch*2, mul=self.amp * self.panL)
        self.del_2 = Delay(self.src, delay=Sine(freq=.009, mul=self.p2*random.uniform(.2, .3), add=self.p2))
        self.sine_2 = Sine(Sine(freq=.008, mul=self.halfpitch*self.moddepth2, add=self.halfpitch))
        self.ring_2 = self.del_2 * self.sine_2
        self.filt_2 = Biquad(self.ring_2, self.pitch*2, mul=self.amp * self.panR)
        self.cross_1 = self.filt_2 * .99
        self.cross_2 = self.filt_1 * .99
        self.del_1.setInput(self.filt_1 * .8 + self.cross_1 + self.src)
        self.del_2.setInput(self.filt_2 * .8 + self.cross_2 + self.src)
        self.out = Mix([self.filt_1.mix(),self.filt_2.mix()], voices=2)

MODULES =   {
            "BBD": { "title": "- Bucket Bridged Device -", "synth": BBD, 
                    "p1": ["Brightness", 0.1, 0, 1, False, False],
                    "p2": ["Delay", .05, .001, 1, False, True],
                    "p3": ["Modulation Depth", 0.001, 0.001, .5, False, True]
                    },
            }
