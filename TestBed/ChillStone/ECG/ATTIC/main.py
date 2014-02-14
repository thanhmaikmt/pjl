import serial
import pygame
import thread
import time
import numpy


FPS=1
N=1200
H=200

BAUD=300

MAX_VAL=1024
SKIP=2

ser = serial.Serial()
ser.port="/dev/tty.usbmodem1421"

#ser.port = "/dev/ttyACM0" # may be called something different

ser.baudrate = BAUD  # may be different
ser.open()

buff=circbuf.CircularBuffer(N)

pygame.init()
modes=pygame.display.list_modes()

dim_display=modes[0]

print dim_display
dim_display=(N,H)

display = pygame.display.set_mode(dim_display)

pygame.display.set_caption('(press escape to exit)')

surf=pygame.Surface((N,H))

clock=pygame.time.Clock()

cnt=0
cntPlot=0

x_points=numpy.zeros(N,dtype='i')
y_points=numpy.zeros(N,dtype='i')
points=numpy.column_stack((x_points,y_points))

for i in range(N):
    x_points[i]=i

def read_ecg(arg):
    
    global cnt
    
    while (not ser.isOpen()):
        time.sleep(1)
        
    while True:
        response = ser.readline()
        #print response
        try:
            val=(int(response)*H)/MAX_VAL
            points[cnt][1]=val
        except:
            print response
        cnt += 1


ecg_reader=thread.start_new_thread(read_ecg,("ECG",))



while True:
    k = pygame.key.get_pressed()
    if k[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
                pygame.display.quit()
                
        
    plot=buff.get_window()
    
    
    if clear:    
        surf.fill((0,0,0))
        cntPlot=0
        
    for i in range(N):
        pygame.draw.lines(surf, (255,0,0), False, points[cnt1:cnt2])
       
    display.blit(surf,(0,0))
    pygame.display.flip()
    clock.tick(FPS)