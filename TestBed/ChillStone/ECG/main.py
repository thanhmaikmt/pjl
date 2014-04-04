import pygame,threading,time,numpy,sys
import fontManager
from filters import *
from process import *
from IO import *
from const import *
import ecgsource
import sonify
import spectral
import classifier

# import voicebowl1

# SOURCE
#  FILE or LIVE to chnge from recored to using device.
data_files="data_good/BAY_*"

# LIVE,LIVE_RECORD,FILE,FILE_LIVE=range(4)
  
mode=ecgsource.EcgSource.FILE


# feedback=FeedBack(target_hrv=TARGET_HRV,srate=INTERPOLATOR_SRATE)
# interpolator=Interpolator(srate=INTERPOLATOR_SRATE,client=None)

#  Signal flow
#
#  ECG at 200Hz  -->  
#  processor    (filter and create moving average ) -->     (moving average, time)  
#  peaker  ( identify RR peaks from processed ECG) -->      (peak_time,  magnitude)
#  TODO next is a mess refactoring needed
#  tachimeter  and   RRtoBPM ( convert intervals into BPM) --->             (bpm, peak_time)


# Clients must implement
# process(bpm,t,val)

pre_rr_samps=.4/DT
post_rr_samps=0.5/DT

qrs_collector=classifier.QRSCollector(pre_rr=pre_rr_samps,post_rr=post_rr_samps,file_name="QRS.txt")

clients=Clients()
clients.add(sonify.PingClient2())

spectralVarDT=spectral.SpectralVarDT(srate=3.2,nsamps=256)
clients.add(spectralVarDT.interpolator)
spectral=spectralVarDT.spectral

bpmfilt=BPMFilter(client=clients)
rrtobpm=RRtoBPM(median_filter_length=5,client=bpmfilt)
tachi=Tachiometer(median_filter_length=5,client=rrtobpm)
peaker=Peaker(client=tachi,dt=DT)
processor=Processor(peak_client=peaker,collector=qrs_collector,dt=DT)


#        Display stuff
pygame.init()
clock=pygame.time.Clock()
modes=pygame.display.list_modes()
fontMgr = fontManager.cFontManager((('Courier New', 16), (None, 48), (None, 24), ('arial', 24)))

caption=" HIT ESCAPE TO QUIT"  

# Allocate screen space.

# full=modes[0]
# MAC puts puts screen below menu so take a bit off the height.
# dim_display=(full[0],full[1]-50)


height=720
width=1280

dim_display=(width,height)


#----------  0
#    ECG
#----------  y1
#
#----------  y2
#     BPM                        CHAOS
#----------- height   ----    |              |
#                             x1           width

y1=int(height/4)
y2=y1+int(height/6)

y12=y2-y1
y2h=height-y2

x1=width-y2h
x1w=y2h

dim_chaos=(x1w,y2h)
print dim_chaos

dim_ecg=(width,y1)
dim_bpm=(x1,y2h)
dim_spect=(width,y12)

display = pygame.display.set_mode(dim_display)

class ReadClient:   
    """
     Does the GUI control
     Handles values from the ECG stream.
     THis is called from the ECG thread so no gui stuff is allowed.
    """

    def __init__(self,processor,mutex):
        self.processor=processor
        self.mutex=mutex

        
    # Read ECG values and feed the processor
    def process(self,val,replay,server):
        
        global space_hit,peakPtr

      
        if ecg_display.is_full():
            if replay:
             
                print " Hit key to continue "
                         
                space_hit=False
                while not space_hit and not server.stopped:
                    time.sleep(0.1)
                space_hit=False
                
                self.mutex.acquire()       
                ecg_display.scroll(0.1)
                self.mutex.release()
           
            else:
            
                print " RESETING CNT"
                self.mutex.acquire()
                ecg_display.reset()
                self.mutex.release()
               
        mutex.acquire()       
         
        self.processor.process(val)
        
        ecg_display.add_points(processor)
        
      
        mutex.release()
        
class ECGDisplay:
    
    def __init__(self,surf):
          
        self.cnt=0
        self.surf=surf
        self.N=surf.get_width()
        N=surf.get_width()
        self.x_points=numpy.zeros(N,dtype='i')    #  time axis 
        
        for i in range(N):
            self.x_points[i]=i
        
        #  Y axis- displays
        self.y_points=numpy.zeros(N,dtype='i')    #  val of ECG
        self.f_points=numpy.zeros(N,dtype='i')    #  filtered ECG
        self.s_points=numpy.zeros(N,dtype='i')    #  processed ECG
        self.a_points=numpy.zeros(N,dtype='i')    
        
        
        self.g_points=[self.y_points,self.f_points,self.s_points,self.a_points]
        
        self.peakPtrStart=0
        self.timeLeft=0
        self.windowTime=DT*N
   
    def is_full(self):
       return self.cnt >= self.N
   
    #  scroll the  ECG by n samples 
    def scroll(self,fact):
        
        # scroll by n samples
        n=int(self.N*fact)
            
        i1=self.N-n
        for pts in self.g_points:
            pts[0:self.N-n]=pts[n:self.N]
        self.cnt -= n
        self.timeLeft = self.timeLeft+n*DT
            
        # This is not very clever Eventually will be a problem  . . .
        self.peakPtrStart=0
    
    def reset(self):
        self.cnt=0
        self.timeLeft=processor.time
        
    def draw(self):    
        self.surf.fill((0,0,0))
    
        if self.cnt > 2:
            cnt=self.cnt
            points1=numpy.column_stack((self.x_points,self.y_points))
            points2=numpy.column_stack((self.x_points,self.s_points))
            points3=numpy.column_stack((self.x_points,self.a_points))
            points4=numpy.column_stack((self.x_points,self.f_points))
        #    pygame.draw.lines(ecg_surf, (0,255,0), False, points1[:(cnt-1)])
            pygame.draw.lines(ecg_surf, (0,0,255), False, points2[:(cnt-1)])
            pygame.draw.lines(ecg_surf, (255,0,255), False, points4[:(cnt-1)],3)
            pygame.draw.lines(ecg_surf, (150,0,0), False, points3[:(cnt-1)])
     
        n=len(tachi.RR)
        
        
        peakPtr=self.peakPtrStart
      
        # medPtLast=None
        
        while peakPtr<n:
            
            t=tachi.RR[peakPtr][0]
            dTime=t - self.timeLeft
            
            if dTime < 0:
                self.peakPtrStart += 1
                peakPtr += 1
            elif dTime > self.windowTime:
                break
            else:
                xi=int(dTime/processor.dt)
                yi=self.val2Screen(tachi.RR[peakPtr][1])
                #med=self.val2Screen(tachi.RRmed[peakPtr][1])
                col=RRstate.color[tachi.RR[peakPtr][2]]
                
                #if medPtLast != None:
                #    pygame.draw.line(ecg_surf,(255,255,255),medPtLast,(xi,med))
                    
                #medPtLast=(xi,med)
                pygame.draw.rect(ecg_surf,col,(xi,yi,4,dim_ecg[1]-yi))
                peakPtr += 1
        
        
            
    def add_points(self,processor):
        self.y_points[self.cnt]=self.ecg2screen(processor.y_val)
        self.f_points[self.cnt]=self.f2screen(processor.f_val)
        self.a_points[self.cnt]=self.val2Screen(peaker.thresh1)        
        self.s_points[self.cnt]=self.val2Screen(processor.s_val)
        self.cnt  += 1
        
    def f2screen(self,val):
        """ 
        map value -640-640  to the height
        """
        return dim_ecg[1]*0.5*(1-val/640.0) 
    
    def ecg2screen(self,val):
        """
        map val in range -1 to 1 to screen
        """
        return dim_ecg[1]*0.5*(1-val) 
                      
    def val2Screen(self,val):
            # moving average to screen value 
            return dim_ecg[1]*(1.0-val/MAX_MV_AV)

class BPMDisplay:
    
    def __init__(self,surf_bpm,surf_chaos):
           # BPM
        self.bpmScreenPtLast=None
        self.surf_bpm=surf_bpm
        self.surf_chaos=surf_chaos
        self.bpmPtr=0
        self.bpm_background=(50,50,50)
        self.surf_bpm.fill(self.bpm_background)
        self.xBPMright=int((surf_bpm.get_width()*5)/6)
        self.xBPM_ref=0
    # map bpm to pixels
        self.tBPMscale=10
        self.draw_bpm_key(0)
        
        #  Chaos window
        self.chaos_last=None
        breath_per_min=10.0
        
        # t*target_hrv_scale      should give 1 per breath
        self.breath_period = 60.0/breath_per_min 
        
    def bpm2screen(self,t,bpm):
        H=self.surf_bpm.get_height()
        return [int(t*self.tBPMscale)-self.xBPM_ref,int(H-(bpm-BPM_MIN_DISP)*H/(BPM_MAX_DISP-BPM_MIN_DISP))]

    def draw_bpm_key(self,bpmVal):
        
        bpmLine=40
        
    
        #val=feedback.dval
        #val_pix=(0.5+val/40.0)*self.surf_bpm.get_height()
        
       
        #print "VAL=", val
        #ival=int(min(255,max(0,(20+val)*5)))
                
        #col=(ival,0,255-ival)
       
        pygame.draw.rect(self.surf_bpm,(0,0,0),(0,0,40, self.surf_bpm.get_height()))
       
        pt=self.bpm2screen(0,bpmVal)
        
        pygame.draw.rect(self.surf_bpm,(0,0,255),(0,pt[1],40,self.surf_bpm.get_height()))
       
       
        while True:
          
          pt=self.bpm2screen(0,bpmLine)
          pt[0]=0
          if pt[1] < 0:
              break
          
          if pt[1] < dim_bpm[1]:
              ttt=str(bpmLine)
              fontMgr.Draw(bpm_surf, 'Courier New', 16, ttt, (pt[0],pt[1]), (20,255,255))
          
          bpmLine+=5
        
    
    def draw(self):
        
       # PLOT the BPM based values ------------------------------------------------------------
        
            
        while self.bpmPtr < len(rrtobpm.BPMraw):
            
            bpmNew=rrtobpm.BPMraw[self.bpmPtr][1]
          #  medNew=rrtobpm.BPMmedian[self.bpmPtr][1]
            timeNew=rrtobpm.BPMraw[self.bpmPtr][0]
            
            xNew,tmp=self.bpm2screen(timeNew,bpmNew)
            
            xOver = xNew-self.xBPMright
            
            if xOver > 0 :
                self.xBPM_ref += xOver
                bpm_surf.scroll(-xOver)
                pygame.draw.rect(self.surf_bpm,self.bpm_background,(self.xBPMright-xOver+1,0,xOver,self.surf_bpm.get_height()))
                self.bpmScreenPtLast[0] -= xOver
             #   self.medScreenPtLast[0] -= xOver
                
                
            self.draw_bpm_key(bpmNew)
             
            
            bpmScreenPtNew=self.bpm2screen(timeNew,bpmNew)
            chaos_new=None
            
            if self.bpmScreenPtLast != None:
                pygame.draw.line(bpm_surf,(0,255,0),self.bpmScreenPtLast,bpmScreenPtNew,5)
             #   pygame.draw.line(bpm_surf,(100,100,100),self.medScreenPtLast,medScreenPtNew,4)
                chaos_new=(self.bpmScreenPtLast[1],bpmScreenPtNew[1])
                
            # print "----",chaos_last,chaos_new
            
            
            if self.chaos_last != None:
    #             chaos_surf.fill((0,0,0,100),special_flags=0) # pygame.BLEND_SUB)
                chaos_surf.fill((250,250,250),special_flags=pygame.BLEND_MULT)
                col=self.chaos_color_at(timeNew)
                print " DRAW CHAOS",self.chaos_last,chaos_new,col
                pygame.draw.line(chaos_surf,col,self.chaos_last,chaos_new,15)
                        
            self.bpmScreenPtLast=bpmScreenPtNew
            self.chaos_last=chaos_new
            self.bpmPtr += 1
   

    def chaos_color_at2(self,t):
        """
        Modulate the colour of chaos line
        """
        i=(t/self.breath_period*512)%512
        
        if i > 256:
            i=512-i
            
        return (i,0,256-i)
    
  
    def chaos_color_at(self,t):
        """
        Modulate the colour of chaos line
        """
        
        
        hue=int(t*7)%360
        col=pygame.Color(255,255,255)
        col.hsva=(hue,100,100,100)
        return col
    
                 
  
class SpectralDisplay:
    
    
    def __init__(self,surf,spectral):
        self.surf=surf
        self.spectral=spectral
        
        
    def draw(self):
        if self.spectral.XX == None:
            return
           
       
        self.surf.fill((0,0,0))
        
        
        
        n=self.surf.get_height()
        wid=self.surf.get_width()
          
        cnt=0
        fact=0.5
        XX=self.spectral.XX
        freqs=self.spectral.freqBin
        
        cnt=0
        WID=10
        str=""
        for xx in XX:
            
            val=abs(xx)
            val=val*fact
    #         print val
            if self.spectral.freqBin[cnt]< RESFREQ_MIN:
                col=(0,0,255)
            elif self.spectral.freqBin[cnt] > RESFREQ_MAX:
                col=(200,0,100)
            else:
                str+= "%3.2f "      % (spectral.freqs[cnt]*60)
      
                col=(255,255,0)
                
            pygame.draw.line(self.surf,col,(cnt*WID,n-1),(cnt*WID,n-val),WID-1)
        
            fontMgr.Draw(self.surf, 'Courier New', 16, str, (wid-400,0), (60,255,255))
            cnt+=1
            
#  GUI stuff ---------------------------------------------------------


ecg_surf=pygame.Surface(dim_ecg)
ecg_display=ECGDisplay(ecg_surf)

chaos_surf=pygame.Surface(dim_chaos,flags=pygame.SRCALPHA)
bpm_surf=pygame.Surface(dim_bpm)
bpm_display=BPMDisplay(bpm_surf,chaos_surf)

spect_surf=pygame.Surface(dim_spect)
spect_display=SpectralDisplay(spect_surf,spectral)
         
#  read ecg on a seperate thread feeding into the processor
#  DON'T DO ANY GUI STUFF ON THIS THREAD
#  aquire the lock before playing around with and display data
mutex=threading.Lock()
 
read_client=ReadClient(processor,mutex)

ecg_src=ecgsource.EcgSource(read_client,mutex,mode=mode,data_files=data_files)

ecg_src.start()
 

"""
main gui loop
"""
while True:
      
#  Display the caption if set.
    if caption != ecg_src.get_caption() :
        caption=ecg_src.get_caption()
        pygame.display.set_caption(caption)
        caption=None
         
    k = pygame.key.get_pressed()
    
    if k[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
        space_hit=True
        time.sleep(.5)
        ecg_src.quit()
        pygame.quit()
        break
    
    if k[pygame.K_SPACE]:
        space_hit=True
        
    
    # Make sure the data does not get tweaked during disply.
    ecg_src.mutex.acquire()
    
    # ECG based values  --------------------------------------------------
    
    ecg_display.draw()
    bpm_display.draw()     
    spect_display.draw()
    
    ecg_src.mutex.release()
   
    
    display.blit(ecg_display.surf,(0,0))
    display.blit(bpm_surf,(0,y2))
    display.blit(chaos_surf,(x1,y2))
    display.blit(spect_surf,(0,y1))

    pygame.display.flip()
    clock.tick(FPS)