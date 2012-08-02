# Getting started with the bregman toolkit
from bregman.suite import *

audio_file = os.path.join(audio_dir,"gmin.wav")

x,sr,fmt = wavread(audio_file) # load the audio file
play(balance_signal(x),sr) # play it

help(Features) # see help on the Features class
p = Features.default_params()
print p # show feature extraction parameter dict
F = Features(audio_file, p) # extract features using dict
F.feature_plot(normalize=True, dbscale=True) # plot features
#title('Constant-Q spectrogram')

x_hat = F.inverse(F.X, pvoc=True) # invert phaseless features to audio
play(balance_signal(x_hat),sr) # play inverted features

p['feature']='stft'
p['nfft']=1024
p['wfft']=512
p['nhop']=256

F = Features(audio_file, p)
F.feature_plot(normalize=True,dbscale=True)
#title('Wide-band spectrogram')

x_hat = F.inverse(F.X, usewin=0) # invert features to audio (use original phases, no windowing)
play(balance_signal(x_hat))

tuts = get_tutorials()

# Audio feature extraction built-in tutorial examples
execfile(tuts[1])

# Test signals built-in tutorial examples
execfile(tuts[2])

# Audio similarity built-in tutorial examples
execfile(tuts[3])

# Concatenative audio synthesis (Soundspotter) built-in tutorial examples
execfile(tuts[4])

# Audio separation with PLCA built-in tutorial examples
execfile(tuts[5])
