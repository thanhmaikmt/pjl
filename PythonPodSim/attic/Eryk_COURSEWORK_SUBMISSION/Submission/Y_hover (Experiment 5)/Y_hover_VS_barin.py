from simulation import *
from backpropbrain import  *
import pygame 
from random import  *
from copy import *
from fontmanager import  *
import time

"""This code presents direct comparison between the Control Theory, Trained Neural Nets and Genetic Algorithm trained network."""

# Please Feel Free to play with this Parameter to see the effect on the perfromance for each of the controllers"
yHover   =  300

# This parameters are necncary for the GA to work Please don't change them here
POP_SIZE=10                
VELOCITY_SCALE=1.0/30       
MAX_AGE=50                   
REPROVE_PROB=0.1           
N_HIDDEN=3                  
Y_scale=1.0/370.0

POOL_FILE_NAME="hover_pool.txt"

# this class is used to draw a line and display text in the pygame window
class Painter:
    
    def __init__(self):
        self.preDraw=None       # define this function to draw on top!
        self.fontMgr = cFontManager(((None, 20), (None, 48), ('arial', 24)))
        
    def postDraw(self,screen):    # called before simulation draws to screen
       #  print "predraw"
        txt="Blue - GA Evolved NN, Red - Trained NN, White - Control theory"
        pg.draw.line(screen,(50,50,50),(15,yHover),(world.rect.width-7,yHover),2)
        self.fontMgr.Draw(screen, None, 20,txt,(20,20), (255,255,255) )




#control theory algorithm lives here
class Control_Theory:

    def process(self,sensor,state,dt):
        pod1.x = 160                    #used to offset the pod so they do not overlap in the game window
        control=Control()
        
        

        control=Control()
        
        err = state.y-yHover
        control.up= (err/(abs(state.dydt+0.01))) *0.05
        if state.y > yHover:
            
            if state.dydt>0:
                control.up= (state.dydt)*err
    

        return control



# Trained neural net Lives here
class BrainControl:

    def __init__(self):
        # load the trained brain       
        file=open("greystuff_Y_hover","r") #The greystuff_Y_hover file was processed and colected using
        self.brain=loadBrain(file)
        
 
            
        
    def process(self,sensor,state,dt):
        pod0.x=130
        control=Control()
            
    
        # create the input for the brain 
        input=[state.dydt]
        err = state.y-yHover
        input.append(err)

            
        # activate the brain to get output    
        output=self.brain.ffwd(input)
       
        # assign values to the controllers
        
        control.up=(output[0])


        
        return control
class Pool:  #  use me to store the best brains and create new brains
  
  
    # create a pool
    # specify the neural net parameters with nin nhidden and nout
    def __init__(self,nin,nhidden,nout):
        self.list=[]
        self.maxMembers=50
        self.layerSizes=[nin,nhidden,nout]
        self.elite_bias=1.0/50
        self.reprover=None
        self.touched=True
        self.reaping=True
        
    # add a new Gene to the Pool  (if better than the worst one in pool)
    # 
    def add(self,gene):  
        
        if len(self.list) >= self.maxMembers:
            if gene.fitness < self.list[self.maxMembers-1].fitness:
                return
          
        for i in range(len(self.list)):
            if gene.fitness > self.list[i].fitness:
                self.touched=True
                self.list.insert(i,gene)
                if len(self.list) > self.maxMembers:
                    self.list.pop()
                return
            
        if len(self.list) < self.maxMembers:
            self.list.append(gene)    
            self.touched=True
             
    # create a neural net from the pool or maybe random
    # might return best net to be reproven
    
    def create_best(self):
        clone=self.list[0].brain.clone()
        #clone.proof_count=self.list[0].brain.proof_count
        return clone


    def best_fitness(self):
        if len(self.list) == 0:
            return 0
        else:
            return self.list[0].fitness
       
    # return average fitness
    
    def load(self,file):
        self.list=[]
        n=pickle.load(file)
        print n
        for i in range(n):
            f=pickle.load(file)
            b=loadBrain(file)
            b.proof_count=0    # sorry we lost the proof count when we saved it
            self.add(Gene(b,f))
         
        print "RELOADED POOL"   
            

# Simple class to store the brain and fitness
class Gene:
    
    def __init__(self,brain,fitness):
        self.brain=brain
        self.fitness=fitness

class GAControl:
    
    def __init__(self):
        file=open(POOL_FILE_NAME,"r")
        pool.load(file)
        file.close()
        self.brain=pool.create_best()
    
    # decide if we want to kill a pod        
    
    
    # normal process called every time step    
    def process(self,sensor,state,dt):
        
                    
        control=Control()
            
        # create the input for the brain
        # first the velocity of the pod 
        input=[(state.y-yHover)*Y_scale]
        input.append(state.dydt*VELOCITY_SCALE)
         
        output=self.brain.ffwd(input)
       
        # assign values to the controllers
        control.up=output[0]-output[1]
        #control.left=output[2]
        #control.right=output[3]
        
        
        return control

pool=Pool(2,N_HIDDEN,2)

dt          =.1
brain       = BrainControl()
brain1      = Control_Theory()
brain2      = GAControl()
nSensors    = 2
sensorRange = 2000
pod0         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pod1        = GravityPod(nSensors,sensorRange,brain1,(255,255,255))
pod2        = GravityPod(nSensors,sensorRange,brain2,(0,0,255))
pods        = [pod0,pod1,pod2]
world       = World("Y_hover.txt",pods)
sim         = Simulation(world,dt)


painter = Painter()
sim.painter=painter


sim.run()
