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

def evaluate1(string):
    sum=0
    for a,b in zip(string,target):
        if a == b:
            sum += 1
    return sum

def evaluate2(string):
    sum=0
    for a,b in zip(string,target):
            sum -= abs(ord(a)-ord(b))
    return sum

def mate(a,b):
    i=random.randint(1,size-1)
    ret = a[0:i]+b[i:size]
    #print ret
    return ret

def mutate(a):
    i=random.randint(0,size-1)
    a[i]=randomChar()
    
def breedPopulation():
    newpop=[]
    for m in pop[0:NELITE]:
        newpop.append(m)

    for m in pop[NELITE:POPSIZE]:
        i1 = random.randint(0,NBREED-1)
        i2 = random.randint(0,NBREED-1)

        newpop.append(Gene(mate(pop[i1].string,pop[i2].string)))

        if random.random()<MUTATEPROB:
            mutate(m.string)
            
    return newpop


if __name__ == '__main__':

    if True:
        evaluate=evaluate2
    else:
        evaluate=evaluate1


    target_fitness=evaluate(target)

    pop=[]

    for i in range(POPSIZE):
        pop.append(Gene(seed()))


    count=0    



    while  count< range(MAXITER):

        for m in pop:
            m.fitness=evaluate(m.string)

        pop = sorted(pop, key = lambda x:x.fitness,reverse=True)
    
        print count,pop[0].string.tostring(),pop[0].fitness  
        
        if pop[0].fitness >=  target_fitness:
            break

        pop = breedPopulation();
        count += 1

  


