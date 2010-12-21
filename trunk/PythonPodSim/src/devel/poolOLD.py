'''
Created on 21 Dec 2010

@author: pjl
'''


from world import *
from random import  *
from simulationMP import *

POOL_SIZE=50               # size of pool of best brains
POP_SIZE=1             # number of pod on circuit
REPROVE_PROB=.1            # probability that selection we trigger a reprove of the best gene
MUTATE_SCALE=4             # amount of mutation
BREED_PROB=0.1             # prob that new entity is from breeding           
#CAN_BREED=False            # by default assume can not breed
SEED_PROB=0.1              # probability a new thing is created from nothing
CHOOSE_FLUKE_PROB=0.0      # chance we use a high scorer
CHOOSE_PROVEN_PROB=0.0


class Pool:  #  use me to store the best brains and create new brains
  
  
    # create a pool
   
    def __init__(self,world,plug):
        self.good_list=[]
        self.fluke_list=[]
        self.proven_list=[]
        self.maxGoodMembers=POOL_SIZE
        self.maxFlukeMembers=POOL_SIZE    
        self.maxProvenMembers=POOL_SIZE    
        #self.elite_bias=1.0/POOL_SIZE
        self.reprover=None
        self.touched=True
        self.reaping=True
        self.world=world
        self.plug=plug

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
                self.touched=True
 
                if len(self.proven_list) > self.maxProvenMembers:
                    self.proven_list.pop()
                return
            
        if len(self.proven_list) < self.maxProvenMembers:
            self.proven_list.append(brain)    
            self.touched=True
        
    # add a new Gene to the Pool  (if better than the worst one in pool)
    # 
    def add_fluke(self,brain):  
                    
        for i in range(len(self.fluke_list)):
            if brain.flukeness > self.fluke_list[i].flukeness:
                self.fluke_list.insert(i,brain)
                self.touched=True
                if len(self.fluke_list) > self.maxFlukeMembers:
                    self.fluke_list.pop()
                return
            
        if len(self.fluke_list) < self.maxFlukeMembers:
            self.fluke_list.append(brain)    
            self.touched=True
        
    # add a new Gene to the Pool  (if better than the worst one in pool)
    # 
    def add_good(self,brain):  
                    
        for i in range(len(self.good_list)):
            if brain.fitness > self.good_list[i].fitness:
                self.touched=True
                self.good_list.insert(i,brain)
                if len(self.good_list) > self.maxGoodMembers:
                    self.good_list.pop()
                return
            
        if len(self.good_list) < self.maxGoodMembers:
            self.good_list.append(brain)    
            self.touched=True
 
        
    # add a new Gene to the Pool  (if better than the worst one in pool)
    # 
    def add(self,brain,fitness):  
        
    
        if fitness > brain.flukeness or brain.flukeness == None:
           brain.flukeness=fitness
        
        brain.proof_count+=1
                                                         
        if fitness < brain.fitness or brain.fitness == None:
           brain.fitness=fitness
             
        # add brain to the fluke with fitness value
        self.add_fluke(brain)
               
        self.add_good(brain)
        
        self.add_proven(brain)
        
 
             
    # create a neural brain from the pool or maybe random
    # might return best brain to be reproven
    def create_new(self):
        
        
        # if pool is not full create a random brain 
        if len(self.good_list) < self.maxGoodMembers or random() < SEED_PROB:         
            #Create a brain
            brain=self.plug.createBrain()
  
        # keep testing the best brain in case it was a fluke!!!
        # this removes the best brain from the pool 
        # it will get back in if it scores OK 
        elif random() < REPROVE_PROB:     
            brain=self.good_list[0] 
            del self.good_list[0]
            return brain
        
        elif self.plug.CAN_BREED and random() < BREED_PROB:
            mum=self.select()
            dad=self.select()
            brain=self.plug.breed(mum,dad)
            
        else:
          
        # Otherwise just select a random brain from the pool
            brain=self.select().clone()
        # mutate the cloned brain by a random amount.
            fact=random()
            fact *= fact*MUTATE_SCALE
            brain.mutate(fact)
            
            
        brain.proof_count=0
        brain.fitness=None
        brain.flukeness=None
        return brain
    
    
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
            return self.fluke_list[0].flukeness
        
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
            brain.proof_count=0
            brain.flukeness=f
            self.add(brain,f)
         
        print "RELOADED POOL"   
        for pod in pods:
            # reset the pod and give it a new brain from the pool
            world.init_pod(pod)
            pod.ang += random()-0.5    # randomize the intial angle
