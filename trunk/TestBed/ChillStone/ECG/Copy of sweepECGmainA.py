import serial
import pygame
import thread
import time
import numpy
import sys
from filters import *
from process import *


THRESH_HALF_LIFE=0.2   #  time for threshold to decay to half it's value 
THRESH_SCALE=2.0       #  scale the threshold value (decrease to make more sensitive)
N_MEDIAN=13

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
        self.averN=MovingDecayAverge(int(THRESH_HALF_LIFE/dt))
        self.delay=Delay(24)
        self.threshLimit=self.maxMvAv*0.1

    def val2Screen(self,val):
        # moving average to screen value 
        return dim_ecg[1]*(1.0-val/self.maxMvAv)
        
        
    # process a single ECG value 
    # assuming a sample rate of 200 Hz and  val is normalize in the range -1 -> 1
    def process(self,val):
        
        global cnt,maxMvAv,space_hit
        
        if self.cnt >= N:
            if Replay:
                space_hit=False
                while not space_hit:
                    time.sleep(0.1)
                space_hit=False
                
            self.cnt = 0
            self.timeLeft = self.time        
         
        mutex.acquire()       
        valP=dim_ecg[1]*0.5*(1-val) 
                  
        y_points[self.cnt]=ecg2screen(val)
        
        val=self.lpf.process(val)
        
        f_points[self.cnt]=f2screen(val)
        
        val=self.hpf.process(val)
                
        val=self.deriv.process(val)
        val=val*val
        
        val1=self.aver.process(val)
    
#     adaptive thresh    
        self.thresh1 = self.delay.process(self.averN.process(min(val,self.threshLimit)*THRESH_SCALE))   
        
        a_points[self.cnt]=self.val2Screen(self.thresh1)
        
        self.peaker.process(val1,self.time-self.latency,self.thresh1)
        
        s_points[self.cnt]=self.val2Screen(val1)
          
        self.cnt  += 1
        self.time += self.dt
        mutex.release()
        


FPS=30   # pygame frames per second refresh rate.

OFFLINE=True

if OFFLINE:
    Record=False
    Replay=True
    space_hit=False
else:
    Record=True
    Replay=False
 

class MultiFileStream:
    
    def __init__(self,dir):
        import glob
        self.fn_iter=glob.glob(dir+"/*.txt").__iter__()
        self.next_file()
    def next_file(self):
        self.file_name=self.fn_iter.next()
        if self.file_name:
            self.fin=open(self.file_name,"r")
        else:   
            self.fin=None
        
    def readline(self):
        if self.fin == None:
            return None
        
        while True:
            line=self.fin.readline()
            if line:
                return line
            
            self.next_file()
            if not self.fin:
                return None
            


mode=0            
            
if mode == 0:        
    fin=MultiFileStream("test_data")
elif mode == 1:
    file_name="test_data/Josh.txt"
    fin=open(file_name,"r")
  
elif mode == 2:

    if Record:
        file_name="data/"+time.strftime("%b%d_%H_%M_%S")+".txt"
        fout=open(file_name,"w")    
        
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
    return (int(t*4),int(dim_ecg[1]-(bpm-45)*dim_ecg[1]/60.0))
    
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

import threading

tachi=Tachiometer(N_MEDIAN)
peaker=Peaker(tachi)
processor=Processor(peaker,1./200.)
ecg_reader=thread.start_new_thread(read_ecg,(processor,))

mutex=threading.Lock()
  
peakPtr=0
peakPtrStart=0

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
    
    mutex.acquire()
    points1=numpy.column_stack((x_points,y_points))
    points2=numpy.column_stack((x_points,s_points))
    points3=numpy.column_stack((x_points,a_points))
    points4=numpy.column_stack((x_points,f_points))
    
    
    cnt=processor.cnt
    
    if processor.cnt > 2:
        pygame.draw.lines(ecg_surf, (0,255,0), False, points1[:(cnt-1)])
        pygame.draw.lines(ecg_surf, (0,0,255), False, points2[:(cnt-1)])
        pygame.draw.lines(ecg_surf, (255,0,255), False, points4[:(cnt-1)])
        pygame.draw.lines(ecg_surf, (150,0,0), False, points3[:(cnt-1)])

    n=len(tachi.RR)
    peakPtr=peakPtrStart
  
    medPtLast=None
    while peakPtr<n:
        
        t=tachi.RR[peakPtr][0]
        dTime=t - processor.timeLeft
        
        if dTime < 0:
            peakPtrStart += 1
            peakPtr += 1
        elif dTime > windowTime:
            break
        else:
            xi=int(dTime/processor.dt)
            yi=processor.val2Screen(tachi.RR[peakPtr][1])
            med=processor.val2Screen(tachi.RRmed[peakPtr][1])
            col=RRstate.color[tachi.RR[peakPtr][2]]
            
            if medPtLast != None:
                pygame.draw.line(ecg_surf,(255,255,255),medPtLast,(xi,med))
                
            medPtLast=(xi,med)
            pygame.draw.rect(ecg_surf,col,(xi,yi,4,dim_ecg[1]-yi))
            peakPtr += 1
    
         
        
    while bpmPtr < len(tachi.BPMraw):
        
        bpmNew=tachi.BPMraw[bpmPtr][1]
        medNew=tachi.BPMmedian[bpmPtr][1]
        timeNew=tachi.BPMraw[bpmPtr][0]
        bpmScreenPtNew=bpm2screen(timeNew,bpmNew)
        medScreenPtNew=bpm2screen(timeNew,medNew)
        
        if bpmScreenPtLast != None:
            pygame.draw.line(bpm_surf,(255,0,0),bpmScreenPtLast,bpmScreenPtNew)
            pygame.draw.line(bpm_surf,(0,255,0),medScreenPtLast,medScreenPtNew)
            
        bpmScreenPtLast=bpmScreenPtNew
        medScreenPtLast=medScreenPtNew
        bpmPtr += 1
        
        
    mutex.release()
        
        
    display.blit(ecg_surf,(0,0))
    display.blit(bpm_surf,(0,dim_ecg[1]))
    pygame.display.flip()
    clock.tick(FPS)