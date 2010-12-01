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
from simulation import *

import pygame 
from random import  *
from copy import *
from fontmanager import  *
import pickle
import time

import gravityPlug


plug=gravityPlug.GravityPlug()


RUN_NAME=plug.RUN_NAME


#  parameters that could be varied
    
POOL_SIZE=50               # size of pool of best brains
POP_SIZE=10                # number of pod on circuit
REPROVE_PROB=.2            # probability that selection we trigger a reprove of the best gene
MUTATE_SCALE=4             # amount of mutation
BREED_PROB=0.0             # prob that new entity is from breeding           
CAN_BREED=False            # by default assume can not breed
SEED_PROB=0.1              # probability a new thing is created from nothing
CHOOSE_FLUKE_PROB=0.0      # chance we use a high scorer
CHOOSE_PROVEN_PROB=0.0     # chance we use a high scorer

# files used by program

POOL_FILE_NAME=RUN_NAME+"_pool.txt"      # file to save/restore the pool
log_file=open(RUN_NAME+"log.txt","w")    # keep a record of the performance

    
# Define some classes

class Painter:   # use me to display stuff
    
    def __init__(self):
        self.preDraw=None       # define this function to draw on top!
        self.fontMgr = cFontManager(((None, 20), (None, 48), ('helvetica', 24)))
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
                
        FMT=plug.FIT_FMT
        avFitStr=FMT % pool.average_fitness()
        tickRateStr="%8.1f" % ticks_per_sec
        bestFlukeStr = FMT % pool.best_fluke_fitness()
        bestStr=FMT  % pool.best_fitness()
        
        str1=RUN_NAME+' pool size :'+ str(POOL_SIZE)+\
                          '   ticks :'+ str(sim.world.ticks) +\
                          '   best :'+ bestStr +\
                          '   best(fluke) :'+ bestFlukeStr +\
                          '   best(proven) :'+ pool.proven_string(FMT) +\
                          '   average :'+ avFitStr+\
                          '   ticks/sec :'+tickRateStr+"    "
                                                    
       # print str1
        self.fontMgr.Draw(screen, None, 20,str1,(X,Y), (0,255,0) )
        plug.postDraw(screen,self.fontMgr)
        
        
        
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
            if  keyinput[pg.K_c]:
                pool.proven_list=[]
                
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
                pod.ang += random()-0.5    # randomize the intial angle
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
            if keyinput[pg.K_l]:
                file=open(POOL_FILE_NAME,"r")
                pool.load(file)
                file.close()
                

        
"""
# Simple class to store the brain and fitness
class Gene:
    
    def __init__(self,brain,fitness):
        self.brain=brain
        self.fitness=fitness
"""        



class Pool:  #  use me to store the best brains and create new brains
  
  
    # create a pool
   
    def __init__(self):
        self.good_list=[]
        self.fluke_list=[]
        self.proven_list=[]
        self.maxMembers=POOL_SIZE
        self.maxFlukeMembers=POOL_SIZE    
        self.maxProvenMembers=POOL_SIZE    
        #self.elite_bias=1.0/POOL_SIZE
        self.reprover=None
        self.touched=True
        self.reaping=True


    def proven_string(self,FMT):
        if len(self.proven_list) == 0:
            return "Null"
        
        str1=FMT % self.proven_list[0].fitness
        str2= " ("+str(self.proven_list[0].proof_count)+")"
        
        return str1+str2
    
    # add a new Gene to the Pool  (if better than the worst one in pool)
    # 
    def add_proven(self,brain):  
                      
        for i in range(len(self.proven_list)):
            if brain.proof_count > self.proven_list[i].proof_count:
                self.proven_list.insert(i,brain)
                if len(self.proven_list) > self.maxProvenMembers:
                    self.proven_list.pop()
                return
            
        if len(self.proven_list) < self.maxProvenMembers:
            self.proven_list.append(brain)    
        
    # add a new Gene to the Pool  (if better than the worst one in pool)
    # 
    def add_fluke(self,brain):  
                    
        for i in range(len(self.fluke_list)):
            if brain.fitness > self.fluke_list[i].fitness:
                self.fluke_list.insert(i,brain)
                if len(self.fluke_list) > self.maxFlukeMembers:
                    self.fluke_list.pop()
                return
            
        if len(self.fluke_list) < self.maxFlukeMembers:
            self.fluke_list.append(brain)    
        
        
    # add a new Gene to the Pool  (if better than the worst one in pool)
    # 
    def add(self,brain):  
                
        if len(self.good_list) >= self.maxMembers:
            if brain.fitness < self.good_list[self.maxMembers-1].fitness:
                return
          
        for i in range(len(self.good_list)):
            if brain.fitness > self.good_list[i].fitness:
                self.touched=True
                self.good_list.insert(i,brain)
                if len(self.good_list) > self.maxMembers:
                    self.good_list.pop()
                return
            
        if len(self.good_list) < self.maxMembers:
            self.good_list.append(brain)    
            self.touched=True
             
    # create a neural brain from the pool or maybe random
    # might return best brain to be reproven
    def create_new(self):
        
        # if pool is not full create a random brain 
        if len(self.good_list) < self.maxMembers or random() < SEED_PROB:         
            #Create a brain
            brain=plug.createBrain()
            brain.proof_count=0   # add proof count field
            return brain


        # keep testing the best brain in case it was a fluke!!!
        # this removes the best brain from the pool 
        # it will get back in if it scores OK 
        if random() < REPROVE_PROB:
        
            brain=self.good_list[0]
            brain.proof_count += 1
        
            fluke=brain.clone();    
            fluke.fitness=brain.fitness
            
            self.add_fluke(fluke)
            
            del self.good_list[0]
            self.add_proven(brain)
            return brain
        
            
        if CAN_BREED and random() < BREED_PROB:
            mum=self.select()
            dad=self.select()
            brain=plug.breed(mum,dad)
            brain.proof_count=0
            return brain
        
        # Otherwise just select a random brain from the pool
        clone=self.select().clone()
  
        # mutate the cloned brain by a random amount.
        fact=random()
        fact *= fact*MUTATE_SCALE
        clone.mutate(fact)
        clone.proof_count=0
        return clone
    
    
    # return top of the pool
    def create_best(self):
        clone=self.good_list[0].clone()
        #clone.proof_count=self.good_list[0].brain.proof_count
        return clone

    # return the one that has been RETESTED the most.
    def create_most_proven(self):
        
        maxProof=-1
        
        for g in self.proven_list:
            if g.proof_count > maxProof:
                maxProof=g.proof_count
                cloneMe=g
                                
        clone=cloneMe.clone()
        #clone.proof_count=self.good_list[0].brain.proof_count
        return clone


    # random selection from the pool
    # can also return None to trigger a new random brain    
    def select(self):


        if len(self.proven_list) > 0 and  random() < CHOOSE_PROVEN_PROB:
            id=randint(0,len(self.proven_list)-1)
            return self.proven_list[id]

        
        if len(self.fluke_list) > 0 and  random() < CHOOSE_FLUKE_PROB:
            id=randint(0,len(self.fluke_list)-1)
            return self.fluke_list[id]
        
        
        id=randint(0,len(self.good_list)-1)
        
        #if id ==len(self.good_list):
        #    return None
        
        return self.good_list[id]
        
        
    # return the best fitness in the pool
    # since I retest the best this value can fall
    def best_fluke_fitness(self):
        if len(self.fluke_list) == 0:
            return 0
        else:
            return self.fluke_list[0].fitness
        
    # return the best fitness in the pool
    # since I retest the best this value can fall
    def best_fitness(self):
        if len(self.good_list) == 0:
            return 0
        else:
            return self.good_list[0].fitness
       
    # return average fitness
    def average_fitness(self):
        if len(self.good_list) == 0:
            return 0
        else:
            sum=0.0
            for x in self.good_list:
                sum +=x.fitness

            return sum/len(self.good_list)
        
    # save the pool to a file
    # (note reproof count is not saved)
    def save(self,file):       
        n=len(self.good_list)
        pickle.dump(n,file)
        
        for x in self.good_list:
            o=deepcopy(x.fitness)
            pickle.dump(o,file)
            x.save(file)
        print "POOL SAVED"
        
    # load pool from a file
    def load(self,file):
        self.good_list=[]
        n=pickle.load(file)
        print n
        for i in range(n):
            f=pickle.load(file)
            brain=plug.loadBrain(file)
            brain.proof_count=0    # sorry we lost the proof count when we saved it
            brain.fitness=f
            self.add(brain)
         
        print "RELOADED POOL"   
        for pod in pods:
            # reset the pod and give it a new brain from the pool
            world.init_pod(pod)
            pod.ang += random()-0.5    # randomize the intial angle
            pod.brain.brain=pool.create_new()
            
# Pod controller
# Note that these are resused with new neural nets during the simulation
# also has a little bit of responsibiltiy for managing the evolution of pods
class GAControl:

    def __init__(self):
        self.brain=pool.create_new()
            
        
    # normal process called every time step    
    def process(self,sensor,state,dt):
    
                    
        # If we are trying to evolve and pod dies
        if pool.reaping:
            
            fitness=plug.reap_pod(state,dt)
            if fitness != None:
            
                " here then time to replace the pod"
            
                self.brain.fitness=fitness
                # save current  brain and fitness in the pool
                #fitness=self.calc_fitness(state,self.brain)
                pool.add(self.brain) 
                world.init_pod(state.pod)
                plug.initPod(state.pod)
                self.brain=pool.create_new()
                return None
               
        # normal control stuff
        control=plug.process(sensor,state,dt,self.brain)
        
        return control


###  START OF PROGRAM

dt = .1      

pool=Pool()    #  create a pool for fittest networks
pods=[]        #  pods on the circuits


for i in range(POP_SIZE):     # create initial population on the circuit
    control=GAControl()
    # random colours
    b=255-(i*167)%256
    g=(i*155)%256
    r=255-(i*125)%256    
    pod = plug.createPod(control,(r,g,b))
    pods.append(pod)


admin       = Admin()
world       = World(plug.WORLD_FILE,pods)
sim         = Simulation(world,dt,admin)

# register the painter to display stuff
sim.painter = Painter()


# go go go  ..........
sim.run()
