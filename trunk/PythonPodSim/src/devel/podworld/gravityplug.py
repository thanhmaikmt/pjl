'''
Created on 1 Dec 2010

@author: pjl
'''

import pygame 
from simulation import *
from random import  *
from copy import *
from math import *
import time
import feedforwardbrain
from pods import *



sensorRange = 2000

BIG=10000

MAX_AGE=100              # pods life span   
N_HIDDEN1=7                 # number of neurons in hidden layer
N_SENSORS=0             # number of sensors
VEL_SCALE=1/80.0
XREF = 350
YREF = 400
X_circ=350
Y_circ=400
RAD_circ=100
X_scale=1/100.0
Y_scale=1/100.0
DANGDT_SCALE=1.0/3.0


layerSizes=[7,N_HIDDEN1,4]

#
# 
#
class GravityPlug:

    RUN_NAME="plugSpin"             # used for file names so you can tag different experiments
    FIT_FMT=" %5.1f "
    WORLD_FILE="rectWorld.world"     # world to use
    CAN_BREED=True
    ###  START OF PROGRAM
    #max_input=[0,0,0,0,0,0,0]
    
        
    def postDraw(self,screen,fontMgr):
        fontMgr.Draw(screen, None, 20,"x",(XREF,YREF), (255,255,255) )       
        pygame.draw.circle(screen,(255,255,255),(X_circ,Y_circ),RAD_circ,2)
        
    # decide if we want to kill a pod        
    def reap_pod(self,pod):
       
        dt=pod.world.dt
        # distance from centre of bounding circle
        dist_BOUND=sqrt((pod.state.x-X_circ)**2+(pod.state.y-Y_circ)**2)
        
        # distance from target
        dist_TARGET= sqrt((pod.state.x-XREF)**2+(pod.state.y-YREF)**2)
     
        # integrate the error 
        try:    
            pod.error_integral += dist_TARGET*dt
        except AttributeError:
            pod.error_integral = 0.0
 
       
        # died of old age!
        # fitness is current distance from the pod plus the average over it's life
        # (this should encourage it to get close quickly)
        if pod.state.age >= MAX_AGE:          
            return -dist_TARGET - pod.error_integral/MAX_AGE
    
        # out of bounds
        # fitness is pod age (offset so it is independent of natural death)
        if dist_BOUND > RAD_circ:
            fit=pod.state.age-BIG
            return  fit
        
        """
        # Same as above if it topples over
        if pod.ang<0.6*pi or pod.ang>1.4*pi:
            fit = pod.age-BIG
            return fit
        """
        
        return None
          
    def  initPod(self,pod):
        # reset the pod and give it a new brain
        pod.state.ang = pi+(0.5 - random())*pi*0.2    # randomize the intial angle
        pod.error_integral=0.0
         
    # normal process called every time step    
    def process(self,pod,dt):
        
        
        # normal control stuff
        control=Control()
        state=pod.state
        
        # create the input for the brain
        # first the velocity of the state 
        input=[state.dxdt*VEL_SCALE]
        input.append(state.dydt*VEL_SCALE)
        input.append(sin(state.ang))
        input.append(cos(state.ang))
        input.append(state.dangdt*DANGDT_SCALE)
        input.append((state.x-XREF)*X_scale)
        input.append((state.y-YREF)*Y_scale)
        
        """
        doit=False
        for i in range(len(input)):
            if abs(input[i]) > GravityPlug.max_input[i]:
                doit=True
                GravityPlug.max_input[i]=abs(input[i])
                
                
        if doit:
            print GravityPlug.max_input
        """
            
        # and all the sensors (in this case none!!!)
        #for s in sensor:
        #    input.append(s.val*SENSOR_SCALE)
            
        # activate the brain to get output    
        output=pod.brain.ffwd(input)
       
        # assign values to the controllers
        control.up=output[0]-output[1]
        control.left=output[2]
        control.right=output[3]
        
        return control

    def createInitialPod(self,i,brain):  
        b=255-(i*167)%256
        g=(i*155)%256
        r=255-(i*125)%256     
        
        sensors=[] 
        for i in range(N_SENSORS):
            ang_ref=i*pi*2.0/N_SENSORS
            sensors.append(Sensor(ang_ref,sensorRange,"sensor"+str(i)))
            
        return GravityPod(sensors,brain,self,(r,g,b))
        
    # If we are trying to evolve and pod dies
    
    def reaper(self,pod,sim):
        
        pool=sim.pool
        if pool.reaping:
            
            fitness=self.reap_pod(pod)
            if fitness != None:
            
                # here then time to replace the pod
                # save current  brain and fitness in the pool
                # fitness=self.calc_fitness(pod,self.brain)
                pool.add(pod.brain,fitness) 
                sim.world.init_pod(pod)
                self.initPod(pod)
                pod.brain=pool.create_new()
                return True
            
        return False
            
                          
    # normal process called every time step
    def createAgent(self,world,pool,id):
        return Agent(world,pool,id)