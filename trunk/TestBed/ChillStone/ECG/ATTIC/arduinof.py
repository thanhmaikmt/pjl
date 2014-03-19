import serial
import pygame
import thread
import time
import numpy
import sys


ser = serial.Serial()
        
# ser.port="/dev/tty.usbmodem1421"   #  LEFT on mac air
ser.port="/dev/tty.usbmodem1411"     #  RIGHT on mac air

FPS=20

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


dim_ecg=(full_screen[0],int(full_screen[1]))

display = pygame.display.set_mode(full_screen)

pygame.display.set_caption('(press escape to exit)')

ecg_surf=pygame.Surface(dim_ecg)
    
def f2screen(val):
    return dim_ecg[1]*0.5*(1-val/640.0) 

def ecg2screen(val):
      return dim_ecg[1]*0.5*(1-val) 
                  
   
clock=pygame.time.Clock()


N=dim_ecg[0]

x_points=numpy.zeros(N,dtype='i')    #  time axis 
y_points=numpy.zeros(N,dtype='i')    #  val of ECG

#  x_axis  set to 1 pixel per sample
for i in range(N):
    x_points[i]=i
 
 
cnt=0

def read_ecg(processor):
    global running,cnt
    
    print "Heelo"
    # Maximium value for raw ECG stream    
    fullScale=1024
    
    # dc should be half fullScale
    ref=fullScale/2.0    
    
    
    running=True
    
    count=0
    valLast=0
    
    while running:
        
        
        print "XXX "
        response = ser.readline()
        
        print response
        
        if response=="":
            continue
        
        try:
            raw=float(response)
        except:
            print "error",response
            continue

        # map onto a -1  to +1 range            
        #val=(raw-ref)/fullScale  
        val =raw
        # crude down sampler  400 Hz --> 200 Hz
        if (count % 2) == 0:
            val=(val+valLast)*0.5
            count += 1
        else:
            valLast=val
            count +=1
            continue
        
        cnt += 1
        if cnt >= N:
            cnt=0
        
        print val
        y_points[cnt]=val
        

# -------------- MAIN BIT -------------------------

import threading

ecg_reader=thread.start_new_thread(read_ecg,(None,))

mutex=threading.Lock()
 
bpmScreenPtLast=None
bpmPtr=0

while True:
    
    k = pygame.key.get_pressed()
    if k[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
        running=False
        time.sleep(.5)
        pygame.quit()
        break
    
    if k[pygame.K_SPACE]:
        space_hit=True
        
    
    ecg_surf.fill((0,0,0))
    
    mutex.acquire()
    points1=numpy.column_stack((x_points,y_points))
    
    
    if cnt > 2:
        pygame.draw.lines(ecg_surf, (0,255,0), False, points1[:(cnt-1)])

        
    mutex.release()
        
        
    display.blit(ecg_surf,(0,0))
    pygame.display.flip()
    clock.tick(FPS)