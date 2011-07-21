from simulation import *
from feedforwardbrain import  *
import pygame 
from random import  *
from copy import *
from fontmanager import  *
import time




RUN_NAME="ems_maze"             # used for file names so you can tag different experiments
load=False

# The world
WORLD_FILE="trip_world.txt"     # world to use
N_TRIP=21        # to avoid end wall remove pod after hitting this (last) trip

# An alternative world!!!
#WORLD_FILE="car_circuit.txt"     # world to use
#N_TRIP=200                       # big number because it is a loop
XREF = 255
YREF = 60
XREF1 = 850
YREF1 = 130 
XREF2 = 860
YREF2 = 500 
XREF3 = 550
YREF3 = 500 

Y_circ=120
X_circ=400
RAD_circ=700.0
#  parameters that could be varied
    
POOL_SIZE=50               # size of pool of best brains
POP_SIZE=10               # number of pod on circuit
SENSOR_SCALE=1.0/100.0      # scale sensors (make more like 0-1)
VELOCITY_SCALE=1.0/90      # scale velocity (pod starts to slip at 80)
MAX_AGE=150                # pods life span   
REPROVE_PROB=0.2            # probability that selection we trigger a reprove of the best gene
N_HIDDEN=7                 # number of neurons in hidden layer
N_SENSORS=8                 # No Sensors
X_scale=1.0/100.0
Y_scale=1.0/100.0
D_scale=1.0/RAD_circ


# files used by program
print "1 - Pool trained form scratch"
print "2 - Pool inherited form Maze_No_Sens"
print "3 - Run without loading a pool"
var = raw_input("Enter 1, 2, or 3: ")
print "you entered ", var

if var=="1":
    POOL_FILE_NAME="maze_ems_pool.txt"
    print "**maze_ems_pool.txt** Loaded"
    load=True
elif var=="2":
    POOL_FILE_NAME="maze_hover_ems_pool.txt"
    print "**maze_hover_ems_pool.txt** Loaded"
    load=True
else:
    POOL_FILE_NAME=RUN_NAME+"_pool.txt"
    print "No Pool loaded"




log_file=open(RUN_NAME+"log.txt","w")    # keep a record of the performance


# Define some classes

def read_data(file_name):
    ftd=open(file_name,"r")
    cnt=[]
    cnt4=[]
    while True: 
        line = ftd.readline()
        #print line
        if line.isspace() or len(line)==0:
            return cnt
        toks = line.split(',')
        for tok in toks:
           #print tok
           if len(tok) != 0 and not tok.isspace() :
                cnt4.append(float(tok))
                if len(cnt4)==4:
                    cnt.append(cnt4)
                    cnt4=[]

                    
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
                          ' ticks/sec:'+tickRate+"    "+str(tot_time)
                          
# print str1
        self.fontMgr.Draw(screen, None, 20,str1,(X,Y), (0,255,0) )
        
        self.fontMgr.Draw(screen, None, 20,"x",(XREF,YREF), (255,255,255) )
        
        self.fontMgr.Draw(screen, None, 20,"x",(XREF1,YREF1), (255,255,255) )
        
        self.fontMgr.Draw(screen, None, 20,"x",(XREF2,YREF2), (255,255,255) )
        
        self.fontMgr.Draw(screen, None, 20,"x",(XREF3,YREF3), (255,255,255) )
        
        #pygame.draw.circle(screen,(255,255,255),(X_circ,Y_circ),RAD_circ,2)
        
class Admin:  # use me to control the simulation
# see comments to see what key hits do


    def process(self):   
        
            # this is called just before each time step
            # do admin tasks here

            global pods, load

# output to a log file
            if pool.reaping and log_file!=None and pool.touched:
                log_file.write(str(sim.world.ticks) +','+ str(pool.best_fitness())+','+str(pool.average_fitness())+'\n')
                pool.touched=False
                                
            keyinput = pygame.key.get_pressed()
        
            # speed up/down  display      
            if keyinput[pg.K_KP_PLUS] or keyinput[pg.K_EQUALS]:
                sim.frameskipfactor = sim.frameskipfactor+1
                print "skip factor" ,sim.frameskipfactor
                
            if keyinput[pg.K_a]:
                for pod in pods:
                    print pod.net.brain.weight
                    print pod.net.brain.layer_size
            
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
                pod.ang = pi + random()/1.25 - 0.4    # randomize the intial angle
                pod.error_ang_integral = 0
                pod.error_dist_integral = 0
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
                pod.ang = pi + random()/1.25 - 0.4   # randomize the intial angle
                pod.error_ang_integral = 0
                pod.error_dist_integral = 0
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
            brain=FeedForwardBrain(self.layerSizes)
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
            brain=FeedForwardBrain(self.layerSizes)
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
            b.resize_inputs(17)
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
    
        dist=sqrt((state.x-X_circ)**2+(state.y-Y_circ)**2)
        
        if dist>RAD_circ:
            return True
        
        if state.ang<0.6*pi or state.ang>1.4*pi:
            return True
        
        return False
    
    # calculate the fitness of a pod
    def calc_fitness(self,state,brain):
        pod=state.pod
        
        dist_FROM_REF=sqrt((state.x-XREF)**2+(state.y-YREF)**2)
        dist_FROM_REF1=sqrt((state.x-XREF1)**2+(state.y-YREF1)**2)
        dist_FROM_REF2=sqrt((state.x-XREF2)**2+(state.y-YREF2)**2)
        dist_FROM_REF3=sqrt((state.x-XREF3)**2+(state.y-YREF3)**2)
        
        dist_BOUND=sqrt((state.x-X_circ)**2+(state.y-Y_circ)**2)
        # Encourage them to stay around the point
        fitness= pod.age-100000 + (state.pod.pos_trips-state.pod.neg_trips)*3
        
        
        if dist_BOUND > RAD_circ:
            #print "rad"
            fitness= pod.age - 100000    
            
            
        
        if state.ang<=0.6*pi or state.ang>=1.4*pi:
            #print "ang"
            fitness = pod.age - 100000
        
        
        # Encourage them to be straight but only when they are close to the point
        # as I found that otherwise they just fall straight down
        if pod.age >= MAX_AGE:
            print "age"
            if (state.pod.pos_trips-state.pod.neg_trips) < 5:
                #print "1st target"
                fitness = -dist_FROM_REF + (state.pod.pos_trips-state.pod.neg_trips)*10#- pod.error_ang_integral*100.0 - pod.error_dist_integral/100.0
            elif (state.pod.pos_trips-state.pod.neg_trips) < 10:
                #print "2nd target"
                fitness = -dist_FROM_REF1 + 1000 + (state.pod.pos_trips-state.pod.neg_trips)*10
                
            elif (state.pod.pos_trips-state.pod.neg_trips) < 15:
                #print "3re target"
                fitness = -dist_FROM_REF2 + 1500 + (state.pod.pos_trips-state.pod.neg_trips)*10
            else:
                #print "4th target"
                fitness = -dist_FROM_REF3 + 2000 + (state.pod.pos_trips-state.pod.neg_trips)*10
                
        #print fitness
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
            state.pod.ang = pi + random()/1.25 - 0.4    # randomize the intial angle
            self.brain=pool.create_new()
            pod.error_ang_integral = 0
            pod.error_dist_integral = 0
            return
        
        
        dist_TARGET= sqrt((state.x-XREF)**2+(state.y-YREF)**2)  
        err_ANG= 0.6333*pod.ang**2 - 3.9789*pod.ang + 6.25
        
        try:    
            state.pod.error_ang_integral += err_ANG*dt
        except AttributeError:
            pod.error_ang_integral = 0.0  
        
        try:    
            state.pod.error_dist_integral += dist_TARGET*dt
        except AttributeError:
            state.pod.error_dist_integral = 0.0    
        # normal control stuff
        
        
        control=Control()
        dist=sqrt((state.x-X_circ)**2+(state.y-Y_circ)**2)
        # create the input for the brain
        # first the velocity of the pod 
        a=(state.pod.pos_trips-state.pod.neg_trips)
        
        
        input=[state.dxdt*VELOCITY_SCALE]
        input.append(state.dydt*VELOCITY_SCALE)
        input.append(sin(state.ang))
        input.append(cos(state.ang))
        input.append(state.dangdt)
        '''
        input.append((state.x-XREF)*X_scale)
        input.append((state.y-YREF)*Y_scale)
        input.append((state.x-XREF1)*X_scale)
        input.append((state.y-YREF1)*Y_scale)'''
        
        #input.append((RAD_circ-dist)*D_scale)
        
    
        # and all the sensors
        # (note: possibly rear pointing sensors are redundant?)
        for i in range(4):
            input.append(beacon[a][i])
        for s in sensor:
            input.append(s.val*SENSOR_SCALE)
            
        # activate the brain to get output    
        output=self.brain.ffwd(input)
       
        # assign values to the controllers
        control.up=output[0]-output[1]
        control.left=output[2]
        control.right=output[3]
        
        
        
        return control

class CursorControl:

    def process(self,sensor,state,dt):
        control=Control()
        keyinput = pygame.key.get_pressed()

        if keyinput[pg.K_LEFT]:
            control.left=1

        if keyinput[pg.K_RIGHT]:
            control.right=1

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1
        
            
        return control



###  START OF PROGRAM
beacon = read_data("beacons")
print beacon


dt          =.1       
sensorRange = 1000
pool=Pool(9+N_SENSORS,N_HIDDEN,4)
pods=[]
#pod = GravityPod(0,sensorRange,CursorControl(),(255,255,255))
#pods.append(pod)


for i in range(POP_SIZE):
    control=GAControl()
    # random colours
    b=255-(i*167)%256
    g=(i*155)%256
    r=255-(i*125)%256    
    pod = GravityPod(N_SENSORS,sensorRange,control,((r,g,b)))
    
    pods.append(pod)
    

        

            
    
    
    
    

#brain       = CarControl()
#pod         = CarPod(8,sensorRange,brain,(255,255,255))

#pods.append(pod)
admin       = Admin()
world       = World(WORLD_FILE,pods)
sim         = Simulation(world,dt,admin)

# register the painter to display stuff
sim.painter = Painter()


# go go go  ..........
sim.run()
