
import numpy
from const import *
import math
import cmath
import pygame
import fontManager
from filters import *
from spectral import *

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
    
    
    spectralVarDT=SpectralVarDT(srate=3.2,nsamps=128)
    # clients.add(spectralVarDT.interpolator)
    spectral=spectralVarDT.spectral
    interpol=spectralVarDT.interpolator
    
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
        XX=spectral.XX
        
        magMax=0.0
        freqMaxVal=None
        xxMax=None
        if XX != None:
            for i in range(10):
                if spectral.freqBin[i] < RESFREQ_MIN:
                    continue
                if spectral.freqBin[i] > RESFREQ_MAX:
                    break
                
                fMag=abs(spectral.XX[i])
                
                if fMag > freqMaxVal:
                    xxMax=spectral.XX[i]
                    freqMax=spectral.freqs[i]
                    freqMaxVal=fMag
                    
                print "%i %3.2f %3.2f %3.4f %s"      % (i,spectral.freqBin[i]*60,abs(spectral.XX[i]), spectral.freqs[i]*60 ,"!"),
                
                
            print freqMax,freqMaxVal
            
        
            jwMax=complex(0,TWO_PI*freqMax)
                
            plot_spectrum(surf,XX)
            z=spectral.xx
#             z=spectra.getX()
            cnt=0
            yLast=None
            ttt=t
            ttt_dt=SPECT_DT
            
            for zz in z:
                xi=cnt*2
                xiL=(cnt-1)*2
                yNow=midY+zz*100
                ySync=midY+(xxMax*cmath.exp(jwMax*(ttt-(NSAMPS*SPECT_DT)))).real
                
                if yLast:
                    pygame.draw.line(surf,(0,255,0),(xiL,yLast),(xi,yNow))
               #     pygame.draw.line(surf,(0,0,255),(xiL,yTrainLast),(xi,yTrain))
               #     pygame.draw.line(surf,(255,0,0),(xiL,yFilt),(xi,yFilt))
               #     pygame.draw.line(surf,(255,255,0),(xiL,ySyncLast),(xi,ySync))
                    
                yLast=yNow
              #  yTrainLast=yTrain
                ySyncLast=ySync
                
                ttt+=ttt_dt
                cnt+=1
                
                
            
            
            display.blit(surf,(0,0))
            pygame.display.flip()
            clock.tick(5)
    
    
    pygame.quit()
            
            
            