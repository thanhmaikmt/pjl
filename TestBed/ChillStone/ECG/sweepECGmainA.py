import serial
import pygame
import thread
import time
import numpy
import sys
from filters import *

FPS=30   # pygame frames per second refresh rate.

OFFLINE=True

if OFFLINE:
    Record=False
    Replay=True
    space_hit=False
else:
    Record=True
    Replay=False
 
  
if Record:
    file_name="data/"+time.strftime("%b%d_%H_%M_%S")+".txt"
    fout=open(file_name,"w")

if Replay:
    file_name="data/lookAtMe.txt"
    fin=open(file_name,"r")

    
else:
    ser = serial.Serial()
    
    # ser.port="/dev/tty.usbmodem1421"   #  LEFT on mac air
    ser.port="/dev/tty.usbmodem1411"     #  RIGHT on mac air
    
    #ser.port = "/dev/ttyACM0"           # ubuntu 
 
    # wait for opening the serial connection.
    while True:    
        try:
            ser.open()
            break
        except:
            print " Waiting for serial connection on ",ser.port
            time.sleep(1)
        
        
pygame.init()
modes=pygame.display.list_modes()

full_screen=modes[0]

print full_screen

dim_ecg=(full_screen[0],int(full_screen[1]*0.5))
dim_bpm=(full_screen[0],full_screen[1]-dim_ecg[1])

display = pygame.display.set_mode(full_screen)

pygame.display.set_caption('(press escape to exit)')

ecg_surf=pygame.Surface(dim_ecg)
bpm_surf=pygame.Surface(dim_ecg)

def bpm2screen(t,bpm):
    return (int(t*2),int(dim_ecg[1]-(bpm-45)*dim_ecg[1]/60.0))
    
def f2screen(val):
    return dim_ecg[1]*0.5*(1-val/640.0) 

def ecg2screen(val):
      return dim_ecg[1]*0.5*(1-val) 
                  
   
clock=pygame.time.Clock()



N=dim_ecg[0]
x_points=numpy.zeros(N,dtype='i')    #  time axis 
y_points=numpy.zeros(N,dtype='i')    #  val of ECG
f_points=numpy.zeros(N,dtype='i')    #  filtered ECG
s_points=numpy.zeros(N,dtype='i')    #  processed ECG
a_points=numpy.zeros(N,dtype='i')    

#  x_axis  set to 1 pixel per sample
for i in range(N):
    x_points[i]=i


class Analysis:

    def __init__(self):    
        self.RR=[]
        self.BPM=[]
        self.tlast=0.0
    
    def process(self,t,y):
        self.RR.append((t,y,2*y))
        dt=t-self.tlast
        bpm=60.0/dt
        self.BPM.append((t,bpm))
        self.tlast=t
                
        
class Peaker:

    def __init__(self,analysis):
        self.state=0
#         self.thresh1=250.0
#         self.thresh2=self.thresh1/2
        self.cnt=0
        self.flast=0
        self.analysis=analysis
        
    def process(self,f,t,thresh1):
        """
        f is th esignal value
        t is the time
        thresh1 is the preak detect threshold
        """
        
        thresh2=thresh1*0.5  #  reset peak detect when signal is half the turnon value.
        
        if self.state == 0:          
            if f > self.flast:
                self.state=1
                self.cnt=0         #  start counting
                self.PEAKI=f
                #print 'armed',f
            
        if self.state == 1:        #  we have detected a positive slope
                      
            if f > thresh1:   #   signal > thresh1 then here we go a QRS is detected
                self.PEAKI = max(f,self.PEAKI)
                self.peakTime=t
                self.state=2
                #print 'QRS'
                
            elif f > self.PEAKI:
              self.PEAKI=max(f,self.PEAKI)  
                
            elif f< self.flast :  #   noise peak detected   
            # Yes record and unarm noise peak detection
                self.PEAKI=0.0
                self.state=0
                #print ' Noise '
                    
        if self.state == 2:  #  We are detecting a peak wait for f < peakVal
        
            if f > self.PEAKI:
                self.PEAKI = max(f,self.PEAKI)      # record max value
               
            elif f < thresh1:   #  peak detected  
        
                
                self.analysis.process(self.peakTime,self.PEAKI)
                
                self.PEAKI=0.0
                self.state=0
                self.cnt=0
                
                #print 'waiting'
                  
        self.flast=f
        
class Processor:

    def __init__(self,peaker,dt):
        self.maxMvAv=3000
        self.cnt=0
        self.time=0
        self.timeLeft=0
        self.peaker=peaker
        self.latency=dt*24
        self.dt=dt
        self.lpf=LPF()
        self.hpf=HPF()
        self.deriv=Dervivative()
        self.aver=MovingAverge()
        self.averN=MovingDecayAverge(int(0.3/dt))
        self.delay=Delay(24)
        self.threshLimit=self.maxMvAv*0.1

    def val2Screen(self,val):
        # moving average to screen value 
        return dim_ecg[1]*(1.0-val/self.maxMvAv)
        
    def process(self,val):
        
        global cnt,maxMvAv,space_hit
        
        if self.cnt >= N:
            if Replay:
                while not space_hit:
                    time.sleep(0.1)
                space_hit=False
            time.sleep(.5)
                
            self.cnt = 0
            self.timeLeft = self.time
                
        
                
        valP=dim_ecg[1]*0.5*(1-val) 
                  
        y_points[self.cnt]=ecg2screen(val)
        
        val=self.lpf.process(val)
        f_points[self.cnt]=f2screen(val)
        
        val=self.hpf.process(val)
        
        
        
        
        val=self.deriv.process(val)
        val=val*val
        
        
        val1=self.aver.process(val)
    
        self.thresh1 = self.delay.process(self.averN.process(min(val,self.threshLimit)*5.0))   
        
        a_points[self.cnt]=self.val2Screen(self.thresh1)
        
        self.peaker.process(val1,self.time-self.latency,self.thresh1)
        
        s_points[self.cnt]=self.val2Screen(val1)
        
        
        self.cnt  += 1
        self.time += self.dt
    
    
def read_ecg(processor):
    global running
    
    # Maximium value for raw ECG stream    
    fullScale=1024
    
    # dc should be half fullScale
    ref=fullScale/2.0    
    
    
    running=True
    
    count=0
    valLast=0
    processor.time1=0.0
    
    while running:
        
        if Replay:
            response =fin.readline()
            # time.sleep(1.0/200.0)
        else:
            response = ser.readline()
        
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
            
        processor.process(val)


# -------------- MAIN BIT -------------------------


analysis=Analysis()
peaker=Peaker(analysis)
processor=Processor(peaker,1./200.)
ecg_reader=thread.start_new_thread(read_ecg,(processor,))

peakerPtr=0
peakerPtrStart=0

windowTime=processor.dt*N

bpmScreenPtLast=None
bpmPtr=0

while True:
    
    k = pygame.key.get_pressed()
    if k[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
        running=False
        time.sleep(.5)
        # ecg_reader.join()
        if Record:
            fout.close()
        pygame.quit()
        break
    
    if k[pygame.K_SPACE]:
        space_hit=True
        
    
    ecg_surf.fill((0,0,0))
    
    points1=numpy.column_stack((x_points,y_points))
    points2=numpy.column_stack((x_points,s_points))
    points3=numpy.column_stack((x_points,a_points))
    points4=numpy.column_stack((x_points,f_points))
    
    
    cnt=processor.cnt
    
    if processor.cnt > 2:
        pygame.draw.lines(ecg_surf, (0,255,0), False, points1[:(cnt-1)])
        pygame.draw.lines(ecg_surf, (0,0,255), False, points2[:(cnt-1)])
        #pygame.draw.lines(ecg_surf, (150,0,0), False, thresh1[:(cnt-1)])
        pygame.draw.lines(ecg_surf, (255,0,255), False, points4[:(cnt-1)])
        pygame.draw.lines(ecg_surf, (150,0,0), False, points3[:(cnt-1)])

    n=len(analysis.RR)
    peakerPtr=peakerPtrStart
    
    while peakerPtr<n:
        
        t=analysis.RR[peakerPtr][0]
        dTime=t - processor.timeLeft
        
        if dTime < 0:
            peakerPtrStart += 1
            peakerPtr += 1
        elif dTime > windowTime:
            break
        else:
            xi=int(dTime/processor.dt)
            yi=processor.val2Screen(analysis.RR[peakerPtr][1])
            pygame.draw.rect(ecg_surf,(255,0,255),(xi,yi,4,dim_ecg[1]-yi))
            peakerPtr += 1
        
    while bpmPtr < len(analysis.BPM):
        
        bpmNew=analysis.BPM[bpmPtr][1]
        timeNew=analysis.BPM[bpmPtr][0]
        bpmScreenPtNew=bpm2screen(timeNew,bpmNew)
        
        if bpmScreenPtLast != None:
            pygame.draw.line(bpm_surf,(255,255,0),bpmScreenPtLast,bpmScreenPtNew)
    
        bpmScreenPtLast=bpmScreenPtNew
        bpmPtr += 1
        
        
            
        
        
    display.blit(ecg_surf,(0,0))
    display.blit(bpm_surf,(0,dim_ecg[1]))
    pygame.display.flip()
    clock.tick(FPS)