
import numpy
from const import *
import math
import cmath
import pygame
import fontManager
from filters import *

# resample at 3.2 Hz
# nPoints  64 or 128

#  so the window time length is 128/3.2 = 40 seconds

#  we should never have 2 RR times between sample points ?

  
  
SAMP_FREQ=3.2
NSAMPS=128
SPECT_DT=1.0/SAMP_FREQ
TWO_PI=math.pi*2
ONE_OVER_TWO_PI_DT=1.0/(TWO_PI*SPECT_DT)
RESFREQ_MIN=4/60.0
RESFREQ_MAX=8/60.0


j=complex(0,1)

        
            
class Clients:
        
    def __init__(self):
           self.clients=[]
           
           
    def process(self,val):
        
        for c in self.clients:
            c.process(val)
            
    def add(self,client):
        self.clients.append(client)

class Specrtral:
    
    def __init__(self):
        
        self.dt=1.0/SAMP_FREQ
        self.nSamps=NSAMPS
        self.N2=self.nSamps*2
        self.nBin=(NSAMPS/2+1)
        self.freqBin=numpy.zeros(self.nBin)
        binFreq=SAMP_FREQ/NSAMPS
        
        for i in range(self.nBin):
            self.freqBin[i]=binFreq*i
            
        self.x=numpy.zeros(self.nSamps*2)
        #  self.x += 1.0/DEFAULT_BPM
        self.win=numpy.hanning(self.nSamps)
        # time of last sample
        self.cnt=0
        self.XX=None
        self.xx=None
        self.ANG_PREV=numpy.zeros(self.nBin)
        self.filt=numpy.zeros(self.nBin)
        self.filt[2:6]=1
        
    def process(self,val):

        
        self.x[self.cnt]=val
        self.x[(self.cnt+self.nSamps)]=val
        self.cnt = (self.cnt+1)%self.nSamps  
    
        i1=self.cnt
        i2=self.cnt+self.nSamps
#             print self.x[i1:i2]
        
        self.xx=self.x[i1:i2]  *self.win
        
        self.XX=numpy.fft.rfft(self.xx)
        
        self.ANG=numpy.angle(self.XX)
        
        dAng=self.ANG-self.ANG_PREV+3*math.pi
        
     #   print dAng
        xx1=numpy.mod(dAng,TWO_PI)-math.pi
    
        dFreqdt = xx1*ONE_OVER_TWO_PI_DT
        
        self.freqs= dFreqdt
        self.ANG_PREV=self.ANG
        
        #print XX
        #self.time+=SPECT_DT
    
        XXF=self.XX*self.filt
        self.filtX=numpy.fft.irfft(XXF)
        
        
        
             
    def getXw(self):
            
            i1=self.cnt
            i2=self.cnt+self.nSamps

            return self.xx   # [i1:i2]

    def getX(self):
            
            i1=self.cnt
            i2=self.cnt+self.nSamps

            return self.x[i1:i2]


   
class  Cheap:
    
    
    def __init__(self,default_freq):         
        self.default=default_freq
        self.tLast=None
        self.im=0
        self.re=0
        self.phase_fact=default_freq*TWO_PI
        self.fact1=.9
        self.fact2=1.0-self.fact1
        
    def process(self,bpm,tNow):
        
        if self.tLast != None:
            self.tLast=tNow
            self.bpmLast=bpm
            return
        
        phase=self.phase_fact*tNow
        
        self.im =  self.im*self.fact1 + self.fact2*bpm*math.sin(phase)
        self.re =  self.re*self.fact1 + self.fact2*bpm*math.cos(phase)
        
        
    def val_at(self,t):
        phase=self.phase_fact*t
        return self.re*math.cos(phase) + self.im*math.sin(phase)
        
        
        
            
def plot_spectrum(surf,XX):
    
    surf.fill((0,0,0))
    n=surf.get_height()
    cnt=0
    fact=10
    for xx in XX:
        val=abs(xx)
        val=val*fact
#         print val
        col=(255,0,0)
        pygame.draw.line(surf,col,(cnt,n-1),(cnt,n-val),4)
        cnt+=5
        
if __name__ == "__main__":
    
    pygame.init()
    clock=pygame.time.Clock()
    modes=pygame.display.list_modes()
    # a font of None means to use the default font
    fontMgr = fontManager.cFontManager((('Courier New', 16), (None, 48), (None, 24), ('arial', 24)))
    
    full=modes[0]

    dim_display=(full[0],full[1]-50)

    display = pygame.display.set_mode(dim_display)

    surf=pygame.Surface(dim_display)
    midY=dim_display[1]/2
    
    clients=Clients()
    
    biq=Biquad(Biquad.LOWPASS,freq=0.2,srate=SAMP_FREQ,Q=10)
    spectra=Specrtral()
    
    clients.add(biq)
    clients.add(spectra)
    
    interpol=Interpolate(clients)
    
    # cheap=Cheap(10.0/60.0)
    
    breath_per_min=5;
    freq=breath_per_min/60.0
    
    t=0
    DT=1.0
    while t < 600:
        k = pygame.key.get_pressed()
        if k[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
            pygame.quit()
            break
       
        val=5+math.cos(t*2*math.pi*freq)
        interpol.process(val,t)
     #   cheap.process(val,t)
        t += DT
        XX=spectra.XX
        
        magMax=0.0
        freqMaxVal=None
        xxMax=None
        if XX != None:
            for i in range(10):
                if spectra.freqBin[i] < RESFREQ_MIN:
                    continue
                if spectra.freqBin[i] > RESFREQ_MAX:
                    break
                
                fMag=abs(spectra.XX[i])
                
                if fMag > freqMaxVal:
                    xxMax=spectra.XX[i]
                    freqMax=spectra.freqs[i]
                    freqMaxVal=fMag
                    
                print "%i %3.2f %3.2f %3.4f %s"      % (i,spectra.freqBin[i]*60,abs(spectra.XX[i]), spectra.freqs[i]*60 ,"!"),
                
                
            print freqMax,freqMaxVal
            
        
            jwMax=complex(0,TWO_PI*freqMax)
                
            plot_spectrum(surf,XX)
            z=spectra.getXw()
            z=spectra.getX()
            cnt=0
            yLast=None
            ttt=t
            ttt_dt=SPECT_DT
            xf=spectra.filtX
            
            for zz,zzf in zip(z,xf):
                xi=cnt*2
                xiL=(cnt-1)*2
                yNow=midY+zz*100
                yTrain=midY+zzf*100
                yFilt=midY+biq.y1*100
                ySync=midY+(xxMax*cmath.exp(jwMax*(ttt-(NSAMPS*SPECT_DT)))).real
                
                if yLast:
                    pygame.draw.line(surf,(0,255,0),(xiL,yLast),(xi,yNow))
                    pygame.draw.line(surf,(0,0,255),(xiL,yTrainLast),(xi,yTrain))
                    pygame.draw.line(surf,(255,0,0),(xiL,yFilt),(xi,yFilt))
                    pygame.draw.line(surf,(255,255,0),(xiL,ySyncLast),(xi,ySync))
                    
                yLast=yNow
                yTrainLast=yTrain
                ySyncLast=ySync
                
                ttt+=ttt_dt
                cnt+=1
                
                
            
            
            display.blit(surf,(0,0))
            pygame.display.flip()
            clock.tick(5)
    
    
    pygame.quit()
            
            
            