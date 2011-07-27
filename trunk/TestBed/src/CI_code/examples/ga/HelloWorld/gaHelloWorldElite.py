import sys
import random
import array


POPSIZE      = 1000;          # population size	  
MAXITER      = 100;           # maximum iterations
MUTATEPROB   = 0.5;	      # mutation rate
NELITE       = 200;           # top of population survive
NBREED       = 500;           # how many are bred

target="Hello World!"
size=len(target);

low_char=32
hi_char=121

class Gene:
    def __init__(self,string):
        self.string=string
        self.fitness=None    

def randomChar():
    return chr(random.randint(32,121))

def seed():
    string=array.array('c')
    for i in xrange(size):
        string.append(randomChar())
    return string

def evaluate1(string):   # number correct
    sum=0
    for a,b in zip(string,target):
        if a == b:
            sum += 1
    return sum

def evaluate2(string):    # sum of diff in char codes
    sum=0
    for a,b in zip(string,target):
            sum -= abs(ord(a)-ord(b))
    return sum

def mate(a,b):
    i=random.randint(1,size-1)
    ret = a[0:i]+b[i:size]
    return ret

def mutate1(a): # randomly replace a character
    i=random.randint(0,size-1)
    a[i]=randomChar()

def mutate2(a):    # add/subtract 1 from the character code
    i=random.randint(0,size-1)
    ic = ord(a[i])
    im=random.randint(0,1)
    ic=ic + 2*im -1
    if ic >hi_char:
        ic=hi_char
    if ic <low_char:
        ic=low_char
    a[i]=chr(ic)
    
def breedPopulation():
    newpop=[]
    
    # copy top NELITE to the new population
    for m in pop[0:NELITE]:
        newpop.append(m)

    # create the rest by breeding from the top NBREED 
    for i in range(NELITE,POPSIZE):
        i1 = random.randint(0,NBREED-1)
        i2 = random.randint(0,NBREED-1)

        gene=Gene(mate(pop[i1].string,pop[i2].string))
        newpop.append(gene)

        if random.random()<MUTATEPROB:
            mutate(gene.string)
            
    return newpop


if __name__ == '__main__':

    if False:  # measure fitness
        evaluate=evaluate2   # use char code distances
        mutate=mutate2       # nudge by +/-1
    else:                    
        evaluate=evaluate1   # count number in right place 
        mutate=mutate1       # random char replacement

    target_fitness=evaluate(target)

    pop=[]

    for i in range(POPSIZE):
        pop.append(Gene(seed()))

    count=0    

    while  count< MAXITER:

        for m in pop:
            m.fitness=evaluate(m.string)

        pop = sorted(pop, key = lambda x:x.fitness,reverse=True)
    
        print count,pop[0].string.tostring(),pop[0].fitness  
        
        if pop[0].fitness >=  target_fitness:
            break

        pop = breedPopulation();
        count += 1

  


