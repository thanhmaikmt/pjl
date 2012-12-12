#!/usr/bin/env python
# encoding: utf-8

class Arpeggiator(BaseSynth):
    """
    Harmonic arpeggiator.
    
    An arpeggiator with different kind of harmonic patterns.

    Parameters:

        Number of notes : Number of notes in the pattern.
        Pattern : Pattern shape.
        Arpeggiator speed : Time between each notes in seconds.
    
    _______________________________________________________________________________
    Author : Olivier Bélanger - 2011
    _______________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        t1 = [1,2,3,4,5,6,7,8,9,10,11,12]
        t2= [1,4,3,6,5,8,7,10,9,12,11,12]
        t3 = [1,3,5,7,9,11,12,10,8,6,4,2]
        t4 = [1,4,7,10,13,12,9,6,3,8,5,2]
        t5 = [1,2,6,4,5,9,7,8,12,9,6,3]
        t6 = [1,2,3,7,5,6,7,11,9,8,2,4]
        t7 = [1,7,6,5,4,12,11,10,9,8,7,6]
        self.table_choice = [t1, t2, t3, t4, t5, t6, t7]
        self.table = DataTable(size=12, init=t1)
        self.changeP1 = Change(self.p1)
        self.trigP1 = TrigFunc(self.changeP1, self.changeHarms)
        self.changeP2 = Change(self.p2)
        self.trigP2 = TrigFunc(self.changeP2, self.changeMode)
        self.norm_amp = self.amp * .15
        self.leftamp = self.norm_amp * self.panL
        self.rightamp = self.norm_amp * self.panR
        self.metro = Metro(self.p3).play()
        self.count = Counter(self.metro, max=8)
        self.harmo = TableIndex(self.table, self.count, mul=0.5)
        self.harmoPort = Port(self.harmo, .003, .003)
        self.osc1 = Sine(freq=self.pitch*self.harmoPort, mul=self.leftamp).mix()
        self.osc2 = Sine(freq=self.pitch*self.harmoPort*1.005, mul=self.rightamp).mix()
        self.osc3 = Sine(freq=self.pitch*self.harmoPort*.997, mul=self.leftamp).mix()
        self.osc4 = Sine(freq=self.pitch*self.harmoPort*.992, mul=self.rightamp).mix()
        self.mix = Mix([self.osc1, self.osc2, self.osc3, self.osc4], voices=2)
        self.out = Freeverb(self.mix, size=.65, damp=.75, bal=.1)
    
    def changeHarms(self):
        num = int(self.p1.get())
        self.count.max = num

    def changeMode(self):
        mode = int(self.p2.get())
        self.table.replace(self.table_choice[mode])

MODULES =   {
            "Arpeggiator": { "title": "- Harmonic Arpeggiator -", "synth": Arpeggiator, 
                    "p1": ["Number of notes", 8, 2, 12, True, False],
                    "p2": ["Pattern", 0, 0, 6, True, False],
                    "p3": ["Arppegiator speed", 0.1, .005, 1, False, True]
                    },
             }