'''
Created on 1 Dec 2010

@author: pjl
'''

from random import  *
from math import *
from pods import *
from copy import *


sensorRange = 2000

BIG=10000

MAX_AGE=200              # pods life span   
N_HIDDEN1=7                 # number of neurons in hidden layer
N_SENSORS=8             # number of sensors
VEL_SCALE=1/80.0
DANGDT_SCALE=1.0/3.0
SENSOR_SCALE=1.0/100.0      # scale sensors (make more like 0-1)
MIN_AGE=.2
N_TRIP=500




 
paramsRoot=[1.259,200.0,0.01,1.0,-0.0083,1.083,100,80];
     
class ParamBrain:
    def __init__(self):
        
        self.params=deepcopy(paramsRoot)
    
    def clone(self):
        clone=ParamBrain()
        clone.params=deepcopy(self.params)
        return clone
    
    def mutate(self,amount):
        x=self.params
        i=randrange(len(self.params))
        x[i]=x[i] + (random()-0.5)*paramsRoot[i]*amount
        
        
class ParamBrainPlug:
    CAN_BREED=False
    
    def loadBrain(self,file):
        pass
    
    def createBrain(self):
        return ParamBrain()
        
    def breed(self,mum,dad):
        pass
    
    def mutate(self,brain,amount):
        brain.mutate(amount)
    
    
#
# 
#
class CarParamPlug:

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
           # normal control stuff
        
        control=Control()
        
        p=pod.brain.params
        sensor=pod.sensors
        state=pod.state
        
        # V=1.259*sensor[0].val   #  param[0]=1.259
        V=p[0]*sensor[0].val   
        if V>p[1]:                #  param[1]=200.0
            V=p[1]
        cont=(V/(abs(state.vel)+p[2])) - p[3]  #  param[2]=0.01   p[3]=1
        if cont > 0:
            control.up = cont
        else:
            control.down = abs(cont)
            
        diff=(sensor[1].val+sensor[2].val)-(sensor[7].val+sensor[6].val)
        
        turn_compensation=p[4]*sensor[0].val+p[5]   #   param[4]=-0.0083     param[5]=1.083
        
        if diff>0.0:
            control.left=abs((diff/p[6])**2/p[7])+turn_compensation    # param6]=100    param[7=80
        else:
            control.right=abs((diff/p[6])**2/p[7])+turn_compensation
        
        return control
       
       
        
    def createInitialPod(self,i,brain):
                  
        b=255-(i*167)%256
        g=(i*155)%256
        r=255-(i*125)%256    
        return CarPod(N_SENSORS,sensorRange,brain,self,(r,g,b))
    
    
    # If we are trying to evolve and pod dies
    
    def reaper(self,pod,sim):
        
        pool=sim.pool
        if pool.reaping:            
            fitness=self.reap_pod(pod)
            if fitness != None:   
                " here then time to replace the pod"
                # save current  brain and fitness in the pool
                #fitness=self.calc_fitness(pod,self.brain)
                pool.add(pod.brain,fitness) 
                sim.world.init_pod(pod)
                self.initPod(pod)
                pod.brain=pool.create_new()
                return True
            
        return False
            
                          
    


