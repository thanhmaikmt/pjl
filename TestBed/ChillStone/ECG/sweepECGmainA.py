import serial
import pygame
import thread
import time
#import circbuf
import numpy
import sys
#!/usr/bin/python
 
import time
 
file_name="data/"+time.strftime("%b%d_%H_%M_%S")+".txt"

fout=open(file_name,"w")

FPS=30   # frames per second.


N=1400
H=400

BAUD=19200

MAX_VAL=1024
fullScale=MAX_VAL
ref=fullScale/2.0
maxMvAv=0.0
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
maxMovAv=0.0

x_points=numpy.zeros(N,dtype='i')
y_points=numpy.zeros(N,dtype='i')
s_points=numpy.zeros(N,dtype='i')

"""
static int y1 = 0, y2 = 0, x[26], n = 12;
int y0;
x[n] = x[n + 13] = data;
y0 = (y1 << 1) - y2 + x[n] - (x[n + 6] << 1) + x[n + 12];
y2 = y1;
y1 = y0;
y0 >>= 5;
if(--n < 0)
n = 12;
return(y0);
"""
class LPF:
    
    def __init__(self):
        self.y1 = 0
        self.y2 = 0
        self.x=numpy.zeros(26)
        self.n = 12
        
    
    def process(self,data):
    
        self.x[self.n] = self.x[self.n + 13] = data;
        y0 = 2*self.y1 - self.y2 + self.x[self.n] - (2*self.x[self.n + 6]) + self.x[self.n + 12];
        self.y2 = self.y1
        self.y1 = y0
        y0 *= 32
        self.n -= 1
        if self.n < 0:
            self.n = 12
        return y0

"""
static int y1 = 0, x[66], n = 32;
int y0;
x[n] = x[n + 33] = data;
y0 = y1 + x[n] - x[n + 32];
y1 = y0;
if(--n < 0)
n = 32;
return(x[n + 16] - (y0 >> 5));
}
"""
        
class HPF:
    
    def __init__(self):
        self.y1 = 0
        self.x=numpy.zeros(66)
        self.n = 32
    
    def process(self,data):
    
        self.x[self.n] = self.x[self.n + 33] = data;
        y0 = self.y1 + self.x[self.n] - self.x[self.n + 32]
        self.y1 = y0;
        self.n -=1
        if self.n < 0:
            self.n = 32
        return self.x[self.n+16]-y0/32.0


"""
int Derivative(int data)
{
int y, i;
static int x_derv[4];
/*y = 1/8 (2x( nT) + x( nT - T) - x( nT - 3T) - 2x( nT -  4T))*/
y = (data << 1) + x_derv[3] - x_derv[1] - ( x_derv[0] << 1);
y >>= 3;
for (i = 0; i < 3; i++)
x_derv[i] = x_derv[i + 1];
x_derv[3] = data;
return(y);
"""
class Dervivative:
    
    def __init__(self):
        self.y = 0
        self.i = 0
        self.x_derv=numpy.zeros(4)
  
    def process(self,data):
    
        y = 2*data + self.x_derv[3] -self.x_derv[1]- 2*self.x_derv[0]
        y = y/8
        self.x_derv[0]=self.x_derv[1]
        self.x_derv[1]=self.x_derv[2]
        self.x_derv[2]=self.x_derv[3]
        self.x_derv[3]=data
        return y

"""
static int x[32], ptr = 0;
static long sum = 0;
long ly;
int y;
if(++ptr == 32)
ptr = 0;
sum -= x[ptr];
sum += data;
x[ptr] = data;
ly = sum >> 5;
if(ly > 32400) /*check for register overflow*/
y = 32400;
else
y = (int) ly;
return(y);
"""

class MovingAverge:
    
    def __init__(self):
        self.sum = 0
        self.ptr = 0
        self.x=numpy.zeros(32)
  
    def process(self,data):
    
        self.ptr+=1
        if self.ptr== 32:
            self.ptr=0
        self.sum -= self.x[self.ptr]
        self.sum += data
        self.x[self.ptr]=data
        
        return self.sum/32.0


count=0
valLast=0.0

def read_ecg(arg):
    
    global cnt,x_points,s_points,maxMvAv,valLast,count
    
    while (not ser.isOpen()):
        time.sleep(1)
        
    while True:
        response = ser.readline()
        
        if response=="":
            continue
        
        fout.write(response)
        if cnt >= N:
            cnt = 0
        
#         try:    
        if True:
            raw=float(response)
            val=(raw-ref)/fullScale  
                       
            if (count % 2) == 0:
                val=(val+valLast)*0.5
                count += 1
            else:
                valLast=val
                count +=1
                continue
                
            valP=H*0.5*(1-val)           
            y_points[cnt]=valP
            
            val=lpf.process(val)
            val=hpf.process(val)
            val=deriv.process(val)
            val=val*val
            val=aver.process(val)
            maxMvAv = max(maxMvAv,val)
            
#             print val,maxMvAv
            if maxMvAv > 0.0 :
                 s_points[cnt]=H*(1.0-val/maxMvAv)
            else:
                 s_points[cnt]=0
#                  
#         except:
#             print "error",response
                
        cnt += 1
       

ecg_reader=thread.start_new_thread(read_ecg,("ECG",))

lpf=LPF()
hpf=HPF()
deriv=Dervivative()
aver=MovingAverge()



for i in range(N):
    x_points[i]=i

while True:
    
    k = pygame.key.get_pressed()
    if k[pygame.K_ESCAPE] or pygame.event.peek(pygame.QUIT):
        fout.close()
        pygame.display.quit()
    
    surf.fill((0,0,0))
    
    points1=numpy.column_stack((x_points,y_points))
    points2=numpy.column_stack((x_points,s_points))

    if cnt > 2:
        pygame.draw.lines(surf, (255,255,0), False, points1[:(cnt-1)])
        pygame.draw.lines(surf, (0,255,255), False, points2[:(cnt-1)])
       
    display.blit(surf,(0,0))
    pygame.display.flip()
    clock.tick(FPS)