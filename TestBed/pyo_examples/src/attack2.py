#!/usr/bin/env python
# encoding: utf-8
"""
Attack detector.

"""
from pyo import *

s = Server(sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

### Settings ###
SND_PATH = '/home/pjl/workspace/JavaSpeechToolData/consonants/Orig/cyrsseWords.wav' # Enter your sound path here...
INPUT = "snd" # or "mic"    # Input type
# INPUT = "mic"

MIN_THRESH = -40            # Minimum threshold in dB (signal must fall below this
                            # threshold to allow a new attack to be detected)
REL_TIME = .1               # Time to wait before reporting a new attack

# Input sound table
snd = SndTable(SND_PATH, chnl=1)
snd.view(" Cyssee")

# triggers table (length is the same as sound table)
trig_table = NewTable(length=snd.getDur())

# Input sound
if INPUT == "snd":
    inp = TableRead(snd, snd.getRate()).out()
else:
    inp = Input()
    
 

# Input rms value
rms = Follower2(inp, risetime=0.1, falltime=.5, mul=.5)

rms_db = AToDB(rms)

thresh = Sig(value=100)
gate = Compare(rms_db, thresh, ">")

thresh.ctrl([SLMap(-50., 10, 'lin', 'value', -20)]) 

# Print it to the console
printing = Print(gate, method=1)


s.gui(locals())
