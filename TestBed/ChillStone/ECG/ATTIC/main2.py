import serial
import pygame
import thread
import time
import circbuf
import numpy


FPS=1
N=1400
H=200

BAUD=19200

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

def read_ecg(arg):
    
    global cnt
    
    while (not ser.isOpen()):
        time.sleep(1)
        
    while True:
        response = ser.readline()
        if cnt % SKIP == 0:
            #print response
            try:
                val=(int(response)*H)/MAX_VAL
                buff.append(val)
#                 print val
            except:
                print response
        cnt += 1


ecg_reader=thread.start_new_thread(read_ecg,("ECG",))

x_points=numpy.zeros(N,dtype='i')

for i in range(N):
    x_points[i]=i

while True:
    k = pygame.key.get_pressed()
    if k[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
                pygame.display.quit()
                
        
    plot=buff.get_window()
    
    points=numpy.column_stack((x_points,plot))

    surf.fill((0,0,0))
    
    pygame.draw.lines(surf, (255,0,0), False, points)
       
    display.blit(surf,(0,0))
    pygame.display.flip()
    clock.tick(FPS)