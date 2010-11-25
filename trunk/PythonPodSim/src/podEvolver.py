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
from simulation import *

import pygame 
from random import  *
from copy import *
from fontmanager import  *
import pickle
import time



RUN_NAME="comobo_breed"             # used for file names so you can tag different experiments


# The world
WORLD_FILE="trip_world.txt"     # world to use
N_TRIP=21        # to avoid end wall remove pod after hitting this (last) trip

# An alternative world!!!
#WORLD_FILE="car_circuit.txt"     # world to use
#N_TRIP=200                       # big number because it is a loop



#  parameters that could be varied
    
POOL_SIZE=50               # size of pool of best brains
POP_SIZE=10                # number of pod on circuit
SENSOR_SCALE=1.0/100.0      # scale sensors (make more like 0-1)
VELOCITY_SCALE=1.0/80      # scale velocity (pod starts to slip at 80)
MAX_AGE=80                 # pods life span   
REPROVE_PROB=.2            # probability that selection we trigger a reprove of the best gene
N_HIDDEN=5                # number of neurons in hidden layer
N_SENSORS=12               # number of sensors
MUTATE_SCALE=1.0          # amount of mutation
MIN_AGE=0.2               # Allow to live this long before reaping for not moving
BREED_PROB=0.5            # prob that new entity is from breeding           
CAN_BREED=False           # by default assume can not breed
SEED_PROB=0.1             # probability a new thing is created from nothing

# files used by program

POOL_FILE_NAME=RUN_NAME+"_pool.txt"      # file to save/restore the pool
log_file=open(RUN_NAME+"log.txt","w")    # keep a record of the performance

nin=N_SENSORS+1    # velocoty + sensors are inputs
nout=4             # controls

# specify the neural net parameters with nin nhidden and nout
layerSizes=[nin,N_HIDDEN,nout]


#    This section allows you experiment with different brain implementations


# Feedforward with output=sigmoid(sum)
# if in doubt do not change


import combobrain
def createBrain(): 
    return  combobrain.ComboBrain(layerSizes)

def loadBrain(file):
    return combobrain.loadBrain(file)   

CAN_BREED=True
def breed(mum,dad):
    return combobrain.breed(mum,dad)

"""

import feedforwardbrain
def createBrain(): 
    return  feedforwardbrain.FeedForwardBrain(layerSizes)

def loadBrain(file):
    return feedforwardbrain.loadBrain(file)   


# Feedforward with out=trheshold(sum)
import perceptronbrain
def createBrain(): 
    return  perceptronbrain.PerceptronBrain(layerSizes)

def loadBrain(file):
    return perceptronbrain.loadBrain(file)   


import backpropbrain 
def createBrain(): 
    return  backpropbrain.BackPropBrain(layerSizes)

def loadBrain(file):
    return backpropbrain.loadBrain(file)   
"""

    
# Define some classes

class Painter:   # use me to display stuff
    
    def __init__(self):
        self.preDraw=None       # define this function to draw on top!
        self.fontMgr = cFontManager(((None, 20), (None, 48), ('arial', 24)))
        self.last_time=time.time()
        self.last_ticks = 0
        
    def postDraw(self,screen):
        Y=20
        X=20
        tot_ticks=sim.world.ticks
        ticks=tot_ticks-self.last_ticks
        
        tot_time=time.time()
        
        delta=tot_time-self.last_time
        ticks_per_sec=ticks/delta
        
        self.last_time=tot_time
        self.last_ticks=tot_ticks
                
        avFit="%4.1f" % pool.average_fitness()
        tickRate="%8.1f" % ticks_per_sec
        
        str1=RUN_NAME+' pool size:'+ str(POOL_SIZE)+\
                          ' ticks:'+ str(sim.world.ticks) +\
                          ' best:'+ str(pool.best_fitness())+\
                          ' average:'+ avFit+\
                          ' ticks/sec:'+tickRate+"    "
                                                    
       # print str1
        self.fontMgr.Draw(screen, None, 20,str1,(X,Y), (0,255,0) )
        
class Admin:  # use me to control the simulation
              # see comments to see what key hits do
        
    def process(self):   
        
            # this is called just before each time step
            # do admin tasks here

            global pods

             # output to a log file
            if pool.reaping and log_file!=None and pool.touched:
                log_file.write(str(sim.world.ticks) +','+ str(pool.best_fitness())+','+str(pool.average_fitness())+'\n')
                pool.touched=False
                                
            keyinput = pygame.key.get_pressed()
        
            # speed up/down  display      
            if keyinput[pg.K_KP_PLUS] or keyinput[pg.K_EQUALS]:
                sim.frameskipfactor = sim.frameskipfactor+1
                print "skip factor" ,sim.frameskipfactor
            
            if keyinput[pg.K_MINUS]:
                sim.frameskipfactor = max(1,sim.frameskipfactor-1)
                print "skip factor" ,sim.frameskipfactor

            # display the performance of the best pod in pool
            if  keyinput[pg.K_b]:
                
                
                if pool.reaping:    # if reaping copy existing to allow restore
                    self.pods_copy=copy(pods)
                    pod=pods[0]
                    del pods[:]
                    pods.append(pod)
                else:
                    pod=pods[0]
                    
                    
                world.init_pod(pod)
                pod.ang += random()-0.5    # randomize the intial angle
                pod.control.net=pool.create_best()
                pool.reaping=False
             
            # display the performance of the most proven pod
            if  keyinput[pg.K_p]:
                
                
                if pool.reaping:    # if reaping copy existing to allow restore
                    self.pods_copy=copy(pods)
                    pod=pods[0]
                    del pods[:]
                    pods.append(pod)
                else:
                    pod=pods[0]
                    
                    
                world.init_pod(pod)
                pod.ang += random()-0.5    # randomize the intial angle
                pod.control.net=pool.create_most_proven()
                pool.reaping=False   
                
            # go back into evolution mode after looking at best pod   
            if not pool.reaping and keyinput[pg.K_r]:
                del pods[:]
                pods.extend(self.pods_copy)
                pool.reaping=True

            # save the pool to a file
            if keyinput[pg.K_s]:
                file=open(POOL_FILE_NAME,"w")
                pool.save(file)
                file.close()
                
            # reload the pool from a file
            if keyinput[pg.K_l]:
                file=open(POOL_FILE_NAME,"r")
                pool.load(file)
                file.close()
                

class Pool:  #  use me to store the best brains and create new brains
  
  
    # create a pool
   
    def __init__(self):
        self.list=[]
        self.maxMembers=POOL_SIZE        
        self.elite_bias=1.0/POOL_SIZE
        self.reprover=None
        self.touched=True
        self.reaping=True
        
    # add a new Gene to the Pool  (if better than the worst one in pool)
    # 
    def add(self,gene):  
                
        if len(self.list) >= self.maxMembers:
            if gene.fitness < self.list[self.maxMembers-1].fitness:
                return
          
        for i in range(len(self.list)):
            if gene.fitness > self.list[i].fitness:
                self.touched=True
                self.list.insert(i,gene)
                if len(self.list) > self.maxMembers:
                    self.list.pop()
                return
            
        if len(self.list) < self.maxMembers:
            self.list.append(gene)    
            self.touched=True
             
    # create a neural net from the pool or maybe random
    # might return best net to be reproven
    def create_new(self):
        
    
        # if pool is not full create a random net 
        if len(self.list) < self.maxMembers:         
            #Create a net
            net=createBrain()
            net.proof_count=0   # add proof count field
            return net


        # keep testing the best net in case it was a fluke!!!
        # this removes the best net from the pool 
        # it will get back in if it scores OK 
        if random() < REPROVE_PROB:
            net=self.list[0].net
            del self.list[0]
            net.proof_count += 1
            return net
        
        if random() < SEED_PROB:
            net=createBrain()
            net.proof_count=0
            return net
            
        if CAN_BREED and random() < BREED_PROB:
            mum=self.select2()
            dad=self.select2()
            net=breed(mum,dad)
            net.proof_count=0
    
        
        # Otherwise just select a random net from the pool
        clone=self.select2()
  
        # mutate the cloned net by a random amount.
        clone.mutate(random()*MUTATE_SCALE)
        clone.proof_count=0
        return clone
    
    
    # return top of the pool
    def create_best(self):
        clone=self.list[0].net.clone()
        #clone.proof_count=self.list[0].net.proof_count
        return clone

    # return the one that has been RETESTED the most.
    def create_most_proven(self):
        
        maxProof=-1
        
        for g in self.list:
            if g.net.proof_count > maxProof:
                maxProof=g.net.proof_count
                cloneMe=g.net
                
        clone=cloneMe.clone()
        #clone.proof_count=self.list[0].net.proof_count
        return clone

    # OLD version of selection that I did not like
    def select1(self):
        
        for x in self.list:
            if random() < self.elite_bias:
                clone=x.net.clone()
                return clone
        
        return None


    # random selection from the pool
    # can also return None to trigger a new random net    
    def select2(self):
        
        id=randint(0,len(self.list)-1)
        
        #if id ==len(self.list):
        #    return None
        
        return self.list[id].net.clone()
        
    # return the best fitness in the pool
    # since I retest the best this value can fall
    def best_fitness(self):
        if len(self.list) == 0:
            return 0
        else:
            return self.list[0].fitness
       
    # return average fitness
    def average_fitness(self):
        if len(self.list) == 0:
            return 0
        else:
            sum=0.0
            for x in self.list:
                sum +=x.fitness

            return sum/len(self.list)
        
    # save the pool to a file
    # (note reproof count is not saved)
    def save(self,file):       
        n=len(self.list)
        pickle.dump(n,file)
        
        for x in self.list:
            o=deepcopy(x.fitness)
            pickle.dump(o,file)
            x.net.save(file)
        print "POOL SAVED"
        
    # load pool from a file
    def load(self,file):
        self.list=[]
        n=pickle.load(file)
        print n
        for i in range(n):
            f=pickle.load(file)
            net=loadBrain(file)
            net.proof_count=0    # sorry we lost the proof count when we saved it
            self.add(Gene(net,f))
         
        print "RELOADED POOL"   
        for pod in pods:
            # reset the pod and give it a new net from the pool
            world.init_pod(pod)
            pod.ang += random()-0.5    # randomize the intial angle
            pod.net.net=pool.create_new()
        

# Simple class to store the net and fitness
class Gene:
    
    def __init__(self,net,fitness):
        self.net=net
        self.fitness=fitness
        


# Pod controller
# Note that these are resused with new neural nets during the simulation
# also has a little bit of responsibiltiy for managing the evolution of pods
class GAControl:

    def __init__(self):
        self.net=pool.create_new()
            
    # decide if we want to kill a pod        
    def reap_pod(self,state):
        pod=state.pod
                
        if pod.collide:
            return True
        
        if  pod.vel < 0:
            # print "backwards"
            return True
        
        if pod.age > MIN_AGE and pod.distanceTravelled == 0:
            return True
        
        if pod.age > MAX_AGE:
            return True 
    
        if pod.pos_trips >= N_TRIP:
            return True
        
        return False
    
    # calculate the fitness of a pod
    def calc_fitness(self,state,net):
      
        # encourage them to go fast once they get round the path
        if state.pod.pos_trips == N_TRIP:
            fitness = N_TRIP + MAX_AGE-state.pod.age
        else:    
        # just count the trip wires we have passed        
            fitness = state.pod.pos_trips-state.pod.neg_trips
        
        return fitness    
        
    # normal process called every time step    
    def process(self,sensor,state,dt):
    
                    
        # If we are trying to evolve and pod dies
        if pool.reaping and self.reap_pod(state):
            " here then time to replace the pod"
            
            # save current  net and fitness in the pool
            fitness=self.calc_fitness(state,self.net)
            pool.add(Gene(self.net,fitness)) 
            
            # reset the pod and give it a new net
            world.init_pod(state.pod)
            state.pod.ang += random()-0.5    # randomize the intial angle
            self.net=pool.create_new()
            return
            
        # normal control stuff
        
        control=Control()
            
        # create the input for the net
        # first the velocity of the pod 
        input=[sqrt(state.dxdt**2+state.dydt**2)*VELOCITY_SCALE]
        
        # and all the sensors
        # (note: possibly rear pointing sensors are redundant?)
        for s in sensor:
            input.append(s.val*SENSOR_SCALE)
            
        # activate the net to get output    
        output=self.net.ffwd(input)
       
        # assign values to the controllers
        control.up=output[0]
        control.down=output[1]
        control.left=output[2]
        control.right=output[3]
        
        return control


###  START OF PROGRAM

dt          =.1      
sensorRange = 2000
pool=Pool()    #  create a pool for fittest networks
pods=[]        #  pods on the circuits


for i in range(POP_SIZE):     # create initial population on the circuit
    control=GAControl()
    # random colours
    b=255-(i*167)%256
    g=(i*155)%256
    r=255-(i*125)%256    
    pod = CarPod(N_SENSORS,sensorRange,control,((r,g,b)))
    
    pods.append(pod)


admin       = Admin()
world       = World(WORLD_FILE,pods)
sim         = Simulation(world,dt,admin)

# register the painter to display stuff
sim.painter = Painter()


# go go go  ..........
sim.run()
