import pygame
import sys
from pygame.locals import *
import numpy
import random
import math

Fs=11025  # sample rate
pygame.mixer.init(Fs, -16, 0)   # mono, 16-bit
pygame.init()
pygame.display.set_mode((800, 600))
sound=[]   # array of Sounds

print "press q,w,e,r,t,y,u,i,o,p, z,x,c,v,b,n,m etc."
print "space to quit."


# sound 0 --------------------
length = Fs * 1.001   # 1.5 seconds
freq = 440.0
amp = 16.0
tmp = []
for t in range(int(length)):
    v= amp * numpy.sin(t*freq/Fs*2*math.pi) 
    tmp.append(v)

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))


# sound 1 --------------------
length = Fs * 1.001   # 1.5 seconds
freq = 440.0 * (5.0/4.0)
amp = 16.0
tmp = []
for t in range(int(length)):
    v= amp * numpy.sin(t*freq/Fs*2*numpy.pi) 
    tmp.append(v)

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))


# sound 2 --------------------
length = Fs * 1.001   # 1.5 seconds
freq = 440.0 * (4.0/3.0)
amp = 16.0
tmp = []
for t in range(int(length)):
    v= amp * numpy.sin(t*freq/Fs*2*numpy.pi) 
    tmp.append(v)

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))


# sound 3 --------------------  tremelo
length = Fs * 1.001   # 1.5 seconds
freq = 440.0 * (4.0/3.0)
freq2 = 2.0
amp = 16.0
tmp = []
for t in range(int(length)):
    v = amp * numpy.sin(t*freq/Fs*2*numpy.pi) 
    v2 = numpy.sin(t*freq2/Fs*2*numpy.pi)
    tmp.append(v*v2)

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))

# sound 4 --------------------  vibrato
length = Fs * 1.001   # 1.5 seconds
freq = 440.0 * (4.0/3.0)
freq2 = 2.0
amp = 16.0
tmp = []
for t in range(int(length)):
    v = 1 + 0.1 * numpy.sin(t*freq2/Fs*2*numpy.pi)
    v2 = amp * numpy.sin(t*freq/Fs*2*numpy.pi * v) 
    tmp.append(v2)

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))


# sound 5 --------------------  vibrato
length = Fs * 1.001   # 1.5 seconds
freq = 440.0 * (4.0/3.0)
freq2 = 17.5
amp = 16.0
tmp = []
for t in range(int(length)):
    v = 1 + 0.02 * numpy.sin(t*freq2/Fs*2*numpy.pi)
    v2 = amp * numpy.sin(t*freq/Fs*2*numpy.pi * v) 
    tmp.append(v2)

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))

# sound 6 --------------------  noise
length = Fs * 0.2   # 0.2 seconds
amp = 16.0
tmp = []
for t in range(int(length)):
    v = amp * random.random()
    tmp.append(v)

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))


# sound 7 --------------------  low-pass filtered noise
length = Fs * 0.2   # 0.2 seconds
Fc = 0.5
amp = 16.0
tmp = []
lastv = 0
for t in range(int(length)):
    v = amp * random.random()
    v2 = v*Fc + (1-Fc)*lastv 
    tmp.append(v2)
    lastv = v2

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))


# sound 8 --------------------  low-pass filtered noise
length = Fs * 0.2   # 0.2 seconds
Fc = 0.1
amp = 16.0
tmp = []
lastv = 0
for t in range(int(length)):
    v = amp * random.random()
    v2 = (1-Fc) * lastv + Fc*v  
    tmp.append(v2)
    lastv = v2

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))


# sound 9 --------------------  several harmonics
length = Fs * 1.0   # 0.2 seconds
base = 400.0
freq  = base * 1.0
freq2 = base * 2.0
freq3 = base * 3.0
freq4 = base * 4.0
amp = 16.0
amp2 = 8.0
amp3 = 4.0
amp4 = 2.0
tmp = []
for t in range(int(length)):
    v  = amp * numpy.sin(t*freq/Fs*2*numpy.pi ) 
    v2 = amp2 * numpy.sin(t*freq2/Fs*2*numpy.pi) 
    v3 = amp3 * numpy.sin(t*freq3/Fs*2*numpy.pi) 
    v4 = amp4 * numpy.sin(t*freq4/Fs*2*numpy.pi) 
    tmp.append(v + v2 + v3 +v4 )

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))


# sound 10 --------------------  several non-harmonic partials
length = Fs * 1.0   # 0.2 seconds
base = 400.0
freq  = base * 1.0
freq2 = base * 2.1
freq3 = base * 2.9
freq4 = base * 3.87
amp = 16.0
amp2 = 8.0
amp3 = 4.0
amp4 = 2.0
tmp = []
for t in range(int(length)):
    v  = amp * numpy.sin(t*freq/Fs*2*numpy.pi ) 
    v2 = amp2 * numpy.sin(t*freq2/Fs*2*numpy.pi) 
    v3 = amp3 * numpy.sin(t*freq3/Fs*2*numpy.pi) 
    v4 = amp4 * numpy.sin(t*freq4/Fs*2*numpy.pi) 
    tmp.append(v+v2+v3+v4)

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))



# sound 11 --------------------  kick drum!  
length = Fs * 0.20
amp = 16.0
tmp = []
phase = 0
for t in range(int(length)):
    env = (length-t)/length    # from 1 to 0
    freq = 220 * env
    phaseDelta = freq/Fs*2*numpy.pi
    phase = phase + phaseDelta
    v2 = amp * numpy.sin(phase)
    tmp.append(v2)

sound.append(pygame.sndarray.make_sound(pygame.sndarray.array(tmp)))








# ------------- don't pay much attention to what's down here ----------

def key2number(e):
   string1 = [K_q,K_w,K_e,K_r,K_t,K_y,K_u,K_i,K_o,K_p,K_z,K_x,K_c,K_v,K_b,K_n,K_m]
   if(len(e)>0):
    if(e[0].key == K_SPACE):
        sys.exit()
    for x in range(len(string1)):
        if(e[0].key == string1[x]):
            return(x)
   return(-1)


while(1):
   e = []
   e = pygame.event.get(KEYDOWN)

   soundNum=key2number(e)
  
   if soundNum != -1:

    if soundNum < len(sound):
        print "playing sound #" + str(soundNum)
        sound[soundNum].play()
    else:
        print "no sound in slot #" + str(soundNum)
