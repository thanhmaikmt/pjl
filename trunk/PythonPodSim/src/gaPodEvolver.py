from simulation import *
from backpropbrain import  *
import pygame 
from random import  *
from copy import *
from fontmanager import  *
    
    
POOL_SIZE=50               # size of pool of best brains
POP_SIZE=10                # number of pod on circuit
SENSOR_SCALE=1.0/10.0      # scale sensors (make more like 0-1)
VELOCITY_SCALE=1.0/80      # scale velocity (pod starts to slip at 80)
MAX_AGE=40                 # pods live for 40 seconds   
POOL_FILE_NAME="pool.txt"  # file to save/restore the pool
REPROVE_PROB=.2            # probability that selection we trigger a reprove of the best gene

log_file=open("log_file.txt","w")


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

            global pods,touched

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
  
  
    def __init__(self,nin,nhidden,nout):
        self.list=[]
        self.maxMembers=POOL_SIZE
        self.layerSizes=[nin,nhidden,nout]
        self.elite_bias=1.0/POOL_SIZE
        self.reprover=None
        self.touched=True
        self.reaping=True
        
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
             
    def create_new(self):
        
    
        if len(self.list) < self.maxMembers:         
            #Create a brain
            brain=BackPropBrain(self.layerSizes)
            brain.proof_count=0
            return brain

        if random() < REPROVE_PROB:
            brain=self.list[0].brain
            del self.list[0]
            brain.proof_count += 1
            return brain
            
            
        clone=self.select2()

        if clone==None:
            brain=BackPropBrain(self.layerSizes)
            brain.proof_count=0
            return brain
        
        
        clone.mutate(random())
        clone.proof_count=0
        return clone
    
    
    def create_best(self):
        clone=self.list[0].brain.clone()
        #clone.proof_count=self.list[0].brain.proof_count
        return clone

    def create_most_proven(self):
        
      
        maxProof=-1
        
        for g in self.list:
            if g.brain.proof_count > maxProof:
                maxProof=g.brain.proof_count
                cloneMe=g.brain
                
        clone=cloneMe.clone()
        #clone.proof_count=self.list[0].brain.proof_count
        return clone

    def select1(self):
        
        for x in self.list:
            if random() < self.elite_bias:
                clone=x.brain.clone()
                return clone
        
        return None


    
    def select2(self):
        
        id=randint(0,len(self.list))
        
        if id ==len(self.list):
            return None
        
        return self.list[id].brain.clone()
        
        
    def best_fitness(self):
        if len(self.list) == 0:
            return 0
        else:
            return self.list[0].fitness
       
    def average_fitness(self):
        if len(self.list) == 0:
            return 0
        else:
            sum=0.0
            for x in self.list:
                sum +=x.fitness

            return sum/len(self.list)
        
            
    def save(self,file):       
        n=len(self.list)
        pickle.dump(n,file)
        
        for x in self.list:
            o=deepcopy(x.fitness)
            pickle.dump(o,file)
            x.brain.save(file)
        print "POOL SAVED"
        
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
            

class Gene:
    
    def __init__(self,brain,fitness):
        self.brain=brain
        self.fitness=fitness
        


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
        
        
        fitness = state.pod.pos_trips-state.pod.neg_trips
        
        return fitness    
        
    # normal process called every time step    
    def process(self,sensor,state,dt):
    
                    
        if pool.reaping and self.reap_pod(state):
            " here then time to replace the pod"
            
            # save the brain and fitness
            fitness=self.calc_fitness(state,self.brain)
            pool.add(Gene(self.brain,fitness)) 
            
            # reset the pod and give it a new brain
            world.init_pod(state.pod)
            state.pod.ang += random()-0.5    # randomize the intial angle
            self.brain=pool.create_new()
            return
            
        
        control=Control()
            
        # create the input for the brain 
        input=[sqrt(state.dxdt**2+state.dydt**2)*VELOCITY_SCALE]
        
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



dt          =.05
nSensors    = 12
sensorRange = 2000

pool=Pool(nSensors+1,5,4)

NPODS=POP_SIZE

pods=[]


for i in range(NPODS):
    control=GAControl()
    b=255-(i*167)%256
    g=(i*155)%256
    r=255-(i*125)%256    
    pod = CarPod(nSensors,sensorRange,control,((r,g,b)))
    pods.append(pod)

admin       = Admin()
world       = World("world.txt",pods)
sim         = Simulation(world,dt,admin)
sim.painter=Painter()


#uncomment the next line to hide the walls.
#sim.world.blind=True
#sim.frameskipfactor=10


sim.run()
