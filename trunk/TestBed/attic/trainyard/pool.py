#import array as A
#import random
#from Tkinter import *
#import  matplotlib.pyplot as P

import sys
import random
import array
import copy






class Pool:
 
    """
    A Pool maintains a list of Genes
    It also has a create method to create new Genes.
    See methods for details.
    Initially the pool is empty
    """
    
    def __init__(self,size):
        
        """
        Create a pool with no initial population
        """
        self.list=[]
        self.size=size
        
        
        
    def add(self,gene):
        """
        If the gene fitness is greater than any in the pool.
        Or the pool is not full then the gene is added to the population.
        
        """
        
        n=len(self.list)
        for i in range(n):
            if self.list[i].fitness < gene.fitness:
                self.list.insert(i,gene)
                if n > self.size-1:
                    self.list.pop()
                return
            
        if n < self.size:
            self.list.append(gene)
            
    def create(self):     
        """ create a new brain from the pool.
            if pool is not full create a random brain
        """
    
        # if list is not full OR randomly depending on SEED_PROB
        # create a random gene.
        if len(self.list) < (self.size) or random.random() < SEED_PROB:    
            print "RANDOM"
            gene=Gene(seed())
            return gene
        
        # randomly depending on BREED_PROB mate 2 existing genes.
        elif  random.random() < BREED_PROB:
            print "BREED"
            mum=self._select()
            dad=self._select()
            string=mate(mum.string,dad.string)
            return Gene(string)
                
        #other wise return a mutated version of a random gene from the pool 
        else:
            print "MUTATE"
            gene=copy.deepcopy(self._select())     
            mutate(gene.string)
            return gene
            
    
    def _select(self):
        
        if len(self.list) == 0:
            return self.list[0]
            
        id=random.randint(0,len(self.list)-1)
        return self.list[id] 
    
    def funcPrint(self):
        print "-----------------------------"
        for g in self.list:
            print g
            

if __name__ == "__main__":        
    pool=Pool(POOL_SIZE)
    
    target_fitness=evaluate(secret)
    
    cnt=0
    max_eval=100000
    while cnt< max_eval:
        gene=pool.create()
        gene.fitness=evaluate(gene.string)
        pool.add(gene)
        best_gene=pool.list[0]
        #pool.funcPrint()
        print cnt,": ",best_gene
        if best_gene.fitness == target_fitness:
            print "DONE IT"            
            break
        cnt = cnt+1

            
        