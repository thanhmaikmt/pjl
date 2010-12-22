'''
Created on 1 Dec 2010

@author: pjl
'''

import pygame 
from simulationMP import *
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
N_SENSORS=8             # number of sensors
VEL_SCALE=1/80.0
DANGDT_SCALE=1.0/3.0
SENSOR_SCALE=1.0/100.0      # scale sensors (make more like 0-1)
MIN_AGE=.2
N_TRIP=21

layerSizes=[N_SENSORS+1,N_HIDDEN1,4]


class Controller:
            def __init__(self,brain,plug):
                self.brain=brain
                brain.fitness=None
                self.plug=plug
                
            def process(self,pod,dt):
                     
                # normal control stuff
                control=self.plug.process(pod,dt)
                
                return control
#
# 
#
class CarPlug:

    RUN_NAME="carPlug"             # used for file names so you can tag different experiments
    FIT_FMT=" %5.1f "
    WORLD_FILE="car_circuit.txt"     # world to use
    CAN_BREED=True
    ###  START OF PROGRAM
    #max_input=[0,0,0,0,0,0,0]
    
    def loadBrain(self,file):
        return feedforwardbrain.loadBrain(file)
    
    def createBrain(self):
        return feedforwardbrain.FeedForwardBrain(layerSizes)
        
    def breed(self,mum,dad):
        
        child=mum.clone()
        for i in range(1,child.num_layer):  
            a=child.weight[i]
            d=dad.weight[i]
            
            n=child.layer_size[i]
            
            split=randrange(n+1)
            #print "split",split
            for j in range(split,n):
                childW=a[j]
                dW=d[j]
                
                for k in range(child.layer_size[i - 1]+1):
                    childW[k]=dW[k]
                    
                    
        return child
        
    def postDraw(self,screen,fontMgr):pass
        
    # decide if we want to kill a pod        
    def reap_pod(self,pod):
       
        dt=pod.world.dt
        
        state=pod.state
        
        if  state.vel < 0:
            print "backwards"
            # print "backwards"
            return 0
        
        if state.age > MIN_AGE and state.distance_travelled == 0:
            print ""
            return 0
        
        if state.age > MAX_AGE or state.collide:
            return  state.pos_trips-state.neg_trips
         
    
        if (state.pos_trips-state.neg_trips) >= N_TRIP:  
            return N_TRIP + MAX_AGE-pod.state.age
        
        return None    
          
    def  initPod(self,pod):
        # reset the pod and give it a new brain
        pod.state.ang = pi+(0.5 - random())*pi*0.2    # randomize the intial angle
         
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
        output=pod.controller.brain.ffwd(input)
       
        # assign values to the controllers
        control.up=output[0]
        control.down=output[1]
        control.left=output[2]
        control.right=output[3] 
      
        return control
        
    def createInitialPod(self,i):
                  
        brain=self.createBrain()
        #control=GAController(self)
        # random colours
        b=255-(i*167)%256
        g=(i*155)%256
        r=255-(i*125)%256    
        return GravityPod(N_SENSORS,sensorRange,Controller(brain,self),(r,g,b))
    

    def init_pod(self,pod,world):
        world.init_pod(pod)
        pod.ang += random()-0.5    # randomize the intial angle
    
    
      # If we are trying to evolve and pod dies
    
    def admin(self,pod,sim):
        
        pool=sim.pool
        if pool.reaping:
            
            fitness=self.reap_pod(pod)
            if fitness != None:
            
                " here then time to replace the pod"
                # save current  brain and fitness in the pool
                #fitness=self.calc_fitness(pod,self.brain)
                pool.add(pod.controller.brain,fitness) 
                sim.world.init_pod(pod)
                self.initPod(pod)
                pod.controller.brain=pool.create_new()
                return True
            
        return False
            
                          
    # normal process called every time step
    def createAgent(self,world,pool,id):
        return Agent(world,pool,id)
    
    


from agent import *
from simulationMP import *
from world import  *
from painter import *
from pool import  *
import gravityplug
from admin import  *

# 
plug=CarPlug()

dt=.1

###  START OF PROGRAM

world       = World(plug.WORLD_FILE,dt)

pool=Pool(world,plug)    #  create a pool for fittest networks

agents=[]        #  pods on the circuits

POP_SIZE=10
for i in range(POP_SIZE):     # create initial population on the circuit
    agents.append(Agent(plug,i))
  
admin       = Admin()
sim         = Simulation(world,agents,plug,pool,admin,plug.RUN_NAME)

# register the painter to display stuff
sim.painter = Painter(sim,plug.RUN_NAME)

# go go go  ..........
sim.run()
