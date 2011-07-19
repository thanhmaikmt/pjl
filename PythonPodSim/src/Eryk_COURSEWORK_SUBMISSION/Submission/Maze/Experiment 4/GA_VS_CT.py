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
from backpropbrain import  *
import pygame 
from random import  *
from copy import *
from fontmanager import  *
import time
    
starty = 0
startx = 0
collision_no = 0
reset=False
sens17 = [0,0]

RUN_NAME="pjl"             # used for file names so you can tag different experiments
print "Please Choose the worls:"
print "1 - Trip_world.txt"
print "2 - Car_circuit.txt"
var = raw_input("Enter 1, or 2: ")


if var=="1":
    WORLD_FILE="trip_world.txt"
    N_TRIP=21
    INIT_ANG=pi/2+ random()-0.5
    load=True
    
    
else:
    WORLD_FILE="car_circuit.txt"
    N_TRIP=50
    INIT_ANG=pi*1.1+ random()-0.5
    load=True
    
print  WORLD_FILE + " Loaded"


# The world
     # world to use
        # to avoid end wall remove pod after hitting this (last) trip

# An alternative world!!!
#WORLD_FILE="car_circuit.txt"     # world to use
#N_TRIP=200                       # big number because it is a loop



#  parameters that could be varied
    
POOL_SIZE=50               # size of pool of best brains
POP_SIZE=10               # number of pod on circuit
SENSOR_SCALE=1.0/100.0      # scale sensors (make more like 0-1)
VELOCITY_SCALE=1.0/90      # scale velocity (pod starts to slip at 80)
MAX_AGE=80                 # pods life span   
REPROVE_PROB=.2            # probability that selection we trigger a reprove of the best gene
N_HIDDEN=5                 # number of neurons in hidden layer
N_SENSORS=12              # number of sensors


# files used by program

POOL_FILE_NAME=RUN_NAME+"_pool.txt"      # file to save/restore the pool
log_file=open(RUN_NAME+"log.txt","w")    # keep a record of the performance


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
        
        str1=' pool size:'+ str(POOL_SIZE)+\
                          ' ticks:'+ str(sim.world.ticks) +\
                          ' best:'+ str(pool.best_fitness())+\
                          ' average:'+ avFit+\
                          ' White pod:'+ str(white_pod)+\
                          ' ticks/sec:'+tickRate+"    "+str(tot_time)
                          
       # print str1
        self.fontMgr.Draw(screen, None, 20,str1,(X,Y), (0,255,0) )
class Admin:  # use me to control the simulation
              # see comments to see what key hits do
        
    def process(self):   
        
            # this is called just before each time step
            # do admin tasks here

            global pods,reset,load

             # output to a log file
            if pool.reaping and log_file!=None and pool.touched:
                log_file.write(str(sim.world.ticks) +','+ str(pool.best_fitness())+','+str(pool.average_fitness())+'\n')
                pool.touched=False
                                
            keyinput = pygame.key.get_pressed()
        
            # speed up/down  display      
            if keyinput[pg.K_KP_PLUS] or keyinput[pg.K_EQUALS]:
                sim.frameskipfactor = sim.frameskipfactor+1
                print "skip factor" ,sim.frameskipfactor
                
            if keyinput[pg.K_q]:
                reset=True
            else:
                reset=False
            
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
                pod.ang = pi/2 + random()-0.5    # randomize the intial angle
                pod.control.brain=pool.create_best()
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
                pod.ang = INIT_ANG    # randomize the intial angle
                pod.control.brain=pool.create_most_proven()
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
            if keyinput[pg.K_l] or load==True:
                load=False
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
# also has a little bit of responsibiltiy for managing the evolution of pods
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
    
        if pod.pos_trips >= N_TRIP:
            return True
        
        return False
    
    # calculate the fitness of a pod
    def calc_fitness(self,state,brain):
      
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
            
            # save current  brain and fitness in the pool
            fitness=self.calc_fitness(state,self.brain)
            pool.add(Gene(self.brain,fitness)) 
            
            # reset the pod and give it a new brain
            world.init_pod(state.pod)
            state.pod.ang =INIT_ANG    # randomize the intial angle
            self.brain=pool.create_new()
            return
            
        # normal control stuff
        
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
sensorRange = 1000
pool=Pool(N_SENSORS+1,N_HIDDEN,4)
pods=[]


for i in range(POP_SIZE):
    control=GAControl()
    # random colours
    b=255-(i*167)%256
    g=(i*155)%256
    r=255-(i*125)%256    
    pod = CarPod(N_SENSORS,sensorRange,control,((r,g,b)))
    
    pods.append(pod)
    
def init(state):

       
    
       
    global startx, starty, previous_sensor_value
    startx = state.x
    starty = state.y
    previous_sensor_value=[0,0,0,0,0,0,0,0]
    sens17 = [0,0]
        
        
        
    return 
        
                

class CarControl:
    
    def calc_fitness(self,state):
      
        # encourage them to go fast once they get round the path
        if state.pod.pos_trips == N_TRIP:
            fitness = N_TRIP + MAX_AGE-state.pod.age
        else:    
        # just count the trip wires we have passed        
            fitness = state.pod.pos_trips-state.pod.neg_trips
        
        return fitness    
     
    
    def process(self,sensor,state,dt):
        
        if starty == 0 and startx ==0:
           init(state)
           global turn
           turn="frw"
                
        control=Control()
        
        
        
       
        if pod.collide==True or reset==True:
            pod.y=starty
            pod.x=startx
            pod.ang = INIT_ANG 
            pod.age= 0
            pod.vel= 0
            pod.distanceTravelled=0
            white_pod=0
            pod.pos_trips=0
            pod.neg_trips=0
            global collision_no
            collision_no+=1
            print "\n\ncollision #no",str(collision_no),startx,starty,"\n\n"
            
            
        if True:
            Front_sensor_Gain=1.51*sensor[0].val
            if Front_sensor_Gain>225:
                Front_sensor_Gain=225
            Vellocity_corection=(Front_sensor_Gain/(abs(pod.vel)+0.01)) - 1
            
            if Vellocity_corection > 0:
                if Vellocity_corection>1:
                    Vellocity_corection=1
                control.up = Vellocity_corection
            else:
                if abs(Vellocity_corection)>1:
                    Vellocity_corection=1
                control.down = abs(Vellocity_corection)
                
            Sensor_diffrence=(sensor[1].val+sensor[2].val)-(sensor[7].val+sensor[6].val)
            Turning_correction=-0.0091*sensor[0].val+1.1818
            #y=-0.00003*(sensor[0].val)**2-0.0018*sensor[0].val+ 1.01
            #y = 0.000001*sensor[0].val**3 - 0.0002*sensor[0].val**2 - 0.0027*sensor[0].val + 1.0179
            if Turning_correction<0:
                Turning_correction = 0
            control.down=Turning_correction

            if Sensor_diffrence>0:
                #control.left=abs((diff/100)**2/70)+y
                control.left= abs(0.0009*Sensor_diffrence)+Turning_correction
                #control.left=0.0396*exp(0.0051*abs(diff))+y
            else:
                #control.right=abs((diff/100)**2/70)+y
                control.right = abs(0.0009*Sensor_diffrence)+Turning_correction
                #control.right=0.0396*exp(0.0051*abs(diff))+y

            dsensdt7=(sensor[7].val - sens17.pop())
            dsensdt1=(sensor[1].val - sens17.pop())
            
            sens17.append(sensor[1].val)
            sens17.append(sensor[7].val)

            
            if dsensdt1>10:
                control.left+=dsensdt1/300.0

            if dsensdt7>10:
                control.right+=dsensdt7/300.0
            
            
            
        global white_pod       
        white_pod=self.calc_fitness(state)
        
        return control
    
    
    
    
    
    
    

brain       = CarControl()
pod         = CarPod(8,sensorRange,brain,(255,255,255))

pods.append(pod)

admin       = Admin()
world       = World(WORLD_FILE,pods)
sim         = Simulation(world,dt,admin)

# register the painter to display stuff
sim.painter = Painter()


# go go go  ..........
sim.run()