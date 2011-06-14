'''
Created on 1 Dec 2010

@author: pjl
'''

from random import  *
from math import *
from pods import *

import pygame as pg

sensorRange = 2000

BIG=10000

MAX_AGE=100              # pods life span   
N_HIDDEN1=7                 # number of neurons in hidden layer
N_SENSORS=8             # number of sensors
VEL_SCALE=1/80.0
DANGDT_SCALE=1.0/3.0
SENSOR_SCALE=1.0/100.0      # scale sensors (make more like 0-1)
MIN_AGE=.2
N_TRIP=200

layerSizes=[N_SENSORS+2,N_HIDDEN1,4]
  
 
#
# 
#
class CarPlug:

    RUN_NAME="carPlug"             # used for file names so you can tag different experiments
    FIT_FMT=" %5.1f "
    WORLD_FILE="carCircuit.world"     # world to use
    
    ###  START OF PROGRAM
    #max_input=[0,0,0,0,0,0,0]
        
          
    def postDraw(self,screen,fontMgr):pass
        
    # decide if we want to kill a pod        
    def reap_pod(self,pod):
       
        dt=pod.world.dt
        
        state=pod.state
        
        if  state.vel < 0:
            # print "backwards"
            return 0
        
        if state.age > MIN_AGE and state.distance_travelled == 0:
            return 0
        
        if state.age > MAX_AGE:
            return  state.pos_trips-state.neg_trips
        
        
        if state.collide:
            return  state.pos_trips-state.neg_trips+state.seg_pos
            
        if (state.pos_trips-state.neg_trips) >= N_TRIP:  
            return N_TRIP + MAX_AGE-pod.state.age
        
        return None    
          
    #def  initPod(self,pod):
        # reset the pod and give it a new brain
    #    pod.state.ang = pi+(0.5 - random())*pi*0.2    # randomize the intial angle
         
    # normal process called every time step    
    def process(self,pod,dt):
         
        # normal control stuff
        control=Control()
        state=pod.state
           
        # create the input for the brain
        # first the velocity of the pod 
        input=[sqrt(state.dxdt**2+state.dydt**2)*VEL_SCALE,state.dangdt*DANGDT_SCALE]
        
        # and all the sensors
        # (note: possibly rear pointing sensors are redundant?)
        for s in pod.sensors:
            input.append(s.val*SENSOR_SCALE)
            
        # activate the brain to get output    
        output=pod.brain.ffwd(input)
       
        # assign values to the controllers
        #"""
        control.up=output[0]
        control.down=output[1]
        control.left=output[2]
        control.right=output[3] 
        """
        
        keyinput=pg.keys.get_pressed()
         
        if keyinput[pg.K_LEFT]:
            control.left=1

        if keyinput[pg.K_RIGHT]:
            control.right=1

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1

        print control.left,control.right,control.up,control.down
        """
        
        return control
        
    def createInitialPod(self,i,brain):
                  
        b=255-(i*167)%256
        g=(i*155)%256
        r=255-(i*125)%256
        sensors=[] 
        for i in range(N_SENSORS):
            ang_ref=i*pi*2.0/N_SENSORS
            sensors.append(Sensor(ang_ref,sensorRange,"sensor"+str(i)))
           
        pod=CarPod(sensors,brain,self,(r,g,b))
        pod.current_goal=0
        pod.brain=brain
        return pod
    
    # If we are trying to evolve and pod dies
    
    def reaper(self,pod,world):
        
        pool=world.pool
        if pool == None:
            return False
         
        if pool.reaping:            
            fit_val=self.reap_pod(pod)
            if fit_val != None:   
                " here then time to replace the pod"
                # save current  brain and fitness in the pool
                #fitness=self.calc_fitness(pod,self.brain)
                pod.brain.vec[pod.current_goal]=fit_val
                pod.current_goal +=1
            
               # print " POD REAP "+ str(pod.brain.vec)
                
                if pool.reject(pod.brain):
                    pod.brain=pool.create_new_brain()    
                    pod.current_goal = 0
                    
                elif pod.current_goal == len(pool.goals):
                #    print " POD --- POOL "
                    pool.add(pod.brain)
                    pod.brain=pool.create_new_brain()    
                    pod.current_goal = 0
                    
                world.init_pod(pod)
                
                pod.state.ang += pool.goals[pod.current_goal].ang
                   
                return True
            
        return False
            
                          
    


