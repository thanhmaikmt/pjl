DT  = 1./200         #  ECG sample rate


DEFAULT_BPM=70.0         #  fall back BPM if we get stuck
TARGET_HRV=0.1           # target HRV in Hertz  0.1 is 6 breadths per minute
INTERPOLATOR_SRATE=3.2   # resampled HRV sample rate in Hertz


#  GUI STUFF
BPM_MIN_DISP=45
BPM_MAX_DISP=90

MAX_BPM=120.0            # maximum possible physically HR
MIN_BPM=40.0             # minimum  "      ....

FPS = 30             # pygame frames per second refresh rate.
