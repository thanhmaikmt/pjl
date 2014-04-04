DT  = 1./200         #  ECG sample rate


DEFAULT_BPM=70.0         #  fall back BPM if we get stuck
TARGET_HRV=0.1           # target HRV in Hertz  0.1 is 6 breadths per minute
INTERPOLATOR_SRATE=3.2   # resampled HRV sample rate in Hertz


#  GUI STUFF
BPM_MIN_DISP=40
BPM_MAX_DISP=100

MAX_BPM=120.0            # maximum possible physically HR
MIN_BPM=40.0             # minimum  "      ....

FPS = 30             # pygame frames per second refresh rate.


# range of breath frequencies
RESFREQ_MIN=4/60.0
RESFREQ_MAX=8/60.0
