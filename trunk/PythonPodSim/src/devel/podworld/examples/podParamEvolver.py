#  demonstration of Evolving pods using a randomish search.
#
#   uses the idea of a population selection and mutatation (does not try crossover)
#
#  Each pod is controlled with a neural brain.
#  Pods have a finite life.
#  Pods die when they reach the age limit or crash into a wall
#  The fitness of a pod is measured by the distance around track when it dies.
#      if it has completed the circuit I also use the age of pod to encourage speed.
#  A good_brain_list (Pool) of the best pods is kept.
#  When a pod dies its neural brain is added to the pool (if it is good enough)
#    it brain is then replaced by a new one created from the pool.
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
#  configurations (e.brain. change the size of the POOL)
#
# For more information on the working of this code see in line comments 
# and look at the code. 


import simulation 

import pygame 
import  random
import  copy
from fontmanager import  *
import pickle
import time
import pods
import world
import math


# The world
WORLD_FILE="../worlds/carCircuit.world"     # world to use

N_SENSORS=8              # number of sensors


# files used by program

POOL_FILE_NAME=RUN_NAME+"_pool.txt"      # file to save/restore the pool
log_file=open(RUN_NAME+"log.txt","w")    # keep a record of the performance

nin=N_SENSORS+1    # velocity + sensors are inputs

nout=4             # controls


 
#paramsRoot=[1.259,200.0,0.01,1.0,-0.0083,1.083,100,80];
paramsInit= [1.0,  200.0, 0.00, 0.5,-0.01,  1.0,  100,100];
paramsScale=[1.259,200.0, 0.01, 1.0,-0.0083,1.083,100,80];     
    
    
# encapsulate the parameters in a class
class ParamBrain:

    def __init__(self):      
        self.params=copy.deepcopy(paramsInit)
    
    def clone(self):
        clone=ParamBrain()
        clone.params=copy.deepcopy(self.params)
        return clone
    
    def mutate(self):
        x=self.params
        #i=randrange(len(self.params))
        MUTATE_SCALE=0.1 
        for i in range(len(self.params)):
            x[i]=x[i] + (random.random()-0.5)*paramsScale[i]*MUTATE_SCALE
    

#   Pool is responsible for keeping track of the fittest solutions                
POOL_SIZE=1              # size of pool of best brains
SEED_PROB=0.1             # probability a new thing is created from nothing

class Pool:  #  use me to store the best brains and create new brains
   
    def __init__(self):
        self.list=[]
        self.maxMembers=POOL_SIZE        
        self.touched=True
        self.reaping=True
        
    # add a new Gene to the Pool  (if better than the worst one in pool)
    def add(self,brain):  
                
        if len(self.list) >= self.maxMembers:
            if brain.fitness < self.list[self.maxMembers-1].fitness:
                return
          
        for i in range(len(self.list)):
            if brain.fitness >= self.list[i].fitness:
                self.touched=True
                self.list.insert(i,brain)
                if len(self.list) > self.maxMembers:
                    self.list.pop()
                return
            
        if len(self.list) < self.maxMembers:
            self.list.append(brain)    
            self.touched=True
             
    # create a neural brain from the pool or maybe random
    # might return best brain to be reproven
    def create_new(self):
        
    
        # if pool is not full create a random brain 
        if len(self.list) < self.maxMembers or random.random() < SEED_PROB:         
            #Create a brain
            brain=ParamBrain()
            return brain
           
        
        # Otherwise just select a random brain from the pool
        clone=self.select()
  
        # mutate the cloned brain by a random amount.
        clone.mutate(random.random()*MUTATE_SCALE)
        return clone
    
 
    # random selection from the pool
    def select(self):
        id=random.randint(0,len(self.list)-1)       
        return self.list[id].clone()
        
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
            o=copy.deepcopy(x.fitness)
            pickle.dump(o,file)
            x.brain.save(file)
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
            net.fitness=f
            self.add(net)
         
        print "RELOADED POOL"   
        for pod in pods:
            # reset the pod and give it a new brain from the pool
            world.init_pod(pod)
            pod.ang += random()-0.5    # randomize the intial angle
            pod.brain.brain=pool.create_new()
        
            
# decide if we want to kill a pod   

MAX_AGE=200           # pods life span   
MIN_AGE=0.2           # Allow to live this long before reaping for not moving    
def reap_pod(state):
     
        if state.collide:
            return True
        
        if  state.vel < 0:
            # print "backwards"
            return True
        
        if state.age > MIN_AGE and state.distance_travelled == 0:
            return True
        
        if state.age > MAX_AGE:
            return True 
    
        if state.pos_trips >= N_TRIP:
            return True
        
        return False
    
# calculate the fitness of a pod
def calc_fitness(state):
        
        if state.collide:
            return  state.pos_trips-state.neg_trips+state.seg_pos
        
        # encourage them to go fast once they get round the path
        
        if state.pos_trips == N_TRIP:
            fitness = N_TRIP + MAX_AGE-state.age
     
        else:    
        # just count the trip wires we have passed        
            fitness = state.pos_trips-state.neg_trips
        
        return fitness    



class MyController:

    def __init__(self):
        self.brain=pool.create_new()
        
    # normal process called every time step    
    def process(self,pod,dt):
    
                    
        # If we are trying to evolve and pod dies
        if pool.reaping and reap_pod(pod.state):
            " here then time to replace the pod"
            
            # save current  brain and fitness in the pool
            self.brain.fitness=calc_fitness(pod.state)
            
            pool.add(self.brain) 
            
            # reset the pod and give it a new brain
            world.init_pod(pod)
            self.brain=pool.create_new()
            return
            
        # normal control stuff
        
        control=pods.Control()
        
        p=self.brain.params
        
        sensor=pod.sensors
        state=pod.state
       
        V=p[0]*sensor[0].val   
        if V>p[1]:
            V=p[1]
        
        cont=(V/(abs(state.vel+1e-6)+p[2])) - p[3]
        
        if cont > 0:
            control.up = cont
        else:
            control.down = abs(cont)
            
        diff=(sensor[1].val+sensor[2].val)-(sensor[7].val+sensor[6].val)
        
        turn_compensation=p[4]*sensor[0].val+p[5]
        
        if diff>0.0:
            control.left=abs((diff/p[6])**2/p[7])+turn_compensation    
        else:
            control.right=abs((diff/p[6])**2/p[7])+turn_compensation
        
        return control



# create a car and equip it with snesors and a controller
def createCar(nSensor):
    control=MyController()
    sensors=[]
    sensorRange = 2000
    for i in range(nSensor):
        ang_ref=i*math.pi*2/nSensor
        sensors.append(pods.Sensor(ang_ref,sensorRange,"sensor"+str(i)))
        
    # random colours
    b=255-(i*167)%256
    brain=(i*155)%256
    r=255-(i*125)%256
    
        
    pod = pods.CarPod((r,brain,b))
    pod.setController(control)
    pod.addSensors(sensors)
    return pod



# Define some cosmetic stuff  ------------------------------------
class Painter:   # use me to display stuff
    
    def __init__(self):
        self.preDraw=None       # define this function to draw on top!
        self.fontMgr = cFontManager(((None, 20), (None, 48), ('arial', 24)))
        self.last_time=time.time()
        self.last_ticks = 0
        
    def postDraw(self,screen):
        Y=20
        X=20
        tot_ticks=sim.ticks
        ticks=tot_ticks-self.last_ticks
        
        tot_time=time.time()
        
        delta=tot_time-self.last_time
        ticks_per_sec=ticks/delta
        
        self.last_time=tot_time
        self.last_ticks=tot_ticks
                
        avFit="%4.1f" % pool.average_fitness()
        tickRate="%8.1f" % ticks_per_sec
        
        str1=RUN_NAME+' pool size:'+ str(POOL_SIZE)+\
                          ' ticks:'+ str(sim.ticks) +\
                          ' best:'+ str(pool.best_fitness())+\
                          ' average:'+ avFit+\
                          ' ticks/sec:'+tickRate+"    "
        
        
                                                    
       # print str1
        self.fontMgr.Draw(screen, None, 20,str1,(X,Y), (0,255,0) )
        
        
        
class Admin:  # use me to control the simulation
              # see comments to see what key hits do
        
    def process(self,sim):   
        
            # this is called just before each time step
            # do admin tasks here

            global pods

             # output to a log file
            if pool.reaping and log_file!=None and pool.touched:
                log_file.write(str(sim.ticks) +','+ str(pool.best_fitness())+','+str(pool.average_fitness())+'\n')
                pool.touched=False
                                
            keyinput = pygame.key.get_pressed()
        
            # speed up/down  display      
            if keyinput[pygame.K_KP_PLUS] or keyinput[pygame.K_EQUALS]:
                sim.frameskipfactor = sim.frameskipfactor+1
                print "skip factor" ,sim.frameskipfactor
            
            if keyinput[pygame.K_MINUS]:
                sim.frameskipfactor = max(1,sim.frameskipfactor-1)
                print "skip factor" ,sim.frameskipfactor

            # display the performance of the best pod in pool
            if  keyinput[pygame.K_b]:
                
                
                if pool.reaping:    # if reaping copy existing to allow restore
                    self.pods_copy=copy(pods)
                    pod=pods[0]
                    del pods[:]
                    pods.append(pod)
                else:
                    pod=pods[0]
                    
                    
                world.init_pod(pod)
                pod.ang += random()-0.5    # randomize the intial angle
                pod.control.brain=pool.create_best()
                pool.reaping=False
             
            # display the performance of the most proven pod
            if  keyinput[pygame.K_p]:
                
                
                if pool.reaping:    # if reaping copy existing to allow restore
                    self.pods_copy=copy(pods)
                    pod=pods[0]
                    del pods[:]
                    pods.append(pod)
                else:
                    pod=pods[0]
                    
                    
                world.init_pod(pod)
                pod.ang += random()-0.5    # randomize the intial angle
                pod.control.brain=pool.create_most_proven()
                pool.reaping=False   
                
            # go back into evolution mode after looking at best pod   
            if not pool.reaping and keyinput[pg.K_r]:
                del pods[:]
                pods.extend(self.pods_copy)
                pool.reaping=True

            # save the pool to a file
            if keyinput[pygame.K_s]:
                file=open(POOL_FILE_NAME,"w")
                pool.save(file)
                file.close()
                
            # reload the pool from a file
            if keyinput[pygame.K_l]:
                file=open(POOL_FILE_NAME,"r")
                pool.load(file)
                file.close()
        
            if keyinput[pygame.K_d]:
                for brain in pool.list:
                    print brain.fitness," : ",brain.params
                    
                
###  START OF PROGRAM


dt          =.1      

pool=Pool()    #  create a pool for evolving 
podlist=[]     #  pods on the circuit

POP_SIZE=1                  # number of pod on circuit
for i in range(POP_SIZE):     # create initial population on the circuit
    podlist.append(createCar(N_SENSORS))

world       = world.World(WORLD_FILE,dt,podlist)

N_TRIP=len(world.trips)*2        # to avoid end wall remove pod after hitting this (last) trip
print "Max trips :",N_TRIP


sim         = simulation.Simulation(world,"simple param evolver")

# register the painter to display stuff
sim.painter = Painter()

admin       = Admin()
sim.setAdmin(admin)

# go go go  ..........
sim.run()
