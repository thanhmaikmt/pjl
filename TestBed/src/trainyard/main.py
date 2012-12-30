import world

from yardurl import *


# parameters

import world 
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

class Context:
    pass

class Run:
    

    def __init__(self,w):
       
        #P.ion()
        #P.xlabel("Evaluations")
        #P.ylabel("Fitness")
        
        self.w=w
        master = Tk()
        self.frame=Frame(master)
        self.frame.pack()
        b = Button(self.frame, text="RANDOM WORLD", fg="black", command=self.init_world)
        c=0
        b.grid(row=0,column=c)
        c+=1
        b = Button(self.frame, text="RESET GA", fg="black", command=self.ga_init)
        b.grid(row=0,column=c)
        c+=1
        b = Button(self.frame, text="STEP SIM", fg="black", command=self.step_sim)
        b.grid(row=0,column=c)
        c+=1
        b = Button(self.frame, text="RUN (GA)", fg="black", command=self.run_ga)
        b.grid(row=0,column=c)
        c+=1
        b = Button(self.frame, text="RUN (RANDOM)", fg="black", command=self.run_random)
        b.grid(row=0,column=c)
        c+=1
        b = Button(self.frame, text="STOP", fg="black", command=self.stop)
        b.grid(row=0,column=c)
        c+=1
        self.bb= IntVar()
        b = Checkbutton(self.frame, text="BREED", fg="black", variable=self.bb,command=self.breed_func)
        b.grid(row=0,column=c)
        #b.pack()
      
 
        self.canvas = Canvas(self.frame, width=600, height=600)
        self.canvas.grid(row=1,columnspan=c)
        self.run_init()       
        self.init_world()
        
        self.context=Context()
        self.context.canvas=self.canvas
        self.context.h=60
        self.context.x=10
        self.context.y=10
        w.draw(self.context)                      
    
    def breed_func(self):
        global do_breed
        do_breed = not do_breed
        print " Breed=",self.bb.get(),do_breed
        
    def init_world(self):
        
        self.ga_init()
        self.canvas.delete(ALL)
        #draw_world_init(self.w, self.canvas)
        
    def run_init(self):
        self.iter=[]
        self.cost=[]
        self.count=0  
        self.best=-1e20
        self.running=False
        
    def ga_init(self): 
        self.pop=[]
        for i in range(POPSIZE):
            self.pop.append(random_gene(self.w.gene_length,self.w.maxTok))
    
        
    def stop(self):
        self.running=False
   
    
    def run_ga(self):
        
        if self.running:
            return
        self.run_init()
        self.running=True
        while self.count < MAXITER and self.running:
            self.step();


    def step_random(self):
        g=random_gene(self.world.gene_length,self.world.maxTok)
        fit=self.world.evaluate(g)
        if fit > self.best:
            text=" evaluations:"+str(self.count)+ "   fitness:"+str(fit) 
            self.iter.append(self.count)
            self.cost.append(fit)
            self.best = fit
            self.world.evaluate(g, True)
            self.canvas.delete(ALL)
            draw_world(self.world, self.canvas,text)
       # give the GUI a chance to do stuff  
        if (self.count % POPSIZE) == 0:
            self.frame.update()
        self.count += 1
      
    def step_sim(self):
        w.step()  
        # give the GUI a chance to do stuff
        self.canvas.delete(ALL)
        
        w.draw(self.context)   
        
    def run_random(self):
        self.run_init()
        self.running=True
        while self.count < MAXITER and self.running:
            self.step_random();
           

    def step(self):
             
        # give the GUI a chance to do stuff  
        self.frame.update()
        return      
              
        for m in self.pop:
            m.fitness=self.w.evaluate(m)
            
        pop = sorted(self.pop, key = lambda x:x.fitness,reverse=True)
    
        p = self.pop[0]
        
        if p.fitness > self.best:
            text=" evaluations:"+str(self.count*POPSIZE)+ "   fitness:"+str(p.fitness) 
            self.iter.append(self.count*POPSIZE)
            self.cost.append(p.fitness)
            self.best = p.fitness
            self.world.evaluate(p, True)
            self.canvas.delete(ALL)
            draw_world(self.world, self.canvas,text)
      
        # give the GUI a chance to do stuff  
        self.frame.update()
              
        self.pop = breedPopulation(pop);
        self.count += 1

      
        
    
puzzle='2exr6'

#puzzle='2ey6e'
puzzle='2esWR'

puzzle='2eyfR'

# Get something to work with.
url = urllib.urlopen("http://trainyard.ca/"+puzzle)

w=worldFromUrl(url)

run=Run(w)
    
mainloop() 
