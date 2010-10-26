import sys
import random
import array
import copy

POPSIZE      = 1000          # population size	  
MAXITER      = 100            # maximum iterations
MUTATEPROB   = 0.5	      # mutation rate
MATEPROB     = 1.0
nellite      = 200

target="Hello World!"
size=len(target)

class Gene:
    def __init__(self,string):
        self.string=copy.copy(string)
        self.fitness=None    

def randomChar():
    return chr(random.randint(32,121))

def seed():
    string=array.array('c')
    for i in xrange(size):
        string.append(randomChar())
    return string

def evaluate(string):
    sum=0.0
    for a,b in zip(string,target):
        if a == b:
            sum += 1.0
    return sum

def mate(a,b):
    i=random.randint(1,size-1)
    ret = a[0:i]+b[i:size]
    #print ret
    return ret

def mutate(a):
    i=random.randint(0,size-1)
    a[i]=randomChar()

class RouletteWheel:
    def __init__(self,pop):
        self.totfit=0.0
        self.totfitsofar=[]
        self.pop=pop

        for m in pop:
            self.totfit += m.fitness
            self.totfitsofar.append(self.totfit)

    def select(self):
        r = random.random()*self.totfit
        # print r,self.totfit        
        for v,m in zip(self.totfitsofar,self.pop):
            if v >= r:
                return m

        print "OOOOOPS"
    
def breedPopulation(wheel):
    newpop=[]

    for i in range(nellite):
        dad=Gene(pop[i].string)
        newpop.append(dad)

    for i in range(POPSIZE-nellite):
        dad=Gene(wheel.select().string)
#        print dad.string.tostring(),dad.fitness
        newpop.append(dad)

        if random.random() < MATEPROB:
            mum=wheel.select()
            dad.string=mate(dad.string,mum.string)

        if random.random() < MUTATEPROB:
            mutate(dad.string)
    
            
    return newpop


if __name__ == '__main__':

    target_fitness=evaluate(target)

    pop=[]

    for i in range(POPSIZE):
        pop.append(Gene(seed()))

    count=0    

    while  count< MAXITER:

        fitmax=0.0
        for m in pop:
            m.fitness=evaluate(m.string)
            if m.fitness > fitmax:
                fitmax=m.fitness
                best=m

        
        pop = sorted(pop, key = lambda x:x.fitness,reverse=True)


        wheel=RouletteWheel(pop)

#        print (wheel.totfit/POPSIZE),POPSIZE

        print count,best.string.tostring()
        
        if  fitmax >=  target_fitness:
            break
        

        pop = breedPopulation(wheel);

        count += 1

  


