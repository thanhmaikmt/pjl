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
INPUT = "mic"
DELAY_TIME = 0.005          # Time between current and previous rms values
RMS_FREQ = 20               # Cutoff of the analysis lowpass filter
ATT_THRESH = -3             # Attack threshold in dB (signal must be higher than
                            # previous rms + threshold to be reported as an attack)
MIN_THRESH = -40            # Minimum threshold in dB (signal must fall below this
                            # threshold to allow a new attack to be detected)
REL_TIME = .1               # Time to wait before reporting a new attack

# Input sound table
snd = SndTable(SND_PATH, chnl=1)
# triggers table (length is the same as sound table)
trig_table = NewTable(length=snd.getDur())

# Input sound
if INPUT == "snd":
    inp = TableRead(snd, snd.getRate()).out()
else:
    inp = Input(0)
# Input rms value
rms = Follower(inp, freq=RMS_FREQ)

rms_db = AToDB(rms)

# Previous rms value
rms_prev_db = Delay(rms_db, delay=DELAY_TIME)

# if current rms plus threshold is larger than previous rms
rms_over_prev = Compare(rms_db + ATT_THRESH, rms_prev_db, ">")
# if current rms is over minimum attack threshold
rms_over_min = Compare(rms_db, MIN_THRESH, ">")
# if both are true
trig = Compare(rms_over_prev + rms_over_min, 2.0, "==")

# On attack signal, closes the gate for REL_TIME seconds
rel_time = Timer(trig, Trig()+trig)
gate = Compare(rel_time, REL_TIME, ">")

# If attack signal and gate is open, there is a real trig
real_trig = trig * gate

# Print it to the console
printing = Print(real_trig, method=1)

# Record triggers in a table (records for the duration of the table "trig_table")
rec_trig = TableRec(real_trig, trig_table).play()

# Save the triggers table as audio file (wav, 16 bits)
def save_as_audio(filepath):
    trig_table.save(filepath)

# Save the triggers table as text file
def save_as_text(filepath):
    trig_table.write(filepath, False)

s.gui(locals())
