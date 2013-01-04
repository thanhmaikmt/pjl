import array as A
import random
from Tkinter import *
import  matplotlib.pyplot as P


POPSIZE      = 200;          # population size      
MAXITER      = 100000;           # maximum iterations
BREEDPROB    = 0.5;          # mutation rate
NELITE       = 10;           # top of population survive
NBREED       = 100;       

do_breed=False



def blank_gene(length):
    g=Gene()  
    g.str=A.array('B',[0] * length)
    return g

def random_gene(length,maxTok):
    g=blank_gene(length)
    for i in range(length):
        g.str[i]=random_token(maxTok)
    return g
    
def mate(a,b):
        length=len(a.str)
        i=random.randint(1,length-1)
        g=Gene()        
        g.str=A.array('B',a.str[0:i]+b.str[i:length])
        return g

def random_token(maxTok):
        return random.randint(0,maxTok)

def mutate(g,maxTok): # randomly replace a character
    length=len(g.str)
    i=random.randint(0,length-1)
    #g2=g.clone()
    g.str[i]=random_token(maxTok)


class Gene:
    
    def clone(self):
        g=Gene()
        g.str=self.str[:]
        return g
 
 
   
   
    
def breedPopulation(pop):
    newpop=[]
    
    # copy top NELITE to the new population
    for m in pop[0:NELITE]:
        newpop.append(m)

    # create the rest by breeding from the top NBREED 
    for i in range(NELITE,POPSIZE):
        i1 = random.randint(0,NBREED-1)
        i2 = random.randint(0,NBREED-1)
        
        if do_breed and random.random()<BREEDPROB:
            gene=mate(pop[i1],pop[i2])
           
        else: 
            gene=pop[i1].clone()
            mutate(gene,world.World.maxTok)
            
        newpop.append(gene)
 
    return newpop