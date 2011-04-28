from matplotlib.pyplot import *


class Fitzhugh:
    
    def __init__(self):
        self.thresh = 0.2   #   theta
        self.shunt = 1.2    # 2.5    #   gamma
        self.coupling = 0.0015 # 0.01   # epsilon
        self.v=0
        self.w=0
        
    def step(self,dt,input):
        dvdt = -self.v*(self.v-self.thresh)*(self.v-1.0)-self.w+input
        dwdt = self.coupling*(self.v-self.shunt*self.w)
        self.v += dvdt*dt
        self.w += dwdt*dt
   
        

nOsc=9
oscs =[] 
va=[]

inputs = []     #.112  omega

for i in range(nOsc):
    oscs.append(Fitzhugh())
    va.append([])
    inputs.append((i+5)*.012)

ta=[]
t=0.0

dt=.1
tend=5000

nstep=int(tend/dt)
   
for i in range(0,nstep):
    ta.append(t)
   
    for osc,vv,input in zip(oscs,va,inputs):
        vv.append(osc.v)
        osc.step(dt,input)
        
        
    # input=0;
    t+=dt

#subplot('311')
#plot(va,wa)

key=str(nOsc)

for i in range(len(oscs)):
    
    subplot(key+'1'+str(i+1))

    plot(ta,va[i])


show()