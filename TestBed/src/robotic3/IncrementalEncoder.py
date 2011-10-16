

import math

class Sensor:
    
    
    def __init__(self,start,space):
        self.start=start
        self.space=space
        self.gap=space/2.0
        self.state=0
        self.resetFlags()
        #self.set(start)
        #self.resetFlags()
        self.fireUp=0
        self.fireDown=0
        
    def set(self,x):
        xx=x-self.start
        
        bit=xx - self.space * math.floor(xx/self.space)
    
        # print bit
        
        stateOld=self.state
        
        if bit < self.gap:
            self.state=1
        else: 
            self.state=0
            
        if self.state > stateOld:
            self.fireUp = 1
        elif self.state < stateOld:
            self.fireDown = 1
            

        
    def resetFlags(self):    
        self.fireUp=0
        self.fireDown=0
    
    

class Logic:
    
    
    def __init__(self,width):
        self.dx=width/4.0
        self.x=0
        
    def step(self,a,b,aUp,aDown,bUp,bDown):
        if (a > 0 and bUp > 0) or  (b>0 and aDown>0) or (a<1 and bDown>0) or (b<1 and aUp >0):
            self.x += self.dx
        elif (b >0 and aUp >0) or  (a>0 and bDown >0) or (b<1 and aDown>0) or (a<1 and bUp >0):
            self.x -= self.dx
            
          
        
def doabit():
    
    global x,time

    tend=time+dtime
    dx=vel*dt
    
    while time < tend:
        xlist.append(x)
        tlist.append(time)
        a.set(x)
        b.set(x)
        aOut.append(a.state)
        bOut.append(b.state)
        aUp.append(a.fireUp)
        bUp.append(b.fireUp)
        aDown.append(a.fireDown)
        bDown.append(b.fireDown)
        l.step(a.state,b.state,a.fireUp,a.fireDown,b.fireUp,b.fireDown)
        lx.append(l.x)
        a.resetFlags()
        b.resetFlags()
        time += dt
        x+=dx
            
            
            

width=4.0
time=0.0
vel=-1.0
dt=.1
dx=vel*dt
x=0.0
t=0.0
dd=width/4.0
bit=0
a=Sensor(0+bit,width)
b=Sensor(dd+bit,width)
l=Logic(width)

aOut=[]
bOut=[]
aUp=[]
bUp=[]
aDown=[]
bDown=[]
lx=[]
tlist=[]
xlist=[]
tlist=[]
    
    
dos=[[.5,8.0],[-1.0,4.],[.5,8.0]]

for do in dos:
    vel=do[0]
    dtime=do[1]
    print vel,dtime
    doabit()

from matplotlib.pyplot import * 

tmax=tlist[len(tlist)-1];

figure(1)   
 
subplot(211)
ylabel("Sensor A")
plot(tlist, aOut)
axis([0.0,tmax,0.0,1.2])    
subplot(212)
ylabel("Sensor B")
plot(tlist, bOut)
xlabel("Time [sec]")
axis([0.0,tmax,0.0,1.2])



figure(2)
plot(tlist,lx)
show()
