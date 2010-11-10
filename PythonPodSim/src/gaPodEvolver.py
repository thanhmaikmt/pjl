#  demonstration of Evolving pods using a randomish search.
#
#   uses the idea of a population selection and mutatation (does not try crossover)
#
#  Each pod is controlled with a neural net.
#  Pods have a finite life.
#  Pods die when they reach the age limit or crash into a wall
#  The fitness of a pod is measured by the distance around track when it dies.
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
from backpropbrain import  *
import pygame 
from random import  *
from copy import *
from fontmanager import  *
    



RUN_NAME="pjl"             # used for file names so you can tag different experiments
WORLD_FILE="world.txt"     # world to use

#  parameters that could be varied
    
POOL_SIZE=50               # size of pool of best brains
POP_SIZE=10                # number of pod on circuit
SENSOR_SCALE=1.0/10.0      # scale sensors (make more like 0-1)
VELOCITY_SCALE=1.0/80      # scale velocity (pod starts to slip at 80)
MAX_AGE=40                 # pods live for 40 seconds   
REPROVE_PROB=.2            # probability that selection we trigger a reprove of the best gene
N_HIDDEN=5                 # number of neurons in hidden layer
N_SENSORS=12               # number of sensors

# files used by program

POOL_FILE_NAME=RUN_NAME+"_pool.txt"      # file to save/restore the pool
log_file=open(RUN_NAME+"log.txt","w")    # keep a record of the performance


# Define some classes

class Painter:   # use me to display stuff
    
    def __init__(self):
        self.preDraw=None       # define this function to draw on top!
        self.fontMgr = cFontManager(((None, 20), (None, 48), ('arial', 24)))
    
    def postDraw(self,screen):
        Y=20
        X=20
        self.fontMgr.Draw(screen, None, 20,\
                          ' pool size:'+ str(POOL_SIZE)+\
                          ' ticks:'+ str(sim.world.ticks) +\
                          ' best:'+ str(pool.best_fitness())+\
                          ' average:'+ str(pool.average_fitness()), (X,Y), (0,255,0))
    
        
class Admin:  # use me to control the simulation
        
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

            # display the performance of the best pod
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
                pod.control.brain=pool.create_best()
                pool.reaping=False
             
            # display the performance of the best pod
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
                pod.control.brain=pool.create_most_proven()
                pool.reaping=False   
                
            # go back into evolution mode    
            if not pool.reaping and keyinput[pg.K_r]:
                del pods[:]
                pods.extend(self.pods_copy)
                pool.reaping=True

            
            if keyinput[pg.K_s]:
                file=open(POOL_FILE_NAME,"w")
                pool.save(file)
                file.close()
                
            if keyinput[pg.K_l]:
                file=open(POOL_FILE_NAME,"r")
                pool.load(file)
                file.close()
                
                
                
                    

class Pool:  #  use me to store the best brains and create new brains
  
  
    # create a pool
    # specify the neural net parameters with nin nhidden and nout
    def __init__(self,nin,nhidden,nout):
        self.list=[]
        self.maxMembers=POOL_SIZE
        self.layerSizes=[nin,nhidden,nout]
        self.elite_bias=1.0/POOL_SIZE
        self.reprover=None
        self.touched=True
        self.reaping=True
        
    
    # add a new Gene to the Pool
    def add(self,x):  
        
        if len(self.list) >= self.maxMembers:
            if x.fitness < self.list[self.maxMembers-1].fitness:
                return
          
        for i in range(len(self.list)):
            if x.fitness > self.list[i].fitness:
                self.touched=True
                self.list.insert(i,x)
                if len(self.list) > self.maxMembers:
                    self.list.pop()
                return
            
        if len(self.list) < self.maxMembers:
            self.list.append(x)    
            self.touched=True
             
    # create a neural net
    def create_new(self):
        
    
        # if pool is not full create a random brain 
        if len(self.list) < self.maxMembers:         
            #Create a brain
            brain=BackPropBrain(self.layerSizes)
            brain.proof_count=0
            return brain


        # keep testing the best brain in case it was a fluke!!!
        # this removes the best net from the pool 
        # it will get back in if it scores OK 
        if random() < REPROVE_PROB:
            brain=self.list[0].brain
            del self.list[0]
            brain.proof_count += 1
            return brain
            
            
        # Otherwise just select a random brain from the pool
        clone=self.select2()

        # if this returned None create a new random brain
        if clone==None:
            brain=BackPropBrain(self.layerSizes)
            brain.proof_count=0
            return brain
        
        
        # mutate the cloned brain by a random amount.
        clone.mutate(random())
        clone.proof_count=0
        return clone
    
    
    # return top of the pool
    def create_best(self):
        clone=self.list[0].brain.clone()
        #clone.proof_count=self.list[0].brain.proof_count
        return clone

    # return the one that has been RETESTED the most.
    def create_most_proven(self):
        
        maxProof=-1
        
        for g in self.list:
            if g.brain.proof_count > maxProof:
                maxProof=g.brain.proof_count
                cloneMe=g.brain
                
        clone=cloneMe.clone()
        #clone.proof_count=self.list[0].brain.proof_count
        return clone

    # OLD version of selection that I did not like
    def select1(self):
        
        for x in self.list:
            if random() < self.elite_bias:
                clone=x.brain.clone()
                return clone
        
        return None


    # random selection from the pool
    # can also return None to trigger a new random brain    
    def select2(self):
        
        id=randint(0,len(self.list))
        
        if id ==len(self.list):
            return None
        
        return self.list[id].brain.clone()
        
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
            x.brain.save(file)
        print "POOL SAVED"
        
    # load pool from a file
    def load(self,file):
        self.list=[]
        n=pickle.load(file)
        print n
        for i in range(n):
            f=pickle.load(file)
            b=loadBrain(file)
            b.proof_count=0    # sorry we lost the proof count when we saved it
            self.add(Gene(b,f))
         
        print "RELOADED POOL"   
            

# Simple class to store the brain and fitness
class Gene:
    
    def __init__(self,brain,fitness):
        self.brain=brain
        self.fitness=fitness
        


# Pod controller
# Note that these are resused with new neural nets during the simulation
class GAControl:

    def __init__(self):
        self.brain=pool.create_new()
    
    # decide if we want to kill a pod        
    def reap_pod(self,state):
        pod=state.pod
        
        if pod.collide:
            return True
        
        if pod.age > MAX_AGE:
            return True 
    
        return False
    
    # calculate the fitness of a pod
    def calc_fitness(self,state,brain):
      
        # just count the trip wires we have passed        
        fitness = state.pod.pos_trips-state.pod.neg_trips
        
        return fitness    
        
    # normal process called every time step    
    def process(self,sensor,state,dt):
    
                    
        # If we are trying to evolve and pod dies
        if pool.reaping and self.reap_pod(state):
            " here then time to replace the pod"
            
            # save current  brain and fitness in the pool
            fitness=self.calc_fitness(state,self.brain)
            pool.add(Gene(self.brain,fitness)) 
            
            # reset the pod and give it a new brain
            world.init_pod(state.pod)
            state.pod.ang += random()-0.5    # randomize the intial angle
            self.brain=pool.create_new()
            return
            
        
        control=Control()
            
        # create the input for the brain
        # first the velocity of the pod 
        input=[sqrt(state.dxdt**2+state.dydt**2)*VELOCITY_SCALE]
        
        # and all the sensors
        # (note: possibly rear pointing sensors are redundant?)
        for s in sensor:
            input.append(s.val*SENSOR_SCALE)
            
        # activate the brain to get output    
        output=self.brain.ffwd(input)
       
        # assign values to the controllers
        control.up=output[0]
        control.down=output[1]
        control.left=output[2]
        control.right=output[3]
        
        return control


###  START OF PROGRAM

dt          =.1       
sensorRange = 2000


pool=Pool(N_SENSORS+1,N_HIDDEN,4)

NPODS=POP_SIZE

pods=[]


for i in range(NPODS):
    control=GAControl()
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


#uncomment the next line to hide the walls.
#sim.world.blind=True
#sim.frameskipfactor=10


sim.run()
