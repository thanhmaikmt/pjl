import serial
import pygame
import thread
import time
#import circbuf
import numpy

#!/usr/bin/python
 
import time
 
file_name="data/"+time.strftime("%b%d_%H_%M_%S")+".txt"

fout=open(file_name,"w")

FPS=30   # frames per second.


N=1400
H=200

BAUD=19200

MAX_VAL=1024

ser = serial.Serial()
# ser.port="/dev/tty.usbmodem1421"   #  LEFT on mac air
ser.port="/dev/tty.usbmodem1411"     #  RIGHT on mac air

#ser.port = "/dev/ttyACM0" # may be called something different

ser.baudrate = BAUD  # may be different
ser.open()


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

x_points=numpy.zeros(N,dtype='i')
y_points=numpy.zeros(N,dtype='i')


def read_ecg(arg):
    
    global cnt,x_points
    
    while (not ser.isOpen()):
        time.sleep(1)
        
    while True:
        response = ser.readline()
        fout.write(response)
        if cnt >= N:
            cnt = 0
        
        try:    
            val=(int(response)*H)/MAX_VAL
            
            y_points[cnt]=val
#             print cnt,val
        except:
            print "error",response
            
        cnt += 1
       

ecg_reader=thread.start_new_thread(read_ecg,("ECG",))



for i in range(N):
    x_points[i]=i

while True:
    
    k = pygame.key.get_pressed()
    if k[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
        fout.close()
        pygame.display.quit()
    
    surf.fill((0,0,0))
    
    points=numpy.column_stack((x_points,y_points))
    
    if cnt > 2:
        pygame.draw.lines(surf, (255,255,0), False, points[:(cnt-1)])
       
    display.blit(surf,(0,0))
    pygame.display.flip()
    clock.tick(FPS)