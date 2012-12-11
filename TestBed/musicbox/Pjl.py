#!/usr/bin/env python
# encoding: utf-8

class GenericModule(BaseSynth):
    """
    Simple frequency modulation synthesis.
    
    With frequency modulation, the timbre of a simple waveform is changed by 
    frequency modulating it with a modulating frequency that is also in the audio
    range, resulting in a more complex waveform and a different-sounding tone.

    Parameters:

        FM Ratio : Ratio between carrier frequency and modulation frequency.
        FM Index : Represents the number of sidebands on each side of the carrier frequency.
        Lowpass Cutoff : Cutoff frequency of the lowpass filter.
    
    ________________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    ________________________________________________________________________________________
    """
    def __init__(self, config):
        # `mode` handles pitch conversion : 1 for hertz, 2 for transpo, 3 for midi
        BaseSynth.__init__(self, config, mode=1)
        self.fm1 = FM(carrier=self.pitch, ratio=self.p1, index=self.p2, mul=self.amp*self.panL).mix(1)
        self.fm2 = FM(carrier=self.pitch*0.997, ratio=self.p1, index=self.p2, mul=self.amp*self.panR).mix(1)
        self.mix = Mix([self.fm1, self.fm2], voices=2)
        self.out = Biquad(self.mix, freq=self.p3, q=1, type=0)

MODULES = {
            "GenericModule": { "title": "- Generic module -", "synth": GenericModule, 
                    "p1": ["Ratio", 0.5, 0, 10, False, False],
                    "p2": ["Index", 5, 0, 20, False, False],
                    "p3": ["LP cutoff", 4000, 100, 15000, False, True]
                    },
          }
