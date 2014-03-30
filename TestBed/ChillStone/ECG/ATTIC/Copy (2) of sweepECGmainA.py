import serial,serial.tools.list_ports
import pygame
import thread
import time
import numpy
import sys
import threading
import fontManager

from filters import *
from process import *
from IO import *
from const import *

FPS = 30             # pygame frames per second refresh rate.


#  mode 1 - OFFLINE scans all test_data  recordings
#       0- online using USB to grab realtime data from arduino + SCG shild
mode=0
Record=True

serial.tools.list_ports.main()

#  ---------------  SERIAL PORT FOR ECG -----------
# WINDOWS      does this work with the leonardo? Does not report the port in the list.
#serial_port='COM4'

# MAC
# serial_port="/dev/tty.usbmodem1421"   #  LEFT on mac air
serial_port="/dev/tty.usbmodem1411"     #  RIGHT on mac air
        
# ubuntu
#ser_port = "/dev/ttyACM0"          


# MUTEX for gui and data processing synschronization
mutex=threading.Lock()

        
#        Display stuff
pygame.init()
clock=pygame.time.Clock()
modes=pygame.display.list_modes()
# a font of None means to use the default font
fontMgr = fontManager.cFontManager((('Courier New', 16), (None, 48), (None, 24), ('arial', 24)))
 


caption=" HIT ESCAPE TO QUIT"  

fout=None

# Allocate screen space.

full=modes[0]

dim_display=(full[0],full[1]-50)

halfH=int(dim_display[1]*0.5)

print " halfH ", halfH

dim_chaos=(halfH,halfH)

dim_ecg=(dim_display[0],int(dim_display[1]-halfH))

dim_bpm=(dim_display[0]-halfH,halfH)

display = pygame.display.set_mode(dim_display)



ecg_surf=pygame.Surface(dim_ecg)
chaos_surf=pygame.Surface(dim_chaos,flags=pygame.SRCALPHA)

tBPMscale=10


#  Set up ECG input dpending on mode
if mode == 0:
    
    class Client:
        
        def notify(self,name):
            global caption
            caption=name
                    
    source=MultiFileStream("test_data",Client())
    Record=False
    Replay=True
    
    
elif mode == 1:

    Replay=False
    
    if Record:
        file_name="data/"+time.strftime("%b%d_%H_%M_%S")+".txt"
        fout=open(file_name,"w")    
        

    source = serial.Serial()
    source.port=serial_port
    # wait for opening the serial connection.
    while True:    
        try:
            source.open()
            break
        except:
            print " Waiting for serial connection on ",serial_port
            time.sleep(1)
    
    print " Using USB serial input "

def bpm2screen(t,bpm):
    return [int(t*tBPMscale)-xBPM_ref,int(dim_bpm[1]-(bpm-BPM_MIN_DISP)*dim_bpm[1]/(BPM_MAX_DISP-BPM_MIN_DISP))]
 
    
def f2screen(val):
    return dim_ecg[1]*0.5*(1-val/640.0) 

def ecg2screen(val):
      return dim_ecg[1]*0.5*(1-val) 
                  
def val2Screen(val):
        # moving average to screen value 
        return dim_ecg[1]*(1.0-val/MAX_MV_AV)
   


#  CHAOS WINDOW   
breath_per_min=10.0

# t*target_hrv_scale      should give 1 per breath
breath_period = 60.0/breath_per_min 


def chaos_color_at(t):
    
    i=(t/breath_period*512)%512
    
    if i > 256:
        i=512-i
        
    return (i,0,256-i)
    
    

#  ECG  gui stufff
#  N is number of samples in window  1 per pixel
N=dim_ecg[0]

x_points=numpy.zeros(N,dtype='i')    #  time axis 

for i in range(N):
    x_points[i]=i

#  Y axis- displays
y_points=numpy.zeros(N,dtype='i')    #  val of ECG
f_points=numpy.zeros(N,dtype='i')    #  filtered ECG
s_points=numpy.zeros(N,dtype='i')    #  processed ECG
a_points=numpy.zeros(N,dtype='i')    


g_points=[y_points,f_points,s_points,a_points]

# graphics sample buffer ptr
cnt=0          

#  scroll by n samples 
def scroll(n):
    
    i1=N-n
    for pts in g_points:
        pts[0:N-n]=pts[n:N]
    
    
    
    
# Read ECG values and feed the processor
def read_ecg(processor):
    global running,cnt,timeLeft,space_hit,peakPtr
    

    # Maximium value for raw ECG stream    
    fullScale=1024
    
    # dc should be half fullScale
    ref=fullScale/2.0    
        
    running=True
    
    count=0
    valLast=0    #  just used to do a crude down sampling 400Hz --> 200Hz
    
    while running:
        
        response=source.readline()
        
        if response=="":
            continue
        
        if Record:
            fout.write(response)
            
        try:
            raw=float(response)
        except:
            print "error",response
            continue

        # map onto a -1  to +1 range            
        val=(raw-ref)/fullScale  
        
        # crude down sampler  400 Hz --> 200 Hz
        if (count % 2) == 0:
            val=(val+valLast)*0.5
            count += 1
        else:
            valLast=val
            count +=1
            continue
   
   
   
        if cnt >= N:
            if Replay:
             
                print " Hit key to continue "
                space_hit=False
                while not space_hit:
                    time.sleep(0.1)
                space_hit=False
        
                mutex.acquire()       
                
                leap=int(N/10)
                scroll(leap)
                cnt -= leap
                timeLeft = timeLeft+leap*processor.dt
            
                 # This is not very clever
                peakPtrStart=0
                mutex.release()
            else:
               #  print " RESETING CNT"
                mutex.acquire()
                cnt=0
                timeLeft=processor.time
                mutex.release()
               
        mutex.acquire()       
         
        processor.process(val)
        
        y_points[cnt]=ecg2screen(processor.y_val)
        f_points[cnt]=f2screen(processor.f_val)
        a_points[cnt]=val2Screen(peaker.thresh1)        
        s_points[cnt]=val2Screen(processor.s_val)
          
        cnt  += 1
      
        mutex.release()
        
        
#  GUI stuff ---------------------------------------------------------

# ECG stuff   ---------------
peakPtr=0      #   RR peak display
peakPtrStart=0
#  left of the display time value
timeLeft=0



# BPM
bpmScreenPtLast=None
bpmPtr=0
bpm_background=(50,50,50)
bpm_surf=pygame.Surface(dim_bpm)
bpm_surf.fill(bpm_background)
xBPMright=int((dim_bpm[0]*5)/6)
xBPM_ref=0
windowTime=DT*N
            

    #  Chaos window

chaos_last=None
chaos_new=None


        
# -------------- MAIN BIT -------------------------
#  non gui stuff

bpm=BPM(5)
tachi=Tachiometer(N_MEDIAN,bpm)
peaker=Peaker(tachi,DT)
processor=Processor(peaker,DT)
bpmAverage=MovingDecayAverge(10,DEFAULT_BPM)


#  read ecg on a seperate thread feeding into the processor
#  DON'T DO ANY GUI STUFF ON THIS THREAD
ecg_reader=thread.start_new_thread(read_ecg,(processor,))
 
def draw_bpm_key():
  bpmLine=40
  
  pygame.draw.rect(bpm_surf,(0,0,0),(0,0,40, dim_bpm[1]))
  while True:
      
      pt=bpm2screen(0,bpmLine)
      pt[0]=0
      if pt[1] < 0:
          return
      
      if pt[1] < dim_bpm[1]:
          ttt=str(bpmLine)
          print pt,ttt
          fontMgr.Draw(bpm_surf, 'Courier New', 16, ttt, (pt[0],pt[1]), (20,255,255))
      
      bpmLine+=5

draw_bpm_key()

while True:
    
    
#  Display the caption if set.
    if caption:
        pygame.display.set_caption(caption)
        caption=None
         
    k = pygame.key.get_pressed()
    if k[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
        running=False
        time.sleep(.5)
        # ecg_reader.join()
        if fout:
            fout.close()
        pygame.quit()
        break
    
    if k[pygame.K_SPACE]:
        space_hit=True
        
    
    # Make sure the data does not get tweaked during disply.
    mutex.acquire()
    
    # ECG based values  --------------------------------------------------
    
    ecg_surf.fill((0,0,0))
    
    points1=numpy.column_stack((x_points,y_points))
    points2=numpy.column_stack((x_points,s_points))
    points3=numpy.column_stack((x_points,a_points))
    points4=numpy.column_stack((x_points,f_points))
    
    
    if cnt > 2:
        pygame.draw.lines(ecg_surf, (0,255,0), False, points1[:(cnt-1)])
        pygame.draw.lines(ecg_surf, (0,0,255), False, points2[:(cnt-1)])
        pygame.draw.lines(ecg_surf, (255,0,255), False, points4[:(cnt-1)])
        pygame.draw.lines(ecg_surf, (150,0,0), False, points3[:(cnt-1)])

    n=len(tachi.RR)
    peakPtr=peakPtrStart
  
    medPtLast=None
    while peakPtr<n:
        
        t=tachi.RR[peakPtr][0]
        dTime=t - timeLeft
        
        if dTime < 0:
            peakPtrStart += 1
            peakPtr += 1
        elif dTime > windowTime:
            break
        else:
            xi=int(dTime/processor.dt)
            yi=val2Screen(tachi.RR[peakPtr][1])
            med=val2Screen(tachi.RRmed[peakPtr][1])
            col=RRstate.color[tachi.RR[peakPtr][2]]
            
            if medPtLast != None:
                pygame.draw.line(ecg_surf,(255,255,255),medPtLast,(xi,med))
                
            medPtLast=(xi,med)
            pygame.draw.rect(ecg_surf,col,(xi,yi,4,dim_ecg[1]-yi))
            peakPtr += 1
    
         
    # PLOT the BPM based values ------------------------------------------------------------
    
    while bpmPtr < len(bpm.BPMraw):
        
        bpmNew=bpm.BPMraw[bpmPtr][1]
        bpmAverage.process(bpmNew)
        medNew=bpm.BPMmedian[bpmPtr][1]
        timeNew=bpm.BPMraw[bpmPtr][0]
        
        xNew,tmp=bpm2screen(timeNew,bpmNew)
        
        xOver = xNew-xBPMright
        
        if xOver > 0 :
            xBPM_ref += xOver
            bpm_surf.scroll(-xOver)
            pygame.draw.rect(bpm_surf,bpm_background,(xBPMright-xOver+1,0,xOver,bpm_surf.get_height()))
            bpmScreenPtLast[0] -= xOver
            medScreenPtLast[0] -= xOver
        draw_bpm_key()
            
         
        
        bpmScreenPtNew=bpm2screen(timeNew,bpmNew)
        medScreenPtNew=bpm2screen(timeNew,bpmAverage.get_value())
        
        if bpmScreenPtLast != None:
            pygame.draw.line(bpm_surf,(0,255,0),bpmScreenPtLast,bpmScreenPtNew,5)
            pygame.draw.line(bpm_surf,(100,100,100),medScreenPtLast,medScreenPtNew,4)
            chaos_new=(bpmScreenPtLast[1],bpmScreenPtNew[1])
            
        # print "----",chaos_last,chaos_new
        
        
        if chaos_last != None:
#             chaos_surf.fill((0,0,0,100),special_flags=0) # pygame.BLEND_SUB)
            chaos_surf.fill((0,0,0,5),special_flags=0) # pygame.BLEND_SUB)
            col=chaos_color_at(timeNew)
            pygame.draw.line(chaos_surf,col,chaos_last,chaos_new,5)
                    
        bpmScreenPtLast=bpmScreenPtNew
        medScreenPtLast=medScreenPtNew
        chaos_last=chaos_new
        bpmPtr += 1
        
        
    mutex.release()
        
    
    display.blit(ecg_surf,(0,0))
    display.blit(bpm_surf,(0,dim_ecg[1]))
    display.blit(chaos_surf,(dim_bpm[0],dim_ecg[1]))

    pygame.display.flip()
    clock.tick(FPS)