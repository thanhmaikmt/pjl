
import numpy
from const import *
import math
import cmath
import pygame
import fontManager
from filters import *
from process import *

# resample at 3.2 Hz
# nPoints  64 or 128

#  so the window time length is 128/3.2 = 40 seconds
#  we should never have 2 RR times between sample points ?


  
  
#SAMP_FREQ=3.2
#NSAMPS=128
#SPECT_DT=1.0/SAMP_FREQ
TWO_PI=math.pi*2


j=complex(0,1)

   
        

class Spectral:
    
    def __init__(self,srate,nsamps):
        
        self.dt=1.0/srate
        self.ONE_OVER_TWO_PI_DT=1.0/(TWO_PI*self.dt)

        self.nSamps=nsamps
        self.N2=self.nSamps*2
        self.nBin=(nsamps/2+1)
        self.freqBin=numpy.zeros(self.nBin)
        binFreq=srate/nsamps
        
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
    
        dFreqdt = xx1*self.ONE_OVER_TWO_PI_DT
        
        self.freqs= dFreqdt
        self.ANG_PREV=self.ANG
        
               
             
    def getXw(self):
            
            i1=self.cnt
            i2=self.cnt+self.nSamps

            return self.xx   # [i1:i2]

    def getX(self):
            
            i1=self.cnt
            i2=self.cnt+self.nSamps

            return self.x[i1:i2]


class SpectralVarDT:

    def __init__(self,srate,nsamps):
        self.dcblock=DCBlock(.95)
        self.spectral=Spectral(srate,nsamps)
        self.interpolator=Interpolator(srate,self)
   
    def process(self,bpm):
       
       bpm=self.dcblock.process(bpm)
       self.spectral.process(bpm)
       
       
            
def plot_spectrum(surf,XX):
    WID=10
    surf.fill((0,0,0))
    n=surf.get_height()
    cnt=0
    fact=1.0
    for xx in XX:
        val=abs(xx)
        val=val*fact
#         print val
        col=(255,0,0)
        pygame.draw.line(surf,col,(cnt*WID,n-1),(cnt*WID,n-val),WID)
        cnt += 1
        
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
   
    spectVar=SpectralVarDT(3.2,128) 
    spectra=spectVar.spectral
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
        spectVar.interpolator.process(val,t)
     #   cheap.process(val,t)
        t += DT
        XX=spectVar.spectral.XX
        
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
                
            
            display.blit(surf,(0,0))
            pygame.display.flip()
            clock.tick(10)
    
    
    pygame.quit()
            
            
            