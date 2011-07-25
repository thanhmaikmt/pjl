'''
Created on 21 Dec 2010

@author: pjl
'''

from random import  *
import pickle
import copy
#from fitness import *



MUTATE_SCALE=4             # amount of mutation
BREED_PROB=0.1             # prob that new entity is from breeding           
SEED_PROB=0.1              # probability a new thing is created from nothing
        
class Pool: 
    
    """ Responsible for managing a GA scheme.
        This implementation attempts multi objective optimisation (list of goals).
        
        :param size: size of archive
        :param brainPlug: responsible for creating new brains (genes)
        :param goals: list of goals
        
    """ 
    
   
    def __init__(self,size,brainPlug,goals):
        self.list=[]
        self.maxMembers=size
        self.touched=True
        self.reaping=True
        self.goals=goals
        self.brainPlug=brainPlug
        self.proto_vec=[]
        
        for g in goals:
            self.proto_vec.append(None)       
        
    def create_new_brain(self):
        """ create a new brain from the pool.
            if pool is not full create a random brain
        """
        
        if len(self.list) < self.maxMembers or random() < SEED_PROB:         
            #Create a brain
            brain=self.brainPlug.createBrain()
  
        
        elif self.brainPlug.CAN_BREED and random() < BREED_PROB:
            mum=self._select()
            dad=self._select()
            brain=self.brainPlug.breed(mum,dad)
            
        else:
          
        # Otherwise just select a random brain from the pool
            brain=self._select().clone()
        # mutate the cloned brain by a random amount.
            fact=random()
            fact *= fact*MUTATE_SCALE
            self.brainPlug.mutate(brain,fact)
            
            
        brain.vec=copy.deepcopy(self.proto_vec)
        
        brain.current_goal=0
        
        return brain
    
    
    def create_best(self):
        """ returns a copy of the brain at the top of the list """
        
        clone=self.list[0].clone()
        #clone.proof_count=self.good_list[0].brain.proof_count
        return clone


    # random selection from the pool
    # can also return None to trigger a new random brain    
    def _select(self):
        id=randint(0,len(self.list)-1)
        return self.list[id]
  
        
    # save the pool to a file
    # (note reproof count is not saved)
    def save(self,file):       
        """ Save pool into a file 
        :param file: file to store brains
        """
        
        
        n=len(self.list)
        pickle.dump(n,file)
        
        for x in self.list:
            #o=copy.deepcopy(x.vector)
            pickle.dump(x,file)
            #x.save(file)
        print "POOL SAVED"
        
    # load pool from a file
    def load(self,file):
        self.list=[]
        n=pickle.load(file)
        print n
        for i in range(n):
            brain=pickle.load(file)
            self.add(brain)
         

       
    def add(self,brain):  
        """  Add  the brain (gene) to the Pool if it is better than the worse one.    
        """   
        raise NotImplemented
        
    def reject(self,brain):
        """ return true if brain is useless.
        """
        return False

class Pool_Pyreto(Pool):
    

    def _remove_vec(self,vec):
        
        n= len(self.goals)
        for i in range(len(self.list)):
            item=self.list[i]
            vec_item=item.vec
            
            for k in range(n):
                if vec_item[k] > vec[k]:
                    item.dom -=1
    
    
                    
    def debug(self,tag):
        print "---------------------- "+tag 
        for i in self.list:
            print str(i.vec)+ str(i.dom)
            
    
    def add(self,brain):  
        """  Add  the brain (gene) to the Pool if it is better than the worse one.    
        """
           
    
        if len(self.list) == 0:
            brain.dom=0
            self.list.append(brain)
            self.debug("1")
            return
                   
        n=len(self.goals)
        vec_new=brain.vec
        
        
        dom=0
                    
        for i in range(len(self.list)):
            item=self.list[i]
            vec_item=self.list[i].vec
            
            for k in range(n):
                if vec_new[k] > vec_item[k]:
                      dom+=1
                elif vec_item[k] > vec_new[k]:
                    item.dom+=1
    
        brain.dom=dom
    
        self.list.append(brain)
        
        pop=self.list
        
        pop.sort(key = lambda x:x.dom,reverse=True)
    
        if len(self.list) == self.maxMembers:
            item=self.list.pop()
            self._remove_vec(item.vec)          
            pop.sort(key = lambda x:x.dom,reverse=True)
            
        
            
        # self._remove_vec(item.vec)
        

    def displayString(self):
        if len(self.list) ==0:
            return "null"
        
        x=self.list[0]
        #return " %4.0f " % x.fitness +  " %4.0f" % x.flukeness + "( %d )"  %  x.proof_count
        return str(x.vec) + " " + str(x.dom)
    
    
class Pool_Mino(Pool):
       
    def add(self,brain):  
        """  Add  the brain (gene) to the Pool if it is better than the worse one.    
        """   
                
        brain.min_val=min(brain.vec)
        brain.sum_val=sum(brain.vec)
        
        self.list.append(brain)
        
        pop=self.list
        
        def cmpmino(x,y):
            if x.min_val == y.min_val:
                if x.sum_val > y.sum_val:
                    return 1
                elif x.sum_val < y.sum_val:
                    return -1
                else:
                    return 0
            elif x.min_val > y.min_val:
                return 1
            else:
                return -1
                  
                
        pop.sort(cmp=cmpmino,reverse=True)
        
        if len(self.list) > self.maxMembers:
            self.list.pop()
    
    
    def displayString(self):
        if len(self.list) ==0:
            return "null"
        
        x=self.list[0]
        
        av=copy.deepcopy(x.vec)
        
        for b in self.list:
            if b != x:
                for i in range(len(av)):
                    av[i] += b.vec[i]
                
        fact=1.0/len(self.list)

        avStr=""
        for i in range(len(x.vec)):
                avStr += " %4.1f" % x.vec[i]
        
        avStr+=" ("
        for i in range(len(av)):
                avStr += " %4.1f" % (av[i] * fact)
        
        avStr+=")"         
                        #return " %4.0f " % x.fitness +  " %4.0f" % x.flukeness + "( %d )"  %  x.proof_count
        return avStr
    
    def reject(self,brain):
        """ if any test is less than min value in pool reject """
        
        n=len(self.list)
        
        if n< self.maxMembers:
            return False
        
        rv=min(self.list[n-1].vec)
        
        for x in brain.vec:
            if x == None:
                return False
            
            if x < rv:
                return True
                           
    def debug(self,tag):
        print "---------------------- "+tag 
        
        a=self.list[0]
        for b in self.list:
            print str(b.vec) + " : " + str(a.dist(b))