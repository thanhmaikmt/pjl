
# parameters

import world
import array
import random
from Tkinter import *
from gui import *


POPSIZE      = 1000;          # population size      
MAXITER      = 100;           # maximum iterations
MUTATEPROB   = 0.5;          # mutation rate
NELITE       = 200;           # top of population survive
NBREED       = 500;       


def random_gene(length):
    g=Gene(length)
    g.str=array.array('u',myArray = [0] * length)
    for i in range(length):
        g.str[i]=random_token()
    return g
    
def mate(a,b):
        i=random.randint(1,a.str.length)
        g=Gene()        
        g.str=array.array('u',myArray= a.str[0:i]+b[i:b.str.length])
        return g

def random_token():
        return random.randint(0,100)

def mutate(g): # randomly replace a character
        i=random.randint(0,str.length-1)
        #g2=g.clone()
        g.str[i]=random_token()


class Gene:
    
    def clone(self):
        g=Gene()
        g.str=g[:]
 
 
   
    
def breedPopulation():
    newpop=[]
    
    # copy top NELITE to the new population
    for m in pop[0:NELITE]:
        newpop.append(m)

    # create the rest by breeding from the top NBREED 
    for i in range(NELITE,POPSIZE):
        i1 = random.randint(0,NBREED-1)
        i2 = random.randint(0,NBREED-1)

        gene=pop[i1].mate(pop[i2])
        newpop.append(gene)

        if random.random()<MUTATEPROB:
            mutate(gene)
            
    return newpop


if __name__ == '__main__':


 
    master = Tk()

    w = Canvas(master, width=xMax, height=yMax)
    w.pack()


    mainloop()   


    world= World()
 
    gene_length= world.nGenerator*world.nConsumer


    

  
    pop=[]

    for i in range(POPSIZE):
        pop.append(random_gene())

    count=0    

    while  count< MAXITER:

        for m in pop:
            m.fitness=world.evaluate(m)

        pop = sorted(pop, key = lambda x:x.fitness,reverse=True)
    
        print count,pop[0].string.tostring(),pop[0].fitness  
        
        pop = breedPopulation();
        count += 1

  


