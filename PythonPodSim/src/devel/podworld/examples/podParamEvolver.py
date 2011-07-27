import simulation 

import pygame 
import  random
import  copy
import fontmanager 
import pickle
import time
import pods
import world
import math


# The world
WORLD_FILE="../worlds/carCircuit.world"     # world to use

N_SENSORS   =8              # number of sensors

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
            scale=paramsScale[i]*MUTATE_SCALE*random.random()
            x[i] = x[i] + (random.random()-0.5)*scale
    

         
# create a neural brain from the pool or maybe random
# might return best brain to be reproven
SEED_PROB=.05
MUTATE_SCALE=.1
def create_new():
        
        # if pool is not full create a random brain 
        if random.random() < SEED_PROB or best_brain == None:         
            #Create a brain
            brain=ParamBrain()
            return brain
  
        # Otherwise just select a random brain from the pool
        clone=best_brain.clone()
  
        # mutate the cloned brain by a random amount.
        clone.mutate()
        return clone
    

            
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

   
    # normal process called every time step    
    def process(self,pod,dt):
    
             
        global best_brain
        global best_fitness
               
        # If we are trying to evolve and pod dies
        if reap_pod(pod.state):
            " here then time to replace the brain"
            # save current  brain and fitness in the pool
            fitness=calc_fitness(pod.state)
            
            if fitness > best_fitness:
                best_brain=pod.brain
                best_fitness=fitness
                print fitness, " : ",pod.brain.params
            
            # reset the pod and give it a new brain
            world.init_pod(pod)
            pod.brain=create_new()
            return
            
        # normal control stuff
        
        control=pods.Control()
        
        p=pod.brain.params
        
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




# Define some cosmetic stuff  ------------------------------------
class Painter:   # use me to display stuff
    
    def __init__(self):
        self.preDraw=None       # define this function to draw on top!
        self.fontMgr = fontmanager.cFontManager(((None, 24), (None, 48), ('arial', 24)))
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
                
        
        tickRate="%8.1f" % ticks_per_sec
        
        str1=' ticks:'+ str(sim.ticks) +\
             ' best:'+ str(best_fitness)+\
             ' ticks/sec:'+tickRate+"    "
                                                   
       # print str1
        self.fontMgr.Draw(screen, None, 24,str1,(X,Y), (0,255,0) )
        
        
        
class Admin:  # use me to control the simulation
              # see comments to see what key hits do
        
    def process(self,sim):   
        
            # this is called just before each time step
            # do admin tasks here
                          
            keyinput = pygame.key.get_pressed()
        
            # speed up/down  display      
            if keyinput[pygame.K_KP_PLUS] or keyinput[pygame.K_EQUALS]:
                sim.frameskipfactor = sim.frameskipfactor+1
                print "skip factor" ,sim.frameskipfactor
            
            if keyinput[pygame.K_MINUS]:
                sim.frameskipfactor = max(1,sim.frameskipfactor-1)
                print "skip factor" ,sim.frameskipfactor

        
                    
                
###  START OF PROGRAM


# keep a record of best found so far and it's fitness
best_fitness=-1e6
best_brain=None  



control=MyController()
sensors=[]
sensorRange = 2000
for i in range(N_SENSORS):
        ang_ref=i*math.pi*2/N_SENSORS
        sensors.append(pods.Sensor(ang_ref,sensorRange,"sensor"+str(i)))
        
        
pod = pods.CarPod()
pod.setController(control)
pod.addSensors(sensors)
pod.brain=create_new()

podlist=[pod]     #  pods on the circuit


dt          =.1    
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
