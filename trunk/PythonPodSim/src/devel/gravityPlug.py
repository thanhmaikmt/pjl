'''
Created on 1 Dec 2010

@author: pjl
'''

#  demonstration of Evolving pods using a randomish search.
#
#   uses the idea of a population selection and mutatation (does not try crossover)
#
#  Each pod is controlled with a neural net.
#  Pods have a finite life.
#  Pods die when they reach the age limit or crash into a wall
#  The fitness of a pod is measured by the distance around track when it dies.
#      if it has completed the circuit I also use the age of pod to encourage speed.
#  A list (Pool) of the best pods is kept.
#  When a pod dies its neural net is added to the pool (if it is good enough)
#    it net is then replaced by a new one created from the pool.
#  The Pool creates new neural nets by mutating one of the brains in the pool.
#  mutation in this version 
#      -  all the weights are changed by a random amount. 
#      -  I also use a random scaling factor so some new pods are small changes whilst
#         others are large changes. 
#  
# Notes: the initial angle of a pod has got a random pertubation.
#        Just because a pod can has achieved a good score does not mean it is the best
#        I keep "re-testing" the best pod in case its score was by chance.
#
#  A log file is written out which could be used to plot graphs of performance to compare different 
#  configurations (e.g. change the size of the POOL)
#
# For more information on the working of this code see in line comments 
# and look at the code. 

import pygame 
from simulation import *
from random import  *
from copy import *
from math import *
import time
import feedforwardbrain

BIG=10000
sensorRange = 2000

#SENSOR_SCALE=1.0/100.0      # scale sensors (make more like 0-1)
MAX_AGE=100                # pods life span   
N_HIDDEN1=5                 # number of neurons in hidden layer
N_HIDDEN2=5
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


layerSizes=[7,N_HIDDEN1,N_HIDDEN2,4]


class GravityPlug:

    RUN_NAME="plug"             # used for file names so you can tag different experiments

    # The world
    WORLD_FILE="rect_world.txt"     # world to use
    ###  START OF PROGRAM
    max_input=[0,0,0,0,0,0,0]
    
    def createBrain(self):
        return feedforwardbrain.FeedForwardBrain(layerSizes)
        
    def postDraw(self,screen,fontMgr):
        fontMgr.Draw(screen, None, 20,"x",(XREF,YREF), (255,255,255) )       
        pygame.draw.circle(screen,(255,255,255),(X_circ,Y_circ),RAD_circ,2)
        
    # decide if we want to kill a pod        
    def reap_pod(self,state,dt):
        pod=state.pod   
       
        # distance from centre of bounding circle
        dist_BOUND=sqrt((state.x-X_circ)**2+(state.y-Y_circ)**2)
        
        # distance from target
        dist_TARGET= sqrt((state.x-XREF)**2+(state.y-YREF)**2)
     
        # integrate the error 
        try:    
            pod.error_integral += dist_TARGET*dt
        except AttributeError:
            pod.error_integral = 0.0
 
       
        # died of old age!
        # fitness is current distance from the pod plus the average over it's life
        # (this should encourage it to get close quickly)
        if pod.age >= MAX_AGE:          
            return -dist_TARGET - pod.error_integral/MAX_AGE
    
        # out of bounds
        # fitness is pod age (offset so it is independent of natural death)
        if dist_BOUND > RAD_circ:
            fit=pod.age-BIG
            return  fit
        
        # Same as above if it topples over
        if state.ang<0.6*pi or state.ang>1.4*pi:
            fit = pod.age-BIG
            return fit
        
        return None
          
    def  initPod(self,pod):
        # reset the pod and give it a new brain
        pod.ang = pi+(0.5 - random())*pi*0.2    # randomize the intial angle
        pod.error_integral=0.0
         
    # normal process called every time step    
    def process(self,sensor,state,dt,brain):
        
        # normal control stuff
        control=Control()
            
        # create the input for the brain
        # first the velocity of the pod 
        input=[state.dxdt*VEL_SCALE]
        input.append(state.dydt*VEL_SCALE)
        input.append(sin(state.ang))
        input.append(cos(state.ang))
        input.append(state.dangdt*DANGDT_SCALE)
        input.append((state.x-XREF)*X_scale)
        input.append((state.y-YREF)*Y_scale)
        
        doit=False
        for i in range(len(input)):
            if abs(input[i]) > GravityPlug.max_input[i]:
                doit=True
                GravityPlug.max_input[i]=abs(input[i])
                
                
        if doit:
            print GravityPlug.max_input
            
        # and all the sensors (in this case none!!!)
        #for s in sensor:
        #    input.append(s.val*SENSOR_SCALE)
            
        # activate the brain to get output    
        output=brain.ffwd(input)
       
        # assign values to the controllers
        control.up=output[0]-output[1]
        control.left=output[2]
        control.right=output[3]
        
        return control

    def createPod(self,control,color):
        return GravityPod(N_SENSORS,sensorRange,control,color)

